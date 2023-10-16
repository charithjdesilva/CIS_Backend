from typing import Annotated
from fastapi import APIRouter,HTTPException, Path,status,Form
from dummydata import user_login , user_question_table , user_query_table
from schemas import LoginOut , Question , Query, fourDigitCodeDisplay
import random
from database import db_dependency
from Email import send_email
from models import User
from dummydata import four_digit_code_storage



router = APIRouter(
    prefix="/users",
    tags=['general pages section']
)




@router.get('/get/four-digit-code/{email}')
def retrieve_four_digit_code(db: db_dependency,  email : Annotated[str, Path(description="Enter Valid Email ID : ")]):
    verify_email = db.query(User).filter(User.Email == email).first()
    if not verify_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Email")
    four_digit_code = str(random.randint(1000, 9999))
    store = {
        verify_email.Email : four_digit_code
    }
    four_digit_code_storage.append(store)
    print(four_digit_code_storage)
    msg = f"Your Four Digit Code : {four_digit_code}"
    subject = "Reset Forgotten Password"
    send_email(msg=msg,subject=subject)
    return status.HTTP_200_OK
    
    









# @router.get('/login-details', response_model=list[LoginOut])
# def get_all_user_login_details(apikey : str):
#     if apikey == api_key:
#         res = [{'username' : user['username'], 'hashed_password' : user['hash_password']} for user in user_login]
#         return res
#     else:
#         raise HTTPException(status_code=status.HTTP_200_OK,detail="No Authorization")
    
    
# @router.get('/login-details/{username}', response_model=LoginOut)
# def get_all_user_login_details(apikey : str, username : Annotated[str, Path()]):
#     if apikey == api_key:
#         for user in user_login:
#             if user['username']  == username:
#                 return {'username' : user['username'], 'hashed_password' : user['hash_password']}
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No username here")
#     else:
#         raise HTTPException(status_code=status.HTTP_200_OK,detail="No Authorization")
    
# # get all the user questions
# @router.get("/user/questions", response_model=list[Question])
# def get_all_questions(apikey : str):
#     if api_key == apikey:
#         return user_question_table
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Authorization")
    
# @router.get("/user/queries", response_model=list[Query])
# def get_all_queries(apikey : str):
#     if api_key == apikey:
#         return user_query_table
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Authorization")
        


