from flask import Blueprint, abort, g
import flask_sijax
from functions import is_website_owner, snapshot_website, delete_if_needed, add_or_edit_website_cell, get_next_index
from models import db, Website, Tab, User
from flask_login import current_user
import settings

ajax = Blueprint('ajax', __name__, template_folder='templates')


def get_tab(obj_response, tab_id):
    tab = Tab.query.get(tab_id)
    if not tab:
        obj_response.alert('cant find a tab with such id')
        return None
    if tab.portal_id != current_user.portal.id:
        obj_response.alert('you do not own this tab!')
        return None
    return tab


def get_website(obj_response, website_cell):
    website_id = int(website_cell[7:])
    website = Website.query.get(website_id)
    if not website:
        #websites does not exist
        obj_response.alert('cant find a website with such id')
        return None
    if not is_website_owner(website_id):
        obj_response.alert('you do not own this website')
        return None
    return website


class SijaxHandler(object):
    @staticmethod
    def swap_websites(obj_response, website1, website2):
        """
        swapping two websites(swapping their indexes)
        
        we actually get the id of the objects so it looks like
        website1 = "website17"
        website2 = "website24"
        in order to get just the id i strip 7 characters from the start
        which is the length of the word "website"
        """
        website1 = get_website(obj_response, website1)
        website2 = get_website(obj_response, website2)
        if not website1 or not website2:
            return
        website1.index, website2.index = website2.index, website1.index
        db.session.commit()

    @staticmethod
    def move_cell_to_tab(obj_response, tab_id, website_cell):
        """
        website_cell is not really an id but a name like "website5"
        so i strip 7 characters from the start which stands for "website"
        in order to get only the id
        """
        tab_id = int(tab_id)
        website = get_website(obj_response, website_cell)
        if not website:
            return
        tab = current_user.portal.tabs.filter_by(id=tab_id).first()
        if not tab:
            obj_response.alert('you do not own this tab or a problem has occurred')
            return
        website.tab_id = tab.id
        db.session.commit()

    @staticmethod
    def delete_website(obj_response, website_cell):
        website = get_website(obj_response, website_cell)
        if not website:
            return
        db.session.delete(website)
        db.session.commit()

    @staticmethod
    def delete_tab(obj_response, tab_id):
        tab_id = int(tab_id)
        tab = get_tab(obj_response, tab_id)
        if not tab:
            return
        tab.deleted = True
        db.session.commit()
        
    @staticmethod
    def hide_tab(obj_response, tab_id):
        tab_id = int(tab_id)
        tab = get_tab(obj_response, tab_id)
        if not tab:
            return
        if tab.hidden:
            tab.hidden = False
        else:
            tab.hidden = True
        db.session.commit()

    @staticmethod
    def edit_tab_text(obj_response, tab_id, tab_text):
        tab_id = int(tab_id)
        tab = get_tab(obj_response, tab_id)
        if not tab:
            return
        if len(tab_text) < 1 or len(tab_text) > settings.tab_max_len:
            obj_response.alert('tab name is too short or too long, max len is %d' % settings.tab_max_len)
            return
        if not tab_text.replace(' ', '').isalnum():
            obj_response.alert('tab name can contain only letters and numbers')
            return
        tab.name = tab_text
        db.session.commit()

    @staticmethod
    def share_tab(obj_response, tab_id):
        tab_id = int(tab_id)
        tab = get_tab(obj_response, tab_id)
        if not tab:
            return
        if tab.shared:
            tab.shared = False
        else:
            tab.shared = True
        db.session.commit()

    @staticmethod
    def transfer_tab(obj_response, tab_id, to_username, row_index):
        tab_id = int(tab_id)
        tab = get_tab(obj_response, tab_id)
        if not tab:
            return
        # find the user
        user = User.query.filter_by(username=to_username).first()
        if not user:
            # failed
            obj_response.alert('can\'t find this username')
            return
        # success!
        websites = tab.websites.all()
        # transfer the websites
        for website in websites:
            website.portal_id = user.portal.id
        tab.portal_id = user.portal.id  # transfer the tab
        tab.hidden = True  # start as invisible so user can choose to show it or not
        db.session.commit()  # complete ;)
        obj_response.call('clean_row', [row_index])

    @staticmethod
    def capture_image(obj_response, website_cell):
        website = get_website(obj_response, website_cell)
        if not website:
            return
        delete_if_needed(website.image_path)
        website.image_path = snapshot_website(website.url)
        db.session.commit()
        obj_response.alert('Done! please refresh your page to see the changes')
        
    @staticmethod
    def add_quick_website(obj_response, url, name, tab_id):
        website = Website('', url, name, get_next_index(), tab_id, current_user.portal.id, snapshot_website(url))
        db.session.add(website)
        db.session.commit()
        #obj_response.alert('Done! page will now refresh')
        obj_response.call('refresh')


    
@flask_sijax.route(ajax, '/ajax')
def global_ajax():
    if g.sijax.is_sijax_request:
        # The request looks like a valid Sijax request
        # Let's register the handlers and tell Sijax to process it
        g.sijax.register_object(SijaxHandler)
        return g.sijax.process_request()
    else:
        abort(403)