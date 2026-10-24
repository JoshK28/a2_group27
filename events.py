from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import db
from .models import Event, Comment, Order
from .forms import EventForm

event_bp = Blueprint('event', __name__, url_prefix='/events')

def create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            image=form.image.data,
            start=form.start.data,
            end=form.end.data,
            location=form.location.data,
            city=form.city.data,
            sport=form.sport.data,
            gender=form.gender.data,
            ticket_price=form.ticket_price.data,
            ticket_capacity=form.ticket_capacity.data,
            tickets_remaining=form.ticket_capacity.data,
            status='Open',
            aoc_mode=form.aoc_mode.data,
            aoc_text=form.aoc_text.data,
            user_id=current_user.id)
        
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('event.create'))  # Redirect to the same page or another page as needed
    return render_template('events/create.html', form=form)