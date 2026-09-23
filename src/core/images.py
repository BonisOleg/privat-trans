"""JPEG/PNG з адмінки стають WebP. Прозорість лишається, готовий WebP не перекодовується."""

from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

RASTER_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
_CONVERT_SUFFIXES = {".jpg", ".jpeg", ".png"}
_WEBP_QUALITY = 82


def convert_image_fields(instance, *field_names: str, update_fields=None) -> None:
    for name in field_names:
        if update_fields is not None and name not in update_fields:
            continue
        convert_image_field_to_webp(instance, name)


def convert_image_field_to_webp(instance, field_name: str) -> None:
    field = getattr(instance, field_name)
    if not field or not field.name:
        return
    if Path(field.name).suffix.lower() not in _CONVERT_SUFFIXES:
        return
    source = _read_field(field)
    if not source:
        return
    webp = _encode_webp(source)
    if webp is None:
        return
    old_name = field.name
    storage = field.storage
    was_committed = field._committed
    field.save(f"{Path(old_name).stem}.webp", ContentFile(webp), save=False)
    if was_committed and old_name != field.name:
        storage.delete(old_name)


def _read_field(field) -> bytes:
    file_obj = field.file
    file_obj.seek(0)
    data = file_obj.read()
    file_obj.seek(0)
    return data


def _encode_webp(data: bytes) -> bytes | None:
    with Image.open(BytesIO(data)) as image:
        if getattr(image, "n_frames", 1) > 1:
            return None
        image = ImageOps.exif_transpose(image)
        buffer = BytesIO()
        if _has_alpha(image):
            image.convert("RGBA").save(buffer, format="WEBP", lossless=True, method=6)
        else:
            image.convert("RGB").save(buffer, format="WEBP", quality=_WEBP_QUALITY, method=6)
        return buffer.getvalue()


def _has_alpha(image: Image.Image) -> bool:
    if image.mode in ("RGBA", "LA"):
        return True
    return image.mode == "P" and "transparency" in image.info
