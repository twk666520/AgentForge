
# AgentForge Architecture

## Overview

AgentForge is a modular platform for building AI agent skills.
Each skill is an independent Python package that implements the
``SkillBase`` interface and registers itself via entry points.

```
+------------------+
|   User Entry     |
| CLI  |  SDK      |
+--------+---------+
         |
+--------v---------+
|   AgentForge      |
|   Core            |
|  (skill_base,     |
|   registry,       |
|   config, result) |
+--------+---------+
         |
+--------v---------+
|   Skills          |
|  OCR | Translate  |
|  Vision | ...     |
+------------------+
```

## Core Module (``agentforge-core``)

The core provides the framework that all skills depend on:

- **SkillBase** — Abstract base class with lifecycle hooks
  (``initialize``, ``cleanup``) and context-manager support.
- **SkillRegistry** — Global registry with explicit registration
  and automatic discovery via ``pkgutil``.
- **SkillResult** — Unified result model (``success`` / ``data`` /
  ``error`` / ``metadata``) returned by every skill operation.
- **ConfigManager** — Hierarchical configuration with dotted-key
  access and JSON/YAML file loading.
- **SkillLoader** — Loads skills by name with config merging.

## Skill Module Pattern

Every skill follows the same structure::

    skills/skill-<name>/
    +-- pyproject.toml    # entry-points: agentforge.skills.<name>
    +-- src/<skill>/
        +-- __init__.py   # exports public API
        +-- engine.py     # main SkillBase subclass
        +-- models.py     # domain data models
        +-- backends/     # (optional) backend abstractions
        +-- cli.py        # (optional) CLI subcommand
        +-- preprocess.py # (optional) data preprocessing

## Entry Point System

Skills are discovered via the ``agentforge.skills`` entry point
group::

    [project.entry-points."agentforge.skills"]
    ocr = "ocr_skill"

The root CLI reads all registered entry points and dispatches
subcommands dynamically.

## Development

See ``CONTRIBUTING.md`` for development setup and workflow.
