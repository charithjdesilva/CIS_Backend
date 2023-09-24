from fastapi import APIRouter,HTTPException, Form , Path
from typing import Annotated
from pydantic import BaseModel,EmailStr
from enum import Enum


router = APIRouter(
    prefix='/police-officer',
    tags=['Police Officer Section']
)

@router.post("/search/biodata")
def search_criminal(id : Annotated[str , Form()]):
    return "give criminal details based on the id"

@router.post("/search/biometrics")
def search_criminal():
    return "give criminal details"

class IdType(str,Enum):
    criminal_id = "Criminal_id"
    Crime_id = "Crime_id"

@router.post("/report")
def send_request(id_type : Annotated[IdType , Form()], id : Annotated[str , Form()] ):
    return {"message" : f"{id_type.name} value submitted"}



