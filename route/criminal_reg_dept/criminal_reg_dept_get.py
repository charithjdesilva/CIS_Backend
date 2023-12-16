from fastapi import APIRouter, HTTPException, Form, Path, status
from pydantic import BaseModel, EmailStr
from enum import Enum
import smtplib
from typing import Annotated
from Security.password import is_valid_password
from fastapi.responses import FileResponse
from dummydata import victims
from database import db_dependency
from models import Crime, Photos, CrimePhoto, Person, PersonPhoto, Evidence, EvidencePhoto , CrimeCriminal, CriminalOrSuspect
from sqlalchemy import text, or_, and_
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section - GET']
)



@router.get('/all/crimes')
def get_all_crimes(db: db_dependency):
    crime_list = []
    crimes = db.query(Crime).all()
    crime_photos = db.query(Photos).filter(Photos.PhotoType == "Crime").all()
    for index,crime in enumerate(crimes):
        crime_data = {
            **crime.__dict__,
            "PhotoPath ":crime_photos[index].PhotoPath
        }
        crime_list.append(crime_data)
    
    return crime_list


@router.get('/all/crimes_desc')
def get_all_crimes(db: db_dependency):
    crime_list = []
    crimes = db.query(Crime).all()
    crime_photos = db.query(Photos).filter(Photos.PhotoType == "Crime").all()
    for index,crime in enumerate(crimes):
        crime_data = {
            crime.CrimeID : f"{crime.CrimeType} {crime.City} {crime.Area}"
        }
        crime_list.append(crime_data)
    
    return crime_list


@router.get('/find/crime/{crime_id}')
def get_crime_by_crimeid(db: db_dependency, crime_id: Annotated[str, Path(description="Enter Crime ID ")]):
    crime = db.query(Crime).filter(Crime.CrimeID == crime_id).first()
    if not crime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No crime details")
    crime_photo = db.query(Photos).filter(Photos.PhotoID == crime.CrimeID).first()
    crime_data = {
        **crime.__dict__, "PhotoPath ": crime_photo.PhotoPath
    }
    return crime_data


@router.get('/all/victim')
def get_all_victims(db: db_dependency):
    victims = db.query(Person).filter(text("PersonID LIKE 'VID%'")).all()
    victims_photos = db.query(Photos).filter(Photos.PhotoType == "Victim").all()
    victim_list = []

    for index,victim in enumerate(victims):
        victim_data = {
            **victim.__dict__,
            "PhotoPath" : victims_photos[index].PhotoPath
        }
        victim_list.append(victim_data)
    
    return victim_list



@router.get('/find/victim/{id}')
def get_victim_by_crimeID_OR_VictimID(db: db_dependency, id: Annotated[str, Path(description="Enter Crime ID / Victim ID")]):
    victims = db.query(Person).filter(or_(Person.PersonID == id, Person.CrimeID == id)).filter(text("PersonID LIKE 'VID%'")).all()
    if not victims:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No victim details")
    
    victim_photos = db.query(Photos).filter(Photos.PhotoID.in_(
        [victim.PersonID for victim in victims])).all()
    
    if not victim_photos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No victim details")
    
    victim_list = []
    
    for index,victim in enumerate(victims):
        victim_data = {
            **victim.__dict__,
            "PhotoPath" : victim_photos[index].PhotoPath
        }
        victim_list.append(victim_data)

    return victim_list


@router.get('/all/evidence')
def get_all_evidence(db: db_dependency):
    evidences = db.query(Evidence).all()
    evidence_photos = db.query(Photos).filter(Photos.PhotoType == "Evidence").all()

    evidence_list = []

    for index,evidence in enumerate(evidences):
        evidence_data = {
            **evidence.__dict__,
            "PhotoPath" : evidence_photos[index].PhotoPath
        }
        evidence_list.append(evidence_data)

    return evidence_list


@router.get('/find/evidence/{id}')
def get_evidence_by_evidenceID_crimeID(db: db_dependency, id: Annotated[str, Path(description="Enter Evidence ID / Crime ID ")]):
    evidences = db.query(Evidence).filter(or_(Evidence.EvidenceID == id, Evidence.CrimeID == id)).all()
    if not evidences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No evidence details")

    evidence_photos = db.query(Photos).filter(Photos.PhotoID.in_(
        [evidence.EvidenceID for evidence in evidences])).all()
    
    evidence_list = []
    
    for index,evidence in enumerate(evidences):
        evidence_data = {
            **evidence.__dict__,
            "PhotoPath " : evidence_photos[index].PhotoPath
        }
        evidence_list.append(evidence_data)
    
    return evidence_list


@router.get('/all/criminals')
def get_all_criminals(db: db_dependency):
    criminals = db.query(Person).filter(Person.PersonType == "Criminal/Suspect").all()

    criminals_photos = db.query(Photos).filter(Photos.PhotoType == "Criminal or Suspect").all()

    criminal_sus = db.query(CriminalOrSuspect).all()

    criminal_list = []

    for index,criminal in enumerate(criminals):
        criminal_data = {
            **criminal.__dict__,
            "InCustody" : criminal_sus[index].InCustody,
            "CrimeJustified" : criminal_sus[index].CrimeJustified,
            "PhotoPath" : criminals_photos[index].PhotoPath
        }
        criminal_list.append(criminal_data)

    return criminal_list


@router.get('/find/criminal/{id}')
def get_criminal_by_crimeID_criminalID(db: db_dependency, id: Annotated[str, Path(description="Enter Criminal ID / Crime ID ")]):
    criminals = db.query(Person).filter(or_(Person.PersonID == id, Person.CrimeID == id)).all()
    if not criminals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No criminal details")

    criminal_photos = db.query(Photos).filter(Photos.PhotoID.in_(
        [criminal.PersonID for criminal in criminals])).all()
    
    criminal_sus = db.query(CriminalOrSuspect).filter(CriminalOrSuspect.PersonID.in_([criminal.PersonID for criminal in criminals])).all()
    
    criminal_details = []
    
    for criminal, sus, photo in zip(criminals, criminal_sus, criminal_photos):
        criminal_data = {
            **criminal.__dict__,
            "InCustody" : sus.InCustody,
            "CrimeJustified" : sus.CrimeJustified,
            "PhotoPath" : photo.PhotoPath
        }
        criminal_details.append(criminal_data)
    
    return criminal_details