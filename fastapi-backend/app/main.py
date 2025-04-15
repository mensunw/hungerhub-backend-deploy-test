from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecurityScheme
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import User, Event
from app.schemas import CreateUser, UserResponse, CreateEvent, EventResponse, LoginUser
from app.crud import create_user, get_event, create_event
import re
from app.auth import verify_pwd, create_access_token, hash_pwd
from app.dependencies import get_current_user

# intialize the fastapi app
app = FastAPI()

# allow requests from the frontend to the endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database tables on startup -- only for in development
Base.metadata.create_all(bind=engine)

@app.post("/signup", response_model=UserResponse)
def signup(user: CreateUser, db: Session = Depends(get_db)):
    '''
    API endpoint to sign up a new user. It requires the user to provide an email and password.
    If the email is already registered, it raises an HTTPException with a 400 status code.
    If the email is not registered, it creates a new user with the provided credentials and returns the user response.
    Hashes the password before storing it in the database.
    
    Inputs: 
        - user: CreateUser object containing email, name, and password
        - db: Database session

    Returns: 
        - new_user: UserResponse object containing the newly created user's information 
    '''
    # require the user to provide an email, password, and name
    if not user.email or not user.password or not user.first_name or not user.last_name:
        raise HTTPException(
            status_code=422, detail="Email, password, and name are required.")
    
    # check if the email contains @ symbol
    if '@' not in user.email:
        raise HTTPException(
            status_code=422, detail="Invalid email address. Please provide a valid email address.")
    
    # check if the length of the password is at least 8 characters
    if len(user.password) < 8:
        raise HTTPException(
                    status_code=422, detail="Password must be at least 8 characters.")
    
    # check that the password confines to these constraints: lowercase letter, uppercase letter, and a number
    if (not re.search(r"\d", user.password)) or (not re.search(r"[A-Z]", user.password)) or (not re.search(r"[a-z]", user.password)):
        raise HTTPException(
                    status_code=422, detail="Password must contain at least one lowercase letter, uppercase letter, and number.")
            
    # check if this email is already in use
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email already registered in Spark! Bytes.")

    else:
        # hash the password
        hashed_password = hash_pwd(user.password)

        # create user model and save
        new_user = User(email=user.email, password=hashed_password, first_name=user.first_name, last_name=user.last_name)
        # add this new user to the corresponding table
        db.add(new_user)
        # save user to database
        # commit the changes to the database
        db.commit()
        # refresh the instance to get the updated data from the database
        db.refresh(new_user)
        return new_user


@app.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    '''
    API endpoint to log in a user. It requires the user to provide an email and password.
    If the email and password do not match any existing user, it raises an HTTPException with a 400 status code.
    If the email and password match an existing user, it returns a JWT access token.

    Inputs:
        - user: CreateUser object containing email and password
        - db: Database session
    
    Returns:
        - access_token: A JWT access token string for the authenticated user
        - token_type: The type of token (bearer)
    '''
    # check if the email and password has been inputted
    if not user.email or not user.password:
        raise HTTPException(
            status_code=400, detail="Email and password are required.")

    # check if the user already exists or not in the users table
    existing_user = db.query(User).filter(User.email == user.email).first()
    # ensure the inputted password is correct
    if not existing_user or not verify_pwd(user.password, existing_user.password):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password. Please try again.")

    token = create_access_token(data={"sub": existing_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

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
            status_code=422, detail="All fields are required (name, location, date, and time).")
    
    # check if this event is already in the database
    existing_event = get_event(db, event.name)
    if existing_event:
        raise HTTPException(
            status_code=400, detail="Event already exists in Spark! Bytes.")

    else:
        # create a new event with these attributes in this db
        new_event = create_event(db, event)
        return new_event
    
@app.get("/profile", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    '''
    Uses FastAPI's Depends() system to automatically inject the currently 
    authenticated user via the get_current_user() function.

    Input:
        - current_user: User model instance that is automatically fetched from the decoded 
        JWT and matched in the DB

    Returns:
        - email: returns user details (name and email)
    '''
    return current_user

@app.put("/events/{event_id}", response_model=EventResponse)
def update_event(event_id: int, updated_event: CreateEvent, db: Session = Depends(get_db)):
    '''
    API endpoint used for updating an event -- using its primary key (ID number).

    Inputs: 
        - event_id: specific ID number for the event (as stored in the events DB)
        - db: Database session
    
    Returns:
        - event: the updated event with the new credentials
    
    '''

    # filters the events database by ID number
    event = db.query(Event).filter(Event.id == event_id).first()
    
    # if there is no event with that ID number, throw an error
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # update the event attributes (e.g. name, description, location, date, and time)
    event.name = updated_event.name
    event.description = updated_event.description
    event.location = updated_event.location
    event.date = updated_event.date
    event.time = updated_event.time

    # commit to the event db
    db.commit()
    db.refresh(event)
    return event

@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to delete an event by its primary key (ID number).
    Returns nothing.

    Inputs:
        - event_id: the unique ID of the event to delete
        - db: database session

    """
    # filters the events database by ID number
    event = db.query(Event).filter(Event.id == event_id).first()

    # if there is no event with that ID number, throw an error
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # delete the found event
    db.delete(event)
    # commit to the database
    db.commit()

def custom_openapi():
    '''
    A security schema in FastAPI/OpenAPI is a way to tell Swaggers these routes are protected. 
    and how clients should authenticate. (Only relevant for testing in FastAPI -- ignore it essentially)
    
    '''
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="API with JWT auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi