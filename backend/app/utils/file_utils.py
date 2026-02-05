import os

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def normalize_filename(filename: str) -> str:
    """
    Normalizes filename:
    - lowercase
    - removes fake/double extensions
    - keeps final valid extension
    """
    name = filename.lower()

    base, ext = os.path.splitext(name)

    # Handle cases like capture.pdf.png
    while ext and ext not in ALLOWED_EXTENSIONS:
        base, ext = os.path.splitext(base)

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    return base + ext
