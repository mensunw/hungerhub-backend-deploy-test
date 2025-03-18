from sqlalchemy import Column, Integer, String
from app.database import Base

# defines the python class that will be used for the users table
class User(Base):
    # actual table name in the database
    __tablename__ = "users"

    # primary key is the id
    id = Column(Integer, primary_key=True, index=True)

    # user credentials: email and password (hashed)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

'''
SQLAlchemy will create a corresponding table like this:

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR
);

'''