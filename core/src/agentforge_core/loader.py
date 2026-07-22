"""Dynamic skill loader — instantiate skills by name."""

from __future__ import annotations

from typing import Any

from agentforge_core.config import ConfigManager
from agentforge_core.registry import SkillRegistry
from agentforge_core.skill_base import SkillBase


class SkillLoader:
    """Loads and instantiates skills, optionally wiring in configuration."""

    def __init__(self, config: ConfigManager | None = None) -> None:
        self._config = config or ConfigManager()

    def load(self, name: str, **overrides: Any) -> SkillBase:
        """Instantiate a registered skill by name.

        Args:
            name: Skill name as registered.
            **overrides: Per-call configuration overrides merged on top of
                         any config from ``ConfigManager``.

        Returns:
            An initialized ``SkillBase`` instance.
        """
        skill_cls = SkillRegistry.get(name)
        skill = skill_cls()

        # Merge: global config -> skill-specific config -> overrides
        merged: dict[str, Any] = dict(self._config.get(name, {}))
        merged.update(overrides)

        skill.initialize(merged)
        return skill

    def load_all(self) -> list[SkillBase]:
        """Load and initialize every registered skill."""
        instances: list[SkillBase] = []
        for skill_cls in SkillRegistry.list_skills():
            name = skill_cls.name
            try:
                instances.append(self.load(name))
            except Exception:
                continue
        return instances
