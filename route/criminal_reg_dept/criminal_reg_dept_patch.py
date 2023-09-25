from fastapi import APIRouter, HTTPException, Form, status, UploadFile
from pydantic import BaseModel,EmailStr
from enum import Enum
from typing import Annotated
import os


from dummydata import victims,crimes,evidences,criminals
from Security.password import is_valid_password
from Images.path import UPLOAD_CRIME, UPLOAD_VICTIM, UPLOAD_EVIDENCE, UPLOAD_CRIMINAL
from Images.path import common_crime_image,common_criminal_image,common_evidence_image,common_victim_image


router = APIRouter(
    prefix="/criminal-reg-dept/update",
    tags=['criminal registration department section']
)

