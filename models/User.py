from db import db
import hashlib
import settings


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(settings.user_len), unique=True)
    password = db.Column(db.String(40))
    portal = db.relationship('Portal', uselist=False, backref='owner')

    def __init__(self, username, password, portal=None):
        self.username = username
        self.password = hashlib.sha1(password + settings.password_salt).hexdigest()
        self.portal = portal

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)