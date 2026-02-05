from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
from contextlib import asynccontextmanager

from app.utils.file_utils import normalize_filename
from app.indexing.inverted_index import InvertedIndex
from app.indexing.index_builder import IndexBuilder
from app.search.exact_search import exact_search
from app.ingestion.ocr import extract_image_words

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------
# Core Engine (In-Memory)
# -------------------------
index = InvertedIndex()
builder = IndexBuilder(index)

# -------------------------
# Lifespan (Startup Indexing)
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Lifespan startup: indexing stored files")

    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        doc_id = filename

        if filename.endswith(".pdf"):
            print("Startup indexing PDF:", filename)
            builder.index_pdf(file_path, doc_id)

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            print("Startup indexing image:", filename)
            words = extract_image_words(file_path)

            if not words:
                continue

            index.increment_doc_count()

            for w in words:
                index.add_token(
                    token=w["text"],
                    doc_id=doc_id,
                    page_no=1,
                    box={
                        "x": w["x"],
                        "y": w["y"],
                        "width": w["width"],
                        "height": w["height"],
                    }
                )

    print("✅ Startup indexing complete")
    print("TOTAL DOCS:", index.total_docs)
    print("TOTAL TOKENS:", len(index.index))
    yield

# -------------------------
# App
# -------------------------
app = FastAPI(lifespan=lifespan)

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"status": "alive"}

# -------------------------
# Upload
# -------------------------
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    indexed_docs = []

    for file in files:
        if not file.filename:
            continue

        try:
            filename = normalize_filename(file.filename)
        except ValueError:
            continue

        file_path = os.path.join(UPLOAD_DIR, filename)
        doc_id = filename

        print("Saving file to:", file_path)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # ---------- PDF ----------
        if filename.endswith(".pdf"):
            builder.index_pdf(file_path, doc_id)
            file_type = "pdf"

        # ---------- IMAGE ----------
        else:
            words = extract_image_words(file_path)
            if not words:
                continue

            index.increment_doc_count()

            for w in words:
                index.add_token(
                    token=w["text"],
                    doc_id=doc_id,
                    page_no=1,
                    box={
                        "x": w["x"],
                        "y": w["y"],
                        "width": w["width"],
                        "height": w["height"],
                    }
                )

            file_type = "image"

        indexed_docs.append({
            "doc_id": doc_id,
            "filename": filename,
            "file_type": file_type
        })

    if not indexed_docs:
        raise HTTPException(status_code=400, detail="No valid files uploaded")

    print("AFTER UPLOAD")
    print("TOTAL DOCS:", index.total_docs)
    print("TOTAL TOKENS:", len(index.index))

    return {
        "status": "success",
        "indexed_documents": indexed_docs
    }

# -------------------------
# Search (still score-only)
# -------------------------
from app.utils.token_normalizer import normalize_token
@app.get("/search")
def search(q: str):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    query_tokens = [
    normalize_token(t) for t in q.split()
    if normalize_token(t)]

    raw_results = exact_search(query_tokens, index)

    ranked = []

    for doc_id, pages in raw_results.items():
        for page_no, data in pages.items():
            ranked.append({
                "doc_id": doc_id,
                "file_type": "pdf" if doc_id.endswith(".pdf") else "image",
                "page": page_no,
                "score": data["score"],
                "highlights": data["highlights"]
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    print("QUERY TOKENS:", query_tokens)
    print("INDEX TOKENS SAMPLE:", list(index.index.keys())[:150])
    return ranked
