from db import db
import settings


class Tab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(settings.tab_max_len))
    websites = db.relationship('Website', backref='tab', lazy='dynamic')
    portal_id = db.Column(db.Integer, db.ForeignKey('portal.id'))
    hidden = db.Column(db.Boolean(), nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False)
    shared = db.Column(db.Boolean(), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'))
    default_image = db.Column(db.String(256))