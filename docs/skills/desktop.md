
# Desktop Skill

Desktop window operations and screen capture.

## CLI Usage
```bash
python -m desktop_skill.cli list
python -m desktop_skill.cli active --format json
```

## Python SDK
```python
from desktop_skill import DesktopEngine
engine = DesktopEngine({"backend": "mock"})
engine.initialize()
r = engine.list_windows()
print(f"Windows: {r.metadata['window_count']}")
engine.cleanup()
```

## Actions
- `list` — List all visible windows
- `active` — Get active window info
- `capture` — Full screen capture

## Backends
- **mock** — No dependencies, for testing
- **windows** — Native Windows (pygetwindow + pyautogui)
