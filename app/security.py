from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()


SECURITY_KEY = os.getenv("SECURITY_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 33

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expire_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, ALGORITHM)
    return encoded_jwt