import settings
from flask import Flask
from views import simple, actions, ajax
from models import db
from session_interface import ItsdangerousSessionInterface
from functions import login_manager, csrf, uploads, sijax
from flask.ext.uploads import configure_uploads
from flask_ghost import GhostManager

#set to true before using /createdb/topsecret
recreate_db = False

#init
app = Flask(__name__)

#settings
app.config.from_object('settings')
#session interface
app.session_interface = ItsdangerousSessionInterface()
#set db
db.init_app(app)
#set login-manager
if recreate_db is False:
    login_manager.init_app(app)
#set CSRF protection
csrf.init_app(app)
#configure the uploads sets
configure_uploads(app, uploads.all_sets)
#configure sijax
sijax.init_app(app)
#configure flask-ghost
GhostManager(app)

#register pages
#for now simple holds all our simple pages like .index and all the rest actually :D
app.register_blueprint(simple)
#holding actions like /register
app.register_blueprint(actions)
#holding all the ajax/sijax requests handlers
app.register_blueprint(ajax)

if __name__ == "__main__":
    import settings
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.sql_lite
    app.run()