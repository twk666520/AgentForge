"""Core translation engine."""

from __future__ import annotations

import time
from typing import Any

from agentforge_core.result import SkillResult
from agentforge_core.skill_base import SkillBase

from translate_skill.backends.base import BaseTranslateBackend
from translate_skill.backends.mock_backend import MockTranslateBackend
from translate_skill.models import Translation, TranslationResult


class TranslateEngine(SkillBase):
    """High-level translation engine."""

    @property
    def name(self) -> str:
        return "translate"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return "Multi-language translation with pluggable backends."

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        backend: BaseTranslateBackend | None = None,
    ) -> None:
        super().__init__()
        self._config: dict[str, Any] = config or {}
        self._backend: BaseTranslateBackend | None = backend

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        merged = dict(self._config)
        if config:
            merged.update(config)
        if self._backend is None:
            bn = merged.get("backend", "mock")
            if bn == "mock":
                self._backend = MockTranslateBackend()
            elif bn == "openai":
                from translate_skill.backends.openai_backend import (
                    OpenAITranslateBackend,
                )

                self._backend = OpenAITranslateBackend()
            else:
                raise ValueError(f"Unknown backend: {bn!r}")
        self._backend.initialize(merged)

    def translate(
        self,
        text: str,
        *,
        source: str = "auto",
        target: str = "en",
        **kwargs: Any,
    ) -> SkillResult:
        """Translate text. Returns SkillResult with TranslationResult data."""
        try:
            result = self.run(text, source=source, target=target, **kwargs)
            return SkillResult.ok(
                result,
                source_lang=result.source_lang,
                target_lang=result.target_lang,
                processing_time=result.processing_time,
            )
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def run(
        self,
        text: str,
        *,
        source: str = "auto",
        target: str = "en",
        **kwargs: Any,
    ) -> TranslationResult:
        """Translate and return domain object directly."""
        if self._backend is None:
            raise RuntimeError("Engine not initialized.")
        start = time.perf_counter()
        translated = self._backend.translate(text, source=source, target=target)
        elapsed = time.perf_counter() - start
        return TranslationResult(
            translations=[
                Translation(
                    text=translated,
                    source_lang=source,
                    target_lang=target,
                    confidence=1.0,
                ),
            ],
            source_text=text,
            source_lang=source,
            target_lang=target,
            processing_time=elapsed,
        )

    def translate_batch(
        self,
        texts: list[str],
        *,
        source: str = "auto",
        target: str = "en",
        **kwargs: Any,
    ) -> SkillResult:
        """Translate multiple texts. Returns SkillResult."""
        try:
            start = time.perf_counter()
            translations: list[Translation] = []
            for text in texts:
                t = self._backend.translate(text, source=source, target=target)
                translations.append(
                    Translation(
                        text=t,
                        source_lang=source,
                        target_lang=target,
                        confidence=1.0,
                    )
                )
            result = TranslationResult(
                translations=translations,
                source_text="\n".join(texts),
                source_lang=source,
                target_lang=target,
                processing_time=time.perf_counter() - start,
            )
            return SkillResult.ok(
                result,
                segments=len(texts),
            )
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def cleanup(self) -> None:
        if self._backend is not None:
            self._backend.cleanup()
            self._backend = None
