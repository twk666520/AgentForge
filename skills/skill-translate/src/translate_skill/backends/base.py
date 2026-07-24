"""Abstract base class for translation backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTranslateBackend(ABC):
    """Interface every translation backend must implement."""

    @abstractmethod
    def initialize(self, config: dict[str, Any]) -> None:
        """Prepare the backend for translation."""

    @abstractmethod
    def translate(
        self,
        text: str,
        *,
        source: str = "auto",
        target: str = "en",
    ) -> str:
        """Translate a single text string.

        Args:
            text: Text to translate.
            source: Source language code or "auto".
            target: Target language code (ISO 639-1).

        Returns:
            Translated text string.
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Release resources."""

    @property
    def name(self) -> str:
        return type(self).__name__
