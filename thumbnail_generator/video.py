from __future__ import annotations

from io import BytesIO
from typing import List, Optional, Tuple

from . import __backend__
from .core import CropMode, OutputFormat, DEFAULT_QUALITY, DEFAULT_SIZE
from .backends.pillow import thumbnail_from_bytes as pillow_thumbnail

try:  # optional dependency loaded lazily for error messaging
    import ffmpeg  # type: ignore
    from ffmpeg import Error as FFMpegError  # type: ignore
except ImportError as _import_exc:  # pragma: no cover - handled at call time
    ffmpeg = None  # type: ignore
    FFMpegError = RuntimeError  # type: ignore
    _FFMPEG_IMPORT_ERROR = _import_exc
else:  # pragma: no cover - trivial branch
    _FFMPEG_IMPORT_ERROR = None

if __backend__ == "vips":  # only import when available to avoid ImportError
    from .backends.vips import thumbnail_from_bytes as vips_thumbnail
else:
    vips_thumbnail = None


class VideoThumbnailError(RuntimeError):
    """Raised when a video thumbnail cannot be produced."""


def _ensure_ffmpeg() -> None:
    if ffmpeg is None:  # type: ignore[truthy-function]
        raise VideoThumbnailError(
            "ffmpeg-python is required for video thumbnails. Install with 'pip install "
            "thumbnail-generator[video]' and ensure the ffmpeg binary is on PATH."
        ) from _FFMPEG_IMPORT_ERROR


def _probe_duration(url: str) -> float:
    _ensure_ffmpeg()
    try:
        metadata = ffmpeg.probe(url, select_streams="v")  # type: ignore[arg-type]
    except FFMpegError as exc:  # pragma: no cover - passthrough for now
        raise VideoThumbnailError(exc.stderr.decode("utf-8", errors="ignore")) from exc

    duration = metadata.get("format", {}).get("duration")
    if duration is None:
        for stream in metadata.get("streams", []):
            if "duration" in stream:
                duration = stream["duration"]
                break
    if duration is None:
        raise VideoThumbnailError("Unable to determine video duration")
    return float(duration)


def _select_seek_times(duration: float, samples: int = 3) -> List[float]:
    if duration <= 0 or samples <= 1:
        return [0.0]
    start, end = 0.15, 0.75
    step = (end - start) / (samples - 1)
    return [float(duration * (start + step * i)) for i in range(samples)]


def _extract_frame(url: str, timestamp: float) -> bytes:
    _ensure_ffmpeg()
    try:
        out, _ = (
            ffmpeg  # type: ignore[attr-defined]
            .input(
                url,
                ss=timestamp,
                analyzeduration="5M",
                probesize="10M",
            )
            .output(
                "pipe:",
                vframes=1,
                format="image2",
                vcodec="mjpeg",
            )
            .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
    except FFMpegError as exc:
        raise VideoThumbnailError(exc.stderr.decode("utf-8", errors="ignore")) from exc

    if not out:
        raise VideoThumbnailError("Received empty frame from ffmpeg")
    return out


def _pick_best_frame(url: str, duration: float) -> bytes:
    errors: List[str] = []
    for timestamp in _select_seek_times(duration):
        try:
            return _extract_frame(url, timestamp)
        except VideoThumbnailError as exc:
            errors.append(str(exc))
    raise VideoThumbnailError("; ".join(errors) if errors else "Failed to extract frame")


def _thumbnail_from_bytes(
    data: bytes,
    *,
    size: Tuple[int, int],
    crop: CropMode,
    format: OutputFormat,
    quality: int,
) -> BytesIO:
    if __backend__ == "vips":
        if vips_thumbnail is None:  # pragma: no cover - failsafe
            raise VideoThumbnailError("libvips backend selected but unavailable")
        backend_fn = vips_thumbnail
    else:
        backend_fn = pillow_thumbnail

    return backend_fn(
        data=data,
        size=size,
        crop=crop,
        format=format,
        quality=quality,
        background=(0, 0, 0),
    )


def video_thumbnail_from_url(
    url: str,
    size: Tuple[int, int] = DEFAULT_SIZE,
    crop: CropMode = CropMode.FIT,
    format: OutputFormat = "JPEG",
    quality: int = DEFAULT_QUALITY,
    seek_timestamp: Optional[float] = None,
) -> BytesIO:
    """Extract a representative frame from a remote video and return it as an image thumbnail."""

    duration = _probe_duration(url)
    frame_bytes = _extract_frame(url, seek_timestamp) if seek_timestamp is not None else _pick_best_frame(url, duration)
    return _thumbnail_from_bytes(
        data=frame_bytes,
        size=size,
        crop=crop,
        format=format,
        quality=quality,
    )
