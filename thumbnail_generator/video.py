
from __future__ import annotations

from io import BytesIO
from typing import Tuple

from .core import CropMode, OutputFormat, DEFAULT_SIZE


def video_thumbnail_from_url(
    url: str,
    size: Tuple[int, int] = DEFAULT_SIZE,
    crop: CropMode = CropMode.FIT,
    format: OutputFormat = "JPEG",
    quality: int = 90,
) -> BytesIO:
    """Placeholder to keep public API stable until video support lands."""
    raise NotImplementedError("Video thumbnail generation is not implemented yet.")
