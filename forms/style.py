from wtforms import Form, TextField, FileField, HiddenField, validators, BooleanField


class StyleForm(Form):
    logo_image = FileField()
    background_color_value = TextField('Background color', [
        validators.Length(max=20),
        validators.Regexp('^[#a-zA-Z0-9 ]+$', message='bad background color')
        ])
    font_color_value = TextField('Font color', [
        validators.Length(max=20),
        validators.Regexp('^[#a-zA-Z0-9 ]+$', message='bad font color')
        ])
    match_header_color = BooleanField()