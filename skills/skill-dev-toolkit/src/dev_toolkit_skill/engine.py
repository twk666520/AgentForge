"""Dev Toolkit engine - wraps tools in SkillBase."""

from __future__ import annotations

from typing import Any

from agentforge_core.result import SkillResult
from agentforge_core.skill_base import SkillBase

from dev_toolkit_skill.models import ToolResult
from dev_toolkit_skill.tools import list_tools, run_tool


class DevToolkitEngine(SkillBase):
    """Developer utility tools engine."""

    @property
    def name(self) -> str:
        return "dev-toolkit"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return (
            "Developer utility tools (JSON, Base64, JWT, UUID, Hash, Regex, Markdown)."
        )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__()
        self._config: dict[str, Any] = config or {}

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        merged = dict(self._config)
        if config:
            merged.update(config)
        self._config = merged

    def list_tools(self) -> SkillResult:
        """List all available tools."""
        return SkillResult.ok(list_tools(), count=len(_get_tools()))

    def run(self, tool_name: str, **kwargs: Any) -> SkillResult:
        """Run a tool by name with parameters."""
        result = run_tool(tool_name, **kwargs)
        if result["success"]:
            return SkillResult.ok(
                ToolResult(
                    tool=tool_name,
                    success=True,
                    output=result.get("output", ""),
                    metadata=result.get("metadata", {}),
                ),
            )
        return SkillResult.fail(result.get("output", "Unknown error"))

    def cleanup(self) -> None:
        pass


def _get_tools() -> list[dict[str, Any]]:
    return list_tools()
