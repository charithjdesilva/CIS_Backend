from fastapi import APIRouter, HTTPException, Form, status, UploadFile,Path
from pydantic import BaseModel,EmailStr
from enum import Enum
from typing import Annotated
import os
from datetime import datetime



from dummydata import victims,crimes,evidences,criminals
from Security.password import is_valid_password
from Images.path import UPLOAD_CRIME, UPLOAD_VICTIM, UPLOAD_EVIDENCE, UPLOAD_CRIMINAL
from Images.path import common_image
from Images.image_upload import  update_crime_image , update_victim_image , update_evidence_image
from models import Crime,Photos,CrimePhoto,Person,PersonPhoto,Evidence,EvidencePhoto,CriminalOrSuspect,CrimeCriminal
from database import db_dependency


router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section - PATCH ']
)

base_url = "http://127.0.0.1:8000"

def make_image_url(file_path : str):
    file_path = file_path.replace("\\", "/").lstrip("/")
    url = f"{base_url}/{file_path}"
    return url

#update crime
@router.patch('/update/crime/{id}')
async def update_crime(
    db: db_dependency,
    id : Annotated[str, Path()],
    CrimeType : Annotated[str, Form()] = None,
    CrimeDate : Annotated[str, Form()] = None,
    CrimeTime : Annotated[str , Form()] = None,
    Province : Annotated[str, Form()] = None,
    District : Annotated[str, Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()] = None,
    Landmarks : Annotated[str, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    testimonials : Annotated[str , Form()] = None,
    photos_crime : UploadFile  = common_image,
):
    crime = db.query(Crime).filter(Crime.CrimeID == id).first()

    if crime:
        crime_photo = db.query(Photos).filter(Photos.PhotoID == crime.CrimeID).first()
        if crime_photo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"crime is not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"crime is not found")
    
    crime_photo = db.query(Photos).filter(Photos.PhotoID == crime.CrimeID).first()
    
    
    if CrimeType is not None:
        crime.CrimeType = CrimeType

    if CrimeDate is not None:
        joined_date = datetime.strptime(CrimeDate, '%Y-%m-%d')
        crime.CrimeDate = joined_date

    if CrimeTime is not None:
        crime.CrimeTime = CrimeTime
    
    if Province is not None:
        crime.Province = Province

    if District is not None:
        crime.District = District
    
    if City is not None:
        crime.City = City

    if Area is not None:
        crime.Area = Area

    if Landmarks is not None:
        crime.Landmarks = Landmarks

    if HouseNoOrName is not None:
        crime.HouseNoOrName = HouseNoOrName

    if testimonials is not None:
        crime.Testimonials = testimonials    

    if photos_crime != common_image:
        crime_photo.PhotoPath = await update_crime_image(photos_crime,UPLOAD_CRIME,crime,crime_photo)


    db.commit()
    db.refresh(crime)
    db.refresh(crime_photo)
    return {"message": "Crime updated successfully"}
    
    
#update victim
@router.patch('/update/victim/{victim_id}',description="If No Need to update a field Just set it as a blank")
async def update_victim(
    db : db_dependency,
    victim_id : Annotated[str, Path(description="Enter victim id")],
    CrimeID : Annotated[str , Form()] = None,
    FirstName : Annotated[str , Form()] = None,
    LastName : Annotated[str, Form()] = None,
    NIC : Annotated[str, Form()] = None,
    Gender : Annotated[str, Form(description="Enter Male or Female")] = None,
    LifeStatus : Annotated[str, Form()] = None,
    PhoneNo : Annotated[str, Form()] = None,
    Province : Annotated[str, Form()] = None,
    District : Annotated[str, Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()] = None,
    Landmark : Annotated[str|None, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    AdditionalDes : Annotated[str|None , Form()] = None,
    photos_victim : UploadFile  = common_image,
):
    victim_details = db.query(Person).filter(Person.PersonID == victim_id).first()

    if victim_details:
        victim_photo = db.query(Photos).filter(Photos.PhotoID == victim_details.PersonID).first()
        if victim_photo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"victim is not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"victim is not found")
    
    victim_photo = db.query(Photos).filter(Photos.PhotoID == victim_details.PersonID).first()

    if photos_victim != common_image:
        victim_photo.PhotoPath = await update_victim_image(photos_victim,UPLOAD_VICTIM,victim_photo)
    

    if CrimeID is not None:
        victim_details.CrimeID = CrimeID
    
    if FirstName is not None:
        victim_details.FirstName = FirstName
    
    if LastName is not None:
        victim_details.LastName = LastName

    if Gender is not None:
        victim_details.Gender = Gender

    if NIC is not None:
        victim_details.NIC = NIC
    
    if LifeStatus is not None:
        victim_details.LifeStatus = LifeStatus
    
    if PhoneNo is not None:
        victim_details.PhoneNo = PhoneNo

    if Province is not None:
        victim_details.Province = Province

    if District is not None:
        victim_details.District = District
    
    if City is not None:
        victim_details.City = City
    
    if Area is not None:
        victim_details.Area = Area
    
    if Landmark is not None:
        victim_details.Landmark = Landmark

    if HouseNoOrName is not None:
        victim_details.HouseNoOrName = HouseNoOrName
    
    if AdditionalDes is not None:
        victim_details.AdditionalDes = AdditionalDes

    db.commit()
    db.refresh(victim_details)
    db.refresh(victim_photo)
    return {"message": "Victim updated successfully"}
    

#update evidence
@router.patch('/update/evidence/{evidence_id}')
async def update_evidence(
    db : db_dependency,
    evidence_id : Annotated[str , Path(description="Enter evidence id ")],
    CrimeID : Annotated[str , Form()] = None,
    photo_of_evidence : UploadFile  = common_image,
    Testimonials : Annotated[str | None, Form()] = None,
):
    evidence_details = db.query(Evidence).filter(Evidence.EvidenceID == evidence_id).first()

    if evidence_details:
        evidence_photo = db.query(Photos).filter(Photos.PhotoID == evidence_details.EvidenceID).first()
        if evidence_photo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"evidence is not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"evidence is not found")
    
    evidence_photo = db.query(Photos).filter(Photos.PhotoID == evidence_details.EvidenceID).first()

    # if photo_of_evidence != common_image:
    #     data = await photo_of_evidence.read()
    #     name, extension = os.path.splitext(photo_of_evidence.filename)
    #     new_photo_filename = f"{evidence_details.EvidenceID}{extension}"
    #     new_photo_path = UPLOAD_EVIDENCE / new_photo_filename

    #     if evidence_photo.PhotoPath and evidence_details.EvidenceID in evidence_photo.PhotoPath:
    #         old_photo_filename = evidence_photo.PhotoPath.split('\\')[-1]
    #         old_photo_path = UPLOAD_EVIDENCE / old_photo_filename
    #         if old_photo_path.exists():
    #             old_photo_path.unlink()
        
    #     with open(new_photo_path, 'wb') as f:
    #         f.write(data)
    #     evidence_photo.PhotoPath = make_image_url(str(new_photo_path))

    if photo_of_evidence != common_image:
        evidence_photo.PhotoPath = await update_evidence_image(photo_of_evidence,UPLOAD_EVIDENCE,evidence_details,evidence_photo)
    
    if CrimeID is not None:
        evidence_details.CrimeID = CrimeID
    
    if Testimonials is not None:
        evidence_details.Testimonials = Testimonials
    
    db.commit()
    db.refresh(evidence_details)
    db.refresh(evidence_photo)
    return {"message": "Evidence updated successfully"}


#Update CriminalOrSuspect
@router.patch('/update/CriminalOrSuspect/{criminal_id:path}')
async def register_crim_suspect(
    db : db_dependency,
    PersonID : Annotated[str, Path(description="Enter Criminal ID")],
    CrimeID : Annotated[str , Form()] = None,
    LifeStatus : Annotated[str , Form()] = None,
    InCustody : Annotated[bool, Form()] = None,
    CrimeJustified : Annotated[bool , Form()] = None,
    FirstName : Annotated[str, Form()] = None,
    LastName : Annotated[str , Form()] = None,
    Gender : Annotated[str, Form(description="Enter Male or Female")]=None,
    NIC : Annotated[str , Form()] = None,
    PhoneNo : Annotated[str, Form()] = None,
    Province : Annotated[str , Form()] = None,
    City : Annotated[str, Form()] = None,
    Area : Annotated[str, Form()] = None,
    District : Annotated[str, Form()] = None,
    Landmark : Annotated[str , Form()]= None,
    AdditionalDes : Annotated[str, Form()] = None,
    HouseNoOrName : Annotated[str , Form()] = None,
    photo_criminal : UploadFile  =  common_image,
):
    criminal_person = db.query(Person).filter(Person.PersonID == PersonID).first()
    criminal_sus = db.query(CriminalOrSuspect).filter(CriminalOrSuspect.PersonID == PersonID).first()

    if criminal_person and criminal_sus:
        criminal_sus_photo = db.query(Photos).filter(Photos.PhotoID == criminal_person.PersonID).first()
        if criminal_sus_photo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"criminal/suspect is not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"criminal/suspect is not found")
    
    criminal_sus_photo = db.query(Photos).filter(Photos.PhotoID == criminal_person.PersonID).first()

    if photo_criminal != common_image:
        data = await photo_criminal.read()
        name, extension = os.path.splitext(photo_criminal.filename)
        new_photo_filename = f"{criminal_person.PersonID}{extension}"
        new_photo_path = UPLOAD_CRIMINAL / new_photo_filename

        if criminal_sus_photo.PhotoPath and criminal_person.PersonID in criminal_sus_photo.PhotoPath:
            old_photo_filename = criminal_sus_photo.PhotoPath.split('\\')[-1]
            old_photo_path = UPLOAD_CRIMINAL / old_photo_filename
            if old_photo_path.exists():
                old_photo_path.unlink()
        
        with open(new_photo_path, 'wb') as f:
            f.write(data)
        criminal_sus_photo.PhotoPath = make_image_url(str(new_photo_path))

    if CrimeID is not None:
        criminal_person.CrimeID = CrimeID

    if LifeStatus is not None:
        criminal_person.LifeStatus = LifeStatus
    
    if InCustody is not None:
        criminal_sus.InCustody = InCustody

    if CrimeJustified is not None:
        criminal_sus.CrimeJustified = CrimeJustified

    if FirstName is not None:
        criminal_person.FirstName = FirstName
    
    if LastName is not None:
        criminal_person.LastName = LastName
    
    if Gender is not None:
        criminal_person.Gender = Gender
    
    if NIC is not None:
        criminal_person.NIC = NIC
        criminal_sus.NIC = NIC
    
    if PhoneNo is not None:
        criminal_person.PhoneNo = PhoneNo
    
    if LifeStatus is not None:
        criminal_person.LifeStatus = LifeStatus

    if Province is not None:
        criminal_person.Province = Province

    if City is not None:
        criminal_person.City = City

    if Area is not None:
        criminal_person.Area = Area

    if District is not None:
        criminal_person.District = District
    
    if Landmark is not None:
        criminal_person.Landmark = Landmark
    
    if AdditionalDes is not None:
        criminal_person.AdditionalDes = AdditionalDes
    
    if HouseNoOrName is not None:
        criminal_person.HouseNoOrName = HouseNoOrName
    
    db.commit()
    db.refresh(criminal_person)
    db.refresh(criminal_sus_photo)
    db.refresh(criminal_sus)
    return {"message": "Evidence updated successfully"}
    
    