"""EasyOCR backend implementation."""

from __future__ import annotations

from typing import Any

from PIL import Image

from ocr_skill.backends.base import BaseOCRBackend


class EasyOCRBackend(BaseOCRBackend):
    """OCR backend powered by EasyOCR."""

    def __init__(self) -> None:
        self._reader: Any = None
        self._langs: list[str] = ["en"]
        self._gpu: bool = False

    def initialize(self, config: dict[str, Any]) -> None:
        self._langs = config.get("langs", self._langs)
        self._gpu = config.get("gpu", self._gpu)
        try:
            import easyocr
        except ImportError:
            raise ImportError("EasyOCR is required. Install with: pip install easyocr")
        self._reader = easyocr.Reader(self._langs, gpu=self._gpu)

    def recognize(self, image: Image.Image, **kwargs: Any) -> list[dict[str, Any]]:
        if self._reader is None:
            raise RuntimeError("Backend not initialized.")
        import numpy as np

        arr = np.array(image.convert("RGB"))
        raw = self._reader.readtext(arr)
        results = []
        for pts, text, conf in raw:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            results.append(
                {
                    "text": text,
                    "confidence": float(conf),
                    "bbox": [
                        float(min(xs)),
                        float(min(ys)),
                        float(max(xs)),
                        float(max(ys)),
                    ],
                }
            )
        return results

    def cleanup(self) -> None:
        self._reader = None
        import gc

        gc.collect()
