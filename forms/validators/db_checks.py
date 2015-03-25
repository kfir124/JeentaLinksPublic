from wtforms import ValidationError

class Unique(object):
    """ validator that checks field uniqueness 
        example use: Unique(User, User.username)
    """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):         
        check = self.model.query.filter(self.field == field.data).limit(1).first()
        if check:
            raise ValidationError(self.message)