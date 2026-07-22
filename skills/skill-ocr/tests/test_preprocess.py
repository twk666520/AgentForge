
"""Tests for image preprocessing."""
from __future__ import annotations
from PIL import Image
from ocr_skill.preprocess import (
    load_image, to_grayscale, binarize,
    enhance_contrast, denoise, sharpen,
    resize_if_needed, standard_pipeline,
)


def _test_image(mode="RGB", size=(100, 50)):
    return Image.new(mode, size, color=(200, 200, 200))


class TestLoadImage:
    def test_from_pil(self):
        img = Image.new("RGB", (10, 10))
        r = load_image(img)
        assert r.mode == "RGB" and r.size == (10, 10)

    def test_converts_grayscale(self):
        img = Image.new("L", (10, 10), 128)
        r = load_image(img)
        assert r.mode == "RGB"

    def test_from_bytes(self):
        import io
        img = Image.new("RGB", (5, 5))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        r = load_image(buf.getvalue())
        assert r.size == (5, 5)

    def test_invalid_type(self):
        import pytest
        with pytest.raises(TypeError):
            load_image(123)


class TestTransforms:
    def test_to_grayscale(self):
        g = to_grayscale(_test_image())
        assert g.mode == "L"

    def test_binarize(self):
        b = binarize(_test_image(), threshold=128)
        assert b.mode == "1"

    def test_enhance_contrast(self):
        r = enhance_contrast(_test_image(), factor=2.0)
        assert r.size == (100, 50)

    def test_denoise(self):
        r = denoise(_test_image(), radius=0.5)
        assert r.size == (100, 50)

    def test_sharpen(self):
        r = sharpen(_test_image(), factor=2.0)
        assert r.size == (100, 50)

    def test_resize_under(self):
        img = _test_image(size=(100, 100))
        r = resize_if_needed(img, max_pixels=100_000)
        assert r.size == (100, 100)

    def test_resize_over(self):
        img = _test_image(size=(1000, 1000))
        r = resize_if_needed(img, max_pixels=100_000)
        assert r.size[0] * r.size[1] <= 100_000

    def test_standard_pipeline(self):
        r = standard_pipeline(_test_image(size=(200, 100)))
        assert r.mode == "L" and r.size == (200, 100)
