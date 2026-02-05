import pdfplumber
from typing import List, Dict
from app.ingestion.ocr import extract_scanned_pdf_words


def extract_pdf_words(pdf_path: str) -> List[List[Dict]]:
    pages = []
    has_text = False

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            words = page.extract_words(use_text_flow=True)
            page_words = []

            if words:
                has_text = True

            page_width = page.width
            page_height = page.height

            for w in words:
                text = w["text"].strip()
                if not text:
                    continue

                page_words.append({
                    "text": text,
                    "page_no": page_index + 1,
                    "x": w["x0"] / page_width,
                    "y": w["top"] / page_height,
                    "width": (w["x1"] - w["x0"]) / page_width,
                    "height": (w["bottom"] - w["top"]) / page_height,
                })

            pages.append(page_words)

    # OCR fallback for scanned PDFs
    if not has_text:
        pages = extract_scanned_pdf_words(pdf_path)

    return pages
