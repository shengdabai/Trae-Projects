# trae-projects

AI + Chinese-teaching tools built in public with Trae: gaokao AI tutor, EN↔ZH learning app, and DIY Claude-style CLI agents.

## Business Context

- **Category:** AI workflow infrastructure
- **Audience:** AI builders, creators, independent developers, and small teams that want repeatable local AI workflows.
- **Repository status:** Public repository. Keep examples, docs, and issues free of credentials, private data, and machine-specific paths.
- **Topics:** ai, chinese, collection, education, gaokao, learning, llm, python, trae

## What This Project Is For

- AI + Chinese-teaching tools built in public with Trae: gaokao AI tutor, EN↔ZH learning app, and DIY Claude-style CLI agents.
- Package repeatable AI workflows into reusable local assets.
- Reduce one-off prompt work with versioned skills, guardrails, and handoff files.

## Where It Fits

This repository is part of a broader AI local-workbench operating model: reusable skills, local automation, auditable configuration, and repeatable delivery workflows.

## Technical Overview

- **Primary language:** Python
- **Detected stack:** Python, Node.js, Python dependencies
- **Default branch:** `main`
- **Visibility:** `PUBLIC`
- **License:** MIT License

## Repository Map

- `Claude Code`
- `Gaokao-AI-Study`
- `LICENSE`
- `README.md`
- `SECURITY.md`
- `bin`
- `zh-learning-app`

## Quick Start

Use the commands that match the current project state:

```bash
cd zh-learning-app
npm ci --registry=https://registry.npmjs.org
npm start
```

| Command | Purpose |
|---|---|
| `npm ci --registry=https://registry.npmjs.org` | Install locked project dependencies from `zh-learning-app`. |
| `npm start` | node server.js |

## Operating Notes

- Keep real credentials out of the repository. Use local environment files, GitHub repository secrets, or the deployment platform secret manager.
- If a `.env.example` file exists, treat it as documentation only; never commit filled-in `.env` files.
- Before publishing screenshots, demos, or client examples, remove private names, internal paths, account IDs, and API endpoints.
- The `Repository Hygiene` workflow is a lightweight guardrail, not a replacement for product-specific tests.

## Delivery Checklist

- [ ] README describes the user, business outcome, and operating boundary.
- [ ] Setup or preview commands are current and do not rely on private machine state.
- [ ] No real secrets, private user data, or machine-local state are tracked.
- [ ] Screenshots, demos, or sample outputs are safe to share publicly when the repository is public.
- [ ] Product-specific tests or smoke checks are documented before production use.

## Roadmap

- Tighten the fastest path from clone to useful demo.
- Add project-specific screenshots, sample outputs, or a short walkthrough where useful.
- Promote repeated manual steps into scripts, tests, or documented workflows.
- Keep security, privacy, and licensing boundaries explicit as the project evolves.

## Maintainer Notes

