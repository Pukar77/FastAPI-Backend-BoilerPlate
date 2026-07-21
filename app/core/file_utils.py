import os
import uuid
from fastapi import UploadFile
from app.core.config import get_settings
from app.core.exceptions import BadRequestException

settings = get_settings()
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def validate_image(file: UploadFile) -> None:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise BadRequestException(
            f"Invalid image format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    max_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > max_bytes:
        raise BadRequestException(
            f"Image too large. Max {settings.MAX_IMAGE_SIZE_MB}MB"
        )


def save_image(file: UploadFile) -> str:
    validate_image(file)

    upload_dir = os.path.join(settings.UPLOAD_DIR, "products")
    os.makedirs(upload_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as f:
        content = file.file.read()
        f.write(content)

    return f"/uploads/products/{filename}"


def delete_image(image_path: str) -> None:
    if not image_path:
        return
    filepath = os.path.join(settings.UPLOAD_DIR, image_path.replace("/uploads/", ""))
    if os.path.exists(filepath):
        os.remove(filepath)
