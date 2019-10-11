from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo ,ValidationError
from dashboard.models import User
from datetime import datetime



class RegistrationForm (FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=1, max=200)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField ('Password', validators =[DataRequired(), Length(min=1)])
    confirm_password = PasswordField ('Confirm Password' , validators =[DataRequired(), Length(min=1), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user= User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('User name is already taken. Please choose a new one')
    def validate_email(self, email):
        user= User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email is already taken. Please choose a new one')



class LoginForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField ('Password' , validators =[DataRequired(), Length(min=1)])
    remember = BooleanField ('Remember Me')
    submit = SubmitField('Login')
