"""Command-line interface for the Desktop skill."""

from __future__ import annotations

import argparse
import json
import sys

from desktop_skill.engine import DesktopEngine


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agentforge-desktop",
        description="Desktop window operations.",
    )
    p.add_argument(
        "action",
        choices=["list", "active", "capture"],
        help="Action to perform.",
    )
    p.add_argument(
        "--backend",
        default="mock",
        choices=["mock", "windows"],
        help="Desktop backend (default: mock).",
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
    engine = DesktopEngine({"backend": args.backend})
    try:
        engine.initialize()
        if args.action == "list":
            result = engine.list_windows()
        elif args.action == "active":
            result = engine.get_active_window()
        elif args.action == "capture":
            result = engine.capture_screen()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        engine.cleanup()
    if not result:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1
    if args.format == "json":
        if args.action == "capture":
            print(
                json.dumps(
                    {"screenshot_size": len(result.data)},
                    indent=2,
                )
            )
        else:
            print(
                json.dumps(
                    result.data.to_dict(),
                    indent=2,
                    ensure_ascii=False,
                )
            )
    else:
        print(result.data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
