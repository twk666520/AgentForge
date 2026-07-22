
"""Tests for the OCR CLI."""
from __future__ import annotations
from pathlib import Path
from unittest.mock import MagicMock, patch
from PIL import Image


class TestCLIParser:
    def test_basic_parsing(self):
        from ocr_skill.cli import build_parser
        args = build_parser().parse_args(["test.png"])
        assert args.image == "test.png"
        assert args.backend == "easyocr"
        assert args.format == "text"

    def test_all_options(self):
        from ocr_skill.cli import build_parser
        args = build_parser().parse_args([
            "test.png", "--backend", "easyocr",
            "--langs", "en+ch_sim", "--gpu",
            "--format", "json", "--preprocess",
        ])
        assert args.langs == "en+ch_sim"
        assert args.gpu is True
        assert args.format == "json"

    def test_missing_image(self):
        import pytest
        from ocr_skill.cli import build_parser
        with pytest.raises(SystemExit):
            build_parser().parse_args([])


class TestCLIMain:
    @patch("ocr_skill.engine.EasyOCRBackend")
    def test_success_text(self, mock_backend_cls, tmp_path):
        fp = tmp_path / "test.png"
        Image.new("RGB", (50, 20)).save(fp)
        mock_backend = MagicMock()
        mock_backend_cls.return_value = mock_backend
        mock_backend.recognize.return_value = [
            {"text": "OCR", "confidence": 0.9, "bbox": [0, 0, 10, 10]},
        ]
        from ocr_skill.cli import main
        assert main([str(fp)]) == 0

    def test_file_not_found(self):
        from ocr_skill.cli import main
        assert main(["/nonexistent/image.png"]) == 1

    @patch("ocr_skill.engine.EasyOCRBackend")
    def test_engine_error(self, mock_backend_cls, tmp_path):
        fp = tmp_path / "test.png"
        Image.new("RGB", (50, 20)).save(fp)
        mock_backend = MagicMock()
        mock_backend_cls.return_value = mock_backend
        mock_backend.initialize.side_effect = RuntimeError("fail")
        from ocr_skill.cli import main
        assert main([str(fp)]) == 1
