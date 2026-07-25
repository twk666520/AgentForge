"""Tests for GitHub data models."""
from __future__ import annotations
from github_skill.models import RepoInfo, GitHubAnalysis


class TestRepoInfo:
    def test_creation(self):
        r = RepoInfo(name="test-repo", stars=100, language="Python")
        assert r.name == "test-repo"
        assert r.stars == 100

    def test_to_dict(self):
        r = RepoInfo(name="test", stars=50, topics=["ai", "python"])
        d = r.to_dict()
        assert d["name"] == "test"
        assert d["topics"] == ["ai", "python"]


class TestGitHubAnalysis:
    def test_full(self):
        repo = RepoInfo(name="agentforge", stars=500)
        a = GitHubAnalysis(
            repo=repo, summary="Great project",
            tech_stack=["Python"], processing_time=1.5,
        )
        assert a.summary == "Great project"
        assert a.repo.name == "agentforge"

    def test_to_dict(self):
        a = GitHubAnalysis(
            repo=RepoInfo(name="test"),
            summary="summary", tech_stack=["Go"],
        )
        d = a.to_dict()
        assert d["summary"] == "summary"
        assert d["repo"]["name"] == "test"