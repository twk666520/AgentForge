"""Image preprocessing utilities for better OCR accuracy."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def load_image(
    source: str | Path | bytes | Image.Image,
) -> Image.Image:
    """Load an image from various input types."""
    if isinstance(source, Image.Image):
        return source.convert("RGB") if source.mode != "RGB" else source
    if isinstance(source, (str, Path)):
        return Image.open(source).convert("RGB")
    if isinstance(source, bytes):
        return Image.open(io.BytesIO(source)).convert("RGB")
    raise TypeError(f"Unsupported image source type: {type(source).__name__}")


def to_grayscale(image: Image.Image) -> Image.Image:
    """Convert to grayscale."""
    return ImageOps.grayscale(image)


def binarize(image: Image.Image, threshold: int = 128) -> Image.Image:
    """Convert to black-and-white using a threshold."""
    gray = to_grayscale(image) if image.mode != "L" else image
    return gray.point(lambda p: 255 if p > threshold else 0, mode="1")


def enhance_contrast(image: Image.Image, factor: float = 1.5) -> Image.Image:
    """Increase image contrast."""
    return ImageEnhance.Contrast(image).enhance(factor)


def denoise(image: Image.Image, radius: float = 1.0) -> Image.Image:
    """Apply mild Gaussian blur for noise reduction."""
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def sharpen(image: Image.Image, factor: float = 1.5) -> Image.Image:
    """Sharpen to emphasise text edges."""
    return ImageEnhance.Sharpness(image).enhance(factor)


def resize_if_needed(
    image: Image.Image,
    max_pixels: int = 4_000_000,
) -> Image.Image:
    """Downscale if image exceeds max_pixels."""
    w, h = image.size
    if w * h <= max_pixels:
        return image
    ratio = (max_pixels / (w * h)) ** 0.5
    return image.resize(
        (int(w * ratio), int(h * ratio)),
        Image.LANCZOS,
    )


def standard_pipeline(image: Image.Image, **config: Any) -> Image.Image:
    """Standard preprocessing: resize, grayscale, contrast,
    denoise, sharpen."""
    mp = config.get("max_pixels", 4_000_000)
    ct = config.get("contrast", 1.2)
    dr = config.get("denoise_radius", 0.5)
    sh = config.get("sharpen", 1.2)
    img = resize_if_needed(image, mp)
    img = to_grayscale(img)
    img = enhance_contrast(img, ct)
    img = denoise(img, dr)
    return sharpen(img, sh)
