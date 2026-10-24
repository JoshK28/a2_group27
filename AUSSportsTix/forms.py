from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email", validators=[InputRequired('Enter email address'), Email('Please enter a valid email')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password'), Length(min=6, max=50)])
    # Login submit button
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired('Enter first name'), Length(min=2, max=50)])
    surname = StringField("Surname", validators=[InputRequired('Enter surname'), Length(min=2, max=50)])
    email = StringField("Email Address", validators=[InputRequired('Enter email address'), Email('Please enter a valid email'), Length(max=100)])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired('Enter user password'), Length(min=6, max=50),
                  EqualTo('confirm', message="Passwords should match")])
    phone_number = StringField("Phone Number", validators=[InputRequired('Enter phone number'), Length(min=10, max=20)])
    street_address = StringField("Street Address", validators=[InputRequired('Enter street address'), Length(min=5, max=200)])
    confirm = PasswordField("Confirm Password")

    # Registration submit button
    submit = SubmitField("Register")