"""Translation data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Translation:
    """A single translated segment."""

    text: str
    source_lang: str
    target_lang: str
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "confidence": self.confidence,
        }


@dataclass
class TranslationResult:
    """Complete translation result."""

    translations: list[Translation] = field(default_factory=list)
    source_text: str = ""
    source_lang: str = "auto"
    target_lang: str = "en"
    processing_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        """Concatenated translated text."""
        return "\n".join(t.text for t in self.translations)

    def to_dict(self) -> dict[str, Any]:
        return {
            "translations": [t.to_dict() for t in self.translations],
            "text": self.text,
            "source_text": self.source_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "processing_time": self.processing_time,
            "metadata": self.metadata,
        }
