
"""Tests for the Translate CLI."""
from __future__ import annotations


class TestCLIParser:
    def test_basic_parsing(self):
        from translate_skill.cli import build_parser
        args = build_parser().parse_args(["Hello", "--target", "zh"])
        assert args.text == "Hello"
        assert args.target == "zh"

    def test_file_option(self):
        from translate_skill.cli import build_parser
        args = build_parser().parse_args(["--file", "input.txt"])
        assert args.file == "input.txt"
        assert args.text is None

    def test_all_options(self):
        from translate_skill.cli import build_parser
        args = build_parser().parse_args([
            "Hello", "--source", "en", "--target", "ja",
            "--backend", "mock", "--format", "json",
        ])
        assert args.source == "en"
        assert args.target == "ja"
        assert args.format == "json"

    def test_empty_args_returns_none(self):
        from translate_skill.cli import build_parser
        args = build_parser().parse_args([])
        assert args.text is None
        assert args.file is None


class TestCLIMain:
    def test_success_text(self):
        from translate_skill.cli import main
        rc = main(["Hello", "--target", "zh"])
        assert rc == 0

    def test_json_output(self):
        from translate_skill.cli import main
        rc = main(["Hello", "--target", "zh", "--format", "json"])
        assert rc == 0

    def test_no_text_or_file(self):
        from translate_skill.cli import main
        rc = main([])
        assert rc == 1

    def test_file_not_found(self):
        from translate_skill.cli import main
        rc = main(["--file", "/nonexistent/file.txt"])
        assert rc == 1
