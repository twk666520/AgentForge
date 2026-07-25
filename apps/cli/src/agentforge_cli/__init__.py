"""AgentForge CLI — discover and dispatch to installed skills."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

__all__ = ["main"]


def _find_skills_dir() -> Path | None:
    """Locate the ``skills/`` directory relative to this project."""
    here = Path(__file__).resolve().parent
    for parent in [here, *here.parents]:
        candidate = parent / "skills"
        if candidate.is_dir():
            return candidate
    return None


def _discover_skills() -> dict[str, object]:
    """Find skills via entry points, falling back to filesystem scan."""
    # Method 1: entry points (installed packages)
    try:
        from importlib.metadata import entry_points

        eps = entry_points(group="agentforge.skills")
        if eps:
            skills: dict[str, object] = {}
            for ep in eps:
                try:
                    skills[ep.name] = ep.load()
                except Exception:
                    continue
            if skills:
                return skills
    except Exception:
        pass

    # Method 2: filesystem scan (development mode)
    skills_dir = _find_skills_dir()
    if skills_dir is None:
        return {}

    skills: dict[str, object] = {}
    for pkg_dir in skills_dir.iterdir():
        if not pkg_dir.is_dir() or not pkg_dir.name.startswith("skill-"):
            continue
        skill_name = pkg_dir.name.removeprefix("skill-")
        src_dir = pkg_dir / "src"
        if not src_dir.is_dir():
            continue
        sys.path.insert(0, str(src_dir))
        try:
            mod = importlib.import_module(f"{skill_name}_skill")
            skills[skill_name] = mod
        except Exception:
            continue
    return skills


def _print_help() -> None:
    """Print the main help text."""
    skills = _discover_skills()
    lines = [
        "Usage: agentforge <skill> [args]",
        "",
        "Available skills:",
    ]
    for name in sorted(skills):
        lines.append(f"  {name}")
    if not skills:
        lines.append("  (no skills installed)")
    lines.extend(
        [
            "",
            "Examples:",
            "  agentforge ocr --image photo.png",
            "  python -m agentforge_cli ocr --image photo.png",
        ]
    )
    print("\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (without program name).

    Returns:
        Exit code (0 = success).
    """
    args = argv if argv is not None else sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        _print_help()
        return 0

    if args[0] == "--version":
        from agentforge_core import __version__ as ver

        print(f"agentforge v{ver}")
        return 0

    skill_name = args[0]
    skill_args = args[1:]
    skills = _discover_skills()

    if skill_name not in skills:
        print(
            f"Error: unknown skill {skill_name!r}",
            file=sys.stderr,
        )
        _print_help()
        return 1

    mod = skills[skill_name]
    try:
        cli = importlib.import_module(f"{mod.__name__}.cli")
    except ImportError:
        print(
            f"Error: skill {skill_name!r} has no CLI",
            file=sys.stderr,
        )
        return 1

    if not hasattr(cli, "main"):
        print(
            f"Error: skill {skill_name!r} CLI has no main()",
            file=sys.stderr,
        )
        return 1

    return cli.main(skill_args)


if __name__ == "__main__":
    sys.exit(main())
