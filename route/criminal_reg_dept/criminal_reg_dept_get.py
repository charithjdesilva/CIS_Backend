from fastapi import APIRouter, HTTPException, Form,Path,status
from pydantic import BaseModel,EmailStr
from enum import Enum
import smtplib
# from secret123 import sender,receiver,password
from typing import Annotated
from Security.password import is_valid_password
from fastapi.responses import FileResponse
from dummydata import victims



router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)

@router.get('/{nic}/photo')
def get_victim_photo(nic : Annotated[str | None , Path()]):
    for victim in victims:
        if nic  == victim['nic']:
            return FileResponse(victim['photos_crime'])
    raise HTTPException(status_code=status.HTTP_200_OK, detail="victim is not found")



