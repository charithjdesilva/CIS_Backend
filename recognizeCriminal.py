from PIL import Image
# from io import BytesIO
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

def recognizeFace(image):
    img = Image.open(image)
    # we are reducing the image size because it will help us by speeding the process
    imgSmall = cv2.resize(img, (0,0), None, 0.25, 0.25)     # small image will be 1/4 th of the size
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)    # convert to RGB

    # in an image we may find multiple faces, so we are first find the location of the faces
    faceLocation = face_recognition.face_locations(imgSmall)  # capture all the face location in the current frame

    # then we send these location to the encoding function
    encodedFace =  face_recognition.face_encodings(imgSmall, faceLocation)

    # find matches
    # iterate through all the faces that we have found in the image
    for encodeFace, faceLocation in zip(encodedFace, faceLocation):
        matches = face_recognition.compare_faces(encodeListForKnownFaces, encodeFace)   # compare with all the encoding that we found before
        faceDistance = face_recognition.face_distance(encodeListForKnownFaces, encodeFace)    # find the distance, this will give us distance according to the all the knownFaces
        print(faceDistance)

        # get the best match which is the lowest distance in faceDistance List
        matchIndex = np.argmin(faceDistance)    # will have the index of the best matched face

        if matches[matchIndex]:
            name = imageNames[matchIndex]
            print(name)

            # display a bounding box around that person and display their name
            y1, x2, y2, x1 = faceLocation    # we have the location of the face in the imageSmall, we destruct the list
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4    # location of the face in the original image
            cv2.rectangle(img, (x1, y1), (x2, y2), (255,255,0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (255,255,0), 2)  # rectangle to display name
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)