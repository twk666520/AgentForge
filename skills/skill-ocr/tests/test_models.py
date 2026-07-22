
"""Tests for OCR data models."""
from __future__ import annotations
from ocr_skill.models import BBox, TextLine, OCRResult


class TestBBox:
    def test_creation(self) -> None:
        b = BBox(x1=10.0, y1=20.0, x2=100.0, y2=80.0)
        assert b.x1 == 10.0 and b.y1 == 20.0
        assert b.x2 == 100.0 and b.y2 == 80.0

    def test_width_height_area(self) -> None:
        b = BBox(x1=10, y1=20, x2=110, y2=70)
        assert b.width == 100.0
        assert b.height == 50.0
        assert b.area == 5000.0

    def test_to_dict(self) -> None:
        b = BBox(x1=1, y1=2, x2=3, y2=4)
        d = b.to_dict()
        assert d["x1"] == 1.0 and d["y1"] == 2.0
        assert d["x2"] == 3.0 and d["y2"] == 4.0

    def test_from_list(self) -> None:
        b = BBox.from_list([5, 10, 50, 100])
        assert b.x1 == 5 and b.y1 == 10
        assert b.x2 == 50 and b.y2 == 100

    def test_from_list_wrong_length(self) -> None:
        import pytest
        with pytest.raises(ValueError, match="Expected 4"):
            BBox.from_list([1, 2, 3])


class TestTextLine:
    def test_creation(self) -> None:
        bbox = BBox(0, 0, 10, 10)
        tl = TextLine(text="hello", bbox=bbox, confidence=0.95)
        assert tl.text == "hello"
        assert tl.confidence == 0.95

    def test_to_dict(self) -> None:
        bbox = BBox(1, 2, 3, 4)
        tl = TextLine(text="hi", bbox=bbox, confidence=0.9)
        d = tl.to_dict()
        assert d["text"] == "hi"
        assert d["confidence"] == 0.9


class TestOCRResult:
    def test_empty(self) -> None:
        r = OCRResult()
        assert r.lines == []
        assert r.raw_text == ""
        assert r.confidence_mean == 0.0

    def test_raw_text_joins_lines(self) -> None:
        r = OCRResult(lines=[
            TextLine("hello", BBox(0, 0, 1, 1), 0.9),
            TextLine("world", BBox(0, 0, 1, 1), 0.8),
        ])
        assert r.raw_text == "hello\nworld"

    def test_confidence_mean(self) -> None:
        r = OCRResult(lines=[
            TextLine("a", BBox(0, 0, 1, 1), 1.0),
            TextLine("b", BBox(0, 0, 1, 1), 0.5),
        ])
        assert r.confidence_mean == 0.75

    def test_to_dict(self) -> None:
        r = OCRResult(
            lines=[TextLine("x", BBox(0, 0, 1, 1), 0.9)],
            image_dimensions=(100, 200),
            processing_time=0.5,
        )
        d = r.to_dict()
        assert len(d["lines"]) == 1
        assert d["image_dimensions"] == [100, 200]
        assert d["raw_text"] == "x"
        assert d["confidence_mean"] == 0.9
