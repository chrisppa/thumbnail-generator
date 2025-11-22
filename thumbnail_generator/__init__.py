from __future__ import annotations

try:
    import pyvips  # noqa: F401
    from .backends.vips import thumbnail_from_url
    __backend__ = "vips"
except ImportError:
    from .backends.pillow import thumbnail_from_url
    __backend__ = "pillow"

from .async_io import athumbnail_from_url
from .video import video_thumbnail_from_url, VideoThumbnailError
from .core import CropMode, OutputFormat

__version__ = "0.1.1"

__all__ = [
    "thumbnail_from_url",
    "athumbnail_from_url",
    "video_thumbnail_from_url",
    "VideoThumbnailError",
    "CropMode",
    "OutputFormat",
    "__backend__",
    "__version__",
]
