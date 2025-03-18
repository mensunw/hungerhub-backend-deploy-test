from sqlalchemy.orm import Session
from app import models, schemas

# create user object using request data after taking a database session
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    # add this new user to the user table
    db.add(db_user)
    # save user to database
    db.commit()
    # updates the database instance with this user
    db.refresh(db_user)
    return db_user

# queries the user table using the ORM by email
def get_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email)
