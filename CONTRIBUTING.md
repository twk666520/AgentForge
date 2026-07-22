# Contributing to AgentForge

## 开发流程

1. 确认你在 main 分支上
2. 创建一个功能分支: `git checkout -b feature/your-feature`
3. 在 core/ 或 skills/ 下进行开发
4. 确保所有测试通过: `pytest core/tests/ -v`
5. 确保 ruff 检查通过: `ruff check core/src/`
6. 提交 PR 到 main 分支

## 代码规范

- Python 版本: 3.10+
- 代码风格: ruff (基于 pycodestyle + isort + flake8)
- 类型标注: 所有公共 API 必须包含完整类型注解
- 测试: 所有新功能必须包含 pytest 测试

## 模块独立原则

每个 Skill 都是一个独立的 Python package，放在 `skills/` 目录下：

- 只依赖 `agentforge-core`
- 不依赖其他 Skill
- 有自己的 `pyproject.toml`
- 可以独立发布到 PyPI

## 架构决策记录 (ADR)

重要架构决策请记录在 `docs/adr/` 目录下。
