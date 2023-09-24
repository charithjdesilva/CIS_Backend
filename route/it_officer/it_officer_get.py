from typing import List,Annotated
from fastapi import APIRouter,Path,HTTPException,status
from dummydata import users
from schemas import UserBase

router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)


@router.get("/view/all-users")
def show_user_details():
    return users

@router.get('/search-user/{id}')
def search_user(id : Annotated[str, Path()]):
    for user in users:
        if id == user['Reg_No'] or id == user['NIC']:
            return user
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not found on the database")

@router.get('/user-details/{id}')
def search_user(id : Annotated[str, Path()]):
    for user in users:
        if id == user['Reg_No']:
            return user
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not found on the database")



