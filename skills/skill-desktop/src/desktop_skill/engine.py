"""Core desktop engine."""

from __future__ import annotations

import time
from typing import Any

from agentforge_core.result import SkillResult
from agentforge_core.skill_base import SkillBase

from desktop_skill.backends.base import BaseDesktopBackend
from desktop_skill.backends.mock_backend import MockDesktopBackend
from desktop_skill.models import DesktopResult, WindowInfo


class DesktopEngine(SkillBase):
    """Desktop automation engine."""

    @property
    def name(self) -> str:
        return "desktop"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return "Desktop window capture and automation."

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        backend: BaseDesktopBackend | None = None,
    ) -> None:
        super().__init__()
        self._config: dict[str, Any] = config or {}
        self._backend: BaseDesktopBackend | None = backend

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        merged = dict(self._config)
        if config:
            merged.update(config)
        if self._backend is None:
            bn = merged.get("backend", "mock")
            if bn == "mock":
                self._backend = MockDesktopBackend()
            elif bn == "windows":
                from desktop_skill.backends.windows_backend import (
                    WindowsDesktopBackend,
                )

                self._backend = WindowsDesktopBackend()
            else:
                raise ValueError(f"Unknown backend: {bn!r}")
        self._backend.initialize(merged)

    def list_windows(self) -> SkillResult:
        """List all visible windows."""
        try:
            result = self._run_list_windows()
            return SkillResult.ok(result, window_count=len(result.windows))
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def _run_list_windows(self) -> DesktopResult:
        if self._backend is None:
            raise RuntimeError("Engine not initialized.")
        start = time.perf_counter()
        raw = self._backend.list_windows()
        windows = [WindowInfo(**w) for w in raw]
        return DesktopResult(
            windows=windows,
            processing_time=time.perf_counter() - start,
        )

    def get_active_window(self) -> SkillResult:
        """Get the currently active window."""
        try:
            if self._backend is None:
                raise RuntimeError("Engine not initialized.")
            start = time.perf_counter()
            raw = self._backend.get_active_window()
            win = WindowInfo(
                title=raw.get("title", ""),
                process_name=raw.get("process_name", ""),
                left=raw.get("left", 0),
                top=raw.get("top", 0),
                width=raw.get("width", 0),
                height=raw.get("height", 0),
                text_content=raw.get("text_content", ""),
            )
            result = DesktopResult(
                active_window=win,
                processing_time=time.perf_counter() - start,
            )
            return SkillResult.ok(result)
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def capture_screen(self) -> SkillResult:
        """Capture the full screen (returns bytes)."""
        try:
            if self._backend is None:
                raise RuntimeError("Engine not initialized.")
            start = time.perf_counter()
            img = self._backend.capture_screen()
            import io

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            elapsed = time.perf_counter() - start
            return SkillResult.ok(
                buf.getvalue(),
                width=img.width,
                height=img.height,
                processing_time=elapsed,
            )
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def cleanup(self) -> None:
        if self._backend is not None:
            self._backend.cleanup()
            self._backend = None
