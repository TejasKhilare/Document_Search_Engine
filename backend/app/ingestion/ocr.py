import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from typing import List


def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text or ""


def extract_text_from_scanned_pdf(pdf_path: str) -> List[str]:
    """
    Returns list of page-wise OCR text
    """
    pages = convert_from_path(pdf_path)
    texts = []

    for page_image in pages:
        text = pytesseract.image_to_string(page_image)
        texts.append(text or "")

    return texts
