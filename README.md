# thumbnail-generator

`thumbnail-generator` is a tiny, modern toolkit for creating thumbnails directly from remote image URLs and videos. It streams the source file, transforms it entirely in memory, and returns ready-to-serve bytes. The library powers a Python API, an async helper, video helpers, and a Typer-based CLI. Pillow is used out of the box; drop in `pyvips` for big speed wins with constant memory usage.

---

## Project Highlights

- Stream thumbnails straight from HTTPS URLs without writing to disk.
- Automatic EXIF orientation correction and high-quality downsampling.
- Unified crop modes: `fit`, `fill`, `pad`, and `smart` (smart switches to libvips smartcrop when available).
- Multiple output formats (`JPEG`, `WEBP`, `AVIF`, `PNG`) with adjustable quality.
- Async helper for event-driven crawlers.
- CLI command for quick batch jobs or scripting.
- Optional libvips backend (5–10× faster than Pillow on large images).
- Optional ffmpeg-powered video thumbnails that reuse the same image pipeline.

Current scope:

- Image thumbnails are production ready (Pillow fallback + libvips optional).
- Async helper delegates to the active backend (libvips or Pillow).
- Video thumbnail extraction works via ffmpeg (install with `[video]` extra and ensure the ffmpeg binary is on PATH).

---

## Requirements

