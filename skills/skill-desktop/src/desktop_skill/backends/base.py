"""Abstract base class for desktop backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from PIL import Image


class BaseDesktopBackend(ABC):
    """Interface every desktop backend must implement."""

    @abstractmethod
    def initialize(self, config: dict[str, Any]) -> None:
        """Prepare the backend."""

    @abstractmethod
    def list_windows(self) -> list[dict[str, Any]]:
        """List all visible windows.
        Returns list of dicts with: title, process_name, left, top, width, height.
        """

    @abstractmethod
    def get_active_window(self) -> dict[str, Any]:
        """Get the currently active window.
        Returns dict with: title, process_name, left, top, width, height, text_content.
        """

    @abstractmethod
    def capture_screen(self) -> Image.Image:
        """Capture the entire screen. Returns PIL Image."""

    @abstractmethod
    def get_window_text(self, title: str) -> str:
        """Extract text content from a window by title."""

    @abstractmethod
    def cleanup(self) -> None:
        """Release resources."""
