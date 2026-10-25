from flask import Blueprint, render_template, request
from .models import Event, SPORT, STATUS, update_inactive_events
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # mark events listed to prior date as inactive
    update_inactive_events()

    # Read the search box
    search = request.args.get('search', '')
    sport = request.args.get('sport', '')
    status = request.args.get('status', '')

    # starts displaying events and narrowing down when searching
    query = db.select(Event).order_by(Event.start)

    if search: 
        query = query.where(Event.title.like(f'%{search}%') )
    if sport:
        query = query.where(Event.sport == sport)
    if status:
        query = query.where(Event.status == status)
    events = db.session.scalars(query).all()

    return render_template('index.html', events=events, search=search, sport=sport, status=status, sports=SPORT, statuses=STATUS)



   

                              

