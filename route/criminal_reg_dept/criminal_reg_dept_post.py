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
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)


#Register Crime
#pending = add to database
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
#pending = add to database
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



#register evidence
#pending = add to database
@router.post('/register-evidence')
async def register_evidence(
    crime_id : Annotated[int , Form()],
    evidence_id : Annotated[int , Form()],
    photo_of_evidence : UploadFile  = common_evidence_image,
    testimonials : Annotated[str | None, Form()] = "",
):
    evidence = {
        "crime_id" : crime_id,
        "evidence_id" : evidence_id,
        "photo_of_evidence" : photo_of_evidence,
        "testimonials" : testimonials
    }

    if photo_of_evidence != common_evidence_image:
        data = await photo_of_evidence.read()
        name , extension = os.path.splitext(photo_of_evidence.filename)
        save_to = UPLOAD_EVIDENCE / f"{crime_id}_{evidence_id}{extension}"
        evidence['photo_of_evidence'] = save_to
        with open(save_to , 'wb') as f:
            f.write(data)

    evidences.append(evidence)
    return evidences

#Register CriminalOrSuspect
# Pending Work - add to database
@router.post('/register-CriminalOrSuspect')
async def register_crim_suspect(
    crime_id : Annotated[int , Form()],
    life_status : Annotated[str , Form()],
    in_custody : Annotated[str, Form()],
    crime_justified : Annotated[str , Form()],
    nic : Annotated[str , Form()],
    first_name : Annotated[str, Form()],
    last_name : Annotated[str , Form()],
    tel_no : Annotated[str, Form()],
    province : Annotated[str , Form()],
    city : Annotated[str | None, Form()] = "",
    area : Annotated[str | None, Form()] = "",
    address : Annotated[str | None, Form()] = "",
    landmark : Annotated[str | None , Form()]= "",
    photo_criminal : UploadFile  =  common_criminal_image,
    add_to_crimes : Annotated[list[str],Form()] = []  
):
    crim_suspect = {
        "crime_id" : crime_id,
        "life_status" : life_status,
        "in_custody" : in_custody,
        "crime_justified" : crime_justified,
        "nic" : nic,
        "first_name" : first_name,
        "last_name" : last_name,
        "tel_no" : tel_no,
        "province" : province,
        "city" : city,
        "area" : area,
        "address" : address,
        "landmark" : landmark,
        "photo_criminal" : photo_criminal,
        "add_to_crimes" : [crime for crime in add_to_crimes]

    }

    if photo_criminal != common_criminal_image:
        data = await photo_criminal.read()
        name , extension = os.path.splitext(photo_criminal.filename)
        save_to = UPLOAD_CRIMINAL / f"{nic}_{crime_id}_{life_status}{extension}"
        print(save_to)
        crim_suspect['photo_criminal'] = save_to
        with open(save_to , 'wb') as f:
            f.write(data)

    criminals.append(crim_suspect)
    return criminals
