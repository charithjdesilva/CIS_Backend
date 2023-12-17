from fastapi import APIRouter, Body, Depends, Form, File, Query, UploadFile, Path, HTTPException, status
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
from Images.path import common_image
from Images.image_upload import upload_image, update_user_image
from models import User
from Security.password import do_hash_password
from models import Crime, Photos, CrimePhoto, Person, PersonPhoto, Evidence, EvidencePhoto, CriminalOrSuspect, CrimeCriminal
from auth import get_current_user_CRD, get_current_user_IT_Officer,get_current_user_Police_Officer, get_current_user_CRD_admin


router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section'],
    # dependencies=[Depends(get_current_user_CRD_admin)]
)

base_url = "http://127.0.0.1:8000"


def date_modification(JoinedDate):
    if JoinedDate:
        joined_date = datetime.strptime(JoinedDate, '%Y-%m-%d')
    else:
        joined_date = None
    return joined_date

def make_image_url(file_path : str):
    file_path = file_path.replace("\\", "/").lstrip("/")
    url = f"{base_url}/{file_path}"
    return url


# @router.post('/register-user/by_CRD', description="Register all types of  User by CRD", dependencies=[Depends(get_current_user_CRD)])
@router.post('/register-user/by_CRD', description="Register all types of  User by CRD")
async def create_user(
    db: db_dependency,
    UserType: Annotated[str, Form(description="CriminalRegDept, ITOfficer, PoliceOfficer")],
    RegNo: Annotated[str, Form()],
    NIC: Annotated[str, Form()],
    FirstName: Annotated[str, Form()],
    LastName: Annotated[str, Form()],
    Gender: Annotated[str, Form(description="Enter Male or Female")],
    Email: Annotated[str, Form()],
    Password: Annotated[str, Form(
        min_length=8, max_length=256, description="Default dummy password included, if not include password")] = "12345678",
    Tel_No: Annotated[str, Form(
        description="can be maximum 10 characters")] = None,
    Branch: Annotated[str, Form(
        description=" branch can be null because, some times a user cannot be associated with a branch such as while training")] = None,
    Province: Annotated[str, Form()] = None,
    District: Annotated[str, Form()] = None,
    City: Annotated[str, Form()] = None,
    Area: Annotated[str, Form()] = None,
    Position: Annotated[str, Form()] = None,
    HouseNoOrName: Annotated[str, Form()] = None,
    JoinedDate: Annotated[str, Form(
        description="Enter YYYY-MM-DD Format")] = None,
    Photo: UploadFile = common_image,

):
    joined_date = date_modification(JoinedDate)

    save_to = None

    if Photo != common_image:
        save_to = await upload_image(Photo, NIC, UPLOAD_USER)

    hashed_password = do_hash_password(Password)

    user = User(
        RegNo=RegNo,
        NIC=NIC,
        FirstName=FirstName,
        LastName=LastName,
        Gender=Gender,
        Tel_No=Tel_No,
        Branch=Branch,
        Email=Email,
        UserType=UserType,
        JoinedDate=joined_date,
        Position=Position,
        Province=Province,
        District=District,
        City=City,
        Area=Area,
        HouseNoOrName=HouseNoOrName,
        PasswordHash=hashed_password,
        Photo=save_to
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User created successfully"}
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    


# -------------------------------------------------------------------------------------------
    

@router.post('/register-user/by_ITOfficer', description="Register ITOfficer and PoliceOfficer by ITOfficer", dependencies=[Depends(get_current_user_IT_Officer)])
async def create_user(
    db: db_dependency,
    UserType: Annotated[str, Form(description="CriminalRegDept, ITOfficer, PoliceOfficer")],
    RegNo: Annotated[str, Form()],
    NIC: Annotated[str, Form()],
    FirstName: Annotated[str, Form()],
    LastName: Annotated[str, Form()],
    Gender: Annotated[str, Form(description="Enter Male or Female")],
    Email: Annotated[str, Form()],
    Password: Annotated[str, Form(
        min_length=8, max_length=256, description="Default dummy password included, if not include password")] = "12345678",
    Tel_No: Annotated[str, Form(
        description="can be maximum 10 characters")] = None,
    Branch: Annotated[str, Form(
        description=" branch can be null because, some times a user cannot be associated with a branch such as while training")] = None,
    Province: Annotated[str, Form()] = None,
    District: Annotated[str, Form()] = None,
    City: Annotated[str, Form()] = None,
    Area: Annotated[str, Form()] = None,
    Position: Annotated[str, Form()] = None,
    HouseNoOrName: Annotated[str, Form()] = None,
    JoinedDate: Annotated[str, Form(
        description="Enter YYYY-MM-DD Format")] = None,
    Photo: UploadFile = common_image,

):
    joined_date = date_modification(JoinedDate)

    save_to = None

    if Photo != common_image:
        save_to = await upload_image(Photo, NIC, UPLOAD_USER)

    hashed_password = do_hash_password(Password)

    user = User(
        RegNo=RegNo,
        NIC=NIC,
        FirstName=FirstName,
        LastName=LastName,
        Gender=Gender,
        Tel_No=Tel_No,
        Branch=Branch,
        Email=Email,
        UserType=UserType,
        JoinedDate=joined_date,
        Position=Position,
        Province=Province,
        District=District,
        City=City,
        Area=Area,
        HouseNoOrName=HouseNoOrName,
        PasswordHash=hashed_password,
        Photo=save_to
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User created successfully"}
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    





# -------------------------------------------------------------------------------------------


@router.patch('/update-user/{id:path}', description="Only update the relevant fields ")
async def update_user(
    db: db_dependency,
    id: Annotated[str, Path(description="Enter Registration Number of the User")],
    NIC: Annotated[str, Form()] = None,
    FirstName: Annotated[str, Form()] = None,
    LastName: Annotated[str, Form()] = None,
    Gender: Annotated[str, Form(description="Enter Male or Female")] = None,
    Tel_No: Annotated[str, Form(
        description="can be maximum 10 characters")] = None,
    Branch: Annotated[str, Form(
        description=" branch can be null because, some times a user cannot be associated with a branch such as while training")] = None,
    Province: Annotated[str, Form()] = None,
    District: Annotated[str, Form()] = None,
    City: Annotated[str, Form()] = None,
    Area: Annotated[str, Form()] = None,
    Position: Annotated[str, Form()] = None,
    HouseNoOrName: Annotated[str, Form()] = None,
    JoinedDate: Annotated[str, Form(
        description="Enter YYYY-MM-DD Format")] = None,
    Photo: UploadFile = File(default=common_image),

):
    user = db.query(User).filter(User.RegNo == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found")

    if NIC is not None:
        user.NIC = NIC

    if FirstName is not None:
        user.FirstName = FirstName

    if LastName is not None:
        user.LastName = LastName

    if Gender is not None:
        user.Gender = Gender

    if Tel_No is not None:
        user.Tel_No = Tel_No

    if Province is not None:
        user.Province = Province

    if District is not None:
        user.District = District

    if HouseNoOrName is not None:
        user.HouseNoOrName = HouseNoOrName

    if City is not None:
        user.City = City

    if Area is not None:
        user.Area = Area

    if Branch is not None:
        user.Branch = Branch

    if Position is not None:
        user.Position = Position

    if JoinedDate is not None:
        join_date = datetime.strptime(JoinedDate, '%Y-%m-%d')
        user.JoinedDate = join_date

    save_to = None

    if Photo != common_image:
        save_to = await update_user_image(Photo, UPLOAD_USER, user)
        user.Photo = save_to

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully"}


@router.patch('/update/CriminalOrSuspect/{criminal_id:path}')
async def register_crim_suspect(
    db : db_dependency,
    PersonID : Annotated[str, Path(description="Enter Criminal ID")],
    CrimeID : Annotated[str , Form()] = None,
    LifeStatus : Annotated[str , Form()] = None,
    InCustody : Annotated[bool, Form()] = None,
    CrimeJustified : Annotated[bool , Form()] = None,
    FirstName : Annotated[str, Form()] = None,
    LastName : Annotated[str , Form()] = None,
    Gender : Annotated[str, Form(description="Enter Male or Female")]=None,
    NIC : Annotated[str , Form()] = None,
    PhoneNo : Annotated[str, Form()] = None,
    Province : Annotated[str , Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()] = None,
    District : Annotated[str, Form()] = None,
    Landmark : Annotated[str , Form()]= None,
    AdditionalDes : Annotated[str, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    photo_criminal : UploadFile  =  common_image,
):
    criminal_person = db.query(Person).filter(Person.PersonID == PersonID).first()
    criminal_sus = db.query(CriminalOrSuspect).filter(CriminalOrSuspect.PersonID == PersonID).first()

    if criminal_person and criminal_sus:
        criminal_sus_photo = db.query(Photos).filter(Photos.PhotoID == criminal_person.PersonID).first()
        if criminal_sus_photo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"criminal/suspect is not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"criminal/suspect is not found")
    
    criminal_sus_photo = db.query(Photos).filter(Photos.PhotoID == criminal_person.PersonID).first()

    if photo_criminal != common_image:
        data = await photo_criminal.read()
        name, extension = os.path.splitext(photo_criminal.filename)
        new_photo_filename = f"{criminal_person.PersonID}{extension}"
        new_photo_path = UPLOAD_CRIMINAL / new_photo_filename

        if criminal_sus_photo.PhotoPath and criminal_person.PersonID in criminal_sus_photo.PhotoPath:
            old_photo_filename = criminal_sus_photo.PhotoPath.split('\\')[-1]
            old_photo_path = UPLOAD_CRIMINAL / old_photo_filename
            if old_photo_path.exists():
                old_photo_path.unlink()
        
        with open(new_photo_path, 'wb') as f:
            f.write(data)
        criminal_sus_photo.PhotoPath = make_image_url(str(new_photo_path))

    if CrimeID is not None:
        criminal_person.CrimeID = CrimeID

    if LifeStatus is not None:
        criminal_person.LifeStatus = LifeStatus
    
    if InCustody is not None:
        criminal_sus.InCustody = InCustody

    if CrimeJustified is not None:
        criminal_sus.CrimeJustified = CrimeJustified

    if FirstName is not None:
        criminal_person.FirstName = FirstName
    
    if LastName is not None:
        criminal_person.LastName = LastName
    
    if Gender is not None:
        criminal_person.Gender = Gender
    
    if NIC is not None:
        criminal_person.NIC = NIC
        criminal_sus.NIC = NIC
    
    if PhoneNo is not None:
        criminal_person.PhoneNo = PhoneNo
    
    if LifeStatus is not None:
        criminal_person.LifeStatus = LifeStatus

    if Province is not None:
        criminal_person.Province = Province

    if City is not None:
        criminal_person.City = City

    if Area is not None:
        criminal_person.Area = Area

    if District is not None:
        criminal_person.District = District
    
    if Landmark is not None:
        criminal_person.Landmark = Landmark
    
    if AdditionalDes is not None:
        criminal_person.AdditionalDes = AdditionalDes
    
    if HouseNoOrName is not None:
        criminal_person.HouseNoOrName = HouseNoOrName
    
    db.commit()
    db.refresh(criminal_person)
    db.refresh(criminal_sus_photo)
    db.refresh(criminal_sus)
    return {"message": "Evidence updated successfully"}