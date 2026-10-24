from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from . import db
from .models import Event, Comment, Order
from .forms import CancelEventForm, EventForm
import os
from uuid import uuid4
from werkzeug.utils import secure_filename

event_bp = Blueprint('event', __name__, url_prefix='/events')

def check_image(form):
    filename = uuid4().hex + "_" + secure_filename(form.image.data.filename)
    upload_path = os.path.join(os.path.dirname(__file__), 'static', 'image', filename)
    form.image.data.save(upload_path)
    return '/static/image/' + filename



@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        if not form.image.data:
            form.image.errors.append('Choose an event image.')
        else:
            event = Event(
                title=form.title.data,
                description=form.description.data,
                image=check_image(form), 
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


@event_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event is None:
        abort(404, description="Event not found")

    if event.user_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('main.index'))  # Redirect to a safe page

    form = EventForm(obj=event)
    
    form.submit.label.text = "Update Event"
    form.image.data = request.files.get('image')  # Get the uploaded file from the request
    booked = event.ticket_capacity - event.tickets_remaining
    if form.validate_on_submit():
            if form.ticket_capacity.data < booked:
                form.ticket_capacity.errors.append(f"Ticket capacity cannot be less than the number of tickets already booked ({booked}).")
            else:
                if form.image.data:
                    event.image=check_image(form)
                event.title=form.title.data
                event.description=form.description.data
                event.start=form.start.data
                event.end=form.end.data
                event.location=form.location.data
                event.city=form.city.data
                event.sport=form.sport.data
                event.gender=form.gender.data
                event.ticket_price=form.ticket_price.data
                event.ticket_capacity=form.ticket_capacity.data
                event.tickets_remaining=form.ticket_capacity.data - booked
                event.aoc_mode=form.aoc_mode.data
                event.aoc_text=form.aoc_text.data
                db.session.commit()
                flash('Event updated successfully!', 'success')
                return redirect(url_for('event.update', id=event.id))  # Redirect to the same page or another page as needed
    return render_template('events/create.html', form=form, event=event, cancel_form=CancelEventForm())


@event_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event is None:
        abort(404, description="Event not found")

    if event.user_id != current_user.id:
        flash('You do not have permission to cancel this event.', 'danger')
        return redirect(url_for('main.index'))  # Redirect to a safe page

    form = CancelEventForm()
    if form.validate_on_submit():
        event.status = 'Cancelled'
        db.session.commit()
        flash('Event cancelled.', 'success')
        return redirect(url_for('event.update', id=event.id))
    flash('Please confirm cancellation.', 'warning')
    return redirect(url_for('event.update', id=event.id))
