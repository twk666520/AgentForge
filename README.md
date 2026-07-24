# AgentForge

**AI Agent Enhancement Platform** — 给 AI Agent 装上可插拔的"感官"和"工具"。

AgentForge 是一个模块化的开源平台，提供可组合的 Skills（技能模块），让 AI Agent 能看、能读、能翻译、能操作桌面、能理解代码仓库。

---

## 项目结构

```
agentforge/
├── core/               # AgentForge Core — 技能框架与插件系统
├── skills/
│   ├── skill-ocr/      # OCR 文字识别 (已完成)
│   ├── skill-translate/ # 翻译 (已完成)
│   ├── skill-vision/   # 视觉分析 (规划中)
│   └── ...
├── apps/cli/           # 全局 CLI
├── docs/               # 文档
└── examples/           # 使用示例
```

## 快速开始

```bash
# 安装 Core
pip install -e core/

# 安装技能模块
pip install -e skills/skill-ocr/
pip install -e skills/skill-translate/

# OCR
python -m ocr_skill.cli photo.png --langs en+ch_sim

# 翻译
python -m translate_skill.cli "Hello world" --target zh
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
| Translate | 已完成 | 多语言翻译，支持 OpenAI 后端、Mock 测试模式 |
| Vision | 规划中 | 图片识别、UI 分析、屏幕理解 |
| Desktop | 规划中 | 截图、窗口信息、AI 操作辅助 |
| GitHub | 规划中 | 仓库分析、文档生成、学习路线 |
| Dev Toolkit | 规划中 | JSON/Markdown/SQL/JWT/正则等工具 |

## License

MIT
