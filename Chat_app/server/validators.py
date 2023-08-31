from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image)as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    "The allowed dimensions for the image 70x70"
                )


def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpeg", ".jpg", ".png", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file type")
