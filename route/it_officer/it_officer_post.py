from fastapi import APIRouter,Form
from typing import Annotated
from pydantic import BaseModel

router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)


@router.post('/search-user')
def search_user(search : Annotated[str, Form()]):
    return {'search' : search}

@router.post('/register-user')
def create_user():
    return "dummy user"

