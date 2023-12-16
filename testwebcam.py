# from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
# import cv2
# import os

# router = APIRouter(
#     prefix="/webcam",
#     tags=['Web cam section'],
#     # dependencies=[Depends(get_current_active_user)]
# )



# # Create a directory to store captured images if it doesn't exist
# os.makedirs("captured_photos", exist_ok=True)

# # Webcam video capture object
# cap = cv2.VideoCapture(0)  # 0 corresponds to the default webcam, change it if needed

# # Check if the webcam is opened
# if not cap.isOpened():
#     raise HTTPException(status_code=500, detail="Could not open the webcam.")

# @router.post("/capture-photo/")
# async def capture_photo():
#     # Capture a frame from the webcam
#     ret, frame = cap.read()

#     if ret:
#         # Save the captured photo
#         cv2.imwrite("captured_photos/captured_photo.jpg", frame)
#         return {"message": "Photo captured from webcam."}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to capture photo from webcam.")

# # Release the webcam when the FastAPI application stops
# @router.on_event("shutdown")
# async def shutdown_event():
#     cap.release()


# from fastapi import FastAPI, File, UploadFile, HTTPException,APIRouter
# import cv2
# import os

# router = APIRouter(
#     prefix="/webcam",
#     tags=['Web cam section'],
#     # dependencies=[Depends(get_current_active_user)]
# )

# # Create a directory to store captured images if it doesn't exist
# os.makedirs("captured_photos", exist_ok=True)

# # Initialize the flag to control photo capturing
# should_capture = True

# # Webcam video capture object
# cap = cv2.VideoCapture(0)  # 0 corresponds to the default webcam, change it if needed

# # Check if the webcam is opened
# if not cap.isOpened():
#     raise HTTPException(status_code=500, detail="Could not open the webcam.")

# def capture_photo():
#     global should_capture
#     while should_capture:
#         # Capture a frame from the webcam
#         ret, frame = cap.read()

#         if ret:
#             # Save the captured photo
#             cv2.imwrite("captured_photos/captured_photo.jpg", frame)
#             should_capture = False
#         else:
#             raise HTTPException(status_code=500, detail="Failed to capture photo from webcam.")

# @router.post("/start-capture/")
# async def start_capture():
#     global should_capture
#     should_capture = True
#     capture_photo()  # Start capturing photos
#     return {"message": "Photo capturing started."}

# @router.post("/stop-capture/")
# async def stop_capture():
#     global should_capture
#     should_capture = False
#     return {"message": "Photo capturing stopped."}

# # Release the webcam when the FastAPI application stops
# @router.on_event("shutdown")
# async def shutdown_event():
#     cap.release()

