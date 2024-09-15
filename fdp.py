import firebase_admin
from firebase_admin import credentials, storage
import os

cert = 'serviceAccountKey.json'

if not os.path.exists(cert):
    raise FileNotFoundError(f"Service account key file not found: {cert}")

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


# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate(cert)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://project-camera-50c3d-default-rtdb.firebaseio.com/',  # เปลี่ยนเป็น URL ของ Firebase Realtime Database ของคุณ
        'storageBucket': 'project-camera-50c3d.appspot.com'  # เปลี่ยนเป็นชื่อ Firebase Storage bucket ของคุณ
    })
except Exception as e:
    print(f"An error occurred while initializing Firebase: {e}")
    raise


# Reference to Firebase Storage
bucket = storage.bucket()

def upload_image(local_file_path, remote_file_path):
    """
    อัปโหลดภาพจากพาธท้องถิ่นไปยัง Firebase Storage
    :param local_file_path: พาธของไฟล์ภาพในเครื่องของคุณ
    :param remote_file_path: พาธที่ต้องการบันทึกไฟล์ใน Firebase Storage
    """
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"File not found: {local_file_path}")

    # สร้าง blob (อ็อบเจ็กต์ที่แทนไฟล์ใน Firebase Storage)
    blob = bucket.blob(remote_file_path)

    # อัปโหลดไฟล์ไปยัง Firebase Storage
    blob.upload_from_filename(local_file_path)

    # รับ URL สาธารณะของไฟล์
    image_url = blob.public_url

    return image_url

# ใช้ฟังก์ชันในการอัปโหลดภาพ
local_image_path = 'C:\Kimmy\reac\Toturial\KKKKK\MY PJ CAM\FL\face_images'  # เปลี่ยนเป็นพาธของไฟล์ภาพในเครื่องของคุณ
remote_image_path = 'project-camera-50c3d.appspot.com/PPP'  # เปลี่ยนเป็นพาธที่ต้องการใน Firebase Storage

try:
    image_url = upload_image(local_image_path, remote_image_path)
    print(f"Image uploaded successfully. Accessible at: {image_url}")
except Exception as e:
    print(f"An error occurred: {e}")
