from models import Website
from flask.ext.login import current_user

def is_portal_owner(portal, user=None):
    """
    :param portal: a portal object
    :param user: a user object
    :return: True if the portal is owned by the user
    """
    if user is None:
        user = current_user
        if not user.is_authenticated():
            return False

    if portal.owner_id == user.id:
        return True
    return False


def is_website_owner(website=None, user=None):
    """
    :param website: a website object or website id
    :param user: a user object or None, None will check against the current_user
    :return: True if the website is owned by the user
    """
    #handle website
    if isinstance(website, int):
        website = Website.query.get(website)
    if website is None:
        return False
    portal_id = website.portal_id

    if user is None:
        user = current_user

    if portal_id == user.portal.id:
        return True
    return False