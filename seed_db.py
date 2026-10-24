from AUSSportsTix import db, create_app
from AUSSportsTix.models import User, Event, Comment, Order
from flask_bcrypt import generate_password_hash
from datetime import datetime

#SEED = False # this will create an empty database with no data
SEED = True # this will also put sample data into the database
image_path = "/static/img/"
password = "SportTicket123"

# This function populates the database
def populate_database_with_sample_data():
    users = [
        {
            "first_name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "password_hash": generate_password_hash(password),
            "phone_number": "123-456-7890",
            "street_address": "123 Main St, Melbourne, VIC 3000"
        },
        {
            "first_name": "Jane",
            "surname": "Crane",
            "email": "jane.crane@example.com",
            "password_hash": generate_password_hash(password),
            "phone_number": "098-765-4321",
            "street_address": "456 Oak Ave, Sydney, NSW 2000"
        },
        {
            "first_name": "Alice",
            "surname": "Smith",
            "email": "alice.happy22@test.com",
            "password_hash": generate_password_hash(password),
            "phone_number": "555-123-4567",
            "street_address": "789 Elm St, Brisbane, QLD 4000"
        }
    ]

    events = [
        {
            "title": "Soccer Match",
            "description": "Exciting soccer match between local teams.",
            "image": "soccer.jpeg",
            "start": datetime(2027, 6, 15, 19, 0),
            "end": datetime(2027, 6, 15, 21, 0),
            "location": "Melbourne Stadium",
            "city": "Melbourne",
            "sport": "Soccer",
            "gender": "Male",
            "ticket_price": 25.0,
            "ticket_capacity": 100,
            "tickets_remaining": 50,
            "status": "Open",
            "aoc_mode": "none",
            "user_id": 1
        }
    ]

    comments = [
        {
            "content": "Great event!",
            "timestamp": datetime(2027, 6, 15, 20, 0),
            "user_id": 1,
            "event_id": 1
        },
        {
            "content": "Looking forward to it!",
            "timestamp": datetime(2026, 12, 15, 7, 30),
            "user_id": 2,
            "event_id": 1
        },
        {
            "content": "How packed do you guys think it will be?",
            "timestamp": datetime(2026, 11, 15, 10, 45),
            "user_id": 3,
            "event_id": 3
        },
        {
            "content": "Can't wait!",
            "timestamp": datetime(2026, 12, 13, 22, 45),
            "user_id": 2,
            "event_id": 3
        },
        {
            "content": "Is there a dress code?",
            "timestamp": datetime(2026, 12, 14, 18, 15),
            "user_id": 4,
            "event_id": 4
        },
        {
            "content": "Shame to have missed it.",
            "timestamp": datetime(2026, 12, 14, 15, 10),
            "user_id": 5,
            "event_id": 4
        }
    ]

    orders = [
        {
            "user_id": 1, 
            "event_id": 1,
            "quantity": 2,
            "price": 25.0
        }
    ]

    if User.query.count() == 0:
        for user in users:
            db.session.add(
                User(
                    first_name=user["first_name"],
                    surname=user["surname"],
                    email=user["email"],
                    password_hash=user["password_hash"],
                    phone_number=user["phone_number"],
                    street_address=user["street_address"]
                )
            )
        db.session.commit()
        print("Users added to database")

    if Event.query.count() == 0:
        for event in events:
            db.session.add(
                Event(
                    title=event["title"],
                    description=event["description"],
                    image=image_path + event["image"],
                    start=event["start"],
                    end=event["end"],
                    location=event["location"],
                    city=event["city"],
                    sport=event["sport"],
                    gender=event["gender"],
                    ticket_price=event["ticket_price"],
                    ticket_capacity=event["ticket_capacity"],
                    tickets_remaining=event["tickets_remaining"],
                    status=event["status"],
                    aoc_mode=event["aoc_mode"],
                    user_id=event["user_id"]
                )
            )
        db.session.commit()
        print("Events added to database")

    if Comment.query.count() == 0:
        for comment in comments:
            db.session.add(
                Comment(
                    content=comment["content"],
                    timestamp=comment["timestamp"],
                    user_id=comment["user_id"],
                    event_id=comment["event_id"]
                )
            )
        db.session.commit()
        print("Comments added to database")

    if Order.query.count() == 0:
        for order in orders:
            db.session.add(
                Order(
                    user_id=order["user_id"],
                    event_id=order["event_id"],
                    quantity=order["quantity"],
                    price=order["price"]
                )
            )
        db.session.commit()
        print("Orders added to database")

    print("Database populated - did you copy the sample images into the package subfolder:",image_path,"?")

  


# ############################################################
# Create (and potentially seed) the database
# ############################################################

if __name__ == "__main__": # so it can be run from the terminal
    app = create_app()
    with app.app_context():
        db.create_all()
        if SEED:
            populate_database_with_sample_data()