"""Tests for GitHubEngine with mock backend."""
from __future__ import annotations
from github_skill.backends.mock_backend import MockGitHubBackend
from github_skill.engine import GitHubEngine
from github_skill.models import GitHubAnalysis


def _engine():
    eng = GitHubEngine(backend=MockGitHubBackend())
    eng.initialize()
    return eng


class TestGitHubEngine:
    def test_identity(self):
        eng = GitHubEngine()
        assert eng.name == "github"
        assert eng.version == "0.1.0"

    def test_analyze_success(self):
        eng = _engine()
        r = eng.analyze("https://github.com/user/repo")
        assert r.success is True

    def test_analyze_returns_data(self):
        eng = _engine()
        r = eng.analyze("https://github.com/user/awesome-project")
        data = r.data
        assert isinstance(data, GitHubAnalysis)
        assert "awesome-project" in data.summary

    def test_run_returns_domain_object(self):
        eng = _engine()
        r = eng.run("https://github.com/user/repo")
        assert isinstance(r, GitHubAnalysis)

    def test_mock_has_tech_stack(self):
        eng = _engine()
        r = eng.analyze("https://github.com/user/repo")
        assert len(r.data.tech_stack) > 0

    def test_cleanup(self):
        eng = _engine()
        backend = eng._backend
        eng.cleanup()
        assert backend.cleaned

    def test_context_manager(self):
        backend = MockGitHubBackend()
        with GitHubEngine(backend=backend) as eng:
            eng.initialize()
        assert backend.cleaned

    def test_uninitialized_returns_fail(self):
        eng = GitHubEngine()
        r = eng.analyze("https://github.com/user/repo")
        assert r.success is False