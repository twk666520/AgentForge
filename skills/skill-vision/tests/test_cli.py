"""Tests for the Vision CLI."""
from __future__ import annotations
from PIL import Image


class TestCLIParser:
    def test_basic_parsing(self):
        from vision_skill.cli import build_parser
        args = build_parser().parse_args(["test.png"])
        assert args.image == "test.png"
        assert args.task == "describe"

    def test_all_options(self):
        from vision_skill.cli import build_parser
        args = build_parser().parse_args(["test.png", "--task", "analyze_ui", "--format", "json"])
        assert args.task == "analyze_ui"
        assert args.format == "json"

    def test_missing_image(self):
        import pytest
        from vision_skill.cli import build_parser
        with pytest.raises(SystemExit):
            build_parser().parse_args([])


class TestCLIMain:
    def test_file_not_found(self):
        from vision_skill.cli import main
        assert main(["/nonexistent/image.png"]) == 1

    def test_text_output(self, tmp_path):
        fp = tmp_path / "test.png"
        Image.new("RGB", (50, 20)).save(fp)
        from vision_skill.cli import main
        assert main([str(fp)]) == 0

    def test_json_output(self, tmp_path):
        fp = tmp_path / "test.png"
        Image.new("RGB", (50, 20)).save(fp)
        from vision_skill.cli import main
        assert main([str(fp), "--format", "json"]) == 0