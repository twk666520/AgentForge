"""Tests for the GitHub CLI."""
from __future__ import annotations


class TestCLIParser:
    def test_basic_parsing(self):
        from github_skill.cli import build_parser
        args = build_parser().parse_args(["https://github.com/user/repo"])
        assert args.url == "https://github.com/user/repo"
        assert args.backend == "mock"

    def test_all_options(self):
        from github_skill.cli import build_parser
        args = build_parser().parse_args([
            "https://github.com/user/repo", "--backend", "openai",
            "--format", "json",
        ])
        assert args.backend == "openai"
        assert args.format == "json"

    def test_missing_url(self):
        import pytest
        from github_skill.cli import build_parser
        with pytest.raises(SystemExit):
            build_parser().parse_args([])


class TestCLIMain:
    def test_success_text(self):
        from github_skill.cli import main
        rc = main(["https://github.com/user/repo"])
        assert rc == 0

    def test_json_output(self):
        from github_skill.cli import main
        rc = main(["https://github.com/user/repo", "--format", "json"])
        assert rc == 0