from fastapi import APIRouter
from enum import Enum


router = APIRouter(
    prefix="/police-officer",
    tags=['Police Officer Section']
)


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