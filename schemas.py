from fastapi import File,UploadFile
from pydantic import BaseModel,Field
from typing import Annotated

# class UserDisplay(BaseModel):



class Image(BaseModel):
    url : str
    name : str

class UserBase(BaseModel):
    Reg_No : str
    NIC : str
    First_Name : str
    Last_Name : str
    Tel_No : str
    Province : str
    City : str
    Area : str | None 
    Address : str
    Branch : str
    Position : str
    Join_Date : str
    photo_of_criminal : list[Image] | None = None


# class UserOut(UserIn):
#     pass




# class Images(BaseModel):
#     photo_of_criminal : Annotated[list[UploadFile], File()]