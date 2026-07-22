# AgentForge

**AI Agent Enhancement Platform** — 给 AI Agent 装上可插拔的"感官"和"工具"。

AgentForge 是一个模块化的开源平台，提供可组合的 Skills（技能模块），让 AI Agent 能看、能读、能翻译、能操作桌面、能理解代码仓库。

---

## 项目结构

```
agentforge/
├── core/               # AgentForge Core — 技能框架与插件系统
│   ├── src/agentforge_core/
│   │   ├── skill_base.py    # 抽象基类
│   │   ├── registry.py      # 技能注册表
│   │   ├── loader.py        # 动态加载器
│   │   ├── config.py        # 配置管理
│   │   └── result.py        # 统一结果模型
│   └── tests/
├── skills/             # 可插拔技能模块
│   ├── skill-ocr/      # OCR 文字识别 (已完成 ✓)
│   ├── skill-translate/   # 翻译 (规划中)
│   ├── skill-vision/      # 视觉分析 (规划中)
│   └── ...
├── apps/               # 应用层 (CLI / API)
├── docs/               # 文档
└── examples/           # 使用示例
```

## 快速开始

```bash
# 安装 Core
pip install -e core/

# 安装一个技能 (以 OCR 为例)
pip install -e skills/skill-ocr/

# OCR 命令行使用
python -m ocr_skill.cli photo.png --langs en+ch_sim

# Python SDK 使用
from ocr_skill import OCREngine

engine = OCREngine({"langs": ["en", "ch_sim"]})
engine.initialize()
result = engine.recognize("photo.png")
print(result.data.raw_text)
engine.cleanup()
```

## 核心概念

- **SkillBase** — 所有技能必须实现的抽象基类
- **SkillRegistry** — 全局注册表，支持显式注册和自动发现
- **SkillResult** — 统一结果模型（success / data / error / metadata）
- **ConfigManager** — 分层配置，支持 JSON/YAML 文件加载

## 技能列表

| 技能 | 状态 | 描述 |
|------|------|------|
| OCR | 已完成 | 文字识别，支持 EasyOCR 后端、多语言、图像预处理 |
| Translate | 规划中 | 全局实时翻译，多语言支持 |
| Vision | 规划中 | 图片识别、UI 分析、屏幕理解 |
| Desktop | 规划中 | 截图、窗口信息、AI 操作辅助 |
| GitHub | 规划中 | 仓库分析、文档生成、学习路线 |
| Dev Toolkit | 规划中 | JSON/Markdown/SQL/JWT/正则等工具 |

## License

MIT