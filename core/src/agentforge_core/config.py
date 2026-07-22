"""Configuration manager for AgentForge skills."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class ConfigManager:
    """Hierarchical configuration with file-based and programmatic access.

    Configuration can be loaded from a YAML/JSON file and overridden
    at runtime. Supports namespaced skill configs under the skill name.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self._data: dict[str, Any] = dict(config or {})

    # --- Accessors ---

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value by dotted key.

        Supports nested lookups via "." separators::

            config.get("ocr.backend")  # -> config["ocr"]["backend"]

        Args:
            key: Dotted config key.
            default: Fallback value if the key path does not exist.

        Returns:
            The value at ``key``, or ``default``.
        """
        parts = key.split(".")
        current: Any = self._data
        for part in parts:
            if not isinstance(current, dict):
                return default
            if part not in current:
                return default
            current = current[part]
        return current

    def set(self, key: str, value: Any) -> None:
        """Set a config value by dotted key.

        Intermediate dicts are created as needed::

            config.set("ocr.backend", "paddle")
            # -> {"ocr": {"backend": "paddle"}}
        """
        parts = key.split(".")
        current = self._data
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def update(self, data: dict[str, Any]) -> None:
        """Deep-merge a dictionary into the current configuration."""
        self._deep_merge(self._data, data)

    # --- Loading ---

    def load_file(self, path: str | Path) -> None:
        """Load configuration from a file.

        Supports JSON and YAML formats (detected by extension).

        Args:
            path: Path to the config file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the extension is not supported.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        suffix = path.suffix.lower()
        raw = path.read_text(encoding="utf-8")

        if suffix in (".yaml", ".yml"):
            try:
                import yaml  # type: ignore[import-untyped]
            except ImportError:
                raise ImportError(
                    "PyYAML is required to load .yaml files. "
                    "Install it with: pip install PyYAML"
                )
            parsed: dict[str, Any] = yaml.safe_load(raw)
        elif suffix == ".json":
            import json

            parsed = json.loads(raw)
        else:
            raise ValueError(
                f"Unsupported config format: {suffix} (supported: .json, .yaml, .yml)"
            )

        self.update(parsed)

    def to_dict(self) -> dict[str, Any]:
        """Return a copy of the raw configuration dictionary."""
        return dict(self._data)

    # --- Internal ---

    @staticmethod
    def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> None:
        """Recursively merge ``overlay`` into ``base``."""
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                ConfigManager._deep_merge(base[key], value)
            else:
                base[key] = value

    def __repr__(self) -> str:
        return f"<ConfigManager keys={list(self._data)}>"
