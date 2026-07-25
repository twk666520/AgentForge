"""Tests for the Desktop CLI."""
from __future__ import annotations


class TestCLIParser:
    def test_list_action(self):
        from desktop_skill.cli import build_parser
        args = build_parser().parse_args(["list"])
        assert args.action == "list"

    def test_active_action(self):
        from desktop_skill.cli import build_parser
        args = build_parser().parse_args(["active", "--format", "json"])
        assert args.action == "active"
        assert args.format == "json"

    def test_missing_action(self):
        import pytest
        from desktop_skill.cli import build_parser
        with pytest.raises(SystemExit):
            build_parser().parse_args([])


class TestCLIMain:
    def test_list_action(self):
        from desktop_skill.cli import main
        assert main(["list"]) == 0

    def test_active_json(self):
        from desktop_skill.cli import main
        assert main(["active", "--format", "json"]) == 0

    def test_capture_text(self):
        from desktop_skill.cli import main
        assert main(["capture"]) == 0

    def test_capture_json(self):
        from desktop_skill.cli import main
        assert main(["capture", "--format", "json"]) == 0