*(Sibling repos above; if a link 404s it just isn't public yet.)*

## License

MIT License — see the [LICENSE](LICENSE) file for details.

---

# 中文

> 一个小而实在的学习工具工作台 —— AI 高考辅导、中英学习应用、DIY 的 Claude 式命令行 Agent —— 全部用 [Trae](https://www.trae.ai/) 在公开环境中构建。

[English](#-trae-projects) | 中文

我是 Tony（盛）—— 一名拥有 6000+ 学员的中文老师，在公开环境里构建 AI + 中文教学工具。这个仓库是这些实验的草稿台：每个文件夹都是一个我真正在用或测试过的独立工具，对它"能做什么、还不能做什么"保持诚实。

## 为什么有这个仓库

大规模教语言会反复遇到同样的摩擦：刷真题、给任意句子快速标拼音和分词、把便宜的大模型接进终端。与其做一个大应用，不如做**一组聚焦的学习应用和 Agent**—— 小到能一口气读完，又实用到值得留下来。

## ✨ 项目一览

| 项目 | 它做什么 | 目录 |
|---|---|---|
| 🎓 **高考 AI 备考助手** | 个性化高考复习。Python 脚本把你的历年真题 PDF 提取成纯文本，配合一份"苏格拉底式辅导员"系统提示词，把任意聊天模型（Trae / Claude / ChatGPT）变成只引导、不直接喂答案的教练。 | [`Gaokao-AI-Study/`](Gaokao-AI-Study/) |
| 🇨🇳 **中文学习应用** | 本地运行的 Node + Express 网页应用：英译中，并为每个词/字逐一标注拼音和分词。翻译通过 `@xenova/transformers` 完全离线运行，分词用 `jieba`，注音用 `pinyin-pro`。 | [`zh-learning-app/`](zh-learning-app/) |
| 🤖 **Claude Code（命令行 Agent）** | DIY 的终端聊天客户端，把 Claude-Code 式的对话循环接到便宜的国产大模型 —— Kimi（月之暗面）和 GLM（智谱）—— 走它们的 OpenAI 兼容接口。附带一个 API Key 安全检查脚本。 | [`Claude Code/`](Claude%20Code/) |
| ⚙️ **bin** | 极简启动脚本：`claude` 通过 [`@musistudio/claude-code-router`](https://github.com/musistudio/claude-code-router) 路由；`kimi` 把月之暗面接口接进去。 | [`bin/`](bin/) |
| 📚 **Claude Skills 合集** | 精选的 12 个第三方 Claude Skills 仓库，以 git submodule 形式收录作参考（superpowers、agent-skill-creator、awesome-claude-skills 等）。 | [`claude skillsmp/`](claude%20skillsmp/) |

## 🧱 技术栈

- **Python** —— `pdfplumber` 做 PDF 提取；纯 `urllib` 的大模型客户端（零重依赖）
- **Node.js** —— Express 5，ES 模块
- **本地 AI** —— `@xenova/transformers`（进程内翻译，无需 API Key）
- **中文 NLP** —— `nodejieba` / `@node-rs/jieba` 分词，`pinyin-pro` 注音标调
- **大模型接口** —— 月之暗面（Kimi）、智谱（GLM）、OpenAI 兼容路由
- **构建工具** —— [Trae](https://www.trae.ai/) AI IDE

## 🚀 快速开始

```bash
git clone https://github.com/shengdabai/trae-projects
cd trae-projects
git submodule update --init --recursive   # 仅当你需要 Claude Skills 合集时
```

每个工具都能单独运行，挑一个：

**🎓 高考 AI 备考助手**（Python）
```bash
cd Gaokao-AI-Study
pip install -r requirements.txt
# 把历年真题 PDF 放进 knowledge_base/papers/，然后：
python3 src/ingest_papers.py
# 最后把 AI_TUTOR.md 粘贴进你的聊天模型，激活辅导员
```

**🇨🇳 中文学习应用**（Node）
```bash
cd zh-learning-app
npm install
npm start          # 服务运行在 http://localhost:3000
# POST /api/translate { "english": "hello world", "granularity": "word" }
```
> 首次运行会把翻译模型下载到本地，之后即可离线运行。

**🤖 Claude Code 命令行 Agent**（Python / Node）
```bash
export MOONSHOT_API_KEY=...   # 或 ZHIPUAI_API_KEY=...
node "Claude Code/claudecc.js" --provider=kimi   # 或 --provider=glm
```

## 🗺️ 状态

这是一个活跃的、公开构建中的工作台 —— 难免有粗糙之处。

- ✅ **高考 AI 备考助手** —— 可用：PDF 提取 + 辅导员提示词
- ✅ **中文学习应用** —— 可用：离线英译中 + 拼音 + 分词，含限流和输入校验
- ✅ **Claude Code 命令行 Agent** —— 可用：Kimi + GLM 对话循环
- 🧪 **bin 启动脚本** —— 好用但极简
- 📦 **Claude Skills 合集** —— 参考用 submodule，不在此仓库维护

## 🤝 关注 / 关于

我在公开环境构建 AI + 中文教学工具。如果觉得有用，最好的关注方式就是点个 ⭐ 和 follow：

- ⭐ **[Star 本仓库](https://github.com/shengdabai/trae-projects)** 并 **[关注 @shengdabai](https://github.com/shengdabai)**

如果你教中文或学中文，还有这些：

- 📚 [everything-claude-code](https://github.com/shengdabai/everything-claude-code) —— 我的 Claude Code 配置、skills 与工作流
- 🎓 [gaokao-study-materials](https://github.com/shengdabai/gaokao-study-materials) —— 高考备考资源
- 🇨🇳 [chinese-learning-app](https://github.com/shengdabai/chinese-learning-app) —— 独立版中文学习应用

*（以上为同系列仓库；若链接 404，仅表示它尚未公开。）*

## 许可

MIT 许可证 —— 详见 [LICENSE](LICENSE) 文件。
