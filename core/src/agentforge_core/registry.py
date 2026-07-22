"""Skill registry — discover, register, and query available skills."""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentforge_core.skill_base import SkillBase


@dataclass
class SkillInfo:
    """Metadata about a registered skill class."""

    name: str
    version: str
    description: str
    module_path: str
    class_name: str


_SKILL_REGISTRY: dict[str, type[SkillBase]] = {}


class SkillRegistry:
    """Global registry for skill discovery and lookups.

    Skills can be registered explicitly or discovered automatically via
    Python package scanning.
    """

    @staticmethod
    def register(skill_cls: type[SkillBase]) -> type[SkillBase]:
        """Register a skill class by its ``name`` property.

        Args:
            skill_cls: A concrete ``SkillBase`` subclass.

        Returns:
            The same class, so this can be used as a decorator.

        Raises:
            ValueError: If a skill with the same name is already registered.
        """
        instance = skill_cls()
        name = instance.name
        if name in _SKILL_REGISTRY:
            raise ValueError(f"Skill {name!r} is already registered")
        _SKILL_REGISTRY[name] = skill_cls
        return skill_cls

    @staticmethod
    def get(name: str) -> type[SkillBase]:
        """Look up a registered skill class by name.

        Args:
            name: The skill name (e.g. ``"ocr"``).

        Returns:
            The registered skill class.

        Raises:
            KeyError: If no skill with that name is registered.
        """
        if name not in _SKILL_REGISTRY:
            msg = f"Skill {name!r} not found. Available: {list(_SKILL_REGISTRY)}"
            raise KeyError(msg)
        return _SKILL_REGISTRY[name]

    @staticmethod
    def list_skills() -> list[SkillInfo]:
        """Return metadata for all registered skills."""
        infos: list[SkillInfo] = []
        for name, cls in _SKILL_REGISTRY.items():
            instance = cls()
            infos.append(
                SkillInfo(
                    name=name,
                    version=instance.version,
                    description=instance.description,
                    module_path=f"{cls.__module__}",
                    class_name=f"{cls.__qualname__}",
                )
            )
        return infos

    @staticmethod
    def clear() -> None:
        """Clear all registered skills (useful in tests)."""
        _SKILL_REGISTRY.clear()

    @staticmethod
    def discover(
        package_prefix: str = "agentforge_skill",
    ) -> list[type[SkillBase]]:
        """Scan installed packages for skill classes.

        Searches for Python packages whose name starts with
        ``package_prefix``, import them, then any module that defines a
        concrete ``SkillBase`` subclass is automatically registered.

        Args:
            package_prefix: Only packages starting with this prefix are scanned.

        Returns:
            A list of registered skill classes.
        """
        for mod_info in pkgutil.iter_modules():
            if not mod_info.name.startswith(package_prefix):
                continue
            try:
                importlib.import_module(mod_info.name)
            except ModuleNotFoundError:
                continue
        return list(_SKILL_REGISTRY.values())

    @staticmethod
    def reset_for_testing() -> None:
        """Reset the registry to its initial empty state.

        Intended for test isolation. Not exposed in ``__all__``.
        """
        _SKILL_REGISTRY.clear()
