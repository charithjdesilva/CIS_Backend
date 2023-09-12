from fastapi import APIRouter

router = APIRouter(
    prefix="/it-officer",
    tags=['IT Officer Section']
)

@router.get('/homepage')
def homepage():
    return "render homepage of it officer"

