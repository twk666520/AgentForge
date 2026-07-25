"""Integration: OCR -> Translate pipeline."""
from PIL import Image, ImageDraw
from ocr_skill import OCREngine
from ocr_skill.backends.base import BaseOCRBackend
from translate_skill import TranslateEngine


class MockOCRBackend(BaseOCRBackend):
    """Simple mock OCR for the integration demo."""
    def initialize(self, config): pass
    def recognize(self, image, **kwargs):
        return [{"text": "Hello World", "confidence": 0.95, "bbox": [10, 20, 200, 50]}]
    def cleanup(self): pass


def main():
    print("=" * 50)
    print("AgentForge Integration Demo")
    print("OCR -> Translate Pipeline")
    print("=" * 50)
    print("\n[1/3] Creating test image...")
    Image.new("RGB", (400, 80), (255, 255, 255))

    print("[2/3] Running OCR...")
    ocr = OCREngine(backend=MockOCRBackend())
    ocr.initialize()
    result = ocr.recognize(Image.new("RGB", (400, 80), (255, 255, 255)))
    text = result.data.raw_text
    print(f"  Detected: {text!r}")
    ocr.cleanup()

    print("[3/3] Translating...")
    tl = TranslateEngine({"backend": "mock"})
    tl.initialize()
    translated = tl.translate(text, target="zh")
    print(f"  Translation: {translated.data.text}")
    tl.cleanup()

    print("\nPipeline complete!")


if __name__ == "__main__":
    main()