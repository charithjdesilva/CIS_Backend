from fastapi import APIRouter,Path,HTTPException,status
from enum import Enum
from typing import Annotated
from sqlalchemy import text, or_, and_


from models import Crime,Photos,CrimePhoto,Person,PersonPhoto,Evidence,EvidencePhoto,CriminalOrSuspect,CrimeCriminal
from database import db_dependency

router = APIRouter(
    prefix="/police-officer",
    tags=['Police Officer Section']
)

@router.get("/search/criminal/biodata/{id}")
def search_criminal(
    db:db_dependency,
    id : Annotated[str, Path(description="Enter NIC or Criminal ID")]):
    criminal_details = db.query(Person).filter(or_(Person.NIC == id , Person.PersonID == id)).first()

    if criminal_details is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criminal Not Found")
    
    crimes_criminal = db.query(CrimeCriminal).filter().all()

    return "give criminal details based on the id"


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