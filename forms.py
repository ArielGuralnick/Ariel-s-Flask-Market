from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField,PasswordField, SubmitField
# from this object we can vaildate things and also check if passwords are equal,
#  and also check Email and also check if data written
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from market.models import User


# This class inherit from flask from class
class RegisterForm(FlaskForm):
    # in the fuction we check if User Name already exists !!!!(doesnt work to me, i dont know why)!!!!
    def vlidate_user_name(self, user_name_to_check):
        user = User.query.filter_by(user_name = user_name_to_check.data).first()
        if user:
            raise ValidationError('User Name already exists! Please try a diffrenet User Name')
    
    # in fuction we checl if Email already exists !!!!(doesnt work to me, i dont know why)!!!!
    def vlidate_email(self, email_to_check):
        email_address = User.query.filter_by(email=email_to_check.data).first()
        if email_address:
            raise ValidationError('Email already exists! Please try a diffrenet Email')

    user_name = StringField(label = 'User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label = 'Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label = 'Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    sumbit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    user_name = StringField(label = 'User Name:', validators=[DataRequired()])
    password = PasswordField(label = 'Password:', validators=[DataRequired()])
    sumbit = SubmitField(label='Sign in')

class purchseItemForm(FlaskForm):
    sumbit = SubmitField(label='Purchase')

class sellItemForm(FlaskForm):
    sumbit = SubmitField(label='Sell')