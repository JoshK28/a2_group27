from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from sqlalchemy import or_
import json
import numpy as np
from .models import Event, Order, SPORT, STATUS, update_inactive_events
from . import db, encoder

main_bp = Blueprint('main', __name__)
SEMANTIC_CUTOFF = 0.39 # Lowest similarity for AI-search (reduce for increasing search scope)

@main_bp.route('/')
def index():
    # mark events listed to prior date as inactive
    update_inactive_events()

    # Read the search box
    search = request.args.get('search', '').strip()
    sport = request.args.get('sport', '')
    status = request.args.get('status', '')

    # starts displaying events and narrowing down when searching
    query = db.select(Event).order_by(Event.start)

    if sport:
        query = query.where(Event.sport == sport)
    if status:
        query = query.where(Event.status == status)
    events = db.session.scalars(query).all()

    if search:
        keyword_query = query.where(or_(Event.title.like(f'%{search}%'), Event.description.like(f'%{search}%')))
        keyword_events = db.session.scalars(keyword_query).all()

        if encoder is not None:
            try:
                query_embedding = encoder.encode(search)
                results= []
                for event in events:
                    if event in keyword_events or not event.description_embedding:
                        continue
                    event_embedding = np.array(json.loads(event.description_embedding))
                    similarity = np.dot(query_embedding, event_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(event_embedding))
                    if similarity >= SEMANTIC_CUTOFF:
                        results.append((event, similarity))

                results.sort(key=lambda x: x[1], reverse=True)
                events = keyword_events + [x[0] for x in results]
            except Exception:
                events = keyword_events
                flash('AI search is not currently available. Search by keywords only.', 'warning')
        else:
            events = keyword_events

    return render_template('index.html', events=events, search=search, sport=sport, status=status, sports=SPORT, statuses=STATUS)


#Show the logged in user bookings ordered by date
@main_bp.route('/history')
@login_required
def history():
    # Refresh event statuses to ensure all events are active.
    update_inactive_events()

    orders = db.session.scalars(db.select(Order).where(Order.user_id == current_user.id)
                                .order_by(Order.book_time.desc())).all()
    return render_template('history.html', orders=orders)

