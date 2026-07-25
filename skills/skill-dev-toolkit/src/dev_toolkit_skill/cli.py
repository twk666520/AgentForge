"""CLI for Dev Toolkit."""

from __future__ import annotations

import argparse
import json
import sys

from dev_toolkit_skill.engine import DevToolkitEngine
from dev_toolkit_skill.tools import list_tools


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agentforge-dev-toolkit",
        description="Developer utility tools.",
    )
    p.add_argument("tool", nargs="?", help="Tool name.")
    p.add_argument("--list", action="store_true", help="List tools.")
    p.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format."
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, unknown = parser.parse_known_args(argv)

    if args.list or not args.tool:
        tools = list_tools()
        if args.format == "json":
            print(json.dumps(tools, indent=2, ensure_ascii=False))
        else:
            print("Available tools:")
            for t in tools:
                print(f"  {t['name']:20s} {t['description']}")
        return 0

    tool_name = args.tool
    tool_args = _parse_tool_args(unknown)

    engine = DevToolkitEngine()
    engine.initialize()
    result = engine.run(tool_name, **tool_args)
    if not result:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1
    data = result.data
    if args.format == "json":
        print(json.dumps(data.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(data.output)
    return 0


def _parse_tool_args(argv: list[str]) -> dict:
    kwargs: dict[str, str] = {}
    for arg in argv:
        if arg.startswith("--") and "=" in arg:
            key = arg[2:].split("=")[0]
            value = arg[2:].split("=", 1)[1]
            kwargs[key] = value
    return kwargs


if __name__ == "__main__":
    sys.exit(main())
