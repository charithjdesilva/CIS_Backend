from fastapi import APIRouter, Body,Form,File, Query,UploadFile,Path,HTTPException,status
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from schemas import UserBase
from dummydata import users
from pathlib import Path
from fastapi.responses import FileResponse


UPLOAD_DIR = Path() / 'uploads'


router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)



@router.post('/register-user',description="user can enter textual details to create user profile with defaullt avatar")
def create_user(user : UserBase):
    user_profile={**user.model_dump(), "user_photo" : UPLOAD_DIR / 'avatar.png'}
    users.append(user_profile)
    return status.HTTP_200_OK

@router.post("/user-photo")
async def upload_user_image( id : Annotated[str,Query()],file: UploadFile| None = None ):
    if file:
        for user in users:
            if user['Reg_No'] == id :
                data = await file.read()
                save_to = UPLOAD_DIR / file.filename
                user['photo'] = save_to
                with open(save_to , 'wb') as f:
                    f.write(data)
                # return status.HTTP_200_OK
                return FileResponse(save_to)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is not found to insert image")
                
        


    

@router.post('/user/upload-photos/{id}')
def upload_user_photo(id : Annotated[str, Path()], user_photo : UploadFile = File(...)):
    for user in users:
        if user['Reg_No'] == id :
            user['photos'] = user_photo.filename
            return status.HTTP_200_OK
        
    raise HTTPException(status_code=404,detail=f"{id} is not found in the db")


@router.patch('/update-user/{id}')
def partial_update_user(id : Annotated[str, Path()],user : UserBase):
    for userIn in users:
        if userIn['Reg_No'] == id :
            userIn['NIC'] = user.NIC if user.NIC != ''  else userIn['NIC']
            userIn['First_Name'] = user.First_Name if user.First_Name != ''  else userIn['First_Name']
            userIn['Last_Name'] = user.Last_Name if user.Last_Name != '' else userIn['Last_Name']
            userIn['Province'] = user.Province if user.Province != ''  else userIn['Province']
            userIn['City'] = user.City if user.City != ''  else userIn['City']
            userIn['Area'] = user.Area if user.Area != ''  else userIn['Area']
            userIn['Address'] = user.Address if user.Address != ''  else userIn['Address']
            userIn['Position'] = user.Position if user.Position != ''  else userIn['Position']
            userIn['Join_Date'] = user.Join_Date if user.Join_Date != ''  else userIn['Join_Date']
            userIn['Branch'] = user.Branch if user.Branch != ''  else userIn['Branch']
            return status.HTTP_200_OK
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" id - {id} is not found")

@router.put('/update-user/{id}')
def full_update_user(id : Annotated[str, Path()],user : UserBase):
    for userIn in users:
        if userIn['Reg_No'] == id :
            userIn['NIC'] = user.NIC 
            userIn['First_Name'] = user.First_Name 
            userIn['Last_Name'] = user.Last_Name 
            userIn['Province'] = user.Province 
            userIn['City'] = user.City 
            userIn['Area'] = user.Area 
            userIn['Address'] = user.Address 
            userIn['Position'] = user.Position 
            userIn['Join_Date'] = user.Join_Date 
            userIn['Branch'] = user.Branch 
            return status.HTTP_200_OK
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id - {id} is not found")
            


            
            
            
    
