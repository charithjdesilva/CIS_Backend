from typing import List,Annotated
from fastapi import APIRouter, Depends,Path,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from sqlalchemy import text, or_, and_



from dummydata import users
from database import db_dependency
from models import User
from schemas import UserDisplay
from auth import get_current_user


router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)

#current_user: dict = Depends(get_current_user)

@router.get("/user/all" , response_model=List[UserDisplay])
def show_user_details(db:db_dependency):
    users = db.query(User).all()
    return users

@router.get('/user/image/{id:path}')
def search_user(id : Annotated[str, Path(description="Enter NIC or Registration Number")], db:db_dependency):
    user = db.query(User).filter(or_(User.RegNo == id, User.NIC == id)).first()
    if user and user.Photo:
        photo_path = str(user.Photo)
        url = "http://127.0.0.1:8000/"
        converted_path = url + photo_path.replace('\\', '/')
        return {"Photolink" : photo_path}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No image") 


@router.get('/user-details/{id:path}',response_model=UserDisplay)
def search_user(id : Annotated[str, Path(description="Enter NIC or Registration Number")], db:db_dependency):
    user = db.query(User).filter(or_(User.RegNo == id , User.NIC == id)).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not found on the database")
    return user





# @router.get('/user-details/{id}')
# def search_user(id : Annotated[str, Path()]):
#     for user in users:
#         if id == user['Reg_No']:
#             return user
        
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not found on the database")



