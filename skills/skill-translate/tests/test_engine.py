
"""Tests for TranslateEngine with mock backend."""
from __future__ import annotations
from agentforge_core.result import SkillResult
from translate_skill.backends.mock_backend import MockTranslateBackend
from translate_skill.engine import TranslateEngine
from translate_skill.models import TranslationResult


def _engine():
    eng = TranslateEngine(backend=MockTranslateBackend())
    eng.initialize()
    return eng


class TestTranslateEngine:
    def test_identity(self):
        eng = TranslateEngine()
        assert eng.name == "translate"
        assert eng.version == "0.1.0"

    def test_translate_success(self):
        eng = _engine()
        r = eng.translate("Hello", target="zh")
        assert isinstance(r, SkillResult)
        assert r.success is True

    def test_translate_returns_data(self):
        eng = _engine()
        r = eng.translate("Hello world", target="zh")
        data = r.data
        assert isinstance(data, TranslationResult)
        assert "[Chinese]" in data.text
        assert "Hello world" in data.text

    def test_run_returns_domain_object(self):
        eng = _engine()
        r = eng.run("Hello", target="zh")
        assert isinstance(r, TranslationResult)
        assert r.target_lang == "zh"

    def test_translate_batch(self):
        eng = _engine()
        r = eng.translate_batch(["Hello", "World"], target="zh")
        assert r.success is True
        assert r.metadata.get("segments") == 2
        assert len(r.data.translations) == 2

    def test_different_languages(self):
        eng = _engine()
        r = eng.translate("Hello", target="ja")
        assert "[Japanese]" in r.data.text

    def test_cleanup(self):
        eng = _engine()
        backend = eng._backend
        eng.cleanup()
        assert eng._backend is None
        assert backend.cleaned

    def test_context_manager(self):
        backend = MockTranslateBackend()
        with TranslateEngine(backend=backend) as eng:
            eng.initialize()
        assert backend.cleaned

    def test_uninitialized_raises(self):
        import pytest
        eng = TranslateEngine()
        with pytest.raises(RuntimeError):
            eng.run("Hello", target="zh")

    def test_metadata_in_result(self):
        eng = _engine()
        r = eng.translate("Hello", target="zh")
        assert "processing_time" in r.metadata
        assert r.metadata["source_lang"] == "auto"
