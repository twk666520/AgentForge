"""Command-line interface for the GitHub skill."""

from __future__ import annotations

import argparse
import json
import sys

from github_skill.engine import GitHubEngine


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agentforge-github",
        description="Analyze GitHub repositories.",
    )
    p.add_argument("url", type=str, help="GitHub repository URL.")
    p.add_argument(
        "--backend",
        default="mock",
        choices=["mock", "openai"],
        help="Backend (default: mock).",
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
    engine = GitHubEngine({"backend": args.backend})
    try:
        engine.initialize()
        result = engine.analyze(args.url)
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
        print(f"Repository: {data.repo.name}")
        print(f"Summary: {data.summary}")
        if data.tech_stack:
            print(f"Tech Stack: {', '.join(data.tech_stack)}")
        if data.directory_structure:
            print(f"\nDirectory:\n{data.directory_structure}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
