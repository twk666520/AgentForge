"""AgentForge Plugin - Unified access to all skills.

Usage:
    from agentforge_plugin import OCREngine, TranslateEngine
"""
from ocr_skill import OCREngine
from translate_skill import TranslateEngine
from vision_skill import VisionEngine
from desktop_skill import DesktopEngine
from github_skill import GitHubEngine
from dev_toolkit_skill import DevToolkitEngine

__all__ = [
    "OCREngine", "TranslateEngine", "VisionEngine",
    "DesktopEngine", "GitHubEngine", "DevToolkitEngine",
]
__version__ = "0.1.0"