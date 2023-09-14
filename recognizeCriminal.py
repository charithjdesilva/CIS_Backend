from PIL import Image
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pickle

# Initialize a dictionary to store image filenames and their corresponding encodings
image_encodings = {}
# Initialize a set to keep track of processed image names
processed_image_names = set()
# Initialize a list to store image filenames
imageNames = []

# Function to add a new image to the imageNames list
def addImageName(imgName):
    # Append the new image name to imageNames
    imageNames.append(os.path.splitext(imgName)[0])

# Initial image encoding function
def encodeImages(new_image_path):
    # Load existing image encodings
    image_encodings = loadImageEncodings('image_encodings.pkl')

    # Load the new image using the provided path
    currentImg = cv2.imread(new_image_path)

    # Find the encoding of the new image
    imgName = os.path.splitext(os.path.basename(new_image_path))[0]
    img = cv2.cvtColor(currentImg, cv2.COLOR_BGR2RGB)
    encodeOfImg = face_recognition.face_encodings(img)[0]

    # Check if the image already exists in the dictionary
    if imgName in image_encodings:
        print(f"Image {imgName} already exists in the dictionary. Skipping.")
    else:
        # Add the new encoding to the dictionary
        image_encodings[imgName] = encodeOfImg

        # Save the updated image encodings to a file
        saveImageEncodings(image_encodings, 'image_encodings.pkl')

        # Save the new encoding to the encodeList
        saveEncodeList([encodeOfImg], 'encodeList.pkl')

def findEncodings(images, imageNames):
    encodeList = []

    for img, imgName in zip(images, imageNames):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeOfImg = face_recognition.face_encodings(img)[0]
        encodeList.append(encodeOfImg)

        # Store the encoding along with the image filename in the dictionary
        image_encodings[imgName] = encodeOfImg

    # Save the updated image encodings dictionary
    saveImageEncodings(image_encodings, 'image_encodings.pkl')

    # Save the updated encodeList
    saveEncodeList(encodeList, 'encodeList.pkl')


# Function to save the encodeList to a file (append mode)
def saveEncodeList(encodeList, file_name):
    # Load existing encodings from the file, if any
    existing_encodings = []
    try:
        with open(file_name, 'rb') as file:
            existing_encodings = pickle.load(file)
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist yet

    # Append the new encodings to the existing ones
    existing_encodings.extend(encodeList)

    # Save the updated encodings to the file
    with open(file_name, 'wb') as file:
        pickle.dump(existing_encodings, file)

# Function to save the image_encodings dictionary to a file
def saveImageEncodings(encodings, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(encodings, file)

# Loading the encodeList from a file
def loadEncodeList(file_name):
    with open(file_name, 'rb') as file:
        encodeList = pickle.load(file)
    return encodeList

# Function to load existing image encodings from a file
def loadImageEncodings(file_name):
    try:
        with open(file_name, 'rb') as file:
            encodings = pickle.load(file)
        return encodings
    except FileNotFoundError:
        return {}

async def recognizeFace(image):
    encodeListForKnownFaces = loadEncodeList('encodeList.pkl')

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
            encoding_name = next((name for name, encoding in image_encodings.items() if np.array_equal(encoding, encodeFace)), None)

            if encoding_name:
                print("Match found with image:", encoding_name)
                return encoding_name
            else:
                print("Match found, but image name not found.")
                return -2

    print("No match found in the encoded list.")
    return -1
