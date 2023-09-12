from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel,EmailStr
from enum import Enum
import smtplib
# from secret123 import sender,receiver,password
from typing import Annotated
from Security.password import is_valid_password



router = APIRouter(
    prefix="/general",
    tags=['general pages section']
)

# class User(BaseModel):
#     username : Form(str)
#     password : Form(str)

user_dict = [{'username': 'user1', 'password' : '1234'}]


@router.post("/login")
def do_login(username : Annotated[str, Form()]  , password : Annotated[str, Form()]  ):
    # It is just logic. not original 
    for pickuser in user_dict:
        if (username == pickuser['username']):
            if(password == pickuser['password']):
                return "Login Successful"
            else:
                raise HTTPException(status_code=404, detail="Invalid username or password")
        else:
            raise HTTPException(status_code=404, detail="Invalid username or password")
        

class Options(Enum):
    Email = 'Email'
    Mobile_Number = 'Mobile Number'

class OptionsValue(BaseModel):
    value :  str | None


@router.post("/forget-password")
def send_code(type:Options, value : OptionsValue):
    if(Options.Email == type):
        return {'message' : f"4 Digit code send to the {value.Email}"}
    else:
        return {'message' : f"4 Digit code send to the {value.Mobile_Number}"}
    # return type


@router.post("/4-digit-code/")
def validate_code():
    return {"message" : "get 4 digit code"}

@router.post("/reset-password")
def validate_reset_pswd(new_pswd : Annotated[str,Form(min_length=8)], confirm_pswd : Annotated[str, Form(min_length=8)]):
    if is_valid_password(new_pswd,confirm_pswd):
        return "response : Password Reset Successfully"
    else:
        raise HTTPException(status_code=404, detail="No match between passwords .  Try again!")


@router.post("/faq/questions")
def post_questions(NIC : Annotated[str, Form()], Email : Annotated[EmailStr, Form()], Question : Annotated[str, Form(max_length=500)]):
    # Need NIC Validation
    return {
        "NIC" : NIC,
        "Email" : Email,
        "Question" : Question
    }

@router.post("/contact_us/queries")
def post_queries(Name : Annotated[str, Form()], Email : Annotated[EmailStr, Form()], Query : Annotated[str , Form(max_length=500)] ):
    return {
        "Name"  : Name, 
        "Email" : Email,
        "Query" : Query
    }









