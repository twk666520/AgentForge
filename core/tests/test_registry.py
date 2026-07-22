"""Tests for the skill registry."""

from __future__ import annotations

import pytest

from agentforge_core.registry import SkillRegistry, SkillInfo
from agentforge_core.skill_base import SkillBase


class SkillA(SkillBase):
    @property
    def name(self) -> str:
        return "skill_a"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "First test skill"


class SkillB(SkillBase):
    @property
    def name(self) -> str:
        return "skill_b"

    @property
    def version(self) -> str:
        return "2.0.0"

    @property
    def description(self) -> str:
        return "Second test skill"


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    SkillRegistry.reset_for_testing()
    yield
    SkillRegistry.reset_for_testing()


class TestSkillRegistry:
    """Verify registration, lookup, and discovery."""

    def test_register_and_get(self) -> None:
        SkillRegistry.register(SkillA)
        cls = SkillRegistry.get("skill_a")
        assert cls is SkillA

    def test_get_unknown_raises_key_error(self) -> None:
        with pytest.raises(KeyError, match="not found"):
            SkillRegistry.get("nonexistent")

    def test_register_duplicate_raises_value_error(self) -> None:
        SkillRegistry.register(SkillA)
        with pytest.raises(ValueError, match="already registered"):
            SkillRegistry.register(SkillA)

    def test_list_skills_empty(self) -> None:
        assert SkillRegistry.list_skills() == []

    def test_list_skills(self) -> None:
        SkillRegistry.register(SkillA)
        SkillRegistry.register(SkillB)
        infos = SkillRegistry.list_skills()
        assert len(infos) == 2
        names = {i.name for i in infos}
        assert names == {"skill_a", "skill_b"}
        versions = {i.name: i.version for i in infos}
        assert versions["skill_a"] == "1.0.0"
        assert versions["skill_b"] == "2.0.0"

    def test_skill_info_dataclass(self) -> None:
        info = SkillInfo(
            name="test",
            version="0.1.0",
            description="testing",
            module_path="tests.test_registry",
            class_name="SkillA",
        )
        assert info.name == "test"
        assert info.version == "0.1.0"

    def test_register_as_decorator(self) -> None:
        @SkillRegistry.register
        class DecoratedSkill(SkillBase):
            @property
            def name(self) -> str:
                return "decorated"

            @property
            def version(self) -> str:
                return "0.1.0"

        cls = SkillRegistry.get("decorated")
        assert cls is DecoratedSkill

    def test_discover_no_skills(self) -> None:
        skills = SkillRegistry.discover("__nonexistent_prefix__")
        assert skills == []
