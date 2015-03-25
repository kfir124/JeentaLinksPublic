import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'X'
#im not using WTForms CSRF protection, im using Flask-SeaSurf
CSRF_ENABLED = False
#CSRF_SESSION_LKEY = 'X'

#flask-uploads
max_upload_size = 0.5 #in megabytes
MAX_CONTENT_LENGTH = max_upload_size * 1024 * 1024 #make it megabytes
uploads_dir = '/static/uploads'
UPLOADS_DEFAULT_DEST = basedir + uploads_dir

#ghost screenshots
screenshots_relative = '/static/screenshots'
screenshots_dir = basedir + screenshots_relative

#flask-sqlalchemy
sql_lite = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql://x?charset=utf8'

#session_interface
cookie_salt = 'X'

#flask-sijax
SIJAX_STATIC_PATH = os.path.join(basedir, 'static/javascript/sijax/')
SIJAX_JSON_URI = '/static/javascript/sijax/json2.js'

#other settings (not related to flask)
user_len = 20
portal_len = 120
website_name_len = 10
website_desc_len = 100
website_long_comment_len = 2048
website_url_len = 256
max_picture_name_len = 25
tab_max_len = 30
password_salt = 'X'
message_title_len = 40
message_len = 2048
tab_rows = 4
tab_items_per_row = 6
#how many images to display in the static images page (/staticimages)
static_images_num = 10
default_tab_image = '/static/img/default.jpg'