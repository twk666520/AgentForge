"""Basic desktop example."""
from desktop_skill import DesktopEngine

engine = DesktopEngine({"backend": "mock"})
engine.initialize()
result = engine.list_windows()
print(f"Windows found: {result.metadata['window_count']}")
for w in result.data.windows:
    print(f"  - {w.title} ({w.width}x{w.height})")
engine.cleanup()