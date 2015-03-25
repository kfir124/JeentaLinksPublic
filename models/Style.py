from db import db


class Style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portal = db.relationship('Portal', backref='style', uselist=False)
    tab = db.relationship('Tab', backref='style', uselist=False)
    logo_image_path = db.Column(db.String(256))
    background_color = db.Column(db.String(20))
    font_color = db.Column(db.String(20))
    match_header_color = db.Column(db.Boolean(), nullable=False)