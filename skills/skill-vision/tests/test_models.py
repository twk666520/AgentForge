"""Tests for Vision data models."""
from __future__ import annotations
from vision_skill.models import ImageAnalysis


class TestImageAnalysis:
    def test_empty_creation(self):
        ia = ImageAnalysis()
        assert ia.description == ""
        assert ia.objects == []

    def test_full_creation(self):
        ia = ImageAnalysis(
            description="A cat sitting on a chair",
            objects=["cat", "chair"],
            labels=["animal", "furniture"],
            image_dimensions=(800, 600),
            processing_time=1.5,
        )
        assert ia.description == "A cat sitting on a chair"
        assert ia.image_dimensions == (800, 600)

    def test_to_dict(self):
        ia = ImageAnalysis(description="test", image_dimensions=(100, 50), processing_time=0.5)
        d = ia.to_dict()
        assert d["description"] == "test"
        assert d["image_dimensions"] == [100, 50]