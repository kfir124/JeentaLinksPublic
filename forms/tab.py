from wtforms import Form, TextField, FileField, validators
import settings


class TabForm(Form):
    name = TextField('name', [
        validators.Length(min=1, max=settings.tab_max_len),
        validators.Regexp('^[a-zA-Z0-9 ]+$', message='can only contain letters and numbers'),
        ])