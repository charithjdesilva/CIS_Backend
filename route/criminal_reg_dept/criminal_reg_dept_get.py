from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel,EmailStr
from enum import Enum
import smtplib
# from secret123 import sender,receiver,password
from typing import Annotated
from Security.password import is_valid_password



router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)

@router.get("/hello")
def hello():
    return {"message" : "hello world"}