"""Tests for the dynamic skill loader."""

from __future__ import annotations

from typing import Any

import pytest

from agentforge_core.config import ConfigManager
from agentforge_core.loader import SkillLoader
from agentforge_core.registry import SkillRegistry
from agentforge_core.skill_base import SkillBase


class ConfigurableSkill(SkillBase):
    @property
    def name(self) -> str:
        return "configurable"

    @property
    def version(self) -> str:
        return "0.1.0"

    def __init__(self) -> None:
        super().__init__()
        self.config: dict[str, Any] = {}

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    def cleanup(self) -> None:
        pass


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    SkillRegistry.reset_for_testing()
    SkillRegistry.register(ConfigurableSkill)
    yield
    SkillRegistry.reset_for_testing()


class TestSkillLoader:
    """Verify loading, config merging, and bulk loading."""

    def test_load_instantiates_skill(self) -> None:
        loader = SkillLoader()
        skill = loader.load("configurable")
        assert isinstance(skill, ConfigurableSkill)

    def test_load_with_overrides(self) -> None:
        loader = SkillLoader()
        skill = loader.load("configurable", threshold=0.8)
        assert skill.config["threshold"] == 0.8

    def test_load_merges_global_config_and_overrides(self) -> None:
        cfg = ConfigManager({"configurable": {"backend": "test", "threshold": 0.5}})
        loader = SkillLoader(config=cfg)
        skill = loader.load("configurable", threshold=0.9)
        assert skill.config["backend"] == "test"
        assert skill.config["threshold"] == 0.9

    def test_load_unknown_skill_raises_key_error(self) -> None:
        loader = SkillLoader()
        with pytest.raises(KeyError):
            loader.load("nonexistent")

    def test_load_all(self) -> None:
        loader = SkillLoader()
        skills = loader.load_all()
        assert len(skills) == 1
        assert isinstance(skills[0], ConfigurableSkill)

    def test_load_all_empty_registry(self) -> None:
        SkillRegistry.reset_for_testing()
        loader = SkillLoader()
        assert loader.load_all() == []
