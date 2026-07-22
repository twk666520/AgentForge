
"""Tests for OCREngine with a mocked backend."""
from __future__ import annotations
from unittest.mock import MagicMock
from PIL import Image
from agentforge_core.result import SkillResult
from ocr_skill.backends.base import BaseOCRBackend
from ocr_skill.engine import OCREngine
from ocr_skill.models import OCRResult


class MockBackend(BaseOCRBackend):
    def __init__(self):
        self.initialized = False
        self.cleaned = False

    def initialize(self, config: dict) -> None:
        self.initialized = True

    def recognize(
        self, image: Image.Image, **kwargs
    ) -> list[dict]:
        return [
            {"text": "Hello World",
             "confidence": 0.95,
             "bbox": [10, 20, 200, 50]},
            {"text": "Line Two",
             "confidence": 0.87,
             "bbox": [10, 55, 150, 80]},
        ]

    def cleanup(self) -> None:
        self.cleaned = True


def _engine():
    eng = OCREngine(backend=MockBackend())
    eng.initialize()
    return eng


class TestOCREngine:
    def test_identity(self):
        eng = OCREngine()
        assert eng.name == "ocr"
        assert eng.version == "0.1.0"

    def test_recognize_success(self):
        eng = _engine()
        r = eng.recognize(Image.new("RGB", (100, 50)))
        assert isinstance(r, SkillResult)
        assert r.success is True

    def test_recognize_returns_ocr_data(self):
        eng = _engine()
        r = eng.recognize(Image.new("RGB", (100, 50)))
        ocr = r.data
        assert isinstance(ocr, OCRResult)
        assert len(ocr.lines) == 2
        assert ocr.lines[0].text == "Hello World"

    def test_run_returns_ocr_result(self):
        eng = _engine()
        r = eng.run(Image.new("RGB", (100, 50)))
        assert isinstance(r, OCRResult)
        assert r.image_dimensions == (100, 50)

    def test_file_not_found(self):
        eng = _engine()
        r = eng.recognize("/nonexistent/image.png")
        assert r.success is False

    def test_cleanup(self):
        eng = _engine()
        backend = eng._backend
        eng.cleanup()
        assert backend.cleaned
        assert eng._backend is None

    def test_context_manager(self):
        backend = MockBackend()
        with OCREngine(backend=backend) as eng:
            eng.initialize()
        assert backend.cleaned

    def test_uninitialized_raises(self):
        import pytest
        eng = OCREngine()
        with pytest.raises(RuntimeError):
            eng.run(Image.new("RGB", (10, 10)))

    def test_metadata(self):
        eng = _engine()
        r = eng.recognize(Image.new("RGB", (50, 50)))
        assert "processing_time" in r.metadata
        assert r.metadata["text_lines"] == 2
