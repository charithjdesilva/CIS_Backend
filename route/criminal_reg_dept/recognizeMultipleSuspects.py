from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import os
import cv2
import numpy as np
import face_recognition
from recognizeCriminal import loadEncodeList, loadImageEncodings
import io

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

@router.post("/recognizeMultipleSuspects")
async def recognizeFace(image: UploadFile = File(...)):
    encodeListForKnownFaces = loadEncodeList('encodeList.pkl')
    image_encodings = loadImageEncodings('image_encodings.pkl')  # Load the image encodings dictionary

    try:
        # Read the content of the UploadFile and decode it as a NumPy array
        image_content = await image.read()
        img_array = np.frombuffer(image_content, np.uint8)
        
        # Decode the NumPy array into an image using OpenCV
        original_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as e:
        print("Error while decoding the image:", e)
        return -1

    # Resize the image while maintaining the aspect ratio
    target_width = 248
    aspect_ratio = original_img.shape[1] / original_img.shape[0]
    target_height = int(target_width / aspect_ratio)
    imgSmall = cv2.resize(original_img, (target_width, target_height))
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceLocations = face_recognition.face_locations(imgSmall)
    encodedFaces = face_recognition.face_encodings(imgSmall, faceLocations)

    for encodeFace, faceLocation in zip(encodedFaces, faceLocations):
        matches = face_recognition.compare_faces(encodeListForKnownFaces, encodeFace)
        faceDistances = face_recognition.face_distance(encodeListForKnownFaces, encodeFace)
        print("Face distances:", faceDistances)

        matchIndex = np.argmin(faceDistances)
        
        top, right, bottom, left = faceLocation
        scale_factor_height = original_img.shape[0] / target_height  # Calculate the height scale factor
        scale_factor_width = original_img.shape[1] / target_width  # Calculate the width scale factor
        top *= scale_factor_height
        right *= scale_factor_width
        bottom *= scale_factor_height
        left *= scale_factor_width
        
        if matches[matchIndex]:
            encoding_name = None
            for name, encoding in image_encodings.items():
                if face_recognition.compare_faces([encoding], encodeFace, tolerance=0.6)[0]:
                    encoding_name = name
                    break

            if encoding_name:
                print("Match found with image:", encoding_name)
                cv2.rectangle(original_img, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 2)
                cv2.putText(original_img, encoding_name, (int(left) + 6, int(top) - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        else:
            # If the face is not recognized, draw a red bounding box around it
            cv2.rectangle(original_img, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), 2)
    
    # Convert the modified image to bytes
    _, img_encoded = cv2.imencode('.jpg', original_img)
    img_bytes = img_encoded.tobytes()
    
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/jpeg")