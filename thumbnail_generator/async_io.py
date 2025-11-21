from __future__ import annotations

from typing import Tuple

import httpx
from io import BytesIO

from .core import CropMode, OutputFormat, DEFAULT_HEADERS, DEFAULT_SIZE
from . import thumbnail_from_url  # uses the selected backend

async def athumbnail_from_url(
    url: str,
    size: Tuple[int, int] = DEFAULT_SIZE,
    crop: CropMode = CropMode.FIT,
    format: OutputFormat = "JPEG",
    quality: int = 90,
) -> BytesIO:
    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=30.0, follow_redirects=True) as client:
        r = await client.get(url)
        r.raise_for_status()
        # Reuse sync function but pass content directly — we'll add a tiny refactor
        from .backends.vips import thumbnail_from_url as vips_func
        from .backends.pillow import thumbnail_from_url as pillow_func
        
        func = vips_func if "__backend__" in globals() and globals()["__backend__"] == "vips" else pillow_func
        # temporarily monkey-patch to use content instead of url (both backends accept bytes already)
        return func.__wrapped__(data=r.content, size=size, crop=crop, format=format, quality=quality)  # we'll make them accept data=