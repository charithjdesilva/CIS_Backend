from fastapi import APIRouter,Form,File,UploadFile,Path,HTTPException,status
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from schemas import UserOut
from dummydata import users

router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)



    

class SelectProvince(str, Enum):
    p1 = "Eastern"
    p2 = "North Western"
    p3 = "Uva"
    p4 = "Southern"
    p5 = "Sabaragamuwa"
    p6 = "North Central"
    p7 = "Central"
    p8 = "Western"
    p9 = "Northern"

@router.post('/register-user')
def create_user(
    Reg_No : Annotated[str , Form()],
    NIC : Annotated[str, Form()],
    First_Name : Annotated[str, Form()],
    Last_Name : Annotated[str, Form()],
    Tel_No : Annotated[str, Form()],
    Province : Annotated[SelectProvince , Form()],
    City : Annotated[str, Form()],
    Area : Annotated[str, Form()],
    Address : Annotated[str, Form()],
    Branch : Annotated[str, Form()],
    Position : Annotated[str , Form()],
    Join_Date : Annotated[str, Form()],
    photo_of_criminal : Annotated[list[UploadFile] , File()]

):
    output =  {
    "Reg_No" : Reg_No,
    "NIC" : NIC,
    "First_Name" : First_Name,
    "Last_Name" : Last_Name,
    "Tel_No" : Tel_No,
    "Province" : Province,
    "City" : City,
    "Area" : Area,
    "Address" : Address,
    "Branch" : Branch,
    "Position" : Position,
    "Join_Date" : Join_Date,
    "photo_of_criminal" : [photo.filename for photo in photo_of_criminal]

    }

    users.append(output)


# @router.patch("/user-details/{id}")
# def update_user(id : Annotated[str, Path()]):

