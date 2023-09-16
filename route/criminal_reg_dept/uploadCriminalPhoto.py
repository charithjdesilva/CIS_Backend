from fastapi import FastAPI, APIRouter, File, UploadFile, Form
import os
import cv2
from recognizeCriminal import encodeImages, findEncodings

router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

@router.post("/criminalPhotoUpload")
async def upload_criminalPhoto(suspect_name: str = Form(...), file: UploadFile = File(...)):
    # Define the upload directory (e.g., "Suspects")
    upload_dir = "Suspects"
    os.makedirs(upload_dir, exist_ok=True)

    # Ensure the provided suspect_name is not empty
    if not suspect_name:
        return {"error": "Person name cannot be empty."}

    # Get the file extension from the uploaded file
    file_extension = os.path.splitext(file.filename)[1].lower()

    # Check if the file extension is supported
    if file_extension not in SUPPORTED_EXTENSIONS:
        return {"error": f"Unsupported file type. Supported extensions: {', '.join(SUPPORTED_EXTENSIONS)}"}

    # Construct the file path with the user-specified persona name as the filename
    file_path = os.path.join(upload_dir, f"{suspect_name}{file_extension}")

    # Save the uploaded file to the "Suspects" directory
    with open(file_path, "wb") as image:
        image.write(file.file.read())

    # Call the encodeImages function with the path of the new image to update the encodings
    new_image_path = file_path
    encodeList = encodeImages(new_image_path)

    return {"filename": f"{suspect_name}{file_extension}"}