# URL-Thumbnail 🖼️➜🖼️

**The fastest, zero-dependency (optional libvips) thumbnail generator that works directly from image URLs.**

No need to download the full image to disk.  
One-liner thumbnails from any public image link — perfect for blogs, link previews, social media cards, crawlers, or static site generators.

## Installation

```bash
pip install url-thumbnail
```

## Quick Start

```python
from url_thumbnail import thumbnail_from_url

# Simple fit-inside thumbnail (preserves aspect ratio)
thumb_bytesio = thumbnail_from_url(
    "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba",
    size=(400, 400)
)

# Save it
with open("thumb.jpg", "wb") as f:
    f.write(thumb_bytesio.getvalue())
```

![Example Before/After](https://raw.githubusercontent.com/yourusername/url-thumbnail/main/assets/example-before-after.jpg)

## Features

* Works directly with remote URLs (no temporary files)
* Powered by Pillow by default → zero system dependencies
* Optional libvips backend (`backend="vips"`) → 5–10× faster + constant memory even on 100 MP photos
* Automatic EXIF orientation correction
* Multiple crop modes: fit (default), fill, center, pad, smart crop (coming soon)
* WebP & AVIF output support
* Async version (`athumbnail_from_url`)
* Simple & modern CLI
* Fully typed, tested, and ready for production

## Installation Options

```bash
# Minimal install (Pillow only)
pip install url-thumbnail

# With optional ultra-fast libvips backend
pip install url-thumbnail[vips]
```

On Linux you may need `apt install libvips` or `brew install vips` first for the `[vips]` extra.

## Quick Examples

### Python API

```python
from url_thumbnail import thumbnail_from_url, CropMode

# Basic usage
thumb = thumbnail_from_url("https://example.com/big.jpg", size=(300, 300))

# Square thumbnail with center crop
thumb = thumbnail_from_url(
    url,
    size=(500, 500),
    crop=CropMode.FILL,
    format="WEBP",
    quality=85
)

# Async
import asyncio
from url_thumbnail.asyncio import athumbnail_from_url

async def main():
    thumb = await athumbnail_from_url(url, size=(400, 400))

asyncio.run(main())
```

### CLI

```bash
url-thumbnail https://example.com/photo.jpg --size 600x400 --output preview.webp

# Batch mode
url-thumbnail *.jpg --size 300x300 --output-dir thumbs/
```

## Why url-thumbnail?

| Package | Remote URLs | Pillow | libvips optional | Async | No temp files | Actively maintained (2025) |
|---------|-------------|--------|------------------|-------|---------------|----------------------------|
| **url-thumbnail** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| easy-thumbnails | ❌ No (Django) | ✅ Yes | ❌ No | ❌ No | ❌ No | ✅ Yes |
| sorl-thumbnail | ❌ No (Django) | ✅ Yes | ❌ No | ❌ No | ❌ No | ✅ Yes |
| thumbnail | ❌ Local only | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ❌ No |
| preview-generator | ❌ Local only | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |

## Performance

300×300 thumbnail from 8000×8000 source:

| Backend | Time | Peak RAM |
|---------|------|----------|
| Pillow | ~0.9 s | ~220 MB |
| libvips | ~0.18 s | ~45 MB |

## Roadmap

* Smart cropping (face / salient region detection)
* Built-in disk & memory caching
* Background fill color / blur for pad mode
* Batch processing with progress bars
* Plugin system for custom backends

## Contributing

Contributions are very welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT © chrisppa
