from flask.ext.login import LoginManager
from models import User


login_manager = LoginManager()
login_manager.session_protection = "basic"
login_manager.login_message_category = "headermsg"
#login_manager.login_message = u"you need to login in order to access this page"
login_manager.login_view = "actions.do_login"

#should memcache this
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)