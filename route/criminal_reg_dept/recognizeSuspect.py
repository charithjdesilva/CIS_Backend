from fastapi import FastAPI, APIRouter, File, UploadFile
import os
from fastapi.responses import JSONResponse
from recognizeCriminal import recognizeFace  # Import the function
import cv2
import numpy as np
import face_recognition
from recognizeCriminal import loadEncodeList, loadImageEncodings

app = FastAPI()

router = APIRouter(
    prefix="/criminal-reg-dept",
    tags=['criminal registration department section']
)

# List of supported image file extensions
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Function to check if a file has a valid image extension
def is_valid_image(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower() in SUPPORTED_EXTENSIONS

@router.post("/recognizeSuspect")
async def recognizeFace(image: UploadFile = File(...)):
    encodeListForKnownFaces = loadEncodeList('encodeList.pkl')
    image_encodings = loadImageEncodings('image_encodings.pkl')  # Load the image encodings dictionary

    try:
        # Read the content of the UploadFile and decode it as a NumPy array
        image_content = await image.read()
        img_array = np.frombuffer(image_content, np.uint8)
        
        # Decode the NumPy array into an image using OpenCV
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as e:
        print("Error while decoding the image:", e)
        return -1

    imgSmall = cv2.resize(img, (124, 124))
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceLocation = face_recognition.face_locations(imgSmall)
    encodedFace = face_recognition.face_encodings(imgSmall, faceLocation)

    for encodeFace, faceLocation in zip(encodedFace, faceLocation):
        matches = face_recognition.compare_faces(encodeListForKnownFaces, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListForKnownFaces, encodeFace)
        print("Face distances:", faceDistance)

        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            # Use the encoding to find the associated name from the dictionary
            # encoding_name = next((name for name, encoding in image_encodings.items() if np.array_equal(encoding, encodeFace)), None)
            encoding_name = None
            for name, encoding in image_encodings.items():
                if face_recognition.compare_faces([encoding], encodeFace, tolerance=0.6)[0]:
                    encoding_name = name
                    break

            if encoding_name:
                print("Match found with image:", encoding_name)
                return encoding_name  # Return the image name (key) as the result if a match is found
            else:
                print("Match found, but image name not found.")
                return -2

    print("No match found in the encoded list.")
    return -1
