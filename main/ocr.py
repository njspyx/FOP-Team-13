from PIL import Image, ImageFilter
import pytesseract


def imageToText(file):
    """Very basic OCR"""

    # For Windows:
    # pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    image = Image.open(file)
    image.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(image)
    return text
