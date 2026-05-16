import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
import uuid

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_upload(file: UploadFile) -> str:
    filename  = f"{uuid.uuid4()}_{file.filename}"
    save_path = UPLOAD_DIR / filename
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return str(save_path)


def prepare_image(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return _pdf_to_image(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
        return _normalize_image(file_path)
    else:
        raise ValueError(f"نوع الملف مش مدعوم: {ext}")


def _pdf_to_image(pdf_path: str) -> str:
    try:
        from pdf2image import convert_from_path
    except ImportError:
        raise ImportError("pdf2image مش متنصب — شغّل: pip install pdf2image")

    pages    = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=1)
    img_path = pdf_path.replace(".pdf", "_page1.jpg")
    pages[0].save(img_path, "JPEG")
    return img_path


def _normalize_image(img_path: str) -> str:
    img = Image.open(img_path).convert("RGB")

    max_size = 2000
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size))

    out_path = img_path.rsplit(".", 1)[0] + "_processed.jpg"
    img.save(out_path, "JPEG", quality=90)
    return out_path
