from fastapi import APIRouter, Depends, HTTPException, Form, Path, status
from pydantic import BaseModel,EmailStr
from enum import Enum
import smtplib
# from secret123 import sender,receiver,password
from typing import Annotated
from Security.password import is_valid_password,is_valid_email,is_valid_sri_lankan_mobile_number
from schemas import LoginCredentials, SendCodeBase , Send4DigitCode , Question , Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from Security.password import hash_password,verify_password
from dummydata import user_login,code_in_four_digit, user_question_table , user_query_table
import random


router = APIRouter(
    prefix="/general",
    tags=['general pages section']
)

# class User(BaseModel):
#     username : Form(str)
#     password : Form(str)

user_dict = [{'username': 'user1', 'password' : '1234'}]

four_digit_code_by_user = 4444




# Sample hardcoded users (In practice, use a database)
hardcoded_users = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"},
]

def authenticate_user(username: str, password: str) -> Optional[LoginCredentials]:
    for user_data in user_login:
        if user_data["username"] == username and verify_password(password,user_data["hash_password"] ):
            return LoginCredentials(**user_data)
    return None



@router.post("/login")
def do_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

        

class Options(Enum):
    Email = 'Email'
    Mobile_Number = 'Mobile Number'

class OptionsValue(BaseModel):
    value :  EmailStr | str






@router.post("/forget-password")
def check_validation(request : SendCodeBase):
    """
        ** email => use email
        ** mobile number => use tel
    """
    if request.type == 'email':
        if is_valid_email(request.value):
            return {"message" : f"4 digit code is send to the {request.value} "}
        else:
            raise HTTPException(status_code=401, detail='It is invalid email')
    elif request.type == 'tel':
        if is_valid_sri_lankan_mobile_number(request.value):
            return {"message" : f"4 digit code is send to the {request.value} "}
        else:
            raise HTTPException(status_code=401, detail="Invalid mobile number")


@router.post("/4-digit-code/")
def validate_code(code : Send4DigitCode):
    if len(str(code.value)) == 4 : 
        four_digit_code_by_user = code.value
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid 4 digit code")

    

@router.post("/reset-password/{username}")
def validate_reset_pswd(username : Annotated[str , Path()], new_pswd : Annotated[str,Form(min_length=8)], confirm_pswd : Annotated[str, Form(min_length=8)]):
    for user in user_login:
        if user['username'] == username:
            if new_pswd == confirm_pswd:
                if is_valid_password(new_pswd,confirm_pswd):
                    user['password'] = new_pswd
                    user['hash_password'] = hash_password(new_pswd)
                    return status.HTTP_200_OK
                else:
                    raise HTTPException(status_code=404, detail="It should include at least one uppercase , one lowercase , one number and one special character")
            else:
                raise HTTPException(status_code=404, detail="No match between passwords")
    raise HTTPException(status_code=404, detail=f"{username} is not found")


@router.post("/faq/questions")
def post_questions(user_question : Question):
    if user_question:
        user_question_table.append(user_question)
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid question")

@router.post("/contact_us/queries")
def post_questions(user_query : Query):
    if user_query:
        user_query_table.append(user_query)
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid question")









