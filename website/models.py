from . import db
from datetime import datetime
from flask_login import UserMixin

DIVISION = ['Open Competition','Youth Competition','Social']
DISCIPLINE = ['Bouldering','Lead','Speed']
GENDER = ['Male','Female']
STATUS = ['Open','Inactive','Sold Out','Cancelled']
AOC_MODE = ['none', 'generic','enhanced']

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    events = db.relationship('Event', backref='owner')
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)

    location = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    division = db.Column(db.String(50), nullable=False)
    discipline = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_capacity = db.Column(db.Integer, nullable=False)
    tickets_remaining = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open', index=True)
    aoc_mode = db.Column(db.String(20), nullable=False, default='none')
    timestamp = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    book_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)