"""Basic vision example."""
from PIL import Image
from vision_skill import VisionEngine

engine = VisionEngine({"backend": "mock"})
engine.initialize()
img = Image.new("RGB", (200, 100))
result = engine.analyze(img, task="describe")
print(f"Analysis: {result.data.description}")
engine.cleanup()