from fastapi import APIRouter, Depends, HTTPException, Form, Path, status
from pydantic import BaseModel,EmailStr
from typing import Optional

from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

from Security.password import do_hash_password,verify_password
import random
from Security.user_defined_datatypes import SriLankaMobileNumber
from database import db_dependency
from models import User
from Email import send_email




router = APIRouter(
    prefix="/general",
    tags=['general pages section']
)

# SECRET_KEY = os.environ.get('SECRET_KEY')
# ALGORITHM = os.environ.get('ALGORITHM')
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="general/token")

# def get_user(db : db_dependency, username: str):
#     user = db.query(User).filter(User.RegNo == username).first()
#     if user:
#         return {
#             "username" : user.RegNo,
#             "email" : user.Email,
#             "full_name" : f"{user.FirstName} {user.LastName}",
#             "hashed_password" : user.PasswordHash
#         }

   
# def authenticate_user(db: db_dependency, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user["hashed_password"]):
#         return False
#     return user 

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt



# async def get_current_user(db: db_dependency,token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=username)
#     if user is None:
#         raise credentials_exception
#     return user

# @router.get("/protected_endpoint")
# async def protected_endpoint(current_user: dict = Depends(get_current_user)):
#     return {"message": "This is a protected endpoint", "user": current_user}



# @router.post("/token")
# async def login_for_access_token(
#     db:db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user['username']}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}






@router.post('/signIn')
def do_signin(db: db_dependency,formdata : OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.RegNo == formdata.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid crendentials")
    
    if user:
        if verify_password(formdata.password, user.PasswordHash):
            return status.HTTP_202_ACCEPTED
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid crendentials")
        

@router.post('/forget-password')
def do_forget_password(db: db_dependency, email : Annotated[str, Form()]):
    verify_email = db.query(User).filter(User.Email == email).first()
    if not verify_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Email")
    code = 4444
    msg = f"Code : {code} "
    subject = "Reset Forgotten Password"
    send_email(msg=msg,subject=subject)
    return status.HTTP_200_OK


@router.post('/reset-password/{id}')
def do_reset_pswd(id : Annotated[str, Path(description="Enter email ID")],
                  db:db_dependency, 
                  new_passowrd : Annotated[str, Form(min_length=8,max_length=256)], 
                  confirm_password : Annotated[str, Form(min_length=8,max_length=256)]):
    user = db.query(User).filter(User.Email == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User")
    
    if new_passowrd != confirm_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Match password")
    
    if verify_password(new_passowrd, user.PasswordHash):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot use previous password")

    
    if new_passowrd == confirm_password:
        user.PasswordHash = do_hash_password(new_passowrd)
        db.commit()
        db.refresh(user)
        return {"message" : "password reset successfully"} #123456789
    


















# class User(BaseModel):
#     username : Form(str)
#     password : Form(str)

# user_dict = [{'username': 'user1', 'password' : '1234'}]

# four_digit_code_by_user = 4444




# # Sample hardcoded users (In practice, use a database)
# hardcoded_users = [
#     {"username": "user1", "password": "password1"},
#     {"username": "user2", "password": "password2"},
# ]

# def authenticate_user(username: str, password: str) -> Optional[LoginCredentials]:
#     for user_data in user_login:
#         if user_data["username"] == username and verify_password(password,user_data["hash_password"] ):
#             return LoginCredentials(**user_data)
#     return None



# @router.post("/login")
# def do_login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if user:
#         return {"message": "Login successful"}
#     else:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
    

        

# class Options(Enum):
#     Email = 'Email'
#     Mobile_Number = 'MobileNumber'

# class OptionsValue(BaseModel):
#     value :  EmailStr | str






# # @router.post("/forget-password/{type}")
# # def check_validation(type : Annotated[Options , Path()], value : Annotated[ str , Form()] ):
# #     if type.value.capitalize() == Options.Email:
# #         if is_valid_email(value):
            

# #     if type.value.capitalize() == Options.Mobile_Number:
        






#     # if request.type == 'email':
#     #     if is_valid_email(request.value):
#     #         return {"message" : f"4 digit code is send to the {request.value} "}
#     #     else:
#     #         raise HTTPException(status_code=401, detail='It is invalid email')
#     # elif request.type == 'tel':
#     #     if is_valid_sri_lankan_mobile_number(request.value):
#     #         return {"message" : f"4 digit code is send to the {request.value} "}
#     #     else:
#     #         raise HTTPException(status_code=401, detail="Invalid mobile number")


# @router.post("/4-digit-code/")
# def validate_code(code : Send4DigitCode):
#     if len(str(code.value)) == 4 : 
#         four_digit_code_by_user = code.value
#         return status.HTTP_200_OK
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid 4 digit code")

    

# @router.post("/reset-password/{username}")
# def validate_reset_pswd(username : Annotated[str , Path()], new_pswd : Annotated[str,Form(min_length=8)], confirm_pswd : Annotated[str, Form(min_length=8)]):
#     for user in user_login:
#         if user['username'] == username:
#             if new_pswd == confirm_pswd:
#                 if is_valid_password(new_pswd,confirm_pswd):
#                     user['password'] = new_pswd
#                     user['hash_password'] = do_hash_password(new_pswd)
#                     return status.HTTP_200_OK
#                 else:
#                     raise HTTPException(status_code=404, detail="It should include at least one uppercase , one lowercase , one number and one special character")
#             else:
#                 raise HTTPException(status_code=404, detail="No match between passwords")
#     raise HTTPException(status_code=404, detail=f"{username} is not found")


# @router.post("/faq/questions")
# def post_questions(user_question : Question):
#     if user_question:
#         user_question_table.append(user_question)
#         return status.HTTP_200_OK
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid question")

# @router.post("/contact_us/queries")
# def post_questions(user_query : Query):
#     if user_query:
#         user_query_table.append(user_query)
#         return status.HTTP_200_OK
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid question")









