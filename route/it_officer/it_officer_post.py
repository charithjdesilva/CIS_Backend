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
    """
    Reg_No : str
    NIC : str
    First_Name : str
    Last_Name : str
    Tel_No : list[str]
    Province : str
    City : str
    Area : str | None 
    Address : str
    Branch : str
    Position : str
    Join_Date : str
    photo_of_criminal : list[Image] | None = None
    
    """
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
            


            
            
            
    
