from fastapi import APIRouter, Body, Depends,Form,File, Query,UploadFile,Path,HTTPException,status
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
from Security.password import do_hash_password
from models import Crime,Photos,CrimePhoto,Person,PersonPhoto,Evidence,EvidencePhoto,CriminalOrSuspect,CrimeCriminal
from auth import get_current_active_user


from Images.image_upload import upload_user_image


router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section'],
    # dependencies=[Depends(get_current_active_user)]
)


@router.post('/register-user',description="Register User")
async def create_user(
    db: db_dependency,
    UserType : Annotated[str, Form(description="CriminalRegDept, ITOfficer, PoliceOfficer")],
    RegNo : Annotated[str , Form()],
    NIC : Annotated[str, Form()],
    FirstName : Annotated[str, Form()],
    LastName : Annotated[str, Form()],
    Email : Annotated[str, Form()],
    Password : Annotated[str, Form(min_length=8,max_length=256, description="Default dummy password included, if not include password")] = "12345678",
    Tel_No : Annotated[str, Form(description="can be maximum 10 characters")] = None,
    Branch : Annotated[str, Form(description=" branch can be null because, some times a user cannot be associated with a branch such as while training")] = None,
    Province : Annotated[str , Form()] = None,
    District : Annotated[str, Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()]= None,
    Position : Annotated[str , Form()] = None,
    HouseNoOrName :Annotated[str , Form()] = None,
    JoinedDate : Annotated[str, Form(description="Enter YYYY-MM-DD Format")] = None,
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
        save_to = UPLOAD_USER / f"{NIC}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)

    
    

    

    # save_to = await upload_user_image(Photo, RegNo)

    hashed_password = do_hash_password(Password)

    user = User(
        RegNo =  RegNo,
        NIC = NIC,
        FirstName = FirstName,
        LastName = LastName,
        Tel_No = Tel_No,
        Branch = Branch,
        Email = Email,
        UserType = UserType,
        JoinedDate = joined_date,
        Position = Position,
        Province=Province,
        District=District,
        City=City,
        Area=Area,
        HouseNoOrName=HouseNoOrName,
        PasswordHash = hashed_password
    )

    if save_to == common_users_image:
        user.Photo = None

    


    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User created successfully"}
    except Exception as e :
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.patch('/update-user/{id:path}' ,description="Only update the relevant fields ")
async def update_user(
    db: db_dependency,
    id : Annotated[str, Path(description="Enter Registration Number of the User")],
    NIC : Annotated[str, Form()] = None,
    FirstName : Annotated[str, Form()] = None,
    LastName : Annotated[str, Form()] = None,
    Tel_No : Annotated[str, Form(description="can be maximum 10 characters")] = None,
    Branch : Annotated[str, Form(description=" branch can be null because, some times a user cannot be associated with a branch such as while training")] = None,
    Province : Annotated[str , Form()] = None,
    District : Annotated[str, Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()]= None,
    Position : Annotated[str , Form()] = None,
    HouseNoOrName :Annotated[str , Form()] = None,
    JoinedDate : Annotated[str, Form(description="Enter YYYY-MM-DD Format")] = None,
    Photo : UploadFile = File(default=common_users_image),

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


    # if Photo != common_users_image:
    #     data = await Photo.read()
    #     name, extension = os.path.splitext(Photo.filename)
    #     save_to = UPLOAD_USER / f"{user.RegNo}{extension}"
    #     with open(save_to, 'wb') as f:
    #         f.write(data)
    #     user.Photo = save_to

    if Photo != common_users_image:
        data = await Photo.read()
        name, extension = os.path.splitext(Photo.filename)
        new_photo_filename = f"{user.RegNo}{extension}"
        new_photo_path = UPLOAD_USER / new_photo_filename

        # Check if the existing photo in the database contains the RegNo
        if user.Photo and user.RegNo in user.Photo:
            # If it contains, construct the old photo path and delete it
            old_photo_filename = user.Photo.split('\\')[-1]
            print("old photo name :", old_photo_filename, user.Photo.split('\\'))
            old_photo_path = UPLOAD_USER / old_photo_filename
            if old_photo_path.exists():
                old_photo_path.unlink()
        
        with open(new_photo_path, 'wb') as f:
            f.write(data)
        user.Photo = str(new_photo_path)


    # save_to = await upload_user_image(Photo, user.RegNo)
    # user.Photo = save_to
    
        

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully"}



# @router.post('/CriminalOrSuspect/Update/{id}')
# async def register_crim_suspect(
#     db : db_dependency,
#     id : Annotated[str, Path(description = "enter person id")],
#     CrimeID : Annotated[int , Form()] = None,
#     LifeStatus : Annotated[str , Form()] = None,
#     InCustody : Annotated[bool, Form()] = None,
#     CrimeJustified : Annotated[bool , Form()] = None,
#     NIC : Annotated[str , Form()] = None,
#     FirstName : Annotated[str, Form()] = None,
#     LastName : Annotated[str , Form()] = None,
#     PhoneNo : Annotated[str, Form()] = None,
#     Province : Annotated[str , Form()] = None,
#     City : Annotated[str, Form()] = None,
#     Area : Annotated[str, Form()] = None,
#     District : Annotated[str, Form()] = None,
#     Landmark : Annotated[str , Form()]= None,
#     AdditionalDes : Annotated[str, Form()] = None,
#     HouseNoOrName : Annotated[str , Form()] = None,
#     photo_criminal : UploadFile  =  common_criminal_image,
# ):
    
#     save_to = common_criminal_image

#     if photo_criminal != common_criminal_image:
#         data = await photo_criminal.read()
#         name , extension = os.path.splitext(photo_criminal.filename)
#         save_to = UPLOAD_CRIMINAL / f"{id}{extension}"
#         with open(save_to , 'wb') as f:
#             f.write(data)
    


#     criminal = Person(
#        CrimeID = CrimeID,
#        PersonID =  NIC,
#        NIC = NIC,
#        FirstName = FirstName,
#        LastName = LastName,
#        PhoneNo = PhoneNo,
#        PersonType = "Criminal or Suspect",
#        LifeStatus = LifeStatus,
#        Province = Province,
#        District = District,
#        City = City,
#        Area = Area,
#        AdditionalDes = AdditionalDes,
#        Landmark = Landmark,
#        HouseNoOrName =  HouseNoOrName

#     )

#     photo_sever = Photos(
#         PhotoID = PersonID,
#         PhotoType = "Criminal or Suspect",
#         PhotoPath = save_to if save_to else None
#     )

#     photo_criminal = PersonPhoto(
#         PhotoID = PersonID,
#         PersonID = PersonID
#     )

#     criminal_suspect = CriminalOrSuspect(
#         InCustody = InCustody,
#         CrimeJustified = CrimeJustified,
#         NIC = NIC,
#         PersonID = PersonID
#     )

#     crime_criminal = CrimeCriminal(
#         PersonID = PersonID,
#         CrimeID = CrimeID
#     )

    
#     try:
#         db.add(criminal)
#         db.commit()
#         db.refresh(criminal)

#         db.add(photo_sever)
#         db.commit()
#         db.refresh(photo_sever)

#         db.add(criminal_suspect)
#         db.commit()
#         db.refresh(criminal_suspect)

#         db.add(crime_criminal)
#         db.commit()
#         db.refresh(crime_criminal)

#         return {"message": "Criminal or Suspect Registered Successfully"}
#     except Exception as e :
#         error_message = str(e)
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")



    
    







            
            
            
    
