"""Command-line interface for the Translate skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from translate_skill.engine import TranslateEngine


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agentforge-translate",
        description="Translate text between languages.",
    )
    p.add_argument(
        "text",
        nargs="?",
        type=str,
        help="Text to translate.",
    )
    p.add_argument(
        "--source",
        default="auto",
        help="Source language (ISO 639-1) or auto.",
    )
    p.add_argument(
        "--target",
        default="zh",
        help="Target language (ISO 639-1, default: zh).",
    )
    p.add_argument(
        "--file",
        type=str,
        help="Translate contents of a file.",
    )
    p.add_argument(
        "--backend",
        default="mock",
        choices=["mock", "openai"],
        help="Translation backend (default: mock).",
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

    # Get input text
    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            return 1
        input_text = path.read_text(encoding="utf-8").strip()
    elif args.text:
        input_text = args.text
    else:
        print("Error: provide text or --file", file=sys.stderr)
        return 1

    engine = TranslateEngine(
        {
            "backend": args.backend,
        }
    )
    try:
        engine.initialize()
        result = engine.translate(
            input_text,
            source=args.source,
            target=args.target,
        )
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
        print(result.data.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
