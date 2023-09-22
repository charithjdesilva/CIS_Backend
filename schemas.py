from fastapi import File,UploadFile
from pydantic import BaseModel,Field, EmailStr
from typing import Annotated, Union

# class UserDisplay(BaseModel):

class LoginCredentials(BaseModel):
    username : str 
    password : str = Field(min_length=8)

class LoginOut(BaseModel):
    username : str
    hashed_password : str

class Image(BaseModel):
    photo_of_criminal : str

class UserBase(BaseModel):
    Reg_No : str = Field(description="Enter the user registration Number")
    NIC : str = Field(max_length=12)
    First_Name : str = Field(max_length=50)
    Last_Name : str = Field(max_length=50)
    Tel_No : int 
    Province : str
    City : str = ""
    Area : str = "" 
    Address : str
    Branch : str
    Position : str
    Join_Date : str = Field(description="format day-month-year 01-02-2023")

class UserUpdate(BaseModel):
    Reg_No : str = ""
    NIC : str = Field(default="",max_length=12)
    First_Name : str = Field(default="",max_length=50)
    Last_Name : str = Field(default="",max_length=50)
    Tel_No : int 
    Province : str = ""
    City : str = ""
    Area : str = "" 
    Address : str = ""
    Branch : str = ""
    Position : str = ""
    Join_Date : str = Field(default="",description="format day-month-year 01-02-2023") 
    
class UserDisplay(UserBase):
    user_photo: str

class SendCodeBase(BaseModel):
    type : str = "email"
    value : str 

class Send4DigitCode(BaseModel):
    value : int 

class Question(BaseModel):
    nic : str
    email : EmailStr
    question : str  = Field(max_length=500, default="") 

class Query(BaseModel):
    nic : str
    email : EmailStr
    query : str  = Field(max_length=500, default="") 

# class UserOut(UserIn):
#     pass




# class Images(BaseModel):
#     photo_of_criminal : Annotated[list[UploadFile], File()]