"""Pure function tools - no external dependencies."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import uuid as uuid_mod
from typing import Any


def json_format(text: str, indent: int = 2) -> dict[str, Any]:
    """Pretty-print a JSON string."""
    parsed = json.loads(text)
    formatted = json.dumps(parsed, indent=indent, ensure_ascii=False)
    return {"output": formatted, "valid": True}


def json_validate(text: str) -> dict[str, Any]:
    """Validate a JSON string."""
    try:
        json.loads(text)
        return {"valid": True, "output": "Valid JSON"}
    except json.JSONDecodeError as e:
        return {"valid": False, "output": str(e)}


def json_minify(text: str) -> dict[str, Any]:
    """Minify a JSON string."""
    parsed = json.loads(text)
    return {"output": json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)}


def base64_encode(text: str) -> dict[str, Any]:
    """Base64 encode a string."""
    encoded = base64.b64encode(text.encode()).decode()
    return {"output": encoded}


def base64_decode(text: str) -> dict[str, Any]:
    """Base64 decode a string."""
    try:
        decoded = base64.b64decode(text).decode()
        return {"output": decoded}
    except Exception as e:
        return {"output": f"Error: {e}"}


def jwt_decode(token: str) -> dict[str, Any]:
    """Decode JWT header and payload (no signature validation)."""
    parts = token.split(".")
    if len(parts) != 3:
        return {"output": "Error: Invalid JWT format (expected 3 parts)"}
    result = {}
    for i, name in enumerate(["header", "payload"]):
        try:
            padded = parts[i] + "=" * (4 - len(parts[i]) % 4)
            decoded = base64.urlsafe_b64decode(padded).decode()
            result[name] = json.loads(decoded)
        except Exception as e:
            result[name] = f"Error: {e}"
    return {"output": json.dumps(result, indent=2, ensure_ascii=False)}


def uuid_generate(version: str = "v4") -> dict[str, Any]:
    """Generate a UUID."""
    if version == "v4":
        uid = str(uuid_mod.uuid4())
    elif version == "v1":
        uid = str(uuid_mod.uuid1())
    else:
        return {"output": f"Unknown version: {version}"}
    return {"output": uid}


def hash_text(text: str, algorithm: str = "sha256") -> dict[str, Any]:
    """Hash text using the specified algorithm."""
    algos = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256}
    if algorithm not in algos:
        return {"output": f"Unsupported: {algorithm} (use md5, sha1, sha256)"}
    h = algos[algorithm](text.encode()).hexdigest()
    return {"output": h}


def regex_test(pattern: str, text: str, flags: str = "") -> dict[str, Any]:
    """Test a regex pattern against text."""
    flag_map = {"i": re.I, "m": re.M, "s": re.S}
    flag_val = 0
    for f in flags:
        flag_val |= flag_map.get(f, 0)
    try:
        compiled = re.compile(pattern, flag_val)
        matches = compiled.findall(text)
        return {
            "output": json.dumps(matches, ensure_ascii=False)
            if matches
            else "No matches",
            "metadata": {"matches": len(matches)},
        }
    except re.error as e:
        return {"output": f"Regex error: {e}"}


def markdown_table(headers: list[str], rows: list[list[str]]) -> dict[str, Any]:
    """Generate a Markdown table."""
    if not headers:
        return {"output": "Error: no headers"}
    sep = "|" + "|".join("---" for _ in headers) + "|"
    header_line = "|" + "|".join(headers) + "|"
    row_lines = ["|" + "|".join(row) + "|" for row in rows]
    table = "\n".join([header_line, sep] + row_lines)
    return {"output": table}


_TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "json-format": {"fn": json_format, "desc": "Pretty-print JSON"},
    "json-validate": {"fn": json_validate, "desc": "Validate JSON"},
    "json-minify": {"fn": json_minify, "desc": "Minify JSON"},
    "base64-encode": {"fn": base64_encode, "desc": "Base64 encode"},
    "base64-decode": {"fn": base64_decode, "desc": "Base64 decode"},
    "jwt-decode": {"fn": jwt_decode, "desc": "Decode JWT token"},
    "uuid": {"fn": uuid_generate, "desc": "Generate UUID"},
    "hash": {"fn": hash_text, "desc": "Hash text (md5/sha1/sha256)"},
    "regex-test": {"fn": regex_test, "desc": "Test regex pattern"},
    "markdown-table": {"fn": markdown_table, "desc": "Generate Markdown table"},
}


def list_tools() -> list[dict[str, Any]]:
    return [{"name": k, "description": v["desc"]} for k, v in _TOOL_REGISTRY.items()]


def run_tool(name: str, **kwargs: Any) -> dict[str, Any]:
    if name not in _TOOL_REGISTRY:
        return {"success": False, "output": f"Unknown tool: {name}"}
    try:
        result = _TOOL_REGISTRY[name]["fn"](**kwargs)
        return {"success": True, **result}
    except Exception as e:
        return {"success": False, "output": str(e)}
