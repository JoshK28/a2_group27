from flask import Blueprint, render_template
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get events in order of date
    events = db.session.scalars(db.select(Event).order_by(Event.start)).all()
    return render_template('index.html', events=events)