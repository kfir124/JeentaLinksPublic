from flask import Blueprint, redirect, url_for, request, render_template, flash, session
from forms import RegistrationForm, LoginForm, WebsiteForm, TabForm, StyleForm, SmsForm
from models import db, User, Portal, Website, Tab, Style, StaticImages
from functions import fill_data, add_or_edit_website_cell, uploads, delete_file, load_style
from flask.ext.login import login_required, logout_user, login_user, current_user
import settings

actions = Blueprint('actions', __name__,
                    template_folder='templates')

@actions.route('/register', methods=['GET', 'POST'])
def do_register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        portal = Portal(form.portal_name.data)
        user = User(form.username.data, form.password.data, portal)
        db.session.add(user)
        db.session.add(portal)
        db.session.commit()
        tab = Tab(name='default', portal_id=portal.id, hidden=False, deleted=False, shared=False)
        db.session.add(tab)
        db.session.commit()
        #log in the user
        login_user(user, remember=True)
        flash('Hi %s thanks for registering' % user.username, 'headermsg')
        return redirect(url_for('simple.portal_viewer', portal_name=portal.name))
    return render_template('register.html', form=form)

@actions.route('/sms', methods=['GET', 'POST'])
def sms():
    form = SmsForm(request.form)
    if request.method == 'POST':
        if form.password.data != '4421':
            return 'bad password'
        form.done = True
        to = '+972' + form.number.data[1:]
        from_ = "+17147930411"
        body = form.msg.data
        from twilio.rest import TwilioRestClient 
 
        # put your own credentials here 
        ACCOUNT_SID = "AC8fa8939bf4942ba2ed6f817409a54931" 
        AUTH_TOKEN = "b7e819009392e7b54169aae3d3d46f76" 
         
        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
         
        client.messages.create(
            to=to, 
            from_=from_, 
            body=body,  
        )
    return render_template('sms.html', form=form)

