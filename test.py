import cv2
import numpy as np
import time
import os
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')  # Update with the path to your service account key file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-camera-50c3d-default-rtdb.firebaseio.com/'  # Update with your Firebase Realtime Database URL
})

# Reference to the Firebase Realtime Database
ref = db.reference('face_images')

# Define the path to save images
save_path = r'C:\Kimmy\reac\Toturial\KKKKK\MY PJ CAM\New folder'

# Load cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

# Wait for the camera to initialize
time.sleep(2)

if not cap.isOpened():
    print("Error: Could not open webcam. Please check if the webcam is connected properly.")
    exit()

user_id = input("Enter user ID: ")
count = 0

# Create the directory if it does not exist
if not os.path.exists(save_path):
    os.makedirs(save_path)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    for (x, y, w, h) in faces:
        count += 1
        # Save the cropped face image
        filename = os.path.join(save_path, f'Pic_{user_id}_{count}.jpg')
        cv2.imwrite(filename, gray[y:y+h, x:x+w])
        
        # Upload metadata to Firebase Realtime Database
        ref.push({
            'user_id': user_id,
            'image_path': filename,
            'timestamp': datetime.now().isoformat()
        })
        
        # Draw a rectangle around the face in the original frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Detect eyes within the face region
        face_roi_gray = gray[y:y+h, x:x+w]
        face_roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
        
        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around the eyes
            cv2.rectangle(face_roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    
    # Display the frame with detected faces and eyes
    cv2.imshow('Face and Eye Detection', frame)
    
    # Stop the loop if 500 face images have been collected
    if count >= 500:
        print("Dataset collection complete.")
        break

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
