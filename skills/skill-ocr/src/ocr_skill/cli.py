"""Command-line interface for the OCR skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ocr_skill.engine import OCREngine


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    p = argparse.ArgumentParser(
        prog="agentforge-ocr",
        description="OCR text recognition from images.",
    )
    p.add_argument(
        "image",
        type=str,
        help="Path to the input image file.",
    )
    p.add_argument(
        "--backend",
        default="easyocr",
        choices=["easyocr"],
        help="OCR backend (default: easyocr).",
    )
    p.add_argument(
        "--langs",
        default="en",
        help="Comma-separated language codes (default: en).",
    )
    p.add_argument(
        "--gpu",
        action="store_true",
        help="Use GPU acceleration.",
    )
    p.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    p.add_argument(
        "--preprocess",
        action="store_true",
        help="Apply image preprocessing.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns exit code."""
    args = build_parser().parse_args(argv)
    ipath = Path(args.image)
    if not ipath.exists():
        print(f"Error: file not found: {ipath}", file=sys.stderr)
        return 1

    langs = [lang.strip() for lang in args.langs.split(",")]
    cfg: dict = {
        "backend": args.backend,
        "langs": langs,
        "gpu": args.gpu,
    }
    if args.preprocess:
        cfg["preprocess"] = {}

    engine = OCREngine(cfg)
    try:
        engine.initialize()
        result = engine.recognize(str(ipath))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        engine.cleanup()

    if not result:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(
            json.dumps(
                result.data.to_dict(),
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(result.data.raw_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
