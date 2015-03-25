#unused
"""
from db import db
import settings


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(settings.message_title_len))
    message = db.Column(db.String(settings.message_len))
    date = db.Column(db.DateTime)

    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    from_user = db.relationship('User', uselist=False, backref=db.backref('outbox', lazy='dynamic'), foreign_keys='[from_id]')
    to_user =  db.relationship('User', uselist=False, backref=db.backref('inbox', lazy='dynamic'), foreign_keys='[to_id]')
"""