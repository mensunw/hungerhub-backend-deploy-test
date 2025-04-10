from pydantic import BaseModel

# requests validation on creating a new user (requiring an email and password)
class CreateUser(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

# used for response formatting when returning user data (excluding the password)
class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        # allows to work with SQLAlchemy object relational models
        orm_mode = True

# requests validation on creating a new event (requiring a name, description, location, date, and time)
class CreateEvent(BaseModel):
    name: str
    description: str
    location: str
    date: str
    time: str

# used for response formatting when returning event data
class EventResponse(BaseModel):
    id: int
    name: str

    class Config:
        # allows to work with SQLAlchemy object relational models
        orm_mode = True

# used for formatting request when logining in a user
class LoginUser(BaseModel):
    email: str
    password: str