# Dev Toolkit

Developer utility tools (no external deps).

## CLI Usage
```bash
python -m dev_toolkit_skill.cli --list
python -m dev_toolkit_skill.cli base64-encode --text=hello
```

## Python SDK
```python
from dev_toolkit_skill import DevToolkitEngine
engine = DevToolkitEngine()
engine.initialize()
r = engine.run("base64-encode", text="hello")
print(r.data.output)
```

## Tools
json-format, json-validate, json-minify, base64-encode/decode, jwt-decode, uuid, hash, regex-test, markdown-table