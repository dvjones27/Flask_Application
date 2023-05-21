from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserSignUpForm(FlaskForm):
    # email, password, submit, first_name, last_name
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Create Password', validators=[DataRequired()])
    submit_button = SubmitField('Sign Up')
    
class UserSigninForm(FlaskForm):
    # email, password, submit, username
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    submit_button = SubmitField('Sign In')
    