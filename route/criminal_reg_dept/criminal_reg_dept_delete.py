from fastapi import APIRouter, HTTPException, Form, Query, status, UploadFile, Path, File
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Annotated, List
import os
from datetime import datetime


from dummydata import victims, crimes, evidences, criminals
from Security.password import is_valid_password
from Images.path import UPLOAD_CRIME, UPLOAD_VICTIM, UPLOAD_EVIDENCE, UPLOAD_CRIMINAL
from Images.path import common_image
from Images.image_upload import update_crime_image, update_victim_image, update_evidence_image
from models import Crime, Photos, CrimePhoto, Person, PersonPhoto, Evidence, EvidencePhoto, CriminalOrSuspect, CrimeCriminal
from database import db_dependency
from Images.image_upload import upload_image, upload_image_with_multiple_photos


router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal Registration Department Section - DELETE ']
)

@router.delete('/update/crime/delete_photo/{id}')
async def delete_one_photo_crime(
    db: db_dependency,
    id : Annotated[str, Path(description="Enter Crime ID : ")],
    file_name : Annotated[list[str], Query(description="Enter image file name with its extension : ")]
):
    crime = db.query(Crime).filter(Crime.CrimeID == id).first()

    if crime:
        # Fetch photos related to the crime
        photo_gallery_crime = db.query(Photos).filter(Photos.PhotoType == "Crime").filter(Photos.PhotoPath.like(f"%{file_name}%")).first()

        if not photo_gallery_crime:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="file name not found")

        if file_name != str(photo_gallery_crime.PhotoPath).split("/")[-1]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="file name not found")


        # print(photo_gallery_crime.PhotoPath)

        

        # Fetch crime photos related to the crime
        crime_photo = db.query(CrimePhoto).filter(CrimePhoto.PhotoID.like(f"%{file_name.split('.')[0]}%")).first()

        if not crime_photo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="file name not found")

        # Delete crime photos first
        db.delete(crime_photo)

        # Commit deletion of crime photos
        db.commit()

        # Delete the photos
        old_photo_filename = photo_gallery_crime.PhotoPath.split('/')[-1]
        old_photo_path = UPLOAD_CRIME / old_photo_filename
        if old_photo_path.exists():
            old_photo_path.unlink()

        db.delete(photo_gallery_crime)

        # Commit deletion of photos
        db.commit()

        return status.HTTP_200_OK
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crime Id is not found")
    





#-------------------------------------------------------------------------------------

@router.delete('/update/crime/delete_all_photos/{id}')
async def update_crime_with_delete_all_photos(
    db: db_dependency,
    id : Annotated[str, Path(description="Enter Crime ID : ")]
):
    crime = db.query(Crime).filter(Crime.CrimeID == id).first()

    if crime:
        # Fetch photos related to the crime
        photo_gallery = db.query(Photos).filter(Photos.PhotoType == "Crime").filter(Photos.PhotoID.like(f'%{id}%')).all()

        # Fetch crime photos related to the crime
        crime_photos = db.query(CrimePhoto).filter(CrimePhoto.CrimeID.like(f'%{id}%')).all()

        # Delete crime photos first
        for photo in crime_photos:
            db.delete(photo)

        # Commit deletion of crime photos
        db.commit()

        # Delete the photos
        for photo in photo_gallery:
            old_photo_filename = photo.PhotoPath.split('/')[-1]
            old_photo_path = UPLOAD_CRIME / old_photo_filename
            if old_photo_path.exists():
                old_photo_path.unlink()

            db.delete(photo)

        # Commit deletion of photos
        db.commit()

        return status.HTTP_200_OK
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crime Id is not found")
    


#delete all victim photos    
@router.delete('/update/victim/delete_all_photos/{id}')
async def update_victim_with_delete_all_photos(
    db: db_dependency,
    id : Annotated[str, Path(description="Enter Victim ID : ")]
):
    victim = db.query(Person).filter(Person.PersonID == id).first()

    if victim:
        # Fetch photos related to the victim
        photo_gallery = db.query(Photos).filter(Photos.PhotoType == "Victim").filter(Photos.PhotoID.like(f'%{id}%')).all()

        # Fetch victim photos related to the victim
        victim_photos = db.query(PersonPhoto).filter(PersonPhoto.PersonID.like(f'%{id}%')).all()

        # Delete victim photos first
        for photo in victim_photos:
            db.delete(photo)

        # Commit deletion of crime photos
        db.commit()

        # Delete the photos
        for photo in photo_gallery:
            old_photo_filename = photo.PhotoPath.split('/')[-1]
            old_photo_path = UPLOAD_VICTIM / old_photo_filename
            if old_photo_path.exists():
                old_photo_path.unlink()

            db.delete(photo)

        # Commit deletion of photos
        db.commit()

        return status.HTTP_200_OK
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Victim Id is not found")