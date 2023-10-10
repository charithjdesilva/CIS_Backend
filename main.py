from fastapi import FastAPI,Depends
from fastapi.staticfiles import StaticFiles
import models
from database import engine, SessionLocal


from route.general import user_post,user_get
from route.police_officer import police_post,police_get
from route.it_officer import it_officer_post,it_officer_get
from route.criminal_reg_dept import criminal_reg_dept_get,criminal_reg_dept_post, uploadCriminalPhoto, recognizeSuspect, recognizeMultipleSuspects 
from route.criminal_reg_dept import criminal_reg_dept_patch



app = FastAPI()

app.include_router(user_post.router)
app.include_router(user_get.router)

app.include_router(police_post.router)
app.include_router(police_get.router)

app.include_router(it_officer_post.router)
app.include_router(it_officer_get.router)

app.include_router(criminal_reg_dept_get.router)
app.include_router(criminal_reg_dept_post.router)
app.include_router(criminal_reg_dept_patch.router)


app.include_router(uploadCriminalPhoto.router)
app.include_router(recognizeSuspect.router)
app.include_router(recognizeMultipleSuspects.router)


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


# env\Scripts\activate.bat


