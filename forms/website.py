from wtforms import Form, TextField, FileField, validators, TextAreaField
import settings


class WebsiteForm(Form):
    image = FileField()
    url = TextField('url', [
        validators.Length(min=0, max=settings.website_url_len),
        ])
    desc = TextField('comment', [
        validators.Length(min=0, max=settings.website_desc_len),
        ])
    long_comment = TextAreaField('long comment', [
        validators.Length(min=0, max=settings.website_long_comment_len),
        ])