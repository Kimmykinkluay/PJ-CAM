import firebase_admin
from firebase_admin import credentials, storage
import os

# Path to your service account key file
cert = 'serviceAccountKey.json'

# Check if the service account key file exists
if not os.path.exists(cert):
    raise FileNotFoundError(f"Service account key file not found: {cert}")

# Validate the JSON file
try:
    with open(cert, 'r') as file:
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
        'storageBucket': 'project-camera-50c3d.appspot.com'  # Replace with your Firebase Storage bucket name
    })
except Exception as e:
    print(f"An error occurred while initializing Firebase: {e}")
    raise

# Reference to Firebase Storage
bucket = storage.bucket()

def upload_image(local_file_path, remote_file_path):
    """
    Upload an image from the local path to Firebase Storage.
    :param local_file_path: Path to the image file on your local machine
    :param remote_file_path: Path where the file should be stored in Firebase Storage
    """
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"File not found: {local_file_path}")

    blob = bucket.blob(remote_file_path)

    try:
        blob.upload_from_filename(local_file_path)
        image_url = blob.public_url
        return image_url
    except Exception as e:
        print(f"An error occurred during upload: {e}")
        raise

def upload_multiple_images(local_folder_path, remote_folder_path):
    """
    Upload multiple images from a local folder to Firebase Storage.
    :param local_folder_path: Path to the local folder containing images
    :param remote_folder_path: Path where the images should be stored in Firebase Storage
    """
    if not os.path.isdir(local_folder_path):
        raise FileNotFoundError(f"Directory not found: {local_folder_path}")

    for file_name in os.listdir(local_folder_path):
        local_file_path = os.path.join(local_folder_path, file_name)
        remote_file_path = os.path.join(remote_folder_path, file_name)
        if os.path.isfile(local_file_path):
            try:
                image_url = upload_image(local_file_path, remote_file_path)
                print(f"Image '{file_name}' uploaded successfully. Accessible at: {image_url}")
            except Exception as e:
                print(f"An error occurred while uploading '{file_name}': {e}")

# Use the function to upload multiple images
local_folder_path = r'C:\Kimmy\reac\Toturial\KKKKK\MY PJ CAM\FL\face_images'  # Replace with the path to your local folder containing images
remote_folder_path = 'images/'  # Replace with the desired path in Firebase Storage

try:
    upload_multiple_images(local_folder_path, remote_folder_path)
except Exception as e:
    print(f"An error occurred: {e}")
