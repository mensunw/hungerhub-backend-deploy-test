from sqlalchemy import Column, Integer, String
from app.database import Base

# defines the python class that will be used for the users table
class User(Base):
    # actual table name in the database
    __tablename__ = "users"

    # primary key is the id
    id = Column(Integer, primary_key=True, index=True)

    # user credentials: email and password -- will need to hash it in the future (just keep it the same for now)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)

'''
SQLAlchemy will create a corresponding table like this:

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    password VARCHAR
);

'''


# defines the python class that will be used for the events table
class Event(Base):
    # actual table name in the database
    __tablename__ = "events"

    # primary key is a random generated id
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # event details -- name, description, location, date, and time
    name = Column(String, index=True)
    description = Column(String, index=True)
    location = Column(String, index=True)
    date = Column(String, index=True)
    time = Column(String, index=True)


'''
SQLAlchemy will create a corresponding table like this:

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR,
    location VARCHAR,
    date VARCHAR,
    time VARCHAR
);

'''