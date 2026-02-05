import pdfplumber

with pdfplumber.open("data/uploaded_docs/Sanket_Resume.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"Page {i+1} text length:", 0 if text is None else len(text))
