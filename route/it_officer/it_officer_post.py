from fastapi import APIRouter,Form,File,UploadFile,Path,HTTPException,status
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from schemas import UserBase
from dummydata import users

router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)



@router.post('/register-user')
def create_user(user : UserBase ):
    users.append(user)
    return status.HTTP_200_OK


@router.patch('/update-user/{id}')
def update_user(id : Annotated[str, Path()],user : UserBase):
    # for each_user in users:
    #     if each_user['Reg_No'] == id:
    #         # for key,value in each_user.items():
    #         #     user.

    #         #     if (key == 'photo_of_criminal'):

    #         #         for key_nest,value_nest in each_user.key.items():
    #         #             each_user.key[key_nest] = user.key.key_nest if (user.key.key_nest != each_user.key[key_nest]) else each_user.key[key_nest]
                
    #         #     each_user[key] = user.key if (user.key != 'string' and user.key != each_user[key] and key != 'Reg_No' and key != 'photo_of_criminal') else each_user[key]
    #         # return status.HTTP_200_OK
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is not found on the dummy data")
    return "hello"
    
