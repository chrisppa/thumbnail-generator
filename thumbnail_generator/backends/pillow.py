from PIL import Image, ImageOps
from io import BytesIO
from typing import Tuple

import httpx

from ..core import CropMode, OutputFormat, DEFAULT_QUALITY, DEFAULT_HEADERS

def thumbnail_from_url(
    url: str,
    size: Tuple[int, int] = (400, 400),
    crop: CropMode = CropMode.FIT,
    format: OutputFormat = "JPEG",
    quality: int = DEFAULT_QUALITY,
    background = (255, 255, 255),
) -> BytesIO:
    response = httpx.get(url, headers=DEFAULT_HEADERS, timeout=30.0, follow_redirects=True)
    response.raise_for_status()

    img = Image.open(BytesIO(response.content))
    img = ImageOps.exif_transpose(img)  # fix orientation

    w, h = size

    if crop == CropMode.FIT:
        img.thumbnail((w, h), Image.LANCZOS)

    elif crop in (CropMode.FILL, CropMode.SMART):  # smart ≈ center crop for Pillow
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