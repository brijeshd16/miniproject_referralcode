from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.database import User, Referal

class SignupForm(FlaskForm):
    username = StringField('Username', 
                            validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', 
                            validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                            validators = [DataRequired(), EqualTo('password'), Length(min = 3, max = 20)])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken, try a different username !')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email ID already present !')

class LoginForm(FlaskForm):
    username = StringField('Username', 
                            validators = [DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('Password', validators = [DataRequired()])
    referal_code = StringField('Referal Code', validators = [DataRequired(), Length(max = 6)])
    remember = BooleanField('Remember Me')

    # def validate_referal(self, referal_code):
    #     referal = Referal.query.filter_by(referal_code=referal_code.data).first()
    #     if referal:
    #         raise ValidationError('This is an Invalid referal code, please check and try again !')

    submit = SubmitField('Login')

class ReferForm(FlaskForm):
    generate = SubmitField('Generate New')