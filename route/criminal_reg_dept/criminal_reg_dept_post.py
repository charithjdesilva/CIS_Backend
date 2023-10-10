from fastapi import APIRouter, HTTPException, Form, status, UploadFile
from pydantic import BaseModel,EmailStr
from enum import Enum
from typing import Annotated
import os
from datetime import datetime

from sqlalchemy import or_



from dummydata import victims,crimes,evidences,criminals
from Security.password import is_valid_password
from Images.path import UPLOAD_CRIME, UPLOAD_VICTIM, UPLOAD_EVIDENCE, UPLOAD_CRIMINAL , UPLOAD_SUSPECT
from Images.path import common_crime_image,common_criminal_image,common_evidence_image,common_victim_image,common_suspect_image
from models import Crime,Photos,CrimePhoto,Person,PersonPhoto,Evidence,EvidencePhoto,CriminalOrSuspect,CrimeCriminal
from database import db_dependency


router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section POST']
)

base_url = "http://127.0.0.1:8000"

def make_image_url(file_path : str):
    file_path = file_path.replace("\\", "/").lstrip("/")
    url = f"{base_url}/{file_path}"
    return url


#Register Crime
@router.post('/register-crime')
async def register_crime(
    db: db_dependency,
    CrimeID : Annotated[str, Form()],
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

    img_url = None
    
    if photos_crime != common_crime_image:
        data = await photos_crime.read()
        name , extension = os.path.splitext(photos_crime.filename)
        save_to = UPLOAD_CRIME / f"{CrimeID}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)
        img_url = make_image_url(str(save_to))
        
        
    
        
    

    
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
        PhotoID =  CrimeID,
        PhotoType = "Crime",
        PhotoPath = img_url
    )

    crime_photo = CrimePhoto(
        PhotoID = CrimeID,
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


# ---------------------------------------------------------------------------------------------------------------


    
#Register Victim
#add the database = doubt
@router.post('/register-victim')
async def register_victim(
    db : db_dependency,
    VictimID : Annotated[str, Form()],
    CrimeID : Annotated[str , Form()],
    FirstName : Annotated[str , Form()],
    LastName : Annotated[str, Form()],
    NIC : Annotated[str, Form()] = None,
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

    img_url = None

    if photos_victim != common_victim_image:
        data = await photos_victim.read()
        name , extension = os.path.splitext(photos_victim.filename)
        save_to = UPLOAD_VICTIM / f"{VictimID}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)
        img_url = make_image_url(str(save_to))
    

    


    victim = Person(
        PersonID = VictimID,
        CrimeID = CrimeID,
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
    )
    
    photo_all = Photos(
       PhotoID =  VictimID,
       PhotoType = "Victim",
       PhotoPath = img_url
    )

    person_photo = PersonPhoto(
        PhotoID = VictimID,
        PersonID = VictimID 
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
    CrimeID : Annotated[str , Form()],
    EvidenceID : Annotated[str , Form()],
    photo_of_evidence : UploadFile  = common_evidence_image,
    Testimonials : Annotated[str | None, Form()] = None,
):
    img_url = None
    
    if photo_of_evidence != common_evidence_image:
        data = await photo_of_evidence.read()
        name , extension = os.path.splitext(photo_of_evidence.filename)
        save_to = UPLOAD_EVIDENCE / f"{EvidenceID}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)
        img_url = make_image_url(str(save_to))
    
    
    

    evidence_details = Evidence(
        EvidenceID = EvidenceID,
        Testimonials = Testimonials,
        CrimeID = CrimeID
    )

    photo_all = Photos(
        PhotoID   =  EvidenceID,
        PhotoType =  "Evidence",
        PhotoPath =  img_url
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


#Register Suspect
@router.post('/register-suspect',description="Register suspect")
async def register_suspect(
    db : db_dependency,
    CrimeID : Annotated[str , Form()],
    SuspectID : Annotated[str, Form()],
    LifeStatus : Annotated[str , Form()],
    FirstName : Annotated[str, Form()],
    LastName : Annotated[str , Form()],
    InCustody : Annotated[bool, Form()],
    CrimeJustified : Annotated[bool , Form()] = False,
    NIC : Annotated[str , Form()] = None,
    PhoneNo : Annotated[str, Form()] = None,
    Province : Annotated[str , Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()] = None,
    District : Annotated[str, Form()] = None,
    Landmark : Annotated[str , Form()]= None,
    AdditionalDes : Annotated[str, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    photo_suspect : UploadFile  =  common_suspect_image,
):
    
    img_url = None

    if photo_criminal != common_criminal_image:
        data = await photo_criminal.read()
        name , extension = os.path.splitext(photo_criminal.filename)
        save_to = UPLOAD_SUSPECT / f"{SuspectID}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)
        img_url = make_image_url(str(save_to))

    
    


    criminal = Person(
       CrimeID = CrimeID,
       PersonID =  SuspectID,
       NIC = NIC,
       FirstName = FirstName,
       LastName = LastName,
       PhoneNo = PhoneNo,
       PersonType = "Suspect",
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
        PhotoID = SuspectID,
        PhotoType = "Suspect",
        PhotoPath = img_url
    )

    photo_criminal = PersonPhoto(
        PhotoID = SuspectID,
        PersonID = SuspectID
    )

    criminal_suspect = CriminalOrSuspect(
        InCustody = InCustody,
        CrimeJustified = CrimeJustified,
        NIC = NIC,
        PersonID = SuspectID
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

        return {"message": "Suspect Registered Successfully"}
    except Exception as e :
        error_message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")



#Register Criminal
@router.post('/register-criminal',description="Register criminal")
async def register_criminal(
    db : db_dependency,
    CriminalID : Annotated[str, Form()],
    LifeStatus : Annotated[str , Form()],
    FirstName : Annotated[str, Form()],
    LastName : Annotated[str , Form()],
    InCustody : Annotated[bool, Form()],
    CrimeJustified : Annotated[bool , Form()] = True,
    CrimeID : Annotated[list[str] , Form()] = [],
    NIC : Annotated[str , Form()] = None,
    PhoneNo : Annotated[str, Form()] = None,
    Province : Annotated[str , Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()] = None,
    District : Annotated[str, Form()] = None,
    Landmark : Annotated[str , Form()]= None,
    AdditionalDes : Annotated[str, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    photo_criminal : UploadFile  =  common_criminal_image,
):
    
    criminal_available = db.query(Person).filter(or_(Person.PersonID == CriminalID ,Person.NIC == NIC)).first()

    if criminal_available is None:
        img_url = None

        if photo_criminal != common_criminal_image:
            data = await photo_criminal.read()
            name , extension = os.path.splitext(photo_criminal.filename)
            save_to = UPLOAD_CRIMINAL / f"{CrimeID}{extension}"
            with open(save_to , 'wb') as f:
                f.write(data)
            img_url = make_image_url(str(save_to))

        criminal = Person(
        CrimeID = CrimeID,
        PersonID =  CrimeID,
        NIC = NIC,
        FirstName = FirstName,
        LastName = LastName,
        PhoneNo = PhoneNo,
        PersonType = "Criminal",
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
            PhotoID = CrimeID,
            PhotoType = "Criminal",
            PhotoPath = img_url
        )

        photo_criminal = PersonPhoto(
            PhotoID = CriminalID,
            PersonID = CriminalID
        )

        crime_criminal = CrimeCriminal(
            PersonID = CriminalID,
            CrimeID = CrimeID
        )

        criminal_suspect = CriminalOrSuspect(
            InCustody = InCustody,
            CrimeJustified = CrimeJustified,
            NIC = NIC,
            PersonID = CriminalID
        )

        try:
            db.add(criminal)
            db.commit()
            db.refresh(criminal)

            db.add(photo_sever)
            db.commit()
            db.refresh(photo_sever)

            return {"message": "Suspect Registered Successfully"}
        except Exception as e :
            error_message = str(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
