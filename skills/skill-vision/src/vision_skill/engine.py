"""Core vision engine."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from agentforge_core.result import SkillResult
from agentforge_core.skill_base import SkillBase
from PIL import Image

from vision_skill.backends.base import BaseVisionBackend
from vision_skill.backends.mock_backend import MockVisionBackend
from vision_skill.models import ImageAnalysis
from vision_skill.utils import load_image


class VisionEngine(SkillBase):
    """High-level vision analysis engine."""

    @property
    def name(self) -> str:
        return "vision"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return "Image analysis and screen understanding."

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        backend: BaseVisionBackend | None = None,
    ) -> None:
        super().__init__()
        self._config: dict[str, Any] = config or {}
        self._backend: BaseVisionBackend | None = backend

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        merged = dict(self._config)
        if config:
            merged.update(config)
        if self._backend is None:
            bn = merged.get("backend", "mock")
            if bn == "mock":
                self._backend = MockVisionBackend()
            elif bn == "openai":
                from vision_skill.backends.openai_backend import OpenAIVisionBackend

                self._backend = OpenAIVisionBackend()
            else:
                raise ValueError(f"Unknown backend: {bn!r}")
        self._backend.initialize(merged)

    def analyze(
        self,
        image: str | Path | bytes | Image.Image,
        task: str = "describe",
    ) -> SkillResult:
        """Analyze an image. Returns SkillResult with ImageAnalysis."""
        try:
            result = self.run(image, task=task)
            return SkillResult.ok(
                result, task=task, processing_time=result.processing_time
            )
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def run(
        self,
        image: str | Path | bytes | Image.Image,
        task: str = "describe",
    ) -> ImageAnalysis:
        """Analyze and return domain object directly."""
        if self._backend is None:
            raise RuntimeError("Engine not initialized.")
        pil_img = load_image(image)
        start = time.perf_counter()
        raw = self._backend.analyze(pil_img, task=task)
        elapsed = time.perf_counter() - start
        return ImageAnalysis(
            description=raw.get("description", ""),
            objects=raw.get("objects", []),
            text_detected=raw.get("text_detected", []),
            labels=raw.get("labels", []),
            image_dimensions=pil_img.size,
            processing_time=elapsed,
        )

    def cleanup(self) -> None:
        if self._backend is not None:
            self._backend.cleanup()
            self._backend = None
