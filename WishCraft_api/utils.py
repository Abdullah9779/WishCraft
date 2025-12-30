import os
import base64
import secrets
import string
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.utils.text import slugify


def generate_unique_code(length=8):
    """Generate a unique 8-character code"""
    while True:
        code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        user_folder = os.path.join(get_upload_folder(), code)
        if not os.path.exists(user_folder):
            return code


def validate_image(img_data):
    """Validate base64 image data"""
    try:
        if img_data.startswith('data:image/'):
            img_data = img_data.split(',')[1]
        
        image_bytes = base64.b64decode(img_data)
        
        # Validate image format
        image = Image.open(BytesIO(image_bytes))
        if image.format not in ['PNG', 'JPEG', 'JPG', 'GIF']:
            return False, "Invalid image format"
        
        # Check image size (max 5MB)
        if len(image_bytes) > 5 * 1024 * 1024:
            return False, "Image too large"
        
        return True, image_bytes
    except Exception as e:
        return False, f"Invalid image data: {str(e)}"


def secure_filename(filename):
    """Generate secure filename"""
    return slugify(filename)


def get_upload_folder():
    """Get upload folder path"""
    upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder