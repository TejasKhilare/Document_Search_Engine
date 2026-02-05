from app.ingestion.pdf_parser import extract_pdf_words
from app.utils.token_normalizer import normalize_token


class IndexBuilder:
    def __init__(self, index):
        self.index = index

    def index_pdf(self, pdf_path: str, doc_id: str):
        pages = extract_pdf_words(pdf_path)

        # increment document count ONCE per document
        self.index.increment_doc_count()

        for page_words in pages:
            for word in page_words:
                # 🔑 normalize token (CRITICAL FIX)
                token = normalize_token(word["text"])
                if not token:
                    continue

                box = {
                    "x": word["x"],
                    "y": word["y"],
                    "width": word["width"],
                    "height": word["height"],
                }

                self.index.add_token(
                    token=token,
                    doc_id=doc_id,
                    page_no=word["page_no"],
                    box=box
                )
