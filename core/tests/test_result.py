"""Tests for the unified result model."""

from __future__ import annotations

from agentforge_core.result import SkillResult


class TestSkillResult:
    """Verify factory methods, truthiness, and repr."""

    def test_ok_factory(self) -> None:
        result = SkillResult.ok(["line1", "line2"], duration=0.5)
        assert result.success is True
        assert result.data == ["line1", "line2"]
        assert result.error is None
        assert result.metadata == {"duration": 0.5}

    def test_fail_factory(self) -> None:
        result = SkillResult.fail("engine crashed")
        assert result.success is False
        assert result.data is None
        assert result.error == "engine crashed"

    def test_fail_factory_with_data(self) -> None:
        result = SkillResult.fail("partial failure", data={"detected": 3})
        assert result.success is False
        assert result.data == {"detected": 3}
        assert result.error == "partial failure"

    def test_truthy_on_success(self) -> None:
        assert bool(SkillResult.ok("data")) is True
        assert bool(SkillResult.fail("error")) is False

    def test_repr_success(self) -> None:
        result = SkillResult.ok("hello")
        assert "OK" in repr(result)
        assert "hello" in repr(result)

    def test_repr_failure(self) -> None:
        result = SkillResult.fail("error message")
        assert "FAIL" in repr(result)
        assert "error message" in repr(result)

    def test_default_metadata_is_empty_dict(self) -> None:
        result = SkillResult.ok("data")
        assert result.metadata == {}

    def test_default_fields(self) -> None:
        result = SkillResult(success=True)
        assert result.data is None
        assert result.error is None
        assert result.metadata == {}
