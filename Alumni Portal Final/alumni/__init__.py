
from flask import *
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
# app.config['SECRET_KEY']="753e765accbb7ca359675bad"
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category="info"
db = SQLAlchemy(app)
    
import alumni.routes