"""Windows native desktop backend (optional)."""

from __future__ import annotations

import importlib
from typing import Any

from PIL import Image

from desktop_skill.backends.base import BaseDesktopBackend

_HAS_WIN_DEPS = importlib.util.find_spec("pygetwindow") is not None
if _HAS_WIN_DEPS:
    import pygetwindow as gw


class WindowsDesktopBackend(BaseDesktopBackend):
    """Native Windows desktop backend using pygetwindow.
    Requires: pip install pygetwindow pyautogui pywinauto
    """

    def __init__(self) -> None:
        self.initialized = False

    def initialize(self, config: dict[str, Any]) -> None:
        if not _HAS_WIN_DEPS:
            raise ImportError("Requires: pip install pygetwindow pyautogui")
        self.initialized = True

    def list_windows(self) -> list[dict[str, Any]]:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        if not _HAS_WIN_DEPS:
            return []
        windows = gw.getAllWindows()
        result = []
        for w in windows:
            if w.title and w.visible:
                result.append(
                    {
                        "title": w.title,
                        "process_name": "",
                        "left": w.left,
                        "top": w.top,
                        "width": w.width,
                        "height": w.height,
                    }
                )
        return result

    def get_active_window(self) -> dict[str, Any]:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        w = gw.getActiveWindow() if _HAS_WIN_DEPS else None
        if w is None:
            return {
                "title": "",
                "process_name": "",
                "left": 0,
                "top": 0,
                "width": 0,
                "height": 0,
            }
        return {
            "title": w.title,
            "process_name": "",
            "left": w.left,
            "top": w.top,
            "width": w.width,
            "height": w.height,
        }

    def capture_screen(self) -> Image.Image:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        import pyautogui

        return pyautogui.screenshot()

    def get_window_text(self, title: str) -> str:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        try:
            import pywinauto

            app = pywinauto.Application().connect(title=title)
            return app.window(title=title).window_text()
        except ImportError:
            return f"(pywinauto required: {title})"
        except Exception:
            return f"(could not read: {title})"

    def cleanup(self) -> None:
        self.initialized = False
