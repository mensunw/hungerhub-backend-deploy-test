from app.auth import SECRET_KEY, ALGORITHM
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from jose import jwt, JWTError
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# tells FastAPI to expect a bearer token for the protected routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''
    Retrieves the current user based on the JWT token provided in the request

    Inputs:
        - token: str = Depends(oauth2_scheme) automatically extracts the Bearer token from the Authorization header.
        - db: Session = Depends(get_db) gives you a database session.

    Returns: 
        - user: the User model instance.
    '''
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    try:
        # decode the token provided in the request using the algorithm and key provided in .env
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # JWT stores the user identity under the 'sub' subject
        email = payload.get("sub")
        if email is None:
            # raise a credential error if token is invalid
            raise credentials_exception
    except JWTError:
        # raise an error for any decoding issues (e.g. invalid format)
        raise credentials_exception

    # query the DB for the user with the provided token
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        # if no user was found, return an error
        raise credentials_exception
    return user
