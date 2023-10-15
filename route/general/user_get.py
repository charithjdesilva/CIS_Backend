from typing import Annotated
from fastapi import APIRouter,HTTPException, Path,status
from dummydata import user_login , user_question_table , user_query_table
from schemas import LoginOut , Question , Query

router = APIRouter(
    prefix="/users",
    tags=['general pages section']
)

api_key = "08956DV"






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
        


