"""Tests for skill_base module."""

from __future__ import annotations

from typing import Any

import pytest

from agentforge_core.skill_base import SkillBase
from agentforge_core.registry import SkillRegistry


class DummySkill(SkillBase):
    """Minimal concrete skill for testing."""

    @property
    def name(self) -> str:
        return "dummy"

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return "A dummy skill for testing"

    def __init__(self) -> None:
        super().__init__()
        self.initialized = False
        self.cleaned_up = False
        self.config: dict[str, Any] = {}

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        self.initialized = True
        self.config = config or {}

    def cleanup(self) -> None:
        self.cleaned_up = True


class TestSkillBase:
    """Verify the abstract base class contract."""

    def test_cannot_instantiate_abstract(self) -> None:
        with pytest.raises(TypeError):
            SkillBase()  # type: ignore[abstract]

    def test_concrete_skill_properties(self) -> None:
        skill = DummySkill()
        assert skill.name == "dummy"
        assert skill.version == "0.1.0"
        assert skill.description == "A dummy skill for testing"

    def test_lifecycle_initialize(self) -> None:
        skill = DummySkill()
        assert not skill.initialized
        skill.initialize({"threshold": 0.5})
        assert skill.initialized
        assert skill.config == {"threshold": 0.5}

    def test_lifecycle_cleanup(self) -> None:
        skill = DummySkill()
        skill.initialize()
        skill.cleanup()
        assert skill.cleaned_up

    def test_context_manager(self) -> None:
        with DummySkill() as skill:
            skill.initialize()
            assert not skill.cleaned_up
        assert skill.cleaned_up

    def test_repr(self) -> None:
        skill = DummySkill()
        rep = repr(skill)
        assert "DummySkill" in rep
        assert "dummy" in rep
        assert "0.1.0" in rep

    def test_registration_and_lifecycle(self) -> None:
        SkillRegistry.reset_for_testing()
        SkillRegistry.register(DummySkill)
        cls = SkillRegistry.get("dummy")
        skill = cls()
        skill.initialize({"key": "val"})
        assert skill.initialized
        assert skill.config == {"key": "val"}
        SkillRegistry.reset_for_testing()
