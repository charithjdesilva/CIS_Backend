from fastapi import APIRouter, Body,Form,File, Query,UploadFile,Path,HTTPException,status
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
from fastapi.responses import FileResponse
import os
from datetime import datetime

from database import db_dependency
from schemas import UserBase
from dummydata import users
from Images.path import UPLOAD_USER, UPLOAD_CRIMINAL
from Images.path import common_users_image, common_criminal_image
from models import User






router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)


@router.post('/register-user',description="Register User")
async def create_user(
    db: db_dependency,
    UserType : Annotated[str, Form(description="CriminalRegDept, ITOfficer, PoliceOfficer")],
    RegNo : Annotated[str , Form()],
    NIC : Annotated[str, Form()],
    FirstName : Annotated[str, Form()],
    LastName : Annotated[str, Form()],
    Tel_No : Annotated[str, Form(description="can be maximum 10 characters")] = None,
    Branch : Annotated[str, Form(description=" branch can be null because, some times a user cannot be associated with a branch such as while training")] = None,
    Province : Annotated[str , Form()] = None,
    District : Annotated[str, Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()]= None,
    Position : Annotated[str , Form()] = None,
    HouseNoOrName :Annotated[str , Form()] = None,
    JoinedDate : Annotated[str, Form()] = None,
    Photo : UploadFile = common_users_image,

):
    if JoinedDate:
        joined_date = datetime.strptime(JoinedDate, '%Y-%m-%d')
    else:
        joined_date = None
    
    save_to = common_users_image
    
    if Photo != common_users_image :
        data = await Photo.read()
        name , extension = os.path.splitext(Photo.filename)
        save_to = UPLOAD_USER / f"{NIC}_{RegNo}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)

    user = User(
        RegNo =  RegNo,
        NIC = NIC,
        FirstName = FirstName,
        LastName = LastName,
        Tel_No = Tel_No,
        Branch = Branch,
        UserType = UserType,
        JoinedDate = joined_date,
        Position = Position,
        Photo = save_to,
        Province=Province,
        District=District,
        City=City,
        Area=Area,
        HouseNoOrName=HouseNoOrName,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User created successfully"}
    except Exception as e :
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    
        
    

    


    


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
    photo_of_user : UploadFile = common_users_image

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
            # if photo_of_user != UPLOAD_DIR / 'avatar.png' and photo_of_user != userIn['photo_of_user'] :
            #     data = await photo_of_user.read()
            #     save_to = UPLOAD_DIR / photo_of_user.filename
            #     userIn['photo_of_user'] = save_to
            #     with open(save_to , 'wb') as f:
            #         f.write(data)
                

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
    Photo_Of_Criminal : UploadFile = common_criminal_image
):
    return "Confusion"

    
    
    







            
            
            
    
