"""Abstract base class for GitHub backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseGitHubBackend(ABC):
    """Interface every GitHub backend must implement."""

    @abstractmethod
    def initialize(self, config: dict[str, Any]) -> None:
        """Prepare the backend."""

    @abstractmethod
    def analyze_repo(self, url: str) -> dict[str, Any]:
        """Analyze a GitHub repository.
        Returns dict with: summary, tech_stack, directory_structure, learning_path.
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Release resources."""
