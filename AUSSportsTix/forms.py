from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import BooleanField, TextAreaField, SubmitField, StringField, PasswordField,SelectField, DateTimeLocalField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, ValidationError
from .models import SPORT, GENDER, STATUS, AOC_MODE
from datetime import datetime


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
    title = StringField("Event Title", validators=[InputRequired(), Length(min=2, max=100)])
    description = TextAreaField("Event Description", validators=[InputRequired()])
    image = FileField("Event Image", validators=[FileAllowed(['jpg', 'jpeg', 'png'], "Only JPG/PNG images allowed.")], 
                      description="Upload an image for the event (optional). If not provided, a default image will be used.")
    start = DateTimeLocalField("Start Time", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    end = DateTimeLocalField("End Time", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    location = StringField("Event Location", validators=[InputRequired(), Length(min=2, max=200)])
    city = StringField("City", validators=[InputRequired(), Length(min=2, max=100)])
    sport = SelectField("Sport", choices=SPORT, validators=[InputRequired()])
    gender = SelectField("Gender", choices=GENDER, validators=[InputRequired()])
    ticket_price = FloatField("Ticket Price", validators=[InputRequired(), NumberRange(min=0, max=10000)])
    ticket_capacity = IntegerField("Ticket Capacity", validators=[InputRequired(), NumberRange(min=1, max=100000)])
    aoc_mode = SelectField("AOC Mode", choices=[(mode, mode.title()) for mode in AOC_MODE], validators=[InputRequired()])
    aoc_text = TextAreaField("AOC Text")

    # Create Event submit button
    submit = SubmitField("Create Event")

    def validate_start(self, field):
        if field.data and field.data <= datetime.now():
            raise ValidationError("The event cannot be in the past.")

    def validate_end(self, field):
        if field.data and self.start.data and field.data <= self.start.data:
            raise ValidationError("The end time cannot be before the start time.")

class CancelEventForm(FlaskForm):
    confirm = BooleanField("Are you sure you want to cancel this event?", validators=[InputRequired()])
    cancel = SubmitField("Cancel Event")


class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[InputRequired('Write a comment...'), Length(min=1, max=500,message ='500 characters max')])
    submit = SubmitField("Post Comment")

