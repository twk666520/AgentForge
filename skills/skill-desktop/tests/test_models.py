"""Tests for Desktop data models."""
from __future__ import annotations
from desktop_skill.models import WindowInfo, DesktopResult


class TestWindowInfo:
    def test_creation(self):
        w = WindowInfo(title="Chrome", process_name="chrome.exe",
                       left=0, top=0, width=1920, height=1040)
        assert w.title == "Chrome"
        assert w.width == 1920

    def test_to_dict(self):
        w = WindowInfo(title="Test", process_name="test.exe")
        d = w.to_dict()
        assert d["title"] == "Test"
        assert d["bounds"] == [0, 0, 0, 0]


class TestDesktopResult:
    def test_empty(self):
        r = DesktopResult()
        assert r.windows == []
        assert r.active_window is None

    def test_with_windows(self):
        w = WindowInfo(title="Code", width=1200, height=800)
        r = DesktopResult(windows=[w])
        assert len(r.windows) == 1
        assert r.windows[0].title == "Code"