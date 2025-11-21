from __future__ import annotations

from enum import StrEnum
from typing import Literal, Tuple

class CropMode(StrEnum):
    FIT = "fit"      # Preserve aspect, fit inside box (default)
    FILL = "fill"    # Cover entire box, crop excess (center)
    SMART = "smart"   # Cover + libvips attention/entropy crop
    PAD = "pad"       # Fit + pad to exact size

OutputFormat = Literal["JPEG", "WEBP", "AVIF", "PNG"]

DEFAULT_SIZE: Tuple[int, int] = (400, 400)
DEFAULT_QUALITY = 90
USER_AGENT = "thumbnail-generator/0.1 (+https://github.com/chrisppa/thumbnail-generator.git)"

DEFAULT_HEADERS = {"User-Agent": USER_AGENT}