import cv2
import pickle
import os
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://project-camera-50c3d-default-rtdb.firebaseio.com/', # เปลี่ยนเป็น URL ของ Firebase Realtime Database ของคุณ
    'storageBucket': 'project-camera-50c3d.appspot.com' # เปลี่ยนเป็นชื่อ Firebase Storage bucket ของคุณ
})

# importing student images
folderPath = 'images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket =storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    # print(path)
    # print(os.path.splitext(path)[0])
print(studentIds)

