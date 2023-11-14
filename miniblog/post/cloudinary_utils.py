# cloudinary_utils.py
from django.conf import settings
import cloudinary
import os
from cloudinary.uploader import upload

def configure_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

def upload_to_cloudinary(file_path, public_id=None):

    configure_cloudinary()

    try:
        result = upload(file_path, public_id=public_id)
        return result['secure_url'], result['asset_id']
    except Exception as e:
        raise RuntimeError(f"Error uploading to Cloudinary: {e}")