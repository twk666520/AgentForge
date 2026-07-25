"""Image loading utilities (no cross-skill dependencies)."""

from __future__ import annotations

import io
from pathlib import Path

from PIL import Image


def load_image(source: str | Path | bytes | Image.Image) -> Image.Image:
    """Load an image from various input types. Returns RGB."""
    if isinstance(source, Image.Image):
        return source.convert("RGB") if source.mode != "RGB" else source
    if isinstance(source, (str, Path)):
        return Image.open(source).convert("RGB")
    if isinstance(source, bytes):
        return Image.open(io.BytesIO(source)).convert("RGB")
    raise TypeError(f"Unsupported source type: {type(source).__name__}")
