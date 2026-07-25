"""Desktop data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WindowInfo:
    """Information about a desktop window."""

    title: str
    process_name: str = ""
    left: int = 0
    top: int = 0
    width: int = 0
    height: int = 0
    text_content: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "process_name": self.process_name,
            "bounds": [self.left, self.top, self.width, self.height],
        }


@dataclass
class DesktopResult:
    """Result from a desktop operation."""

    windows: list[WindowInfo] = field(default_factory=list)
    active_window: WindowInfo | None = None
    processing_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "windows": [w.to_dict() for w in self.windows],
            "active_window": self.active_window.to_dict()
            if self.active_window
            else None,
            "processing_time": self.processing_time,
            "metadata": self.metadata,
        }
