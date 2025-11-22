from __future__ import annotations

from io import BytesIO
from typing import Optional, Tuple

import httpx
import pyvips

from ..core import CropMode, OutputFormat, DEFAULT_QUALITY, DEFAULT_HEADERS


def _download(url: str) -> bytes:
    with httpx.stream("GET", url, timeout=30.0, headers=DEFAULT_HEADERS) as response:
        response.raise_for_status()
        return b"".join(response.iter_bytes(65536))


def thumbnail_from_bytes(
    data: bytes,
    size: Tuple[int, int],
    crop: CropMode,
    format: OutputFormat,
    quality: int,
    background: Tuple[int, int, int],
) -> BytesIO:
    width, height = size

    interesting = pyvips.Interesting.NONE
    if crop in (CropMode.FILL, CropMode.SMART):
        interesting = pyvips.Interesting.CENTRE

    image = pyvips.Image.thumbnail_buffer(
        data,
        width,
        height=height,
        crop=interesting,
        size=pyvips.Size.DOWN,
    )

    if crop == CropMode.SMART:
        image = image.smartcrop(width, height)
    elif crop == CropMode.PAD:
        pad_x = max((width - image.width) // 2, 0)
        pad_y = max((height - image.height) // 2, 0)
        image = image.embed(
            pad_x,
            pad_y,
            width,
            height,
            extend="background",
            background=list(background[:3]),
        )

    buffer = image.write_to_buffer(f".{format.lower()}", Q=quality, strip=True)
    return BytesIO(buffer)


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
        data = _download(url)

    return thumbnail_from_bytes(
        data=data,
        size=size,
        crop=crop,
        format=format,
        quality=quality,
        background=background,
    )
