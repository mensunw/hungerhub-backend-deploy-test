from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import User, Event
from app.schemas import CreateUser, UserResponse, CreateEvent, EventResponse
from app.crud import create_user, get_email, get_event, create_event

# file that defines the API endpoints to login and sign-up a user

# intialize the fastapi app
app = FastAPI()

# create database tables on startup -- only for in development
Base.metadata.create_all(bind=engine)

# api endpoint to sign-up a user, responding with the user response defined in schemas.py


@app.post("/signup", response_model=UserResponse)
# need to interact with database (Depends(get_db))
def signup(user: CreateUser, db: Session = Depends(get_db)):
    # require the user to provide an email and password
    if not user.email or not user.password:
        raise HTTPException(
            status_code=400, detail="Email and password are required.")
    # check if this email is already in use
    existing_user = get_email(db, user.email, user.password)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email already registered in Spark! Bytes.")

    else:
        # create a new user with these credentials in this db
        new_user = create_user(db, user)
        return new_user


# api endpoint to login an existing user
@app.post("/login")
# need to interact with database (Depends(get_db))
def login(user: CreateUser, db: Session = Depends(get_db)):
    if not user.email or not user.password:
        raise HTTPException(
            status_code=400, detail="Email and password are required.")

    existing_user = get_email(db, user.email, user.password)
    # check if the user already exists or not
    if not existing_user:
        raise HTTPException(
            status_code=400, detail="Incorrect credentials. Please try again.")

    else:
        return {"message": "Login successful"}

# returns all users found in the user database
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    # ORM query for all users
    users = db.query(User).all()
    return users

# returns all events found in the user database
@app.get("/events")
def get_all_events(db: Session = Depends(get_db)):
    # ORM query for all events
    events = db.query(Event).all()
    return events 


# api endpoint to create an event, responding with the event response defined in schemas.py
@app.post("/create-event", response_model=EventResponse)
# need to interact with database (Depends(get_db))
def event_creation(event: CreateEvent, db: Session = Depends(get_db)):
    # require the user to provide a name, description, location, date, and time
    if not event.name or not event.description or not event.location or not event.date or not event.time:
        raise HTTPException(
            status_code=400, detail="All fields are required (name, location, date, and time).")
    # check if this event is already in the database
    existing_event = get_event(db, event.name)
    if existing_event:
        raise HTTPException(
            status_code=400, detail="Event already exists in Spark! Bytes.")

    else:
        # create a new event with these attributes in this db
        new_event = create_event(db, event)
        return new_event