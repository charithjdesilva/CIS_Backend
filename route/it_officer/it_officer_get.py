from typing import List,Annotated
from fastapi import APIRouter,Path,HTTPException,status
from dummydata import users
from schemas import UserBase

router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)



@router.get('/homepage')
def homepage():
    return "render homepage of it officer"


@router.get("/user-details")
def show_user_details():
    return users

@router.get('/search-user/{search}')
def search_user(search : Annotated[str, Path()]):
    for user in users:
        if search == user['Reg_No']:
            return user
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{search} id is not found on the database")


