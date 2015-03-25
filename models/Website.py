from db import db
import settings


class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portal_id = db.Column(db.Integer, db.ForeignKey('portal.id'))
    tab_id = db.Column(db.Integer, db.ForeignKey('tab.id'))
    name = db.Column(db.String(settings.website_name_len))
    url = db.Column(db.String(settings.website_url_len))
    desc = db.Column(db.String(settings.website_desc_len))
    index = db.Column(db.Integer)  # lower index will be showed first
    image_path = db.Column(db.String(256))
    long_comment = db.Column(db.String(settings.website_long_comment_len))
    
    def __init__(self, name, url, desc, index, tab, portal_id=None, image_path='', long_comment=''):
        self.name = name
        self.url = url
        self.desc = desc
        self.index = index
        self.tab_id = tab
        self.portal_id = portal_id
        self.image_path = image_path
        self.long_comment= long_comment