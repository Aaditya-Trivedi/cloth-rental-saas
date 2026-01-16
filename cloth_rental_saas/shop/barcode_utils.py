import barcode
from barcode.writer import ImageWriter
from django.conf import settings
import os

def generate_barcode(cloth_code):
    """
    Generates barcode image and returns relative path
    """
    barcode_dir = settings.MEDIA_ROOT / "barcodes"
    os.makedirs(barcode_dir, exist_ok=True)

    file_path = barcode_dir / cloth_code

    code128 = barcode.get("code128", cloth_code, writer=ImageWriter())
    code128.save(str(file_path))

    return f"barcodes/{cloth_code}.png"
