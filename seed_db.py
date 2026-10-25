from AUSSportsTix import db, create_app
from AUSSportsTix.models import User, Event, Comment, Order
from flask_bcrypt import generate_password_hash
from datetime import datetime

#SEED = False # this will create an empty database with no data
SEED = True # this will also put sample data into the database
image_path = "/static/image/"
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
        }
    ]

    
    events = [
        {
            "title": "A-League Men: Melbourne Derby",
            "description": "Melbourne Victory host Melbourne City in the first derby of the season. Gates open 90 minutes prior to kick off.",
            "image": "event-01.svg",
            "start": datetime(2027, 3, 13, 19, 30) ,
            "end": datetime(2027, 3, 13, 21, 30),
            "location": "AAMI Park", 
            "city": "Melbourne",
            "sport": "Soccer",
            "gender": "Male",
            "ticket_price": 35.0,
            "ticket_capacity": 300,
            "tickets_remaining": 212,
            "status": "Open",
            "aoc_mode": "none",
            "user_id": 1
        },

        {
            "title": "Matildas v New Zealand Friendly",
            "description": "Matildas take on the Ferns in a pre-tournament friendly. Family zone & player signings after the match.",
            "image": "event-02.svg",
            "start": datetime(2027, 4, 10, 18, 0),
            "end": datetime(2027, 4, 10, 20, 0),
            "location": "Suncorp Stadium", 
            "city": "Brisbane",
            "sport": "Soccer",
            "gender": "Female",
            "ticket_price": 30.0,
            "ticket_capacity": 400,
            "tickets_remaining": 0,
            "status": "Sold Out",
            "aoc_mode": "none",
            "user_id": 1
        },

        {
            "title": "Queensland Bouldering Open",
            "description": "The best boulderers in the state compete over qualification and final rounds on a fresh set of problems.",
            "image": "event-03.svg",
            "start": datetime(2027, 4, 10, 18, 0),
            "end": datetime(2027, 4, 10, 20, 0),
            "location": "Urban Climb West end", 
            "city": "Brisbane",
            "sport": "Bouldering",
            "gender": "Female",
            "ticket_price": 20.0,
            "ticket_capacity": 120,
            "tickets_remaining": 74,
            "status": "Open",
            "aoc_mode": "none",
            "user_id": 1
        },

        {
            "title": "Adelaide International Tennis Day Session",
            "description": "Day session of the Adelaide International with three singles matches on the centre court.",
            "image": "event-04.svg",
            "start": datetime(2027, 1, 12, 11, 0),
            "end": datetime(2027, 1, 12, 18, 0),
            "location": "Memorial Drive Tennis Centre", 
            "city": "Adelaide",
            "sport": "Tennis",
            "gender": "Female",
            "ticket_price": 45.0,
            "ticket_capacity": 250,
            "tickets_remaining": 168,
            "status": "Open",
            "aoc_mode": "none",
            "user_id": 1
        },

        {
            "title": "Super Rugby: Waratahs v Brumbies",
            "description": "A round 3 local derby under lights. The pre-match game entertainment starts at 6pm.",
            "image": "event-05.svg",
            "start": datetime(2027, 3, 6, 19, 35),
            "end": datetime(2027, 3, 6, 21, 30),
            "location": "Allianz Stadium", 
            "city": "Sydney",
            "sport": "Rugby",
            "gender": "Male",
            "ticket_price": 40.0,
            "ticket_capacity": 350,
            "tickets_remaining": 290,
            "status": "Open",
            "aoc_mode": "none",
            "user_id": 1
        },

        {
            "title": "WBBL: Perth Scorchers v Sydney Sixers",
            "description": "Women's big baash league T20 match. Cancelled due to ground requiring resurfacing.",
            "image": "event-06.svg",
            "start": datetime(2026, 11, 21, 21, 15, 0),
            "end": datetime(2026, 11, 21, 18, 30),
            "location": "WACA Ground", 
            "city": "Perth",
            "sport": "Cricket",
            "gender": "Female",
            "ticket_price": 15.0,
            "ticket_capacity": 200,
            "tickets_remaining": 200,
            "status": "Cancelled",
            "aoc_mode": "none",
            "user_id": 1
        },

        {
            "title": "Sheffield Shield: QLD v VIC",
            "description": "Day one of the four day first class match between Queelsand and Victoria.",
            "image": "event-01.svg",
            "start": datetime(2027, 2, 4, 10, 30),
            "end": datetime(2027, 2, 4, 17, 30),
            "location": "The Gabba", 
            "city": "Brisbane",
            "sport": "Cricket",
            "gender": "Male",
            "ticket_price": 12.0,
            "ticket_capacity": 500,
            "tickets_remaining": 455,
            "status": "Open",
            "aoc_mode": "none",
            "user_id": 1
        },

        {
            "title": "Sydney Winter Tennis Classic",
            "description": "The mens single semi-finals and final event at the indoor winter classic.",
            "image": "event-02.svg",
            "start": datetime(2026, 8, 15, 10, 0),
            "end": datetime(2026, 8, 15, 18, 0),
            "location": "Ken Rosewall Arena", 
            "city": "Sydney",
            "sport": "Tennis",
            "gender": "Male",
            "ticket_price": 25.0,
            "ticket_capacity": 150,
            "tickets_remaining": 40,
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