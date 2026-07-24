"""OpenAI-compatible translation backend."""

from __future__ import annotations

from typing import Any

from translate_skill.backends.base import BaseTranslateBackend

_LANG_PROMPTS = {
    "zh": "Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
}


class OpenAITranslateBackend(BaseTranslateBackend):
    """Uses OpenAI Chat Completions API for translation.

    Config:
        api_key: OpenAI API key (env: OPENAI_API_KEY).
        model: Model name (default: gpt-4o-mini).
        base_url: Custom API endpoint.
    """

    def __init__(self) -> None:
        self._client: Any = None
        self._model: str = "gpt-4o-mini"

    def initialize(self, config: dict[str, Any]) -> None:
        self._model = config.get("model", self._model)
        api_key = config.get("api_key")
        base_url = config.get("base_url")
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package required. pip install openai")
        kwargs: dict[str, Any] = {}
        if api_key:
            kwargs["api_key"] = api_key
        if base_url:
            kwargs["base_url"] = base_url
        self._client = OpenAI(**kwargs)

    def translate(
        self,
        text: str,
        *,
        source: str = "auto",
        target: str = "en",
    ) -> str:
        if self._client is None:
            raise RuntimeError("Backend not initialized.")
        target_name = _LANG_PROMPTS.get(target, target)
        src_hint = (
            f" from {_LANG_PROMPTS.get(source, source)}" if source != "auto" else ""
        )
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a translator. Translate the user text"
                        f"{src_hint} to {target_name}. "
                        f"Output ONLY the translation."
                    ),
                },
                {"role": "user", "content": text},
            ],
            temperature=0.0,
        )
        return resp.choices[0].message.content or ""

    def cleanup(self) -> None:
        self._client = None
        import gc

        gc.collect()
