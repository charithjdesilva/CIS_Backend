from fastapi import APIRouter,Path,HTTPException,status
from enum import Enum
from typing import Annotated
from sqlalchemy import text, or_, and_


from models import Crime,Photos,CrimePhoto,Person,PersonPhoto,Evidence,EvidencePhoto,CriminalOrSuspect,CrimeCriminal
from database import db_dependency
from ..criminal_reg_dept.criminal_reg_dept_get import get_crime_by_crimeid, get_victim_by_crimeID_OR_VictimID, get_evidence_by_evidenceID_crimeID

router = APIRouter(
    prefix="/police-officer",
    tags=['Police Officer Section']
)

@router.get("/search/criminal/biodata/{id}")
def search_criminal(
    db:db_dependency,
    id : Annotated[str, Path(description="Enter NIC or Criminal ID")]):
    criminal_details = db.query(Person).filter(or_(Person.NIC == id , Person.PersonID == id)).first()

    evidence_details = []
    victim_details = []
    crime_details = []

    if criminal_details is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criminal Not Found")
    
    crimes_criminal = db.query(CrimeCriminal).filter(CrimeCriminal.PersonID == criminal_details.PersonID).all()

    # for crime in crimes_criminal:
    #     crime_data = get_crime_by_crimeid(db,crime_id=crime.CrimeID)
    #     if crime_data:
    #         crime_details.append(crime_data)
    #     victim_data = get_victim_by_crimeID_OR_VictimID(db,id=crime.CrimeID)
    #     if victim_data:
    #         victim_details.append(victim_data)
    #     evidence_data = get_evidence_by_evidenceID_crimeID(db,id=crime.CrimeID)
    #     if evidence_data:
    #         evidence_details.append(evidence_data)
    

    return {
        'criminal details' : criminal_details,
        'crimes details'   : crimes_criminal,
        # 'victim details'   : victim_details,
        # "evidence details" : evidence_details
    }


@router.get("/search-result")
def show_result():
    return {"message" : "It shows criminal detail and crimes involved"}

@router.get("/captures")
def show_multimedia():
    return {"message" : "It shows Photos and Videos of the searched criminal"}

class Category(str,Enum):
    Crime = "Crime section"
    Victims = "Victims section"
    Evidences = "Evidences section"

@router.get("/crime/{id}")
def show_crime(id : int, category : Category ):
    return{
        "logic" : f"it searches crime table based on the crime id {id} ",
        "data" : f"it returns  {category.name} -- {category.value} "
    }


@router.get('/find/criminal/biodata/{id}')
def get_criminal_by_crimeID_criminalID_NIC(db: db_dependency, id: Annotated[str, Path(description="Enter Criminal ID / Crime ID / NIC ")]):
    criminal = db.query(Person).filter(or_(Person.PersonID == id,Person.NIC == id)).first()
    if not criminal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No criminal details")

    # criminal_photos = db.query(Photos).filter(Photos.PhotoID.in_(
    #     [criminal.PersonID for criminal in criminals])).all()

    criminal_photo = db.query(Photos).filter(Photos.PhotoID == criminal.PersonID).first()
    
    # criminal_sus = db.query(CriminalOrSuspect).filter(CriminalOrSuspect.PersonID.in_([criminal.PersonID for criminal in criminals])).all()

    criminal_sus = db.query(CriminalOrSuspect).filter(CriminalOrSuspect.PersonID == criminal.PersonID).first()

    crimes_criminal = db.query(CrimeCriminal).filter(CrimeCriminal.PersonID == criminal.PersonID).all()

    
    
    # for criminal, sus, photo in zip(criminals, criminal_sus, criminal_photos):
    #     criminal_data = {
    #         **criminal.__dict__,
    #         "InCustody" : sus.InCustody,
    #         "CrimeJustified" : sus.CrimeJustified,
    #         "PhotoPath" : photo.PhotoPath
    #     }
    #     criminal_details.append(criminal_data)

    criminal_data = {
        **criminal.__dict__,
        "InCustody" : criminal_sus.InCustody,
        "CrimeJustified" : criminal_sus.CrimeJustified,
        "PhotoPath" : criminal_photo.PhotoPath
    }
    
    return criminal_data