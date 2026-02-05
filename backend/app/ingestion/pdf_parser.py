import pdfplumber
from typing import List,Dict
from app.ingestion.ocr import extract_text_from_scanned_pdf


def extract_pdf_pages(pdf_path:str)->List[Dict]:
    pages=[]
    has_text = False
    with pdfplumber.open(pdf_path) as pdf:
        for i,page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                has_text = True
            pages.append({
                "page_no": i + 1,
                "text": text or ""
            })

    if not has_text:
        ocr_texts = extract_text_from_scanned_pdf(pdf_path)
        pages = [
            {"page_no": i + 1, "text": ocr_texts[i]}
            for i in range(len(ocr_texts))
        ]   
    return pages
    