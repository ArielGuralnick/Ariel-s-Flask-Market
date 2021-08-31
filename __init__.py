from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# hash password
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' # we use app object, and add extra configuration so flask applictaion can recognize its database

app.config['SECRET_KEY'] = '741aadf92a9ec5b700cbe576' # for safety - we go to terminal, import os, then - os.urandom(12).hex(), and copy the result and paste here.
db = SQLAlchemy(app)
# crypting our passwords
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# specifing where the login route located
login_manager.login_view = "loginpage"
login_manager.login_message_category = "info" #showing message in more beatiful way
from market import routes