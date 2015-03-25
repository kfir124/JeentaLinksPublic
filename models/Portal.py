from db import db
import settings


class Portal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(settings.portal_len), unique=True)
    websites = db.relationship('Website', backref='portal', lazy='dynamic')
    tabs = db.relationship('Tab', backref='portal', lazy='dynamic')
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'))
    
    def __init__(self, name):
        self.name = name