@actions.route('/login', methods=['GET', 'POST'])
def do_login():
    if current_user.is_authenticated():
        flash('you can\'t login while already logged in', 'headermsg')
        return redirect(url_for('simple.index'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        #only the user class knows how to hash the password
        user = User(form.username.data, form.password.data)
        user = User.query.filter_by(username=user.username, password=user.password).first()
        if user is None:
                error = 'invalid username or password'
        else:
            login_user(user, remember=True)
            portal = user.portal
            #flash('Hi %s, you have been logged in' % user.username, 'headermsg')
            if portal is None:
                return redirect(url_for('simple.index'))
            return redirect(url_for('simple.portal_viewer', portal_name=portal.name))
    return render_template('login.html', form=form, error=error)


@actions.route('/logout/<serial>')
def do_logout(serial=''):
    data = fill_data()
    if serial == data['cookie__csrf_token']:
        logout_user()
    return redirect(url_for('simple.index'))


@actions.route('/website/edit/<int:website_id>/<int:tab_id>', methods=['GET', 'POST'])
@login_required
def do_edit_website(tab_id=0, website_id=0):
    data = fill_data()
    form = WebsiteForm(request.form)
    portal = current_user.portal
    static_images = current_user.StaticImages.limit(settings.static_images_num).all()
    empty_images = settings.static_images_num - len(static_images)
    if empty_images > 0:
        static_images += [None for i in range(empty_images)]
    data['portal'] = portal
    data['user'] = current_user
    data['form'] = form
    data['static_images'] = static_images
    if request.method == 'POST' and form.validate():
        return add_or_edit_website_cell(website_id, tab_id, portal, form)
    #he didn't send a form he just wants to view the page
    else:
        #get the website that the user is trying to view
        if website_id != 0:
            website = Website.query.get(website_id)
            #he lied! this website does not exist
            if website is None:
                flash('this website id does not exist', 'headermsg')
                return redirect(url_for('simple.portal_viewer', portal_name=portal.name, action='edit'))
            #lets load the data from the existing website
            form.url.data = website.url
            form.desc.data = website.desc
            form.long_comment.data = website.long_comment
        data['website_id'] = website_id
        data['tab_id'] = tab_id
    return render_template('website.html', **data)

    
@actions.route('/tab/add', methods=['GET', 'POST'])
@login_required
def do_edit_tab(tab_id=0):
    data = fill_data()
    form = TabForm(request.form)
    portal = current_user.portal
    data['portal'] = portal
    data['user'] = current_user
    data['form'] = form
    data['tab_id'] = tab_id
    if request.method == 'POST' and form.validate():
        if tab_id == 0:
            tab = Tab(name=form.name.data, portal_id=portal.id, hidden=False, deleted=False, shared=False)
            db.session.add(tab)
            db.session.commit()
            return redirect(url_for('simple.portal_viewer', portal_name=portal.name))
    return render_template('tab.html', **data)


@actions.route('/managestyle', methods=['GET', 'POST'])
@login_required
def do_manage_style():
    form = StyleForm(request.form)
    data = fill_data()
    style = current_user.portal.style
    if style:
        data['logo_image_path'] = style.logo_image_path
        data['match_header_color'] = style.match_header_color
    if request.method == 'POST' and form.validate():
        #we are talking about the portal style so it belongs to the current_user
        if style is None:
            #create the style cause it does not exist
            style = Style(portal=current_user.portal)
            #please note i still didnt commit, im waiting for changes and will commit when this request ends
            db.session.add(style)
        logo_image = request.files['logo_change']
        if logo_image.filename:
            try:
                logo_image_path = uploads.logophotos.save_random(logo_image)
                #if already had an image delete it
                if style.logo_image_path:
                    delete_file(style.logo_image_path)
                style.logo_image_path = logo_image_path
                data['logo_image_path'] = style.logo_image_path
                data['logo_path'] = style.logo_image_path
            except uploads.UploadNotAllowed:
                flash('this image is not allowed', 'headermsg')
                return redirect(url_for('actions.do_manage_style'))
        style.background_color = form.background_color_value.data
        style.font_color = form.font_color_value.data
        style.match_header_color = True if form.match_header_color.data else False
        load_style(data, style)
        db.session.commit()
    return render_template('manage_style.html', **data)


@actions.route('/staticimages', methods=['GET', 'POST'])
@login_required
def do_manage_static_images():
    data = fill_data()
    data['tables_number'] = settings.static_images_num / 5
    if settings.static_images_num % 5 > 0:
        data['tables_number'] += 1
    data['images_per_table'] = settings.static_images_num / data['tables_number']
    static_images = current_user.StaticImages.limit(settings.static_images_num).all()
    empty_images = settings.static_images_num - len(static_images)
    if empty_images > 0:
        static_images += [None for i in range(empty_images)]
    if request.method == 'POST':
        #check how many "backs" we need to do when the user press cancel [history.go(X)]
        num_back = int(request.form.get('num_back', -1)) - 1
        data['num_back'] = num_back
        #for each needed photo check if the user has uploaded a one
        counter = 0
        for photo in request.files.itervalues():
            counter += 1
            if photo.filename != '':
                #there is a file here so lets try to upload it
                try:
                    image_path = uploads.staticphotos.save_random(photo)
                except uploads.UploadNotAllowed:
                    flash('this image is not allowed', 'headermsg')
                    return redirect(url_for('actions.do_manage_static_images'))

                if photo.name[:4] == 'None':
                    #we need to add a new image lets see if he has empty_image for it
                    if empty_images <= 0:
                        flash('you dont have any empty image slots left', 'headermsg')
                        return redirect(url_for('actions.do_manage_static_images'))
                    staticimage = StaticImages(path=image_path, user=current_user, user_id=current_user.id)
                    db.session.add(staticimage)
                    #we are adding a new image to the display (its just to update the data[] dict - refresh the gui)
                    #i'll find the first empty box and remove it, while inserting the new image instead
                    location = static_images.index(None)
                    static_images.remove(None)
                    static_images.insert(location, staticimage)
                else:
                    #he is editing an existing static image slot
                    #we remove the start of the name cause the last part is the id
                    staticimage_id = int(photo.name[len('static_photo_'):])
                    staticimage = StaticImages.query.get(staticimage_id)
                    #delete the old image
                    delete_file(staticimage.path)
                    #update to new path
                    staticimage.path = image_path
                    #and now lets update the data[] dict - the gui
                    for s_image in static_images:
                        if s_image is None:
                            continue
                        if s_image.id == staticimage.id:
                            s_image.path = staticimage.path
            #we do not allow more than static_images_num image slots
            if counter >= settings.static_images_num:
                break
        db.session.commit()
    data['static_images'] = static_images
    return render_template('manage_static_images.html', **data)


@actions.route('/tabimages', methods=['GET', 'POST'])
@login_required
def do_edit_tab_images():
    data = fill_data()
    data['last_btn'] = request.form.get('last_btn', 0)  # if we are not in a POST it will be 0 so its ok
    data['tabs'] = current_user.portal.tabs.filter_by(deleted=False)
    if request.method == 'POST':
        # there should be only one photo but i cant find a way to access it other than looping
        for photo in request.files.itervalues():
            try:
                image_path = uploads.tabphotos.save_random(photo)
            except uploads.UploadNotAllowed:
                flash('this image is not allowed', 'headermsg')
                return redirect(url_for('actions.do_edit_tab_images'))
            tab = Tab.query.get(request.form['tab_id'])
            if not tab:
                flash('can\'t find tab with such id', 'headermsg')
                return redirect(url_for('actions.do_edit_tab_images'))
            if current_user.portal.id != tab.portal_id:
                flash('you do not own this tab', 'headermsg')
                return redirect(url_for('actions.do_edit_tab_images'))
            if tab.default_image:
                # delete old image
                delete_file(tab.default_image)
            tab.default_image = image_path
            db.session.commit()
    return render_template('edit_tab_images.html', **data)

