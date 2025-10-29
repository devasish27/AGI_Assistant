import pytesseract
import os
from PIL import Image

img_path = "src/tests/test_image.png"  # place an image with text here to test
print("Tesseract executable:", pytesseract.pytesseract.tesseract_cmd)
if os.path.exists(img_path):
    print("OCR result:", pytesseract.image_to_string(Image.open(img_path)))
else:
    print("Place a test image at", img_path)
