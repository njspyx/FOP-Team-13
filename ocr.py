from PIL import Image
import pytesseract


def imageToText(filename):
    """Very basic OCR"""

    # For Windows:
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    image = Image.open(filename)
    text = pytesseract.image_to_string(image)
    return text
