"""OCR skill data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BBox:
    """Bounding box of detected text.

    Coordinates are in the original image pixel space.
    """

    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def area(self) -> float:
        return self.width * self.height

    def to_dict(self) -> dict[str, float]:
        return {"x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2}

    @classmethod
    def from_list(cls, coords: list[float]) -> BBox:
        """Create from a 4-element list [x1, y1, x2, y2]."""
        if len(coords) != 4:
            raise ValueError(f"Expected 4 coordinates, got {len(coords)}")
        return cls(x1=coords[0], y1=coords[1], x2=coords[2], y2=coords[3])


@dataclass
class TextLine:
    """A single line of detected text."""

    text: str
    bbox: BBox
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "bbox": self.bbox.to_dict(),
            "confidence": self.confidence,
        }


@dataclass
class OCRResult:
    """Complete OCR recognition result."""

    lines: list[TextLine] = field(default_factory=list)
    image_dimensions: tuple[int, int] = (0, 0)
    processing_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def raw_text(self) -> str:
        """Concatenate all detected text lines."""
        return "\n".join(line.text for line in self.lines)

    @property
    def confidence_mean(self) -> float:
        """Average confidence across all detected lines."""
        if not self.lines:
            return 0.0
        return sum(line.confidence for line in self.lines) / len(self.lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lines": [line.to_dict() for line in self.lines],
            "raw_text": self.raw_text,
            "image_dimensions": list(self.image_dimensions),
            "processing_time": self.processing_time,
            "confidence_mean": self.confidence_mean,
            "metadata": self.metadata,
        }
