from fastapi import APIRouter, HTTPException, Form, status, UploadFile
from pydantic import BaseModel,EmailStr
from enum import Enum
from typing import Annotated
import os
from datetime import datetime



from dummydata import victims,crimes,evidences,criminals
from Security.password import is_valid_password
from Images.path import UPLOAD_CRIME, UPLOAD_VICTIM, UPLOAD_EVIDENCE, UPLOAD_CRIMINAL
from Images.path import common_crime_image,common_criminal_image,common_evidence_image,common_victim_image
from models import Crime,Photos,CrimePhoto,Person,PersonPhoto
from database import db_dependency


router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)


#Register Crime
#pending = add to database
@router.post('/register-crime')
async def register_crime(
    db: db_dependency,
    CrimeID : Annotated[int, Form()],
    CrimeType : Annotated[str, Form()],
    CrimeDate : Annotated[str, Form()],
    CrimeTime : Annotated[str , Form()],
    Province : Annotated[str, Form()],
    District : Annotated[str, Form()],
    City : Annotated[str, Form()],
    Area : Annotated[str, Form()],
    Landmarks : Annotated[str, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    testimonials : Annotated[str , Form()] = None,
    photos_crime : UploadFile  = common_crime_image,
):
    if CrimeDate:
        joined_date = datetime.strptime(CrimeDate, '%Y-%m-%d')
    else:
        joined_date = None
    


    save_to = common_crime_image
    
    if photos_crime != common_victim_image:
        data = await photos_crime.read()
        name , extension = os.path.splitext(photos_crime.filename)
        save_to = UPLOAD_CRIME / f"{CrimeID}_{CrimeDate}_{CrimeType}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)
    
    crime = Crime(
        CrimeID = CrimeID,
        CrimeType = CrimeType,
        CrimeDate = joined_date,
        CrimeTime = CrimeTime,
        Province = Province,
        District = District,
        City = City,
        Area = Area,
        HouseNoOrName = HouseNoOrName,
        Landmarks = Landmarks,
        Testimonials = testimonials
    )

    photo = Photos(
        PhotoID = f"{CrimeID}_{CrimeDate}_{CrimeType}",
        PhotoType = "Crime",
        PhotoPath = save_to
    )

    crime_photo = CrimePhoto(
        PhotoID = f"{CrimeID}_{CrimeDate}_{CrimeType}",
        CrimeID = CrimeID
    )

    try:
        db.add(crime)
        db.commit()
        db.refresh(crime)

        db.add(photo)
        db.commit()
        db.refresh(photo)

        db.add(crime_photo)
        db.commit()
        db.refresh(crime_photo)

        return {"message": "Crime Registered Successfully"}
    except Exception as e :
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")




    
    

#Register Victim
#pending = add to database
@router.post('/register-victim')
async def register_victim(
    CrimeID : Annotated[int, Form()],
    LifeStatus : Annotated[str, Form()],
    NIC : Annotated[str, Form()],
    FirstName : Annotated[str , Form()],
    LastName : Annotated[str, Form()],
    PhoneNo : Annotated[str, Form()],
    Branch : Annotated[str, Form()],
    Province : Annotated[str, Form()],
    District : Annotated[str, Form()],
    City : Annotated[str, Form()],
    Area : Annotated[str, Form()],
    Landmark : Annotated[str|None, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    AdditionalDes : Annotated[str|None , Form()] = None,
    photos_victim : UploadFile  = common_victim_image,
):

    save_to = common_victim_image

    if photos_victim != common_victim_image:
        data = await photos_victim.read()
        name , extension = os.path.splitext(photos_victim.filename)
        save_to = UPLOAD_VICTIM / f"{CrimeID}_{NIC}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)

    victim = Person(
        PersonID = f"{CrimeID}_{NIC}",
        NIC = NIC,
        FirstName = FirstName,
        LastName = LastName,
        PhoneNo = PhoneNo,
        Branch = Branch,
        PersonType = "Victim",
        LifeStatus = LifeStatus,
        Province = Province,
        District = District,
        City = City,
        Area = Area,
        AdditionalDes = AdditionalDes,
        Landmark = Landmark,
        HouseNoOrName = HouseNoOrName,
        Photo = save_to
    )
    
    photo_all = Photos(
       PhotoID =  f"{CrimeID}_{NIC}",
       PhotoType = "Victim",
       PhotoPath = save_to
    )

    person_photo = PersonPhoto(
        PhotoID = f"{CrimeID}_{NIC}",
        PersonID = f"{CrimeID}_{NIC}"
    )


    

    
    



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
