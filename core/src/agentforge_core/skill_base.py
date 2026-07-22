"""Abstract base class for all AgentForge skills."""

from abc import ABC, abstractmethod
from typing import Any


class SkillBase(ABC):
    """Base class that every AgentForge skill must implement.

    Provides the contract between the skill system and individual skill
    implementations. Each skill is expected to:

    - Declare its identity (name, version, description)
    - Support initialize/cleanup lifecycle
    - Accept a typed configuration object
    """

    # --- Identity (class-level overrides) ---

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique skill name, e.g. ``ocr``, ``translate``."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Semantic version string for this skill."""
        ...

    @property
    def description(self) -> str:
        """Human-readable description of what this skill does."""
        return ""

    # --- Lifecycle ---

    def initialize(self, config: dict[str, Any] | None = None) -> None:
        """Prepare the skill for use.

        Called once before any work method is invoked. Subclasses should
        override this to set up resources (model loading, API clients, etc.).

        Args:
            config: Optional configuration dictionary provided by the caller
                    or loaded from a config file.
        """

    def cleanup(self) -> None:
        """Release resources held by the skill.

        Called once when the skill is no longer needed.  Subclasses that
        allocate resources (open file handles, model sessions, thread pools)
        must override this method.
        """

    # --- Context manager support ---

    def __enter__(self) -> "SkillBase":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        self.cleanup()

    # --- Metadata ---

    def __repr__(self) -> str:
        return f"<{type(self).__name__} name={self.name!r} version={self.version!r}>"
