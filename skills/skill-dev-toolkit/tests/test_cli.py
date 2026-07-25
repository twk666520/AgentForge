"""Tests for the Dev Toolkit CLI."""
from __future__ import annotations


class TestCLI:
    def test_list_tools(self):
        from dev_toolkit_skill.cli import main
        rc = main(["--list"])
        assert rc == 0

    def test_list_json(self):
        from dev_toolkit_skill.cli import main
        rc = main(["--list", "--format", "json"])
        assert rc == 0

    def test_run_tool(self):
        from dev_toolkit_skill.cli import main
        rc = main(["base64-encode", "--text=hello"])
        assert rc == 0

    def test_run_with_format(self):
        from dev_toolkit_skill.cli import main
        rc = main(["uuid", "--format", "json"])
        assert rc == 0