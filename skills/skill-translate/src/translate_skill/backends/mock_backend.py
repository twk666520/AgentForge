"""Mock translation backend for testing."""

from __future__ import annotations

from typing import Any

from translate_skill.backends.base import BaseTranslateBackend

_LANG_NAMES = {
    "en": "English",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
}


class MockTranslateBackend(BaseTranslateBackend):
    """Returns mock translations. No external API needed."""

    def __init__(self) -> None:
        self.initialized = False
        self.cleaned = False

    def initialize(self, config: dict[str, Any]) -> None:
        self.initialized = True

    def translate(
        self,
        text: str,
        *,
        source: str = "auto",
        target: str = "en",
    ) -> str:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        target_name = _LANG_NAMES.get(target, target)
        return f"[{target_name}] {text}"

    def cleanup(self) -> None:
        self.cleaned = True
