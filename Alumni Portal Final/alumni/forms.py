from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Length,Email,DataRequired,ValidationError
from alumni.models import User

class RegisterForm(FlaskForm):
    def validate_email(self,email_to_check):
        email=User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email already exists! Try a different email address.")

    name=StringField(label="Full Name:",validators=[Length(min=3,max=40,message='The name should be between 3 and 40 characters.'),DataRequired()])
    email=StringField(label="Email:",validators=[Email(message="Please enter a valid email address"),DataRequired()])
    password1=PasswordField(label="Password:",validators=[Length(min=6,message='The password should be minimum of 6 characters.'),DataRequired()])
    password2=PasswordField(label="Confirm your password:",validators=[EqualTo('password1',message='Second password should be matched with above password'),DataRequired()])
    submit=SubmitField(label="Create Account")
    dob=DateField(label="Date of Birth:")
    address=StringField(label="Residential Address:",validators=[Length(min=3,max=150),DataRequired()])
    passed_out_year=StringField(label="Passed Out Year:",validators=[Length(min=4,max=4),DataRequired()])
    roll_no=StringField(label="Academic Roll Number:",validators=[Length(min=10,max=10,message='Roll Number must be 10 characters long'),DataRequired()])
    branch=SelectField(label="Branch:",choices=["Computer Science and Engineering","Electronics and Communication Engineering","Civil Engineering","Electrical and Electronics Engineering","Mechanical Engineering"],validators=[DataRequired()])
    phone_no=StringField(label="Phone Number:",validators=[DataRequired(),Length(min=10,max=10,message="Phone number should be 10 characters long")])
    current_job=StringField(label="Working at:",validators=[Length(max=40)])
    

class LoginForm(FlaskForm):
    email=StringField(label="Email:",validators=[DataRequired(message="Email address is required")])
    password=PasswordField(label="Password:",validators=[DataRequired(message="Password is required")])
    submit=SubmitField(label="Login")



class PostForm(FlaskForm):
    post=TextAreaField(validators=[DataRequired(),Length(min=1,max=2000)])
    submit=SubmitField()

class Id(FlaskForm):
    user_id=StringField(validators=[DataRequired()])
    submit=SubmitField(label="Posts")