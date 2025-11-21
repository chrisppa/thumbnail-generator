import typer
from . import thumbnail_from_url, CropMode, OutputFormat, __backend__

app = typer.Typer(help="Generate thumbnails from image/video URLs")

@app.command()
def main(
    url: str,
    output: str = "thumb.jpg",
    size: str = "400x400",
    crop: CropMode = CropMode.FIT,
    format: OutputFormat = "JPEG",
    quality: int = 90,
):
    w, h = map(int, size.split("x"))
    buf = thumbnail_from_url(url, (w, h), crop=crop, format=format, quality=quality)
    with open(output, "wb") as f:
        f.write(buf.read())
    typer.echo(f"Saved {output} using {__backend__} backend")

if __name__ == "__main__":
    app()