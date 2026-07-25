"""Mock desktop backend for testing."""

from __future__ import annotations

from typing import Any

from PIL import Image

from desktop_skill.backends.base import BaseDesktopBackend


class MockDesktopBackend(BaseDesktopBackend):
    """Returns mock desktop data. No GUI dependencies needed."""

    def __init__(self) -> None:
        self.initialized = False
        self.cleaned = False

    def initialize(self, config: dict[str, Any]) -> None:
        self.initialized = True

    def list_windows(self) -> list[dict[str, Any]]:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        return [
            {
                "title": "Chrome",
                "process_name": "chrome.exe",
                "left": 0,
                "top": 0,
                "width": 1920,
                "height": 1040,
            },
            {
                "title": "Code",
                "process_name": "Code.exe",
                "left": 0,
                "top": 0,
                "width": 1200,
                "height": 900,
            },
        ]

    def get_active_window(self) -> dict[str, Any]:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        return {
            "title": "Chrome",
            "process_name": "chrome.exe",
            "left": 0,
            "top": 0,
            "width": 1920,
            "height": 1040,
            "text_content": "Mock window content",
        }

    def capture_screen(self) -> Image.Image:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        return Image.new("RGB", (1920, 1080), color=(200, 200, 200))

    def get_window_text(self, title: str) -> str:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        return f"Mock text content for window: {title}"

    def cleanup(self) -> None:
        self.cleaned = True
