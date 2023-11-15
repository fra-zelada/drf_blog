from django.conf import settings
import cloudinary
import os
from cloudinary.uploader import upload

def configure_cloudinary():
    try:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY['CLOUD_NAME'],
            api_key=settings.CLOUDINARY['API_KEY'],
            api_secret=settings.CLOUDINARY['API_SECRET'],
            api_proxy=settings.CLOUDINARY['API_PROXY'],
            secure=True
        )
    except KeyError as e:
        raise RuntimeError(f"Error configuring Cloudinary: {e}")

def upload_to_cloudinary(file_path, public_id=None):

    configure_cloudinary()

    try:
        result = upload(file_path, public_id=public_id)
        return result['secure_url'], result['asset_id']
    except Exception as e:
        raise RuntimeError(f"Error uploading to Cloudinary: {e}")