import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from typing import List, Dict

OCR_LANGS = "eng+hin+mar"   # English + Hindi + Marathi


def extract_image_words(image_path: str) -> List[Dict]:
    image = Image.open(image_path)
    width, height = image.size

    data = pytesseract.image_to_data(
        image,
        lang=OCR_LANGS,
        output_type=pytesseract.Output.DICT
    )

    words = []
    n = len(data["text"])

    for i in range(n):
        text = data["text"][i].strip()
        if not text:
            continue

        words.append({
            "text": text,        # DO NOT lowercase non-latin
            "page_no": 1,
            "x": data["left"][i] / width,
            "y": data["top"][i] / height,
            "width": data["width"][i] / width,
            "height": data["height"][i] / height,
        })

    return words


def extract_scanned_pdf_words(pdf_path: str) -> List[List[Dict]]:
    images = convert_from_path(pdf_path,dpi=300)
    pages = []

    for page_index, img in enumerate(images):
        width, height = img.size

        data = pytesseract.image_to_data(
            img,
            lang=OCR_LANGS,
            output_type=pytesseract.Output.DICT
        )

        page_words = []
        n = len(data["text"])

        for i in range(n):
            text = data["text"][i].strip()
            if not text:
                continue

            page_words.append({
                "text": text,
                "page_no": page_index + 1,
                "x": data["left"][i] / width,
                "y": data["top"][i] / height,
                "width": data["width"][i] / width,
                "height": data["height"][i] / height,
            })

        pages.append(page_words)

    return pages
