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
from models import Crime,Photos,CrimePhoto,Person,PersonPhoto,Evidence,EvidencePhoto,CriminalOrSuspect,CrimeCriminal
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
#add the database = doubt
@router.post('/register-victim')
async def register_victim(
    db : db_dependency,
    CrimeID : Annotated[int, Form()],
    NIC : Annotated[str, Form()],
    FirstName : Annotated[str , Form()],
    LastName : Annotated[str, Form()],
    LifeStatus : Annotated[str, Form()] = None,
    PhoneNo : Annotated[str, Form()] = None,
    Province : Annotated[str, Form()] = None,
    District : Annotated[str, Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()] = None,
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
        PersonID = f"{NIC}_{CrimeID}",
        NIC = NIC,
        FirstName = FirstName,
        LastName = LastName,
        PhoneNo = PhoneNo,
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
       PhotoID =  NIC,
       PhotoType = "Victim",
       PhotoPath = save_to
    )

    person_photo = PersonPhoto(
        PhotoID = NIC,
        PersonID = f"{CrimeID}_{NIC}"
    )


    try:
        db.add(victim)
        db.commit()
        db.refresh(victim)

        db.add(photo_all)
        db.commit()
        db.refresh(photo_all)

        db.add(person_photo)
        db.commit()
        db.refresh(person_photo)

        return {"message": "Victim Registered Successfully"}
    except Exception as e :
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


    

    
    



#register evidence
#pending = add to database
@router.post('/register-evidence')
async def register_evidence(
    db : db_dependency,
    CrimeID : Annotated[int , Form()],
    EvidenceID : Annotated[int , Form()],
    photo_of_evidence : UploadFile  = common_evidence_image,
    Testimonials : Annotated[str | None, Form()] = "",
):
    
    if photo_of_evidence != common_evidence_image:
        data = await photo_of_evidence.read()
        name , extension = os.path.splitext(photo_of_evidence.filename)
        save_to = UPLOAD_EVIDENCE / f"{CrimeID}_{EvidenceID}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)
    
    save_to = common_victim_image

    evidence_details = Evidence(
        EvidenceID = EvidenceID,
        Testimonials = Testimonials
    )

    photo_all = Photos(
        PhotoID   =  EvidenceID,
        PhotoType =  "Evidence",
        PhotoPath =  save_to
    )

    evidence_photo = EvidencePhoto(
        PhotoID = EvidenceID,
        EvidenceID = EvidenceID
    )
    
    try:
        db.add(evidence_details)
        db.commit()
        db.refresh(evidence_details)

        db.add(photo_all)
        db.commit()
        db.refresh(photo_all)

        db.add(evidence_photo)
        db.commit()
        db.refresh(evidence_photo)

        return {"message": "Evidence Registered Successfully"}
    except Exception as e :
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


#Register CriminalOrSuspect
# Pending Work - add to database
@router.post('/register-CriminalOrSuspect')
async def register_crim_suspect(
    db : db_dependency,
    crime_id : Annotated[int , Form()],
    LifeStatus : Annotated[str , Form()],
    InCustody : Annotated[bool, Form()],
    CrimeJustified : Annotated[bool , Form()],
    NIC : Annotated[str , Form()],
    FirstName : Annotated[str, Form()],
    LastName : Annotated[str , Form()],
    PhoneNo : Annotated[str, Form()],
    Province : Annotated[str , Form()],
    City : Annotated[str | None, Form()] = "",
    Area : Annotated[str | None, Form()] = "",
    District : Annotated[str | None, Form()] = "",
    Landmark : Annotated[str | None , Form()]= "",
    AdditionalDes : Annotated[str | None, Form()] = "",
    HouseNoOrName : Annotated[str | None, Form()] = "",
    photo_criminal : UploadFile  =  common_criminal_image,
):
    
    save_to = common_criminal_image

    if photo_criminal != common_criminal_image:
        data = await photo_criminal.read()
        name , extension = os.path.splitext(photo_criminal.filename)
        save_to = UPLOAD_CRIMINAL / f"{NIC}_{crime_id}_{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)

    criminal = Person(
       PersonID =  NIC,
       NIC = NIC,
       FirstName = FirstName,
       LastName = LastName,
       PhoneNo = PhoneNo,
       PersonType = "Criminal or Suspect",
       LifeStatus = LifeStatus,
       Province = Province,
       District = District,
       City = City,
       Area = Area,
       AdditionalDes = AdditionalDes,
       Landmark = Landmark,
       HouseNoOrName =  HouseNoOrName

    )

    photo_sever = Photos(
        PhotoID = NIC,
        PhotoType = "Criminal or Suspect",
        PhotoPath = common_criminal_image
    )

    photo_criminal = PersonPhoto(
        PhotoID = NIC,
        PersonID = NIC
    )

    criminal_suspect = CriminalOrSuspect(
        InCustody = InCustody,
        CrimeJustified = CrimeJustified,
        NIC = NIC,
    )

    crime_criminal = CrimeCriminal(
        NIC = NIC,
        CrimeID = crime_id
    )

    
    try:
        db.add(criminal)
        db.commit()
        db.refresh(criminal)

        db.add(photo_sever)
        db.commit()
        db.refresh(photo_sever)

        db.add(criminal_suspect)
        db.commit()
        db.refresh(criminal_suspect)

        db.add(crime_criminal)
        db.commit()
        db.refresh(crime_criminal)

        return {"message": "Criminal or Suspect Registered Successfully"}
    except Exception as e :
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
