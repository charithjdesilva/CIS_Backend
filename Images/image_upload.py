from fastapi import UploadFile
import os

from Images.path import UPLOAD_USER
from Images.path import common_users_image



async def upload_user_image(Photo : UploadFile, RegNo : str):
    if Photo != common_users_image :
        data = await Photo.read()
        name , extension = os.path.splitext(Photo.filename)
        save_to = UPLOAD_USER / f"{RegNo}{extension}"
        with open(save_to , 'wb') as f:
            f.write(data)
        print(save_to)
        return save_to
    return common_users_image