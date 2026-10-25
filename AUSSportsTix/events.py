import json
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from . import db, encoder
from .models import Event, Comment, Order, update_inactive_events
from .forms import CancelEventForm, EventForm, CommentForm, BookingForm
import os
from uuid import uuid4
from werkzeug.utils import secure_filename

event_bp = Blueprint('event', __name__, url_prefix='/events')

#save uploaded image as unique name and return database path
def check_image(form):
    filename = uuid4().hex + "_" + secure_filename(form.image.data.filename)
    upload_path = os.path.join(os.path.dirname(__file__), 'static', 'image', filename)
    form.image.data.save(upload_path)
    return '/static/image/' + filename


# Create event for logged in users
@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        #image required
        if not form.image.data:
            form.image.errors.append('Choose an event image.')
        else:

            #Store description embedding if encoder is available
            embedding_text=None
            if encoder is not None: 
                try:
                    embedding_text = json.dumps(encoder.encode(form.description.data).tolist())
                except Exception:
                    flash('AI search is not currently available. Search by keywords only.', 'warning')
            #new events form format with status:Open
            event = Event(
                title=form.title.data,
                description=form.description.data,
                description_embedding=embedding_text,
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

            #save and commit to database
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=form)

# Update event details for event owner only
@event_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    # Automatically check for events that are no longer active.
    update_inactive_events()

    # Thrown 404 if event can't be found
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event is None:
        abort(404, description="Event not found")

    # Only event owner can update.
    if event.user_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('main.index'))  # Redirect to a safe page

    form = EventForm(obj=event)

    form.submit.label.text = "Update Event"
    form.image.data = request.files.get('image')  # Get the uploaded file from the request

    # Already sold tickets
    booked = event.ticket_capacity - event.tickets_remaining

    # Validate and update event details
    if form.validate_on_submit():
            
            if form.ticket_capacity.data < booked:
                form.ticket_capacity.errors.append(f"Ticket capacity cannot be less than the number of tickets already booked ({booked}).")
            else:
                # Validate image
                if form.image.data:
                    event.image=check_image(form)
                event.title=form.title.data

                # Refresh embedding when description changes.
                if form.description.data != event.description:
                    event.description_embedding = None
                    if encoder is not None:
                        try:
                            embedding = encoder.encode(form.description.data)
                            event.description_embedding = json.dumps(embedding.tolist())
                        except Exception:
                            flash('AI search is not currently available. Search by keywords only.', 'warning')
                event.description= form.description.data
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

                #Event status logic to switch event status
                if event.status != 'Cancelled':
                    event.status = 'Sold Out' if event.tickets_remaining == 0 else 'Open'
                db.session.commit()
                flash('Event updated successfully!', 'success')
                return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=form, event=event, cancel_form=CancelEventForm())


# Cancel even after only owner confirms
@event_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event is None:
        abort(404, description="Event not found")

    #Prevent unauthorised users from cancelling. Redirect.
    if event.user_id != current_user.id:
        flash('You do not have permission to cancel this event.', 'danger')
        return redirect(url_for('main.index'))  # Redirect to a safe page

    #import flask form:CancelEventForm. Tick box must be active to cancel
    form = CancelEventForm()
    if form.validate_on_submit():
        event.status = 'Cancelled'
        db.session.commit()
        flash('Event cancelled.', 'success')
        return redirect(url_for('event.show', id=event.id))
    
    flash('Please confirm cancellation.', 'warning')
    return redirect(url_for('event.update', id=event.id))


# Show event details and comments to anyone
@event_bp.route('/<int:id>')
def show(id):
    update_inactive_events()

    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event is None:
        abort(404)

    # Create comment and booking form
    form = CommentForm()
    booking_form = BookingForm()

    return render_template('events/show.html', event = event, form = form, booking_form= booking_form)



# Post a comment to an event as logged in user
@event_bp.route('/<int:id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event is None:
        abort(404)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user=current_user, event=event)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
    elif request.method == 'POST':
        # Invalid submission. Either empty or exceeds 500 characters. Show error message. 
        flash('Write comment between 1 and 500 characters before submitting.', 'warning')

    return redirect(url_for('event.show', id=event.id))


# Book tickets for an event as logged in user
@event_bp.route('/<int:id>/book', methods=['GET', 'POST'])
@login_required
def book(id):

    update_inactive_events()

    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event is None:
        abort(404)

    form = BookingForm()
    if event.status != 'Open':
        flash(f'Tickets cannot be booked for this event. Event status: {event.status}.', 'warning')

    elif form.validate_on_submit():
        quantity = form.quantity.data
        # Prevent overbooking.
        if quantity > event.tickets_remaining:
            flash(f'Only {event.tickets_remaining} tickets remaining. Please adjust your booking.', 'warning')
        else:
            # Update and save remaining tickets and user order.
            order = Order(quantity=quantity, price=event.ticket_price, user=current_user, event=event)
            event.tickets_remaining -= quantity

            # Update event status if sold out
            if event.tickets_remaining == 0:
                event.status = 'Sold Out'
            db.session.add(order)
            db.session.commit()
            flash(f'Order ID : #{order.id}. Successfully booked {quantity} tickets for {event.title}.', 'success')
            return redirect(url_for('main.history'))
    elif request.method == 'POST':
        flash('Please enter a valid quantity between 1 and 10.', 'warning')

    # Redirect to event page: GET after login or failed booking.
    return redirect(url_for('event.show', id=event.id))