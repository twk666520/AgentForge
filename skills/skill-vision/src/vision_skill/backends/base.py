"""Abstract base class for vision backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from PIL import Image


class BaseVisionBackend(ABC):
    """Interface every vision backend must implement."""

    @abstractmethod
    def initialize(self, config: dict[str, Any]) -> None:
        """Prepare the backend."""

    @abstractmethod
    def analyze(
        self,
        image: Image.Image,
        task: str = "describe",
    ) -> dict[str, Any]:
        """Analyze an image.
        Args:
            image: PIL Image to analyze.
            task: Analysis task type.
                - describe: General image description
                - extract_text: Extract visible text
                - analyze_ui: Analyze UI layout
                - identify: Identify objects
        Returns:
            Dict with keys: description, objects, text_detected, labels.
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Release resources."""

    @property
    def name(self) -> str:
        return type(self).__name__
