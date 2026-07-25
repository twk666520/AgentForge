# Translate Skill

Multi-language translation.

## CLI Usage
```bash
python -m translate_skill.cli "Hello world" --target zh
python -m translate_skill.cli --file input.txt --target ja --backend openai
```

## Python SDK
```python
from translate_skill import TranslateEngine
engine = TranslateEngine({"backend": "mock"})
engine.initialize()
r = engine.translate("Hello", target="zh")
print(r.data.text)
engine.cleanup()
```

## Backends
- **mock** — No dependencies, for testing
- **openai** — Real translation (pip install openai)