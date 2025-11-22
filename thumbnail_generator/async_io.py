from __future__ import annotations

from typing import Tuple

import httpx
from io import BytesIO

from .core import CropMode, OutputFormat, DEFAULT_HEADERS, DEFAULT_SIZE
from . import thumbnail_from_url


async def athumbnail_from_url(
    url: str,
    size: Tuple[int, int] = DEFAULT_SIZE,
    crop: CropMode = CropMode.FIT,
    format: OutputFormat = "JPEG",
    quality: int = 90,
) -> BytesIO:
    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=30.0, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return thumbnail_from_url(
            url=url,
            size=size,
            crop=crop,
            format=format,
            quality=quality,
            data=response.content,
        )
