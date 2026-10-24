from flask import Blueprint, render_template, request
from .models import Event, update_inactive_events
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # mark events listed to prior date as inactive
    update_inactive_events()

    # Read the search box
    search = request.args.get('search', '')

    #s tart with all events and narrow down if search is utilised
    query = db.select(Event).order_by(Event.start)

    if search: 
        query = query.where(Event.title.like(f'%{search}%') )
    events = db.session.scalars(query).all()

    return render_template('index.html', events=events, search=search)



   

                              

