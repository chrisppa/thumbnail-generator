from __future__ import annotations

from io import BytesIO
from typing import Optional, Tuple

import httpx
from PIL import Image, ImageOps

from ..core import CropMode, OutputFormat, DEFAULT_QUALITY, DEFAULT_HEADERS


def _open_image(data: bytes) -> Image.Image:
    img = Image.open(BytesIO(data))
    img = ImageOps.exif_transpose(img)
    return img


def thumbnail_from_bytes(
    data: bytes,
    size: Tuple[int, int],
    crop: CropMode,
    format: OutputFormat,
    quality: int,
    background: Tuple[int, int, int],
) -> BytesIO:
    img = _open_image(data)

    w, h = size

    if crop == CropMode.FIT:
        img.thumbnail((w, h), Image.LANCZOS)

    elif crop in (CropMode.FILL, CropMode.SMART):
        ratio = max(w / img.width, h / img.height)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
        left = (img.width - w) // 2
        top = (img.height - h) // 2
        img = img.crop((left, top, left + w, top + h))

    elif crop == CropMode.PAD:
        img.thumbnail((w, h), Image.LANCZOS)
        new_img = Image.new("RGB", (w, h), background)
        new_img.paste(img, ((w - img.width) // 2, (h - img.height) // 2))
        img = new_img

    buf = BytesIO()
    save_kwargs = {"quality": quality, "optimize": True}
    if format == "JPEG":
        save_kwargs["progressive"] = True
    img.save(buf, format=format, **save_kwargs)
    buf.seek(0)
    return buf


def thumbnail_from_url(
    url: str,
    size: Tuple[int, int] = (400, 400),
    crop: CropMode = CropMode.FIT,
    format: OutputFormat = "JPEG",
    quality: int = DEFAULT_QUALITY,
    background: Tuple[int, int, int] = (255, 255, 255),
    data: Optional[bytes] = None,
) -> BytesIO:
    if data is None:
        response = httpx.get(url, headers=DEFAULT_HEADERS, timeout=30.0, follow_redirects=True)
        response.raise_for_status()
        data = response.content

    return thumbnail_from_bytes(
        data=data,
        size=size,
        crop=crop,
        format=format,
        quality=quality,
        background=background,
    )
