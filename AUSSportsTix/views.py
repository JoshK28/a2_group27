from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from .models import Event, Order, SPORT, STATUS, update_inactive_events
from .aoc import CAPITAL_CITIES, find_country
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

# Acknowledgement of country, with a Country lookup
@main_bp.route('/acknowledgement')
def acknowledgement():
    return render_template('acknowledgement.html', cities=CAPITAL_CITIES.values())

#Show the logged in user bookings ordered by date
@main_bp.route('/history')
@login_required
def history():
    # Refresh event statuses to ensure all events are active.
    update_inactive_events()

    orders = db.session.scalars(db.select(Order).where(Order.user_id == current_user.id)
                                .order_by(Order.book_time.desc())).all()
    return render_template('history.html', orders=orders)

