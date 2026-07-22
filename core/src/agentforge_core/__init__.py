"""AgentForge Core - Base interfaces and framework for the Skills system."""

from agentforge_core.config import ConfigManager
from agentforge_core.loader import SkillLoader
from agentforge_core.registry import SkillInfo, SkillRegistry
from agentforge_core.result import SkillResult
from agentforge_core.skill_base import SkillBase

__all__ = [
    "SkillBase",
    "SkillRegistry",
    "SkillInfo",
    "ConfigManager",
    "SkillResult",
    "SkillLoader",
]

__version__ = "0.1.0"
