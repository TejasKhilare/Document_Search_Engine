from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
import uuid
from contextlib import asynccontextmanager
from app.utils.file_utils import normalize_filename

from app.ingestion.text_cleaner import clean_text
from app.indexing.inverted_index import InvertedIndex
from app.indexing.index_builder import IndexBuilder
from app.search.exact_search import exact_search
from app.indexing.tokenizer import tokenize
from app.ingestion.ocr import extract_text_from_image

# -------------------------
# App & Paths
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Lifespan startup: indexing stored files")

    if not os.path.exists(UPLOAD_DIR):
        yield
        return

    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        doc_id = filename.lower()

        # ---------- PDFs (text + OCR fallback handled internally) ----------
        if filename.lower().endswith(".pdf"):
            print("Startup indexing PDF:", filename)
            builder.index_pdf(file_path, doc_id)

        # ---------- Images (OCR only) ----------
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            print("Startup indexing image:", filename)

            raw_text = extract_text_from_image(file_path)
            cleaned = clean_text(raw_text)
            tokens = tokenize(cleaned)

            if not tokens:
                continue

            index.increment_doc_count()

            for token, pos in tokens:
                index.add_token(
                    token=token,
                    doc_id=doc_id,
                    page_no=1,
                    position=pos
                )

    print("✅ Startup indexing complete")
    print("TOTAL DOCS:", index.total_docs)
    print("TOTAL TOKENS:", len(index.index))

    yield
  # App runs here

    # Shutdown logic (optional)
    print("Lifespan shutdown")

app = FastAPI(lifespan=lifespan)

# backend/app/main.py -> backend/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploaded_docs")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# Core Engine (In-Memory)
# -------------------------

index = InvertedIndex()
builder = IndexBuilder(index)
# -------------------------
# Health Check (IMPORTANT)
# -------------------------
@app.get("/health")
def health():
    return {"status": "alive"}
# -------------------------
# Upload & Index PDFs
# -------------------------

@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    indexed_docs = []

    for file in files:
        filename=file.filename
        if not filename:
            continue
        try:
            filename = normalize_filename(filename)
        except ValueError:
            continue
        if not filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
            continue


        doc_id = filename
        file_path = os.path.join(UPLOAD_DIR, filename)

        print("Saving file to:", file_path) 

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Index immediately (Phase-1 design)
        if filename.lower().endswith(".pdf"):
            builder.index_pdf(file_path, doc_id)
        else:
            raw_text = extract_text_from_image(file_path)
            cleaned = clean_text(raw_text)
            tokens = tokenize(cleaned)

            index.increment_doc_count()

            for token, pos in tokens:
                index.add_token(
                    token=token,
                    doc_id=doc_id,
                    page_no=1,      # images are single-page docs
                    position=pos
                )

        if filename.endswith(".pdf"):
            file_type = "pdf"
        else:
            file_type = "image"

        indexed_docs.append({
            "doc_id": doc_id,
            "filename": filename,
            "file_type": file_type
        })


    if not indexed_docs:
        raise HTTPException(status_code=400, detail="No valid files uploaded")

    # 🔍 DEBUG (keep during development)
    print("AFTER UPLOAD")
    print("TOTAL DOCS:", index.total_docs)
    print("TOTAL UNIQUE TOKENS:", len(index.index))

    return {
        "status": "success",
        "indexed_documents": indexed_docs
    }


# -------------------------
# Exact Search
# -------------------------

@app.get("/search")
def search(q: str):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Normalize query exactly like indexed text
    cleaned_query = clean_text(q)
    tokens = [t for t, _ in tokenize(cleaned_query)]

    # 🔍 DEBUG (keep during development)
    print("QUERY:", cleaned_query)
    print("TOKENS:", tokens)
    print("INDEX DOCS:", index.total_docs)
    print("INDEX TOKENS:", len(index.index))

    if not tokens:
        return []

    raw_results = exact_search(tokens, index)

    ranked = []
    for doc_id, pages in raw_results.items():
        for page_no, score in pages.items():
            ranked.append({
                "doc_id": doc_id,
                "page": page_no,
                "score": score
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
