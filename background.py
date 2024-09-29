import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

cred = credentials.Certificate("AccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://test-project-camera-default-rtdb.firebaseio.com/', # เปลี่ยนเป็น URL ของ Firebase Realtime Database ของคุณ
    'storageBucket': 'test-project-camera.appspot.com' # เปลี่ยนเป็นชื่อ Firebase Storage bucket ของคุณ
})

bucket = storage.bucket()


cap = cv2.VideoCapture(0)  
cap.set(3, 450) 
cap.set(4, 370)

imgBackground = cv2.imread(r'C:\Kimmy\reac\Toturial\KKKKK\MY PJ CAM\FL\attendance\background.png')
#Importing images into list
folderModePath = 'attendance/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

#print(len(imgModeList))

#Load encoding file
print("Load encoding file ...")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#print(studentIds)
print("Encoding file loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    img = cv2.resize(img, (450, 370))

    imgBackground[214:214 + 370, 75:75 + 450] = img
    imgBackground[44:44 + 566, 680:680 + 400] = imgModeList[modeType]


    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print("matches", matches)
            #print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            #print("match Index", matchIndex)

            if matches[matchIndex]:
                #print("Known face detected")
                #print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

                imgBackground = cvzone.cornerRect(imgBackground,bbox ,rt=0)
                id = studentIds[matchIndex]
                

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 3

        if counter != 0:

            if counter ==1:
                # Get the data
                StudentInfo = db.reference(f'Students/{id}').get()
                print(StudentInfo)
                #Get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)
                #Update data of attendance
                datetimeObject = datetime.strptime(StudentInfo['last_attendance'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    StudentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(StudentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 566, 680:680 + 400] = imgModeList[modeType]

            if modeType != 3:
                
                if 10<counter<20:
                    modeType = 2

            imgBackground[44:44 + 566, 680:680 + 400] = imgModeList[modeType]

            if counter <= 10:
                cv2.putText(imgBackground, str(StudentInfo['total_attendance']), (710, 90),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(StudentInfo['major']), (880, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(StudentInfo['id']), (880, 450),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (200, 100, 100), 1)
                cv2.putText(imgBackground, str(StudentInfo['name']), (676, 125),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(StudentInfo['last_attendance']), (900, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (200, 100, 100), 1)

            imgBackground[155:155 + 210, 750:750 + 255] = imgStudent

            counter+=1 

            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgBackground[44:44 + 566, 680:680 + 400] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    
    cv2.imshow("webcam", img)
    cv2.imshow("Face attendance", imgBackground)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()
