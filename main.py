import os
import pathlib
from fastapi import FastAPI,Depends, UploadFile ,APIRouter
from fastapi.staticfiles import StaticFiles
import models
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware



from route.general import user_post,user_get
from route.police_officer import police_post,police_get
from route.it_officer import it_officer_post,it_officer_get
from route.criminal_reg_dept import criminal_reg_dept_get,criminal_reg_dept_post, uploadCriminalPhoto, recognizeSuspect, recognizeMultipleSuspects, criminal_reg_dept_delete 
from route.criminal_reg_dept import criminal_reg_dept_patch
import auth
from Images.path import UPLOAD_CRIME_VIDEOS
from auth import get_current_user_CRD_admin



app = FastAPI(title="AI Based Criminal Identification System to Sri Lankan Police API",
    description="CIS uses fastAPI as a Web back-end development framework based on REST API",
    summary="Manage data related to Crime and staffs through API",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Department Of Criminal Investigation",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    # dependencies=[Depends(get_current_user_CRD_admin)],
    )

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ['*']
)


app.include_router(user_post.router)
app.include_router(user_get.router)

app.include_router(police_post.router)
app.include_router(police_get.router)

app.include_router(it_officer_post.router)
app.include_router(it_officer_get.router)

app.include_router(criminal_reg_dept_get.router)
app.include_router(criminal_reg_dept_post.router)
app.include_router(criminal_reg_dept_patch.router)
app.include_router(criminal_reg_dept_delete.router)

app.include_router(auth.router)

app.include_router(uploadCriminalPhoto.router)
app.include_router(recognizeSuspect.router)
app.include_router(recognizeMultipleSuspects.router)

# app.include_router(testwebcam.router)


models.Base.metadata.create_all(bind=engine)

# app.mount('/Images/crime_images', StaticFiles(
#     directory="/Images/crime_images"
# ) , name="crime_images")

app.mount("/Images/crime_images", StaticFiles(directory="Images/crime_images"), name="crime_images")
app.mount("/Images/victim_images", StaticFiles(directory="Images/victim_images"), name="victim_images")
app.mount("/Images/users_image", StaticFiles(directory="Images/users_image"), name="users_image")
app.mount("/Images/criminal_images", StaticFiles(directory="Images/criminal_images"), name="criminal_images")
app.mount("/Images/evidence_images", StaticFiles(directory="Images/evidence_images"), name="evidence_images")




@app.get("/hello")
def show():
    return {"message" : "hello world"}

# @app.post("/post-video")
# async def upload_video(video: UploadFile):
#     data = await video.read()
#     name, extension = os.path.splitext(video.filename)
#     save_to = UPLOAD_CRIME_VIDEOS / f"{video.filename}{extension}"
    
#     with open(save_to, 'wb') as f:
#         f.write(data)
    
#     return "okay"



# env\Scripts\activate.bat