- Python 3.9 or newer (repository is tested with Python 3.12).
- Linux, macOS, or Windows.
- Optional: system `libvips` if you plan to use the high-performance backend.
  - Ubuntu/Debian: `sudo apt install libvips`
  - macOS: `brew install vips`
  - Windows: install the prebuilt libvips bundle from [libvips releases](https://github.com/libvips/libvips/releases) and add it to `PATH`.

> **Note on Anaconda:** when using libvips, keep Python and the native libraries from the same toolchain. Mixing a conda-based Python with system `libvips` often results in loader errors. Creating a virtual environment from `/usr/bin/python3` (Linux/macOS) or using a clean conda environment that installs `libvips` from conda-forge solves this.

---

## Installation

### PyPI (recommended)

```bash
pip install thumbnail-generator
```

Upgrade anytime:

```bash
pip install --upgrade thumbnail-generator
```

For the high-performance libvips backend (5–10× faster at large resolutions):

```bash
pip install thumbnail-generator[vips]
```

Make sure the native `libvips` shared library is available (e.g. `apt install libvips`, `brew install vips`, or `conda install -c conda-forge libvips pyvips`). If libvips cannot be imported the package automatically falls back to Pillow and prints `using pillow backend` when you run the CLI.

The CLI depends on [Typer](https://typer.tiangolo.com/) and is bundled automatically from version `0.1.1` onward. If you are on `0.1.0`, run `pip install typer` once or upgrade: `pip install --upgrade thumbnail-generator`.

Enable video thumbnails (requires the ffmpeg binary and `ffmpeg-python` binding):

```bash
pip install thumbnail-generator[video]
```

Ensure the `ffmpeg` executable is available on your PATH (Linux/macOS: `sudo apt install ffmpeg` / `brew install ffmpeg`; Windows: install the static build from https://ffmpeg.org/download.html and add its `bin/` directory to PATH).

### From Source

```bash
git clone https://github.com/chrisppa/thumbnail-generator.git
cd thumbnail-generator

python3 -m venv venv          # /usr/bin/python3 on Linux
source venv/bin/activate      # .\venv\Scripts\activate on Windows
pip install -U pip

pip install -e .              # Pillow backend
pip install -e .[vips]        # Optional libvips backend
```

Keep the virtual environment active whenever you run the CLI or tests:

```bash
source venv/bin/activate
```

---

## Usage

### CLI

```bash
thumbnail-generator https://images.unsplash.com/photo-1682687220742-aba13b6e50ba \
  --size 800x800 \
  --crop smart \
  --format WEBP \
  --output hero.webp
```

Options (via `thumbnail-generator --help`):

- `--output` – destination file path (default `thumb.jpg`).
- `--size` – `<width>x<height>` integers (default `400x400`).
- `--crop` – one of `fit`, `fill`, `smart`, `pad`.
- `--format` – `JPEG`, `WEBP`, `AVIF`, `PNG`.
- `--quality` – integer 1–100 (backend-specific defaults to 90).

When `pyvips` is available the CLI reports `Saved … using vips backend`, otherwise Pillow is used automatically.

### Python API

```python
from thumbnail_generator import thumbnail_from_url, CropMode

buf = thumbnail_from_url(
    "https://example.com/large.jpeg",
    size=(500, 300),
    crop=CropMode.FILL,
    format="WEBP",
    quality=85,
)

with open("thumb.webp", "wb") as fp:
    fp.write(buf.getvalue())
```

### Async API

```python
import asyncio
from thumbnail_generator import athumbnail_from_url

async def main():
    buf = await athumbnail_from_url(
        "https://example.com/scene.jpg",
        size=(320, 320),
    )
    with open("async-thumb.jpg", "wb") as fp:
        fp.write(buf.getbuffer())

asyncio.run(main())
```

The async helper uses the currently active backend under the hood.

### Video API

```python
from thumbnail_generator import video_thumbnail_from_url, CropMode

thumb = video_thumbnail_from_url(
    "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    size=(640, 360),
    crop=CropMode.FILL,
    format="WEBP",
)

with open("video-thumb.webp", "wb") as fp:
    fp.write(thumb.getvalue())
```

Install with `pip install thumbnail-generator[video]` and ensure the `ffmpeg` binary is available. The helper samples multiple timestamps and reuses the active image backend for resizing/cropping.

---

## Backends Explained

| Backend  | Activation                             | Strengths                                  | Notes                                    |
|----------|----------------------------------------|--------------------------------------------|------------------------------------------|
| Pillow   | Installed automatically with `pip install -e .` | Zero native deps, works everywhere          | Best for small/medium images             |
| libvips  | Install `libvips` + `pip install -e .[vips]`   | Fast, constant memory, smart cropping available | Requires OS-level libvips libraries      |

- `CropMode.FIT`: fits inside the target box, preserving aspect ratio.
- `CropMode.FILL`: fills the target box by scaling and center-cropping.
- `CropMode.SMART`: same as `FILL`; if libvips is active, switches to `smartcrop`.
- `CropMode.PAD`: letterboxes the image on a background color.

Output formats are passed straight to the backend. The default quality is 90; adjust for smaller files or higher fidelity.

---

## Development Workflow

```bash
source venv/bin/activate
pip install -e .[dev,vips]  # add dev extras when they land
pytest                      # once the test suite is added
python -m thumbnail_generator.cli --help
```

Recommended extras (when available) include Ruff for linting, Mypy for typing, and pytest with responses for mocking HTTP downloads.

---

## Troubleshooting

- **`ImportError: cannot load library 'libvips.so.42'`**  
  Ensure `libvips` is installed system-wide *and* that your Python runtime comes from the same toolchain. Recreate the virtualenv with `/usr/bin/python3` or use a dedicated conda env with `conda install -c conda-forge libvips`.

- **PyPI install without libvips**  
  If you install the package elsewhere and want to force Pillow, omit the `[vips]` extra or `pip uninstall pyvips`.

- **Video thumbnails fail: `ffmpeg` not found**  
  Install the `[video]` extra (`pip install thumbnail-generator[video]`) and ensure the `ffmpeg` executable is discoverable on PATH. On Windows, download a static build and restart your shell after updating PATH.

- **Timeouts fetching images**  
  The default HTTP timeout is 30 seconds. If you need retries, wrap `thumbnail_from_url` in your own retry logic or extend `DEFAULT_HEADERS`/`DEFAULT_TIMEOUT` in `core.py`.

---

## Roadmap

- Smart crop improvements (face/saliency detection fallback when Pillow is active).
- Configurable caching (memory/disk).
- CLI batch mode with globbing and progress indicators.
- Intelligent frame scoring (sharpness / aesthetic ranking) for video thumbnails.

---

## License

MIT © chrisppa
