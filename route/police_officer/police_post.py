from fastapi import APIRouter,HTTPException, Form
from typing import Annotated
from pydantic import BaseModel,EmailStr
from enum import Enum





router = APIRouter(
    prefix='/police-officer',
    tags=['Police Officer Section']
)





@router.post("/search/biodata")
def search_criminal(*,type : Annotated[str, Form(min_length=7)] = 'biodata', Biodata: Annotated[str , Form(description="Name or NIC")] ):
    return {
        "type" : type,
        "Biodata" : Biodata
    }

@router.post("/search/biometrics")
def search_criminal(*,type : Annotated[str, Form(min_length=7)] = 'biometrics', Biometrics: Annotated[str , Form(description="Scan Face or Upload Image or Fingerprint")] ):
    return {
        "type" : type,
        "Biodata" : Biometrics
    }



