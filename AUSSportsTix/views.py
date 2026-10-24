from flask import Blueprint, render_template
from .models import Event, update_inactive_events
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # mark events listed to prior date as inactive
    update_inactive_events()

    # Get events in order of date
    events = db.session.scalars(db.select(Event).order_by(Event.start)).all()
    return render_template('index.html', events=events)