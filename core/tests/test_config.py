"""Tests for the configuration manager."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from agentforge_core.config import ConfigManager


class TestConfigManager:
    """Verify hierarchical config access, mutation, and file loading."""

    def test_empty_init(self) -> None:
        cfg = ConfigManager()
        assert cfg.to_dict() == {}

    def test_init_with_dict(self) -> None:
        cfg = ConfigManager({"key": "val"})
        assert cfg.get("key") == "val"

    def test_get_dotted_key(self) -> None:
        cfg = ConfigManager({"ocr": {"backend": "paddle"}})
        assert cfg.get("ocr.backend") == "paddle"

    def test_get_missing_returns_default(self) -> None:
        cfg = ConfigManager()
        assert cfg.get("missing", "fallback") == "fallback"
        assert cfg.get("nested.missing", None) is None

    def test_set_simple(self) -> None:
        cfg = ConfigManager()
        cfg.set("host", "localhost")
        assert cfg.get("host") == "localhost"

    def test_set_dotted_creates_nesting(self) -> None:
        cfg = ConfigManager()
        cfg.set("ocr.backend", "easyocr")
        assert cfg.get("ocr.backend") == "easyocr"

    def test_set_overwrites_existing(self) -> None:
        cfg = ConfigManager({"ocr": {"backend": "paddle"}})
        cfg.set("ocr.backend", "easyocr")
        assert cfg.get("ocr.backend") == "easyocr"

    def test_update_deep_merge(self) -> None:
        cfg = ConfigManager({"a": {"x": 1, "y": 2}})
        cfg.update({"a": {"y": 99, "z": 3}, "b": 4})
        assert cfg.get("a.x") == 1
        assert cfg.get("a.y") == 99
        assert cfg.get("a.z") == 3
        assert cfg.get("b") == 4

    def test_load_json(self) -> None:
        cfg = ConfigManager()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({"server": {"port": 8080}}, f)
            tmp = f.name
        try:
            cfg.load_file(tmp)
            assert cfg.get("server.port") == 8080
        finally:
            Path(tmp).unlink(missing_ok=True)

    def test_load_file_not_found(self) -> None:
        cfg = ConfigManager()
        with pytest.raises(FileNotFoundError):
            cfg.load_file("/nonexistent/config.yaml")

    def test_load_unsupported_format(self) -> None:
        cfg = ConfigManager()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False, encoding="utf-8"
        ) as f:
            f.write("[tool]\nkey = 1\n")
            tmp = f.name
        try:
            with pytest.raises(ValueError, match="Unsupported"):
                cfg.load_file(tmp)
        finally:
            Path(tmp).unlink(missing_ok=True)

    def test_repr(self) -> None:
        cfg = ConfigManager({"a": 1})
        rep = repr(cfg)
        assert "ConfigManager" in rep
        assert "a" in rep
