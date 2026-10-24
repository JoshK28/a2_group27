from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField,SelectField, DateTimeLocalField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from .models import SPORT, GENDER, STATUS, AOC_MODE

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

    #Creates the form for creating an event
class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[InputRequired()])
    description = TextAreaField("Event Description", validators=[InputRequired()])
    start = DateTimeLocalField("Start Time", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    end = DateTimeLocalField("End Time", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    location = StringField("Event Location", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    sport = SelectField("Sport", choices=SPORT, validators=[InputRequired()])
    gender = SelectField("Gender", choices=GENDER, validators=[InputRequired()])
    ticket_price = FloatField("Ticket Price", validators=[InputRequired()])
    ticket_capacity = IntegerField("Ticket Capacity", validators=[InputRequired()])
    aoc_mode = SelectField("AOC Mode", choices=[(mode, mode.title()) for mode in AOC_MODE], validators=[InputRequired()])
    aoc_text = TextAreaField("AOC Text")

    # Create Event submit button
    submit = SubmitField("Create Event")