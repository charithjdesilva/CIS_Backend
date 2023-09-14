from fastapi import FastAPI, APIRouter, File, UploadFile, Form
import os

router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

@router.post("/criminalPhotoUpload/")
async def upload_criminalPhoto(suspect_name: str = Form(...), file: UploadFile = File(...)):
    # Define the upload directory (e.g., "Suspects")
    upload_dir = "Suspects"
    os.makedirs(upload_dir, exist_ok=True)

    # Ensure the provided suspect_name is not empty
    if not suspect_name:
        return {"error": "Persona name cannot be empty."}

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

    return {"filename": f"{suspect_name}{file_extension}"}