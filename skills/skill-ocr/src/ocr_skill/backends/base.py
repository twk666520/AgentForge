"""Abstract base class for OCR backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from PIL import Image


class BaseOCRBackend(ABC):
    """Interface that every OCR backend must implement."""

    @abstractmethod
    def initialize(self, config: dict[str, Any]) -> None:
        """Prepare the backend for recognition (load models, etc.).

        Args:
            config: Backend-specific configuration dictionary.
        """

    @abstractmethod
    def recognize(self, image: Image.Image, **kwargs: Any) -> list[dict[str, Any]]:
        """Run OCR on a PIL Image.

        Args:
            image: The input image to process.
            **kwargs: Per-call options (e.g. language list).

        Returns:
            A list of dicts with keys ``text``, ``confidence``, and
            ``bbox`` (a list of 4 corner points *or* [x1, y1, x2, y2]).
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Release any resources held by the backend."""

    @property
    def name(self) -> str:
        """Human-readable backend identifier."""
        return type(self).__name__

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"
