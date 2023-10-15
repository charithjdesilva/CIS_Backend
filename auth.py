from fastapi import APIRouter, Depends, HTTPException, Form, Path, status
from pydantic import BaseModel,EmailStr
from typing import Optional

from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

from Security.password import do_hash_password,verify_password
import random
from Security.user_defined_datatypes import SriLankaMobileNumber
from database import db_dependency
from models import User
from Email import send_email

from schemas import UserIn




router = APIRouter(
    prefix="/admin",
    tags=['admin Section']
)

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/token")

def get_user(db : db_dependency, username: str):
    user = db.query(User).filter(User.RegNo == username).first()
    if user:
        return {
            "username" : user.RegNo,
            "email" : user.Email,
            "full_name" : f"{user.FirstName} {user.LastName}",
            "hashed_password" : user.PasswordHash,
            "type" : user.UserType
        }

   
def authenticate_user(db: db_dependency, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user 

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(db: db_dependency,token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expires = payload.get("exp")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserIn, Depends(get_current_user)]
):
    return {
        "username" : current_user['username'],
        "email" : current_user["email"],
        "full_name" : current_user["full_name"],
        "type" : current_user["type"]
    }

@router.get("/protected_endpoint")
async def protected_endpoint(current_user: dict = Depends(get_current_active_user)):
    return {"message": "This is a protected endpoint", "user": current_user}


    


@router.post("/token")
async def login_for_access_token(
    db:db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


