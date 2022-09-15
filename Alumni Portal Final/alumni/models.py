from alumni import bcrypt,login_manager
from alumni import db,login_manager
from flask_login import UserMixin
import datetime
from flask_sqlalchemy import SQLAlchemy

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    email= db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50),nullable=False, unique=False)
    dob=db.Column(db.Date(),nullable=False)
    address = db.Column(db.String(length=200),nullable=False)
    roll_no = db.Column(db.String(length=10),nullable=False)
    branch = db.Column(db.String(length=40),nullable=False)
    phone = db.Column(db.String(length=13),nullable=False,unique=True)
    current_job = db.Column(db.String(length=30),nullable=True)
    secret_key= db.Column(db.String(length=16),nullable=False,unique=True)
    # users=db.relationship('Post',backref='owned_user',lazy=True)
    passed_out_year=db.Column(db.String(length=4),nullable=False,unique=False)

    @property
    def password(self,plain_text_password):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)



class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=False)
    email=db.Column(db.String(length=40),nullable=False)
    post = db.Column(db.String(length=10000),nullable=False,unique=False)
    date_time=db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)
    user_id=db.Column(db.Integer(),nullable=False)
    # owner=db.Column(db.String(),db.ForeignKey('User.email'))