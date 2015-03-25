from flask import redirect, url_for, request, flash
from functions import uploads, fix_url, is_website_owner, delete_file
from models import Website, Tab, db, StaticImages
from flask_ghost import haunted
import settings


def get_next_index():
    # returns the next index that should be used when adding a new site
    last_index = Website.query.order_by(Website.index.desc()).limit(1).first()
    if last_index:
        index = last_index.index + 1
    else:
        index = 1
    return index

def add_or_edit_website_cell(website_id, tab_id, portal, form):
    #check if the user wants to add a new image
        image_path = ''
        sep = '\n' + '-' * 120 + '\n'
        if request.form['chosen_image'] != 'uploaded_image':
            #the user wants one of his static images
            static_image = StaticImages.query.get(request.form['chosen_image'])
            if static_image is None:
                flash('couldn\'t locate this static image location', 'headermsg')
                return redirect(url_for('simple.portal_viewer', portal_name=portal.name))
            image_path = static_image.path
        if 'image' in request.files:
            image = request.files['image']
            if image.filename:
                try:
                    image_path = uploads.webphotos.save_random(image)
                except uploads.UploadNotAllowed:
                    flash('this image is not allowed', 'headermsg')
                    return redirect(url_for('simple.portal_viewer', portal_name=portal.name))

        if website_id == 0:
            #create a new website at the user's portal
            portal_id = portal.id
            if not portal_id:
                flash('can\'t locate your portal', 'headermsg')
                return redirect(url_for('simple.index'))
            #we need to find the highest index possible
            index = get_next_index()
            tab = Tab.query.get(tab_id)
            if not tab:
                flash('tab id does not exist')
                return redirect(url_for('simple.index'))
            if tab.portal_id != portal.id:
                flash('this tab is not belongs to you')
                return redirect(url_for('simple.index'))
            # if he wrote something we need to add the sep
            if form.long_comment.data != '':
                form.long_comment.data += sep
            if not image_path:
                # we shall use our flask_ghost to snapshot the webpage
                image_path = snapshot_website(fix_url(form.url.data))
            website = Website('', fix_url(form.url.data), form.desc.data, index, tab_id, portal_id, image_path, form.long_comment.data)
            db.session.add(website)
            db.session.commit()
            return redirect(url_for('simple.portal_viewer', portal_name=portal.name))
        else:  # editing an existing website
            if is_website_owner(website_id):
                website = Website.query.get(website_id)
                website.url = fix_url(form.url.data)
                website.desc = form.desc.data
                if not website.image_path:
                    # we shall use our flask_ghost to snapshot the webpage
                    website.image_path = snapshot_website(fix_url(form.url.data))
                if form.long_comment.data != '':
                    last_characters = form.long_comment.data[-10:]
                    should_add_sep = False
                    # if the last row is not made of '-' or '\n' we need to add
                    for char in last_characters:
                        if char != '\n' and char != '-' and char != '' and char != '\r':
                            should_add_sep = True
                            break
                    if should_add_sep:
                        form.long_comment.data += sep
                website.long_comment = form.long_comment.data
                if image_path:
                    delete_if_needed(website.image_path)
                    website.image_path = image_path
                db.session.commit()
                #flash('updated', 'headermsg')
            else:
                flash('you can\'t change this website since you dont own it', 'headermsg')
            return redirect(url_for('simple.portal_viewer', portal_name=portal.name))


def snapshot_website(url):
    name = haunted.take_picture(url, settings.screenshots_dir)
    if not name:
        return ''
    return settings.screenshots_relative + '/' + name


def delete_if_needed(image_path):
    """
    deletes the image if its in a path that should get deleted
    """
    if 'webphotos' in image_path:
        #we only delete images that are in the webphotos directory
        delete_file(image_path)