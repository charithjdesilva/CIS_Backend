from fastapi import UploadFile
import os
import pathlib

from Images.path import UPLOAD_USER
from models import User, Crime , Person , Photos ,Evidence
from .path import common_image
from database import Base

base_url = "http://127.0.0.1:8000"





def make_image_url(file_path : str):
    file_path = file_path.replace("\\", "/").lstrip("/")
    url = f"{base_url}/{file_path}"
    return url



async def upload_image(Photo : UploadFile, Id : str, filePath : pathlib.Path):
    data = await Photo.read()
    name , extension = os.path.splitext(Photo.filename)
    save_to = filePath / f"{Id}{extension}"
    with open(save_to , 'wb') as f:
        f.write(data)
    # print(save_to)
    return make_image_url(str(save_to))

async def update_user_image(Photo : UploadFile, filePath : pathlib.Path, user: User):
    data = await Photo.read()
    name, extension = os.path.splitext(Photo.filename)
    new_photo_filename = f"{user.NIC}{extension}"
    new_photo_path = filePath / new_photo_filename

    # Check if the existing photo in the database contains the RegNo
    if user.Photo and user.NIC in user.Photo:
        # If it contains, construct the old photo path and delete it
        old_photo_filename = user.Photo.split('/')[-1]
        # print("old photo name :", old_photo_filename, user.Photo.split('\\'))
        old_photo_path = filePath / old_photo_filename
        if old_photo_path.exists():
            old_photo_path.unlink()
    
    with open(new_photo_path, 'wb') as f:
        f.write(data)
    return str(new_photo_path)

async def update_crime_image(Photo : UploadFile, filePath : pathlib.Path, crime: Crime, photo_obj :Photos):
    data = await Photo.read()
    name, extension = os.path.splitext(Photo.filename)
    new_photo_filename = f"{crime.CrimeID}{extension}"
    new_photo_path = filePath / new_photo_filename

    if photo_obj.PhotoPath and crime.CrimeID in photo_obj.PhotoPath:
        # If it contains, construct the old photo path and delete it
        old_photo_filename = photo_obj.PhotoPath.split('/')[-1]
        old_photo_path = filePath / old_photo_filename
        if old_photo_path.exists():
            old_photo_path.unlink()
    
    with open(new_photo_path, 'wb') as f:
        f.write(data)
    return make_image_url(str(new_photo_path))



async def update_victim_image(Photo : UploadFile, filePath : pathlib.Path, victim: Person, photo_obj :Photos):
    data = await Photo.read()
    name, extension = os.path.splitext(Photo.filename)
    new_photo_filename = f"{victim.PersonID}{extension}"
    new_photo_path = filePath / new_photo_filename

    if photo_obj.PhotoPath and victim.PersonID in photo_obj.PhotoPath:
        old_photo_filename = photo_obj.PhotoPath.split('/')[-1]
        old_photo_path = filePath / old_photo_filename
        if old_photo_path.exists():
            old_photo_path.unlink()
    
    with open(new_photo_path, 'wb') as f:
        f.write(data)
    return make_image_url(str(new_photo_path))   

async def update_evidence_image(Photo : UploadFile, filePath : pathlib.Path, evidence: Evidence, photo_obj :Photos):
    data = await Photo.read()
    name, extension = os.path.splitext(Photo.filename)
    new_photo_filename = f"{evidence.EvidenceID}{extension}"
    new_photo_path = filePath / new_photo_filename

    if photo_obj.PhotoPath and evidence.EvidenceID in photo_obj.PhotoPath:
        old_photo_filename = photo_obj.PhotoPath.split('/')[-1]
        old_photo_path = filePath / old_photo_filename
        if old_photo_path.exists():
            old_photo_path.unlink()
    
    with open(new_photo_path, 'wb') as f:
        f.write(data)
    return make_image_url(str(new_photo_path))    
