
"""Tests for Translation data models."""
from __future__ import annotations
from translate_skill.models import Translation, TranslationResult


class TestTranslation:
    def test_creation(self):
        t = Translation(text="你好", source_lang="zh", target_lang="en")
        assert t.text == "你好"
        assert t.source_lang == "zh" and t.target_lang == "en"
        assert t.confidence == 1.0

    def test_to_dict(self):
        t = Translation(text="hello", source_lang="en", target_lang="zh", confidence=0.95)
        d = t.to_dict()
        assert d["text"] == "hello"
        assert d["confidence"] == 0.95


class TestTranslationResult:
    def test_empty(self):
        r = TranslationResult()
        assert r.text == ""
        assert r.translations == []

    def test_text_property(self):
        r = TranslationResult(
            translations=[
                Translation("你好", "zh", "en"),
                Translation("世界", "zh", "en"),
            ],
        )
        assert r.text == "你好\n世界"

    def test_to_dict(self):
        r = TranslationResult(
            translations=[Translation("hello", "en", "zh")],
            source_text="你好",
            source_lang="zh",
            target_lang="en",
            processing_time=0.5,
        )
        d = r.to_dict()
        assert d["source_text"] == "你好"
        assert d["text"] == "hello"
        assert len(d["translations"]) == 1
