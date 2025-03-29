import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# get the database url from the .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy manages connections to our database (communicating with PostgreSQL)
engine = create_engine(DATABASE_URL)

# creates database sessions for SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for defining database models (all database tabels with inherit from this class to map python classes to tables)
Base = declarative_base()

# create all tables and import models -- may need to change later (recreates table after every change to schema)
from app.models import User
Base.metadata.create_all(bind=engine)

# create a new session, and allow for injection in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
