"""OpenAI Vision backend."""

from __future__ import annotations

import base64
import io
from typing import Any

from PIL import Image

from vision_skill.backends.base import BaseVisionBackend


class OpenAIVisionBackend(BaseVisionBackend):
    """Uses GPT-4o for image analysis.

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
            raise ImportError("openai required: pip install openai")
        kwargs: dict[str, Any] = {}
        if api_key:
            kwargs["api_key"] = api_key
        if base_url:
            kwargs["base_url"] = base_url
        self._client = OpenAI(**kwargs)

    def _encode_image(self, image: Image.Image) -> str:
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def analyze(
        self,
        image: Image.Image,
        task: str = "describe",
    ) -> dict[str, Any]:
        if self._client is None:
            raise RuntimeError("Backend not initialized.")

        prompts = {
            "describe": (
                "Describe this image in detail. "
                "List visible objects and scene elements."
            ),
            "extract_text": (
                "Extract all visible text from this image. List each text string found."
            ),
            "analyze_ui": (
                "Analyze this UI screenshot. Describe the layout, "
                "buttons, inputs, and navigation elements."
            ),
            "identify": (
                "Identify the main objects and content in this image. "
                "List labels with confidence levels."
            ),
        }
        prompt = prompts.get(task, prompts["describe"])

        b64 = self._encode_image(image)
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64}",
                            },
                        },
                    ],
                },
            ],
            temperature=0.0,
        )
        content = resp.choices[0].message.content or ""

        return {
            "description": content,
            "objects": [],
            "text_detected": [],
            "labels": [],
        }

    def cleanup(self) -> None:
        self._client = None
        import gc

        gc.collect()
