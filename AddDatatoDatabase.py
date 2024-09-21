import firebase_admin
from firebase_admin import credentials, db, storage
import os

# ตรวจสอบว่าพาธของไฟล์คีย์ถูกต้อง
cert = 'serviceAccountKey.json'





# ตรวจสอบว่ามีไฟล์อยู่ในตำแหน่งที่ระบุ
if not os.path.exists(cert):
    raise FileNotFoundError(f"Service account key file not found: {cert}")

# ตรวจสอบสิทธิ์การเข้าถึงไฟล์
try:
    with open(cert, 'r') as file:
        # ตรวจสอบว่าไฟล์เป็น JSON ที่ถูกต้อง
        import json
        try:
            json.load(file)
        except json.JSONDecodeError:
            raise ValueError("The service account key file is not a valid JSON.")

except PermissionError:
    raise PermissionError(f"Permission denied to access the file: {cert}")

# เริ่มต้น Firebase Admin SDK
try:
    cred = credentials.Certificate(cert)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://project-camera-50c3d-default-rtdb.firebaseio.com/',  # เปลี่ยนเป็น URL ของ Firebase Realtime Database ของคุณ
        'storageBucket': 'project-camera-50c3d.appspot.com'  # เปลี่ยนเป็นชื่อ Firebase Storage bucket ของคุณ
    })
except Exception as e:
    print(f"An error occurred while initializing Firebase: {e}")
    raise

# Reference to the Firebase Realtime Database
ref = db.reference('face_images')

data = {
    "km": {
        "id": "100000",
        "name": "Thanakim Pudpong",
        "major": "IT",
        "starting_year": 2020,
        "total_attendance": 0,
        "standing": "6",
        "year": 1,
        "last_attendance": "2020-11-11 00:00:00"
    },
    "Ohm": {
        "id": "100001",
        "name": "Thanapipat Binohmar",
        "major": "IT",
        "starting_year": 2020,
        "total_attendance": 0,
        "standing": "6",
        "year": 1,
        "last_attendance": "2020-11-11 00:00:00"
    }
}

try:
    for key, value in data.items():
        ref.child(key).set(value)
except Exception as e:
    print(f"An error occurred while setting data to Firebase: {e}")
