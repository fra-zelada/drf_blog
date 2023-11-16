
from cloudinary.uploader import upload
import cloudinary.uploader
import cloudinary.api


def upload_to_cloudinary(file_path, public_id=None,):

    try:
        result = upload(file_path,  upload_preset='react-journal')
        return result['secure_url'], result['asset_id'], result['public_id']
    except Exception as e:
        raise RuntimeError(f"Error uploading to Cloudinary: {e}")

def delete_image_from_cloudinary(public_id):
    try:
        # Verificar si la imagen existe en Cloudinary
        image_info = cloudinary.api.resource(public_id)
        if image_info.get('error'):
            # La imagen no existe, no se puede eliminar
            return {"success": False, "message": "Image does not exist in Cloudinary"}

        # La imagen existe, intentar eliminarla
        result = cloudinary.uploader.destroy(public_id)

        return result  # El resultado podría contener información sobre el éxito o el error en caso de falla
    except Exception as e:
        raise RuntimeError(f"Error deleting from Cloudinary: {e}")