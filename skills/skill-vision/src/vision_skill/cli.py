"""Command-line interface for the Vision skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vision_skill.engine import VisionEngine


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agentforge-vision",
        description="Analyze images using AI vision.",
    )
    p.add_argument("image", type=str, help="Path to the image file.")
    p.add_argument(
        "--task",
        default="describe",
        choices=["describe", "extract_text", "analyze_ui", "identify"],
        help="Analysis task (default: describe).",
    )
    p.add_argument(
        "--backend",
        default="mock",
        choices=["mock", "openai"],
        help="Vision backend (default: mock).",
    )
    p.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ipath = Path(args.image)
    if not ipath.exists():
        print(f"Error: file not found: {ipath}", file=sys.stderr)
        return 1
    engine = VisionEngine({"backend": args.backend})
    try:
        engine.initialize()
        result = engine.analyze(str(ipath), task=args.task)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        engine.cleanup()
    if not result:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1
    data = result.data
    if args.format == "json":
        print(json.dumps(data.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"=== Analysis ({args.task}) ===")
        print(data.description)
        if data.objects:
            print(f"\nObjects: {', '.join(data.objects)}")
        if data.labels:
            print(f"Labels: {', '.join(data.labels)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
