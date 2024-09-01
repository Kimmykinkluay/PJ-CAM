import cv2
import numpy as np
import time
import os
from datetime import datetime

# กำหนดเส้นทางไปยังโฟลเดอร์ที่เก็บภาพ
save_path = r'C:\Kimmy\reac\Toturial\KKKKK\MY PJ CAM\New folder'

# โหลด cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# เปิดกล้องเว็บแคม
cap = cv2.VideoCapture(0)

# รอให้กล้องเริ่มต้น
time.sleep(2)

if not cap.isOpened():
    print("Error: Could not open webcam. Please check if the webcam is connected properly.")
    exit()

user_id = input("Enter user ID: ")
count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # ตรวจจับใบหน้าในภาพขาวดำ
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    for (x, y, w, h) in faces:
        count += 1
        # บันทึกภาพใบหน้า
        filename = os.path.join(save_path, f'Pic_{user_id}_{count}.jpg')
        cv2.imwrite(filename, gray[y:y+h, x:x+w])
        
        # วาดกรอบรอบใบหน้าในภาพต้นฉบับ
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # ตรวจจับตาในพื้นที่ใบหน้า
        face_roi_gray = gray[y:y+h, x:x+w]
        face_roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
        
        for (ex, ey, ew, eh) in eyes:
            # วาดกรอบรอบตา
            cv2.rectangle(face_roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    
    # แสดงภาพที่ตรวจจับใบหน้าและตา
    cv2.imshow('Face and Eye Detection', frame)
    
    # หยุดการทำงานเมื่อรวบรวมภาพครบ 500 ภาพ
    if count >= 500:
        print("Dataset collection complete.")
        break

    # กด 'q' เพื่อออกจากลูป
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดกล้องและปิดหน้าต่างทั้งหมด
cap.release()
cv2.destroyAllWindows()
