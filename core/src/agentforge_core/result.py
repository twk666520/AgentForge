"""Unified result model for all AgentForge skill operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillResult:
    """Standardised result returned by every skill operation.

    Attributes:
        success: Whether the operation completed without error.
        data: The primary payload produced by the skill.
        error: A human-readable error message (None when ``success`` is True).
        metadata: Optional key-value pairs describing the result context
                  (e.g. processing time, input dimensions, confidence scores).
    """

    success: bool
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: Any = None, **metadata: Any) -> SkillResult:
        """Create a successful result."""
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def fail(cls, error: str, data: Any = None, **metadata: Any) -> SkillResult:
        """Create a failed result."""
        return cls(success=False, data=data, error=error, metadata=metadata)

    def __bool__(self) -> bool:
        """A result is truthy when ``success`` is ``True``."""
        return self.success

    def __repr__(self) -> str:
        status = "OK" if self.success else "FAIL"
        summary = self.data if self.data is not None else self.error
        return f"<SkillResult {status}: {summary!r}>"
