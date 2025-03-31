from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import User, Event
from app.schemas import CreateUser, UserResponse, CreateEvent, EventResponse
from app.crud import create_user, get_email, get_event, create_event

# intialize the fastapi app
app = FastAPI()
# create database tables on startup -- only for in development
Base.metadata.create_all(bind=engine)

@app.post("/signup", response_model=UserResponse)
def signup(user: CreateUser, db: Session = Depends(get_db)):
    '''
    API endpoint to sign up a new user. It requires the user to provide an email and password.
    If the email is already registered, it raises an HTTPException with a 400 status code.
    If the email is not registered, it creates a new user with the provided credentials and returns the user response.
    
    Inputs: 
        - user: CreateUser object containing email and password
        - db: Database session

    Returns: 
        - new_user: UserResponse object containing the newly created user's information (email and password)
    '''
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


@app.post("/login")
def login(user: CreateUser, db: Session = Depends(get_db)):
    '''
    API endpoint to log in a user. It requires the user to provide an email and password.
    If the email and password do not match any existing user, it raises an HTTPException with a 400 status code.
    If the email and password match an existing user, it returns a success message.

    Inputs:
        - user: CreateUser object containing email and password
        - db: Database session
    
    Returns:
        - message: A success message indicating that the login was successful
    '''
    if not user.email or not user.password:
        raise HTTPException(
            status_code=400, detail="Email and password are required.")

    existing_user = get_email(db, user.email, user.password)
    # check if the user already exists or not in the users table
    if not existing_user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password. Please try again.")

    else:
        return {"message": "Login successful"}


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    '''
    API endpoint to retrieve all users from the database (just for testing purposes).
    
    Input:
        - db: Database session
    Returns:
        - users: A list of User objects representing all users in the database
    '''
    # ORM query for all users
    users = db.query(User).all()
    return users


@app.get("/events")
def get_all_events(db: Session = Depends(get_db)):
    '''
    API endpoint to retrieve all events from the database (for view all events page).
    
    Input:
        - db: Database session  
    Returns:
        - events: A list of Event objects representing all events in the database
    '''
    # ORM query for all events
    events = db.query(Event).all()
    return events 

@app.post("/create-event", response_model=EventResponse)
def event_creation(event: CreateEvent, db: Session = Depends(get_db)):
    '''
    API endpoint to create a new event. It requires the user to provide a name, description, location, date, and time.
    If any of these fields are missing, it raises an HTTPException with a 400 status code.
    If the event already exists in the database, it raises an HTTPException with a 400 status code.
    If the event does not exist, it creates a new event with the provided attributes and returns the event response.
    
    Inputs:
        - event: CreateEvent object containing name, description, location, date, and time
        - db: Database session
        
    Returns:    
        - new_event: EventResponse object containing the newly created event's information (name, description, location, date, and time)
    '''
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