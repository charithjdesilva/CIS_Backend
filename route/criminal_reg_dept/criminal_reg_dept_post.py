from fastapi import APIRouter, HTTPException, Form, status
from pydantic import BaseModel,EmailStr
from enum import Enum
import smtplib
# from secret123 import sender,receiver,password
from typing import Annotated
from Security.password import is_valid_password
from fastapi import UploadFile
from pathlib import Path
import os
from dummydata import victims

UPLOAD_CRIME = Path() / 'crime_images'
UPLOAD_VICTIM = Path() / 'victim_images'


router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)

crimes = []

common_crime_image = UPLOAD_CRIME / 'common.jpg'
common_victim_image = UPLOAD_VICTIM / 'common.png'

#Register Crime
@router.post('/register-crime')
async def register_crime(
    crime_id : Annotated[int, Form()],
    crime_type : Annotated[str, Form()],
    date : Annotated[str, Form()],
    time : Annotated[str , Form()],
    province : Annotated[str, Form()],
    district : Annotated[str, Form()],
    city : Annotated[str, Form()],
    area : Annotated[str, Form()],
    address : Annotated[str|None, Form()] = None,
    landmark : Annotated[str|None, Form()] = None,
    houseNoOrName : Annotated[str , Form()] = None,
    testimonials : Annotated[str|None , Form()] = None,
    photos_crime : UploadFile  = common_crime_image,
):
    crime = {
        "crime_id" : crime_id ,
        "crime_type" :crime_type,
        "date" : date,
        "time" : time,
        "province" : province,
        "district" : district,
        "city" : city,
        "area" : area,
        "address" : address if address else "",
        "landmark" : landmark if landmark else "",
        "houseNoOrName" : houseNoOrName if houseNoOrName else "",
        "testimonials" : testimonials if testimonials else "",
        "photos_crime" : photos_crime,
    }

    if photos_crime != common_victim_image:
        data = await photos_crime.read()
        name , extension = os.path.splitext(photos_crime.filename)
        save_to = UPLOAD_CRIME / photos_crime.filename
        crime['photos_crime'] = save_to
        with open(save_to , 'wb') as f:
            f.write(data)
    
    crimes.append(crime)
    return crimes

#Register Victim
@router.post('/register-victim')
async def register_victim(
    crime_id : Annotated[int, Form()],
    life_status : Annotated[str, Form()],
    nic : Annotated[str, Form()],
    first_name : Annotated[str , Form()],
    last_name : Annotated[str, Form()],
    tel_no : Annotated[str, Form()],
    province : Annotated[str, Form()],
    district : Annotated[str, Form()],
    city : Annotated[str, Form()],
    area : Annotated[str, Form()],
    address : Annotated[str|None, Form()] = None,
    landmark : Annotated[str|None, Form()] = None,
    houseNoOrName : Annotated[str , Form()] = None,
    additional_info : Annotated[str|None , Form()] = None,
    photos_victim : UploadFile  = common_victim_image,
):
    victim = {
        "crime_id" : crime_id ,
        "life_status" :life_status,
        "nic" : nic,
        "first_name" : first_name,
        "last_name" : last_name,
        "tel_no" : tel_no,
        "province" : province,
        "district" : district,
        "city" : city,
        "area" : area,
        "address" : address if address else "",
        "landmark" : landmark if landmark else "",
        "houseNoOrName" : houseNoOrName if houseNoOrName else "",
        "additional_info" : additional_info if additional_info else "",
        "photos_crime" : photos_victim,
    }

    if photos_victim != common_victim_image:
        data = await photos_victim.read()
        name , extension = os.path.splitext(photos_victim.filename)
        save_to = UPLOAD_VICTIM / f"{crime_id}_{nic}{extension}"
        victim['photos_crime'] = save_to
        with open(save_to , 'wb') as f:
            f.write(data)
    
    victims.append(victim)
    return victims
