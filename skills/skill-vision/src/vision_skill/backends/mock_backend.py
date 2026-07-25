"""Mock vision backend for testing."""

from __future__ import annotations

from typing import Any

from PIL import Image

from vision_skill.backends.base import BaseVisionBackend


class MockVisionBackend(BaseVisionBackend):
    """Returns mock analysis. No external API needed."""

    def __init__(self) -> None:
        self.initialized = False
        self.cleaned = False

    def initialize(self, config: dict[str, Any]) -> None:
        self.initialized = True

    def analyze(
        self,
        image: Image.Image,
        task: str = "describe",
    ) -> dict[str, Any]:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        w, h = image.size
        return {
            "description": f"A {w}x{h} image with test content.",
            "objects": ["sample_object"],
            "text_detected": ["mock text 1", "mock text 2"],
            "labels": ["test_label"],
        }

    def cleanup(self) -> None:
        self.cleaned = True
