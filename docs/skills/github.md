# GitHub Skill

Analyze GitHub repositories.

## CLI Usage
```bash
python -m github_skill.cli https://github.com/user/repo
python -m github_skill.cli https://github.com/user/repo --format json
```

## Python SDK
```python
from github_skill import GitHubEngine
engine = GitHubEngine({"backend": "mock"})
engine.initialize()
r = engine.analyze("https://github.com/user/repo")
print(r.data.summary)
engine.cleanup()
```

## Backends
- **mock** — Mock analysis for testing
- **openai** — GPT-4o analysis (pip install openai)