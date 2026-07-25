"""Basic GitHub example."""
from github_skill import GitHubEngine

engine = GitHubEngine({"backend": "mock"})
engine.initialize()
result = engine.analyze("https://github.com/user/repo")
print(f"Repo: {result.data.repo.name}")
print(f"Summary: {result.data.summary}")
print(f"Tech Stack: {', '.join(result.data.tech_stack)}")
engine.cleanup()