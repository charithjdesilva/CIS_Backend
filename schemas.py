from pydantic import BaseModel
from typing import Annotated

# class UserDisplay(BaseModel):




    

class UserOut(BaseModel):
    Reg_No : str
    NIC : str
    First_Name : str
    Last_Name : str
    Tel_No : str
    Province : str
    City : str
    Area : str
    Address : str
    Branch : str
    Position : str
    Join_Date : str
    photo_of_criminal : list[str]