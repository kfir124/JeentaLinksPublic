from wtforms import Form, TextField, FileField, validators, PasswordField, TextAreaField
import settings


class SmsForm(Form):
    password = PasswordField('password')
    number = TextField('number (for example: 0545441876)')
    msg = TextAreaField('text')