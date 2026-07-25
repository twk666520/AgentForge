"""Basic translation example."""
from translate_skill import TranslateEngine

engine = TranslateEngine({"backend": "mock"})
engine.initialize()
result = engine.translate("Hello world", target="zh")
print(f"Input:  {result.data.source_text}")
print(f"Output: {result.data.text}")
engine.cleanup()