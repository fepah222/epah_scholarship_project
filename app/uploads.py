from pathlib import Path
from uuid import uuid4

from flask import current_app


ALLOWED_IMAGE_TYPES = {
    "jpg": ("image/jpeg",),
    "jpeg": ("image/jpeg",),
    "png": ("image/png",),
    "webp": ("image/webp",),
}


def _matches_signature(extension, header):
    if extension in ("jpg", "jpeg"):
        return header.startswith(b"\xff\xd8\xff")
    if extension == "png":
        return header.startswith(b"\x89PNG\r\n\x1a\n")
    if extension == "webp":
        return len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP"
    return False


def save_public_image(file_storage, folder):
    original = (file_storage.filename or "").strip()
    if "." not in original:
        raise ValueError("Choose a JPG, PNG, or WEBP image.")
    extension = original.rsplit(".", 1)[1].lower()
    if extension not in ALLOWED_IMAGE_TYPES:
        raise ValueError("Only JPG, PNG, and WEBP images are allowed.")

    header = file_storage.stream.read(16)
    file_storage.stream.seek(0)
    if not _matches_signature(extension, header):
        raise ValueError("The uploaded file is not a valid image of the selected type.")

    relative = Path(folder) / f"{uuid4().hex}.{extension}"
    root = Path(current_app.config["PUBLIC_UPLOAD"]).resolve()
    destination = (root / relative).resolve()
    if root not in destination.parents:
        raise ValueError("Invalid upload destination.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_storage.save(destination)
    return relative.as_posix()


def remove_public_image(relative_path):
    if not relative_path:
        return
    root = Path(current_app.config["PUBLIC_UPLOAD"]).resolve()
    candidate = (root / relative_path).resolve()
    if root in candidate.parents and candidate.is_file():
        candidate.unlink()
