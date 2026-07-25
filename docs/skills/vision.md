
# Vision Skill

Analyze images using AI vision.

## CLI Usage
```bash
python -m vision_skill.cli photo.png --task describe
python -m vision_skill.cli photo.png --task extract_text --format json
```

## Python SDK
```python
from vision_skill import VisionEngine
engine = VisionEngine({"backend": "mock"})
engine.initialize()
result = engine.analyze("photo.png", task="describe")
print(result.data.description)
engine.cleanup()
```

## Tasks
- `describe` — General image description
- `extract_text` — Extract visible text
- `analyze_ui` — Analyze UI layout
- `identify` — Identify main objects

## Backends
- **mock** — No dependencies, for testing
- **openai** — GPT-4o vision (pip install openai)
