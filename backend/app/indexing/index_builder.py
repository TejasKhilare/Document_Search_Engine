from app.ingestion.pdf_parser import extract_pdf_pages
from app.ingestion.text_cleaner import clean_text
from app.indexing.tokenizer import tokenize

class IndexBuilder:
    def __init__(self,index):
        self.index=index

    def index_pdf(self,pdf_path:str,doc_id:str):
        pages = extract_pdf_pages(pdf_path)
        self.index.increment_doc_count()
        for page in pages:
            page_no = page["page_no"]
            cleaned = clean_text(page["text"])
            tokens = tokenize(cleaned)

            for token, pos in tokens:
                self.index.add_token(token, doc_id, page_no, pos)