"""Core GitHub analysis engine."""

from __future__ import annotations

import time
from typing import Any

from agentforge_core.result import SkillResult
from agentforge_core.skill_base import SkillBase

from github_skill.backends.base import BaseGitHubBackend
from github_skill.backends.mock_backend import MockGitHubBackend
from github_skill.models import GitHubAnalysis, RepoInfo


class GitHubEngine(SkillBase):
    """GitHub repository analysis engine."""

    @property
    def name(self) -> str:
        return "github"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return "GitHub repository analysis and documentation."

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        backend: BaseGitHubBackend | None = None,
    ) -> None:
        super().__init__()
        self._config: dict[str, Any] = config or {}
        self._backend: BaseGitHubBackend | None = backend

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        merged = dict(self._config)
        if config:
            merged.update(config)
        if self._backend is None:
            bn = merged.get("backend", "mock")
            if bn == "mock":
                self._backend = MockGitHubBackend()
            elif bn == "openai":
                from github_skill.backends.openai_backend import (
                    OpenAIGitHubBackend,
                )

                self._backend = OpenAIGitHubBackend()
            else:
                raise ValueError(f"Unknown backend: {bn!r}")
        self._backend.initialize(merged)

    def analyze(self, url: str) -> SkillResult:
        """Analyze a GitHub repository."""
        try:
            result = self.run(url)
            return SkillResult.ok(
                result,
                processing_time=result.processing_time,
            )
        except Exception as exc:
            return SkillResult.fail(str(exc))

    def run(self, url: str) -> GitHubAnalysis:
        """Analyze and return domain object."""
        if self._backend is None:
            raise RuntimeError("Engine not initialized.")
        start = time.perf_counter()
        raw = self._backend.analyze_repo(url)
        repo_name = url.rstrip("/").split("/")[-1] if "/" in url else url
        elapsed = time.perf_counter() - start
        return GitHubAnalysis(
            repo=RepoInfo(name=repo_name, url=url),
            summary=raw.get("summary", ""),
            tech_stack=raw.get("tech_stack", []),
            directory_structure=raw.get("directory_structure", ""),
            learning_path=raw.get("learning_path", ""),
            processing_time=elapsed,
        )

    def cleanup(self) -> None:
        if self._backend is not None:
            self._backend.cleanup()
            self._backend = None
