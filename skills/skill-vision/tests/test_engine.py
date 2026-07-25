"""Tests for VisionEngine with mock backend."""
from __future__ import annotations
from PIL import Image
from agentforge_core.result import SkillResult
from vision_skill.backends.mock_backend import MockVisionBackend
from vision_skill.engine import VisionEngine
from vision_skill.models import ImageAnalysis


def _engine():
    eng = VisionEngine(backend=MockVisionBackend())
    eng.initialize()
    return eng


class TestVisionEngine:
    def test_identity(self):
        eng = VisionEngine()
        assert eng.name == "vision"
        assert eng.version == "0.1.0"

    def test_analyze_success(self):
        eng = _engine()
        r = eng.analyze(Image.new("RGB", (100, 50)))
        assert isinstance(r, SkillResult)
        assert r.success is True

    def test_analyze_returns_data(self):
        eng = _engine()
        r = eng.analyze(Image.new("RGB", (100, 50)))
        data = r.data
        assert isinstance(data, ImageAnalysis)
        assert "100x50" in data.description

    def test_run_returns_domain_object(self):
        eng = _engine()
        r = eng.run(Image.new("RGB", (200, 100)))
        assert isinstance(r, ImageAnalysis)
        assert r.image_dimensions == (200, 100)

    def test_different_tasks(self):
        eng = _engine()
        for task in ["describe", "extract_text", "analyze_ui", "identify"]:
            r = eng.analyze(Image.new("RGB", (50, 50)), task=task)
            assert r.success is True

    def test_analyze_from_bytes(self):
        eng = _engine()
        import io
        buf = io.BytesIO()
        Image.new("RGB", (30, 20)).save(buf, format="PNG")
        r = eng.analyze(buf.getvalue())
        assert r.success is True

    def test_cleanup(self):
        eng = _engine()
        backend = eng._backend
        eng.cleanup()
        assert backend.cleaned

    def test_context_manager(self):
        backend = MockVisionBackend()
        with VisionEngine(backend=backend) as eng:
            eng.initialize()
        assert backend.cleaned

    def test_uninitialized_raises(self):
        import pytest
        eng = VisionEngine()
        with pytest.raises(RuntimeError):
            eng.run(Image.new("RGB", (10, 10)))