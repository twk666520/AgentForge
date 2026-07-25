"""Tests for DevToolkitEngine."""
from __future__ import annotations
from dev_toolkit_skill.engine import DevToolkitEngine


class TestDevToolkitEngine:
    def test_identity(self):
        eng = DevToolkitEngine()
        assert eng.name == "dev-toolkit"
        assert eng.version == "0.1.0"

    def test_list_tools(self):
        eng = DevToolkitEngine()
        eng.initialize()
        r = eng.list_tools()
        assert r.success is True
        assert r.metadata["count"] > 0

    def test_run_valid_tool(self):
        eng = DevToolkitEngine()
        eng.initialize()
        r = eng.run("base64-encode", text="hello")
        assert r.success is True
        assert r.data.output
        assert r.data.tool == "base64-encode"

    def test_run_invalid_tool(self):
        eng = DevToolkitEngine()
        eng.initialize()
        r = eng.run("nonexistent")
        assert r.success is False

    def test_run_json_format(self):
        eng = DevToolkitEngine()
        eng.initialize()
        r = eng.run("json-format", text='{"a":1}')
        assert r.success is True