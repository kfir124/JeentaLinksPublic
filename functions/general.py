from flask import request, session
from flask.ext.login import current_user
import os
import settings


def fix_url(url):
    """
    :param url: url to add http:// to it
    :return: returns the url with http:// if needed
    """
    if '://' not in url:
        url = 'http://' + url
    return url


def load_style(data_dict, style):
    """
    loads into data_dict the given style
    """
    if style:
        data_dict['logo_path'] = style.logo_image_path
        data_dict['background_color'] = style.background_color
        data_dict['font_color'] = style.font_color
        data_dict['match_header_color'] = style.match_header_color

def fill_data(data_dict=None):
    """
    takes data_dict and ADDS to it all the data from the request.cookies
    and the session dict and the current_user
    in the following format:
    data['cookie_' + cookie_name] = cookie_value
    
    if data_dict is None then creates and return a dictionary with the cookies
    """
    if data_dict is None:
        data_dict = {}
    data_dict['edit_mode'] = False
    for cookie_name in request.cookies:
        data_dict['cookie_' + cookie_name] = request.cookies[cookie_name]
    for session_name in session:
        data_dict['session_' + session_name] = session[session_name]
    if current_user and current_user.is_authenticated():
        data_dict['user'] = current_user
        data_dict['portal'] = current_user.portal
        style = current_user.portal.style
        load_style(data_dict, style)
    return data_dict
    

def delete_file(path_to_file, stop_recursion=False):
    """
    path must be relative e.g '/static/uploads/mypic.jpg'
    tries to remove a file if exists
    returns True on success, False on failure
    """
    try:
        os.remove(settings.basedir + path_to_file)
        return True
    except:
        #first lets try to change windows style to linux and vise versa
        if not stop_recursion:
            if path_to_file.find('\\') != -1:
                return delete_file(path_to_file.replace('\\', '/'), True)
            else:
                return delete_file(path_to_file.replace('/', '\\'), True)
        return False