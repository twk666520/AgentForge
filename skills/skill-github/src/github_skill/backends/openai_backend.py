"""OpenAI GitHub analysis backend."""

from __future__ import annotations

from typing import Any

from github_skill.backends.base import BaseGitHubBackend


class OpenAIGitHubBackend(BaseGitHubBackend):
    """Uses GPT-4o for repo analysis.

    Config:
        api_key: OpenAI API key (env: OPENAI_API_KEY).
        model: Model name (default: gpt-4o-mini).
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

    def analyze_repo(self, url: str) -> dict[str, Any]:
        if self._client is None:
            raise RuntimeError("Backend not initialized.")
        prompt = (
            f"Analyze this GitHub repository: {url}\n\n"
            "Provide output in this exact format:\n"
            "SUMMARY: <2-3 sentence summary>\n"
            "TECH_STACK: <comma-separated list of technologies>\n"
            "STRUCTURE: <directory structure overview>\n"
            "LEARNING_PATH: <step-by-step learning path>"
        )
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = resp.choices[0].message.content or ""

        summary = ""
        tech_stack = []
        structure = ""
        learning_path = ""
        for line in content.split("\n"):
            if line.startswith("SUMMARY:"):
                summary = line.replace("SUMMARY:", "").strip()
            elif line.startswith("TECH_STACK:"):
                tech_stack = [
                    t.strip() for t in line.replace("TECH_STACK:", "").split(",")
                ]
            elif line.startswith("STRUCTURE:"):
                structure = line.replace("STRUCTURE:", "").strip()
            elif line.startswith("LEARNING_PATH:"):
                learning_path = line.replace("LEARNING_PATH:", "").strip()

        return {
            "summary": summary,
            "tech_stack": tech_stack,
            "directory_structure": structure,
            "learning_path": learning_path,
        }

    def cleanup(self) -> None:
        self._client = None
        import gc

        gc.collect()
