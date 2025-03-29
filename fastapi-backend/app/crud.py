from sqlalchemy.orm import Session
from app import models, schemas

def create_user(db: Session, user: schemas.CreateUser):
    '''
    Create a new user in the users database table.
    
    Inputs:
        - db: Database session
        - user: CreateUser object containing email and password
        
    Returns:
        - db_user: User object representing the newly created user
    '''
    db_user = models.User(email=user.email, password=user.password)
    # add this new user to the user table
    db.add(db_user)
    # save user to database
    db.commit()
    # updates the database instance with this user
    db.refresh(db_user)
    return db_user

def get_email(db: Session, email: str, password: str):
    '''
    Query the users table using the ORM by email and password m -- checks if a user exists with inputted credentials (for login endpoint).
    
    Inputs: 
        - db: Database session
        - email: User's email
        - password: User's password

    Returns:
        - db_user: User object representing the user with the given email and password, or None if no such user exists.
    '''
    return db.query(models.User).filter(
        models.User.email == email,
        models.User.password == password
    ).first()


def create_event(db: Session, event: schemas.CreateEvent):
    '''
    Create a new event in the events database table.
    
    Inputs: 
        - db: Database session
        - event: CreateEvent object containing event details (name, description, location, date, time)
    
    Returns:
        - db_event: Event object representing the newly created event
    '''
    db_event = models.Event(name=event.name, description=event.description, location=event.location, date=event.date, time=event.time)
    # add this new event to the corresponding table
    db.add(db_event)
    # save event to database
    db.commit()
    # updates the database instance with this event
    db.refresh(db_event)
    return db_event

def get_event(db: Session, name: str):
    '''
    Query the events table using the ORM by name -- checks if an event exists with inputted name (for creating events endpoint).
    
    Inputs:
        - db: Database session
        - name: Event name
        
    Returns:
        - db_event: Event object representing the event with the given name, or None if no such event exists.
    '''
    return db.query(models.Event).filter(
        models.Event.name == name,
    ).first()
