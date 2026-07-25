"""Tests for DesktopEngine with mock backend."""
from __future__ import annotations
from desktop_skill.backends.mock_backend import MockDesktopBackend
from desktop_skill.engine import DesktopEngine


def _engine():
    eng = DesktopEngine(backend=MockDesktopBackend())
    eng.initialize()
    return eng


class TestDesktopEngine:
    def test_identity(self):
        eng = DesktopEngine()
        assert eng.name == "desktop"
        assert eng.version == "0.1.0"

    def test_list_windows(self):
        eng = _engine()
        r = eng.list_windows()
        assert r.success is True
        assert r.metadata["window_count"] == 2

    def test_get_active_window(self):
        eng = _engine()
        r = eng.get_active_window()
        assert r.success is True
        assert r.data.active_window.title == "Chrome"

    def test_capture_screen(self):
        eng = _engine()
        r = eng.capture_screen()
        assert r.success is True
        assert len(r.data) > 0

    def test_cleanup(self):
        eng = _engine()
        backend = eng._backend
        eng.cleanup()
        assert backend.cleaned

    def test_context_manager(self):
        backend = MockDesktopBackend()
        with DesktopEngine(backend=backend) as eng:
            eng.initialize()
        assert backend.cleaned

    def test_uninitialized_returns_fail(self):
        eng = DesktopEngine()
        r = eng.list_windows()
        assert r.success is False