from typing import List,Annotated
from fastapi import APIRouter, Depends,Path,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse


from dummydata import users
from database import db_dependency
from models import User
from schemas import UserDisplay


router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)


@router.get("/user/all" , response_model=List[UserDisplay])
def show_user_details(db:db_dependency):
    users = db.query(User).all()
    # print(type(users[1].JoinedDate), users[1].JoinedDate)
    return users

@router.get('/user/image/{id:path}')
def search_user(id : Annotated[str, Path(description="Enter NIC or Registration Number")], db:db_dependency):
    user = db.query(User).filter(User.RegNo == id or User.NIC == id).first()
    if user and user.Photo:
        return FileResponse(user.Photo)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No image") 


@router.get('/user-details/{id:path}',response_model=UserDisplay)
def search_user(id : Annotated[str, Path(description="Enter NIC or Registration Number")], db:db_dependency):
    user = db.query(User).filter(User.RegNo == id or User.NIC == id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not found on the database")
    return user





# @router.get('/user-details/{id}')
# def search_user(id : Annotated[str, Path()]):
#     for user in users:
#         if id == user['Reg_No']:
#             return user
        
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not found on the database")



