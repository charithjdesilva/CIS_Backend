from fastapi import APIRouter, Body,Form,File, Query,UploadFile,Path,HTTPException,status
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from schemas import UserBase
from dummydata import users
from pathlib import Path
from fastapi.responses import FileResponse


UPLOAD_DIR = Path() / 'users_image'
UPLOAD_DIR1 = Path() / 'criminal_images'


router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)


@router.post('/register-user')
async def create_user(
    Reg_No : Annotated[str , Form()],
    NIC : Annotated[str, Form()],
    First_Name : Annotated[str, Form()],
    Last_Name : Annotated[str, Form()],
    Tel_No : Annotated[str, Form()],
    Province : Annotated[str , Form()],
    City : Annotated[str, Form()],
    Area : Annotated[str, Form()],
    Address : Annotated[str, Form()],
    Branch : Annotated[str, Form()],
    Position : Annotated[str , Form()],
    Join_Date : Annotated[str, Form()],
    photo_of_user : UploadFile = UPLOAD_DIR / 'avatar.png'

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
    "photo_of_user" : UPLOAD_DIR / 'avatar.png'
    }
    
    if photo_of_user != output['photo_of_user']:
        data = await photo_of_user.read()
        save_to = UPLOAD_DIR / photo_of_user.filename
        output['photo_of_user'] = save_to
        with open(save_to , 'wb') as f:
            f.write(data)

    users.append(output)

    return status.HTTP_200_OK


@router.patch('/update-user/{id}')
async def update_user(
    id : Annotated[str, Path()],
    NIC : Annotated[str, Form()]= None,
    First_Name : Annotated[str, Form()]= None,
    Last_Name : Annotated[str, Form()]= None,
    Tel_No : Annotated[str, Form()]= None,
    Province : Annotated[str , Form()]= None,
    City : Annotated[str, Form()]= None,
    Area : Annotated[str, Form()]= None,
    Address : Annotated[str, Form()]= None,
    Branch : Annotated[str, Form()]= None,
    Position : Annotated[str , Form()]= None,
    Join_Date : Annotated[str, Form()]= None,
    photo_of_user : UploadFile = UPLOAD_DIR / 'avatar.png'

):
    for userIn in users:
        if userIn['Reg_No'] == id :
            if NIC:
                userIn['NIC'] = NIC
            if First_Name:
                userIn['First_Name'] = First_Name
            if Last_Name:
                userIn['Last_Name'] = Last_Name
            if Province:
                userIn['Province'] = Province
            if City:
                userIn['City'] = City
            if Area:
                userIn['Area'] = Area
            if Address:
                userIn['Address'] = Address
            if Position:
                userIn['Position'] = Position
            if Join_Date:
                userIn['Join_Date'] = Join_Date
            if Branch:
                userIn['Branch'] = Branch
            if photo_of_user != UPLOAD_DIR / 'avatar.png' and photo_of_user != userIn['photo_of_user'] :
                data = await photo_of_user.read()
                save_to = UPLOAD_DIR / photo_of_user.filename
                userIn['photo_of_user'] = save_to
                with open(save_to , 'wb') as f:
                    f.write(data)
                

            return status.HTTP_200_OK
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" id - {id} is not found")


@router.patch('/update-criminal/{id}')
def update_criminal(
    id : Annotated[str, Path()],
    NIC : Annotated[str, Form()]= None,
    First_Name : Annotated[str, Form()]= None,
    Last_Name : Annotated[str, Form()]= None,
    Tel_No : Annotated[str, Form()]= None,
    Province : Annotated[str , Form()]= None,
    City : Annotated[str, Form()]= None,
    Area : Annotated[str, Form()]= None,
    Address : Annotated[str, Form()]= None,
    Landmark : Annotated[str, Form()] = None,
    Photo_Of_Criminal : UploadFile = UPLOAD_DIR / 'avatar.png'
):
    return "Confusion"

    
    
    







            
            
            
    
