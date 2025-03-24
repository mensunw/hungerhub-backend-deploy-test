from sqlalchemy.orm import Session
from app import models, schemas

# create user object using request data after taking a database session


def create_user(db: Session, user: schemas.CreateUser):
    db_user = models.User(email=user.email, password=user.password)
    # add this new user to the user table
    db.add(db_user)
    # save user to database
    db.commit()
    # updates the database instance with this user
    db.refresh(db_user)
    return db_user

# queries the user table using the ORM by email
def get_email(db: Session, email: str, password: str):
    return db.query(models.User).filter(
        models.User.email == email,
        models.User.password == password
    ).first()


# create the event object using request data after taking a database session
def create_event(db: Session, event: schemas.CreateEvent):
    db_event = models.Event(name=event.name, description=event.description, location=event.location, date=event.date, time=event.time)
    # add this new event to the corresponding table
    db.add(db_event)
    # save event to database
    db.commit()
    # updates the database instance with this event
    db.refresh(db_event)
    return db_event


# queries the event table using the ORM by name
def get_event(db: Session, name: str):
    return db.query(models.Event).filter(
        models.Event.name == name,
    ).first()
