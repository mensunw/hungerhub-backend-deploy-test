from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# creates a password hashing object uses bcrypt as the password hashing algorithm (and re-hashes old passwords when a user logs in)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashes a plain-text password into a bcrypt hash
def hash_pwd(password: str):
    '''
    Hashes a plain-text password using bcrypt algorithm.

    Input: 
        - password: A plain-text password to be hashed
    Returns:
        - hashed_password: A hashed password string
    '''
    return pwd_context.hash(password)

# verify a plain-text password against the stored hash password in the DB (using during login)
def verify_pwd(plain_password: str, hashed_password: str):
    '''
    Verifies a plain-text password against a hashed password.
    
    Input:
        - plain_password: A plain-text password to be verified
        - hashed_password: A hashed password to compare against
    Returns:
        - bool: True if the password matches, False otherwise
    '''
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    '''
    Creates a JWT access token with an expiration time.
    
    Inputs:
        - data: A dictionary containing user information (e.g., user ID, email)
        - expires_delta: Optional timedelta for token expiration time; if it is not provided, 
        the default expiration time is used from .env
        
    Returns:
        - str: A JWT access token string
    '''
    # make a copy of the data dictionary to avoid modifying the original data
    to_encode = data.copy()

    # calculate the expiration time for the token (datetime.now(timezone.utc) gets the current UTC time and adds the expiration time)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # add the expiration time to the data dictionary to indicate when the token will expire
    to_encode.update({"exp": expire})

    # returns an encrypted JWT token using the secret key and algorithm specified in the .env file
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)