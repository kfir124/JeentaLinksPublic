from db import db


#used to save the user prefered images for easy choice when he opens a new website cell
class StaticImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref=db.backref('StaticImages', lazy='dynamic'))
