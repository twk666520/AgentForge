"""GitHub data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RepoInfo:
    """Information about a GitHub repository."""

    name: str
    description: str = ""
    stars: int = 0
    forks: int = 0
    language: str = ""
    topics: list[str] = field(default_factory=list)
    url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "stars": self.stars,
            "forks": self.forks,
            "language": self.language,
            "topics": self.topics,
            "url": self.url,
        }


@dataclass
class GitHubAnalysis:
    """Complete analysis of a GitHub repository."""

    repo: RepoInfo = field(default_factory=RepoInfo)
    summary: str = ""
    tech_stack: list[str] = field(default_factory=list)
    directory_structure: str = ""
    learning_path: str = ""
    processing_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "repo": self.repo.to_dict(),
            "summary": self.summary,
            "tech_stack": self.tech_stack,
            "directory_structure": self.directory_structure,
            "learning_path": self.learning_path,
            "processing_time": self.processing_time,
        }
