"""Core OCR engine -- main entry point for text recognition."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from agentforge_core.result import SkillResult
from agentforge_core.skill_base import SkillBase
from PIL import Image

from ocr_skill.backends.base import BaseOCRBackend
from ocr_skill.backends.easyocr_backend import EasyOCRBackend
from ocr_skill.models import BBox, OCRResult, TextLine
from ocr_skill.preprocess import load_image, standard_pipeline


class OCREngine(SkillBase):
    """High-level OCR engine.

    Coordinates image preprocessing and backend recognition.
    """

    @property
    def name(self) -> str:
        return "ocr"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return "Text recognition with EasyOCR backend."

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        backend: BaseOCRBackend | None = None,
    ) -> None:
        super().__init__()
        self._config: dict[str, Any] = config or {}
        self._backend: BaseOCRBackend | None = backend
        self._preprocess_config: dict[str, Any] = {}

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        merged = dict(self._config)
        if config:
            merged.update(config)
        self._preprocess_config = merged.get("preprocess", {})
        if self._backend is None:
            bn = merged.get("backend", "easyocr")
            if bn == "easyocr":
                self._backend = EasyOCRBackend()
            else:
                raise ValueError(f"Unknown OCR backend: {bn!r}")
        self._backend.initialize(
            {
                "langs": merged.get("langs", ["en"]),
                "gpu": merged.get("gpu", False),
            }
        )

    def recognize(
        self,
        image: str | Path | bytes | Image.Image,
        **kwargs: Any,
    ) -> SkillResult:
        """Run OCR and return a standard SkillResult."""
        try:
            result = self.run(image, **kwargs)
            return SkillResult.ok(
                result,
                processing_time=result.processing_time,
                text_lines=len(result.lines),
            )
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def run(
        self,
        image: str | Path | bytes | Image.Image,
        **kwargs: Any,
    ) -> OCRResult:
        """Run OCR and return the domain result object."""
        start = time.perf_counter()
        img = load_image(image)
        osize = img.size
        pp = standard_pipeline(img, **self._preprocess_config)
        if self._backend is None:
            raise RuntimeError("Engine not initialized.")
        raw = self._backend.recognize(pp, **kwargs)
        lines = [
            TextLine(
                text=item["text"],
                bbox=BBox.from_list(item["bbox"]),
                confidence=item["confidence"],
            )
            for item in raw
        ]
        return OCRResult(
            lines=lines,
            image_dimensions=osize,
            processing_time=time.perf_counter() - start,
        )

    def cleanup(self) -> None:
        if self._backend is not None:
            self._backend.cleanup()
            self._backend = None
