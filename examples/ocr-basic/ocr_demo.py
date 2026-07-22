
"""Basic OCR example.

Usage:
    python examples/ocr-basic/ocr_demo.py <image_path>
"""
from __future__ import annotations
import sys
from pathlib import Path
from ocr_skill import OCREngine


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <image_path>", file=sys.stderr)
        return 1
    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"Error: file not found: {image_path}", file=sys.stderr)
        return 1
    engine = OCREngine({"langs": ["en", "ch_sim"]})
    engine.initialize()
    try:
        result = engine.recognize(str(image_path))
    finally:
        engine.cleanup()
    if not result:
        print(f"OCR failed: {result.error}", file=sys.stderr)
        return 1
    ocr = result.data
    print(f"--- OCR Result ---")
    print(f"Lines: {len(ocr.lines)}")
    print(f"Time:  {ocr.processing_time:.2f}s")
    print(f"Confidence: {ocr.confidence_mean:.2%}")
    print()
    print(ocr.raw_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
