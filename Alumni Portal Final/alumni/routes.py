from re import I
import re
from sqlalchemy import desc
from alumni import app
from flask import Flask,render_template,request,flash,redirect,url_for,flash,redirect,session
from alumni.models import User,Post
from alumni.forms import RegisterForm,LoginForm,PostForm,Id
import pyotp
from alumni import db
from flask_login import login_user,logout_user,current_user,login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/about")
def about_page():
    # items = Item.query.all()
    return render_template('about.html')
    # items=items
# class RegisterForm(FlaskForm):
#     name=StringField(label="Full Name:")
#     email=StringField(label="Email:")
#     password1=PasswordField(label="Password:")
#     password2=PasswordField(label="Confirm your password:")
#     submit=SubmitField(label="Create Account")
#     dob=DateField(label="Date of Birth:",format='%d-%m-%Y')
#     address=StringField(label="Residential Address:")
#     roll_no=StringField(label="Academic Roll Number:")
#     branch=SelectField(label="Branch:",choices=["Computer Science and Engineering","Electronics and Communication Engineering","Civil Engineering","Electrical and Electronics Engineering","Mechanical Engineering"])
#     phone_no=StringField(label="Phone Number")
#     current_job=StringField(label="Working at:")

@app.route("/register",methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(name=form.name.data, email=form.email.data,password=form.password1.data,dob=form.dob.data,address=form.address.data,roll_no=form.roll_no.data,branch=form.branch.data,phone=form.phone_no.data,current_job=form.current_job.data,secret_key=pyotp.random_base32(),passed_out_year=form.passed_out_year.data)
        db.session.add(user_to_create)
        db.session.commit()
        # login_user(user_to_create)
        flash(f"Account created successfully! Please enter OTP login as  {user_to_create.name}. ",category="success")
        session['email'] = user_to_create.email
        return redirect(url_for('login_2fa'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
    return render_template('register.html',form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # login_user(attempted_user)
            email=form.email.data
            session['email']=email
            flash(f'Please enter otp to login as:{attempted_user.name}',category='success')
            return redirect(url_for('login_2fa'))
        else:
            flash(f'Wrong credentials! Please try again',category='danger')
    return render_template('login.html',form=form)

# @app.route("/auth", methods=["GET", "POST"])
# def login_form():
#     # demo creds
#     creds = {"username": "test", "password": "password"}

#     if request.args["name"]=="test" and request.args["password"]=="password":
#         return "success"
#     else:
#         return "Wrong credentials"
    

@app.route("/login/2fa",methods=['GET','POST'])
def login_2fa():
    if 'email' in session:
            email=session['email']
            attempted_user=User.query.filter_by(email=email).first()
    # generating random secret key for authentication
    # secret = pyotp.random_base32()
    secret =attempted_user.secret_key
    return render_template("login_2fa.html",secret=secret)

@app.route("/login_2fa", methods=["GET", "POST"])
def login_2fa_form():
    
    
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = request.form.get("otp")
    
    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        if 'email' in session:
            email=session['email']
            attempted_user=User.query.filter_by(email=email).first()
        login_user(attempted_user)
        flash("You are successfully logged in to your account.", category="success")
        return redirect(url_for("home_page"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid OTP!", category="danger")
        return redirect(url_for("login_2fa"))


@app.route("/feed",methods=['GET','POST'])
@login_required
def feed_page():
    posts=Post.query.order_by(desc('date_time')).all()
    form=PostForm()
    if form.validate_on_submit():
        post_to_create=Post(name=current_user.name,post=form.post.data,email=current_user.email,user_id=current_user.id)
        db.session.add(post_to_create)
        db.session.commit()
        flash(f'You have successfully uploaded your post.',category='success')
        return redirect(url_for('feed_page'))
    return render_template("feed.html",form=form,posts=posts)

@app.route("/members",methods=['GET','POST'])
@login_required
def members_page():
    users=User.query.order_by('name').all()
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        return redirect(url_for('posts_page', user_id=user_id))
    return render_template("members.html",users=users)

@app.route("/post",methods=['GET','POST'])
def posts_page():
    user_id = request.args.get('user_id')
    # print(date)
    posts=Post.query.filter_by(user_id=user_id).order_by(desc('date_time')).all()
    post=User.query.filter_by(id=user_id).first()
    return render_template("uposts.html",posts=posts,user=post)


@app.route("/logout")
def logout_page():
    logout_user()
    flash(f'You have been logged out!',category='info')
    return redirect(url_for('home_page'))