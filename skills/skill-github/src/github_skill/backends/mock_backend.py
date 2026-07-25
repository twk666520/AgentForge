"""Mock GitHub backend for testing."""

from __future__ import annotations

from typing import Any

from github_skill.backends.base import BaseGitHubBackend


class MockGitHubBackend(BaseGitHubBackend):
    """Returns mock analysis results."""

    def __init__(self) -> None:
        self.initialized = False
        self.cleaned = False

    def initialize(self, config: dict[str, Any]) -> None:
        self.initialized = True

    def analyze_repo(self, url: str) -> dict[str, Any]:
        if not self.initialized:
            raise RuntimeError("Backend not initialized.")
        repo_name = url.rstrip("/").split("/")[-1] if "/" in url else url
        return {
            "summary": f"{repo_name} is a mock repository for testing.",
            "tech_stack": ["Python", "TypeScript"],
            "directory_structure": "src/\ntests/\nREADME.md",
            "learning_path": "1. Read the README\n2. Run tests\n3. Explore src/",
        }

    def cleanup(self) -> None:
        self.cleaned = True
