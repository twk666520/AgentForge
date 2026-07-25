"""Vision data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ImageAnalysis:
    """Result of analyzing an image."""

    description: str = ""
    objects: list[str] = field(default_factory=list)
    text_detected: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    image_dimensions: tuple[int, int] = (0, 0)
    processing_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "description": self.description,
            "objects": self.objects,
            "text_detected": self.text_detected,
            "labels": self.labels,
            "image_dimensions": list(self.image_dimensions),
            "processing_time": self.processing_time,
            "metadata": self.metadata,
        }
