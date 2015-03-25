from validators import Unique
from models import User, Portal
from wtforms import Form, TextField, PasswordField, validators
import settings


class RegistrationForm(Form):
    username = TextField('Username', [
        validators.Length(min=4, max=settings.user_len),
        validators.Regexp('^[a-zA-Z0-9]+$', message='can only contain letters and numbers'),
        Unique(User, User.username, message='user already exists')
        ])
    portal_name = TextField('Portal name', [
        validators.Length(min=4, max=settings.portal_len),
        Unique(Portal, Portal.name, message='portal with this name already exists')
        ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')