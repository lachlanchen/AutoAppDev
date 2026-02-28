[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)




[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# AutoAppDev

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Backend](https://img.shields.io/badge/Backend-Tornado-222222)
![Frontend](https://img.shields.io/badge/Frontend-PWA-0A7EA4)
![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Self--Dev-51%2F55%20tasks%20done-2E8B57)
![i18n](https://img.shields.io/badge/i18n-11%20languages-1f6feb)
![Pipeline](https://img.shields.io/badge/Pipeline-Resumable-ff6b35)
![Docs](https://img.shields.io/badge/Docs-Workflow%20First-0e9f6e)
![Automation](https://img.shields.io/badge/Automation-README%20Pipeline-f97316)
![API](https://img.shields.io/badge/API-JSON%20HTTP-0ea5e9)
![State Machine](https://img.shields.io/badge/Lifecycle-start%2Fpause%2Fresume%2Fstop-f59e0b)

可复用脚本和指南，使用 Codex 作为非交互式工具，从截图/Markdown 逐步构建应用。

> 🎯 **使命：** 让应用开发流水线具备确定性、可恢复、且以工件为驱动。
>
> 🧩 **设计原则：** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ 项目信号

| 信号 | 当前方向 |
| --- | --- |
| 运行时模型 | Tornado backend + static PWA controller |
| 流水线执行 | 确定性且可恢复（`start/pause/resume/stop`） |
| 持久化策略 | PostgreSQL 优先，并带兼容回退行为 |
| 文档流程 | 以根 README 为规范来源，配套自动化 `i18n/` 变体 |

### 🔗 快速导航

| 需求 | 前往 |
| --- | --- |
| 首次本地运行 | [⚡ 快速开始](#-快速开始) |
| 环境与必需变量 | [⚙️ 配置](#️-配置) |
| API 总览 | [📡 API 快照](#-api-快照) |
| 运行/调试手册 | [🧭 运维 Runbook](#-运维-runbook) |
| README/i18n 生成规则 | [🌐 README 与 i18n 工作流](#-readme-与-i18n-工作流) |
| 故障排查矩阵 | [🔧 故障排查](#-故障排查) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## 自研状态（自动更新）

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

本节由 `scripts/auto-autoappdev-development.sh` 自动更新。
请勿编辑标记之间的内容。

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ 目录
- [🚀 概览](#-概览)
- [🧭 方法论](#-方法论)
- [✨ 特性](#-特性)
- [📌 一览](#-一览)
- [🏗️ 架构](#️-架构)
- [📚 内容索引](#-内容索引)
- [🗂️ 项目结构](#️-项目结构)
- [✅ 前置要求](#-前置要求)
- [🧩 兼容性与假设](#-兼容性与假设)
- [🛠️ 安装](#️-安装)
- [⚡ 快速开始](#-快速开始)
- [⚙️ 配置](#️-配置)
- [▶️ 使用方式](#️-使用方式)
- [🧭 运维 Runbook](#-运维-runbook)
- [📡 API 快照](#-api-快照)
- [🧪 示例](#-示例)
- [🧱 开发说明](#-开发说明)
- [🔐 安全说明](#-安全说明)
- [🔧 故障排查](#-故障排查)
- [🌐 README 与 i18n 工作流](#-readme-与-i18n-工作流)
- [📘 README 生成上下文](#-readme-生成上下文)
- [❓ FAQ](#-faq)
- [🗺️ 路线图](#️-路线图)
- [🤝 贡献](#-贡献)
- [❤️ Support](#-support)
- [📄 许可证](#-许可证)

## 🚀 概览
AutoAppDev 是一个面向长时间运行、可恢复的应用开发流水线控制器项目，结合了：

1. 一个基于 PostgreSQL 持久化的 Tornado 后端 API（存储代码中包含本地 JSON 回退行为）。
2. 一个 Scratch 风格的静态 PWA 控制器界面。
3. 一套用于流水线编写、确定性代码生成、self-dev 循环与 README 自动化的脚本与文档。

该项目专为可预测的代理执行进行优化，采用严格顺序和以工件为导向的工作流历史。

### 🎨 为什么有这个仓库

| 主题 | 实际含义 |
| --- | --- |
| 确定性 | 规范化流水线 IR + parser/import/codegen 流程，面向可复现结果 |
| 可恢复性 | 对长时间运行任务提供显式生命周期状态机（`start/pause/resume/stop`） |
| 可运维性 | 运行日志、inbox/outbox 通道，以及脚本驱动的验证循环 |
| 文档优先 | 规范与示例位于 `docs/`，并配套多语言 README 流程 |

## 🧭 方法论
AutoAppDev 将 agent 视作执行工具，通过严格且可恢复的循环保持工作稳定：

1. Plan（规划）
2. Implement（实现）
3. Debug/verify（带超时）
4. Fix（修复）
5. Summarize + log（总结 + 日志）
6. Commit + push（提交 + 推送）

控制器应用目标是通过 Scratch 风格的块/动作体现同样的理念（含通用 `update_readme` action），确保每个 workspace 保持同步且可复现。

### 🔁 生命周期状态意图

| 状态迁移 | 运行意图 |
| --- | --- |
| `start` | 从 stopped/ready 状态启动流水线 |
| `pause` | 在不丢失上下文的前提下安全暂停长期执行 |
| `resume` | 从已保存运行时状态/工件继续执行 |
| `stop` | 结束执行并回到非运行状态 |

## ✨ 特性
- 可恢复的流水线生命周期控制：start、pause、resume、stop。
- 脚本库 API，支持 AAPS 流水线脚本（`.aaps`）和标准 IR（`autoappdev_ir` v1）。
- 确定性的 parser/import 流程：
  - 解析格式化的 AAPS 脚本。
  - 通过 `# AAPS:` 注释导入带注解的 shell。
  - 可选的 Codex 辅助解析回退（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 动作注册表包含内置动作与可编辑/自定义动作（只读内置动作支持 clone/edit）。
- Scratch 风格的 PWA 块与运行时加载动作面板（`GET /api/actions`）。
- 运行时消息通道：
  - Inbox（`/api/inbox`）用于操作者到流水线的指引。
  - Outbox（`/api/outbox`）支持从 `runtime/outbox` 的文件队列摄取。
- 来自后端与流水线日志的增量流式输出（`/api/logs`, `/api/logs/tail`）。
- 基于标准 IR 的确定性 runner 代码生成（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用于仓库迭代演进的 self-dev 驱动（`scripts/auto-autoappdev-development.sh`）。
- 具备多语言生成脚手架的 README 自动化流水线（`i18n/`）。

## 📌 一览

| 领域 | 说明 |
| --- | --- |
| 核心运行时 | Tornado backend + static PWA 前端 |
| 持久化 | PostgreSQL 优先，`backend/storage.py` 中兼容回退 |
| 流水线模型 | 标准 IR（`autoappdev_ir` v1）与 AAPS 脚本格式 |
| 控制流 | Start / Pause / Resume / Stop 生命周期 |
| 开发模式 | 可恢复 self-dev 循环 + 确定性脚本/codegen 工作流 |
| README/i18n | 基于 `i18n/` 脚手架的自动化 README 流程 |

## 🏗️ 架构

```text
Operator / Developer
        |
        v
   PWA (static files, pwa/)
        |
        | HTTP JSON API
        v
Tornado backend (backend/app.py)
        |
        +--> Postgres (DATABASE_URL)
        +--> runtime/ (logs, outbox, llm_parse artifacts)
        +--> scripts/ (pipeline runner + codegen helpers)
```

### 后端职责
- 提供 scripts、actions、plan、pipeline lifecycle、logs、inbox/outbox、workspace config 等控制器 API。
- 校验并持久化流水线脚本资产。
- 协调流水线执行状态及其状态变更。
- 当数据库连接池不可用时提供确定性回退。

### 前端职责
- 渲染 Scratch 风格的块式 UI 与流水线编辑流程。
- 从后端动态加载动作面板（action palette）。
- 驱动生命周期控制并监控状态、日志、消息。

## 📚 内容索引
常用文档、脚本和示例的快速映射：

- `docs/auto-development-guide.md`：Bilingual（EN/ZH）长时间运行、可恢复自动开发代理的理念与要求。
- `docs/ORDERING_RATIONALE.md`：截图驱动步骤顺序示例依据。
- `docs/controller-mvp-scope.md`：控制器 MVP 范围（页面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`：确定性的人工端到端演示检查清单（backend + PWA happy path）。
- `docs/env.md`：环境变量（`.env`）约定。
- `docs/api-contracts.md`：控制器 API 请求与响应契约。
- `docs/pipeline-formatted-script-spec.md`：标准流水线脚本格式（AAPS）与标准 IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`：从标准 IR 生成可执行 bash runner 的确定性生成器。
- `docs/common-actions.md`：通用 action 契约与规范（含 `update_readme`）。
- `docs/workspace-layout.md`：标准 workspace 目录与约定（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`：在 tmux 中启动 AutoAppDev（backend + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`：在 tmux 中启动 AutoAppDev self-dev 驱动。
- `scripts/app-auto-development.sh`：线性流水线驱动（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`），支持 resume/state。
- `scripts/generate_screenshot_docs.sh`：截图 -> markdown 描述生成器（由 Codex 驱动）。
- `scripts/setup_autoappdev_env.sh`：本地运行主 conda 环境初始化脚本。
- `scripts/setup_backend_env.sh`：后端环境辅助脚本。
- `examples/ralph-wiggum-example.sh`：Codex CLI 自动化助手示例。

## 🗂️ 项目结构
```text
AutoAppDev/
├── README.md
├── .env.example
├── .github/
│   └── FUNDING.yml
├── backend/
│   ├── app.py
│   ├── storage.py
│   ├── schema.sql
│   ├── apply_schema.py
│   ├── db_smoketest.py
│   ├── action_registry.py
│   ├── builtin_actions.py
│   ├── update_readme_action.py
│   ├── pipeline_parser.py
│   ├── pipeline_shell_import.py
│   ├── llm_assisted_parse.py
│   ├── workspace_config.py
│   ├── requirements.txt
│   └── README.md
├── pwa/
│   ├── index.html
│   ├── app.js
│   ├── i18n.js
│   ├── api-client.js
│   ├── styles.css
│   ├── service-worker.js
│   ├── manifest.json
│   └── README.md
├── docs/
├── scripts/
│   └── pipeline_codegen/
├── prompt_tools/
├── examples/
├── references/
├── i18n/
└── .auto-readme-work/
```

## ✅ 前置要求
- 支持 `bash` 的操作系统。
- Python `3.11+`。
- Conda（`conda`）用于提供的设置脚本。
- `tmux`，用于一键启动 backend+PWA 或 self-dev 会话。
- 可通过 `DATABASE_URL` 访问的 PostgreSQL。
- 可选：`codex` CLI（用于 Codex 驱动流程：self-dev、parse-llm 回退、auto-readme 流水线）。

快速需求矩阵：

| 组件 | 必需 | 用途 |
| --- | --- | --- |
| `bash` | 是 | 脚本执行 |
| Python `3.11+` | 是 | 后端 + codegen 工具 |
| Conda | 是（推荐） | 环境初始化脚本 |
| PostgreSQL | 是（首选） | 通过 `DATABASE_URL` 提供主持久化 |
| `tmux` | 推荐 | 托管 backend/PWA 与 self-dev 会话 |
| `codex` CLI | 可选 | LLM 辅助解析与 README/self-dev 自动化 |

## 🧩 兼容性与假设

| 主题 | 当前预期 |
| --- | --- |
| 本地操作系统 | 以 Linux/macOS shell 为主（`bash` 脚本） |
| Python 运行时 | `3.11`（由 `scripts/setup_autoappdev_env.sh` 管理） |
| 持久化模式 | PostgreSQL 为首选并作为标准 |
| 回退行为 | `backend/storage.py` 在降级场景中包含 JSON 兼容回退 |
| 网络模型 | 本地 localhost 分端口开发（backend + static PWA） |
| 代理工具 | 除非使用 LLM 辅助解析或 self-dev 自动化，否则 `codex` CLI 可选 |

本文档所依据的假设：
- 除非章节另有说明，命令均在仓库根目录执行。
- 启动后端服务前已配置 `.env`。
- 推荐的一键工作流依赖 `conda` 与 `tmux`。

## 🛠️ 安装
### 1) 克隆并进入仓库
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) 配置环境
```bash
cp .env.example .env
```
编辑 `.env` 并至少设置：
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` 与 `AUTOAPPDEV_PORT`（或 `PORT`）

### 3) 创建/更新后端环境
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) 应用数据库 schema
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) 可选：数据库 smoke test
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ 快速开始
```bash
# from repo root
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

然后打开：
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- 健康检查: `http://127.0.0.1:8788/api/health`

一条命令做 smoke-check：
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

快速端点映射：

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ 配置
主配置文件：`.env`（见 `docs/env.md` 和 `.env.example`）。

### 重要变量

| 变量 | 用途 |
| --- | --- |
| `SECRET_KEY` | 约定上的必需值 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | 后端绑定设置 |
| `DATABASE_URL` | PostgreSQL DSN（推荐） |
| `AUTOAPPDEV_RUNTIME_DIR` | 覆盖运行时目录（默认 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 默认流水线运行目标 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | 启用 `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Codex 的 actions/endpoints 默认值 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 预留给未来集成 |

快速校验 `.env`：
```bash
bash -lc 'set -euo pipefail; test -f .env; set -a; source .env; set +a; \
python3 - <<"PY"\
import os, sys\
req = ["SECRET_KEY", "DATABASE_URL"]\
missing = [k for k in req if not os.getenv(k)]\
port_ok = bool(os.getenv("AUTOAPPDEV_PORT") or os.getenv("PORT"))\
if not port_ok: missing.append("AUTOAPPDEV_PORT or PORT")\
if missing:\
  print("Missing env:", ", ".join(missing))\
  sys.exit(1)\
print("OK: env looks set")\
PY'
```

## ▶️ 使用方式

| 模式 | 命令 | 说明 |
| --- | --- | --- |
| 启动 backend + PWA（推荐） | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`，PWA `http://127.0.0.1:5173/` |
| 仅启动 backend | `conda run -n autoappdev python -m backend.app` | 使用 `.env` 里的 bind 与 DB 配置 |
| 仅启动 PWA 静态服务 | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | 适用于前端单独检查 |
| 在 tmux 中运行 self-dev 驱动 | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 可恢复的 self-dev 循环 |

### 常用脚本参数
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### 解析并存储脚本
- 通过 API 解析 AAPS：`POST /api/scripts/parse`
- 导入带注释 shell：`POST /api/scripts/import-shell`
- 可选的 LLM 解析：`POST /api/scripts/parse-llm`（需要 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### 流水线控制 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 其他高频 API
- 健康/版本/配置：`/api/health`, `/api/version`, `/api/config`
- Plan 和脚本：`/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions：`/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- 消息：`/api/chat`, `/api/inbox`, `/api/outbox`
- 日志：`/api/logs`, `/api/logs/tail`

详细请求/响应结构见 `docs/api-contracts.md`。

## 🧭 运维 Runbook

### Runbook：启动完整本地栈
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

验证检查点：
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- 打开 `http://127.0.0.1:5173/` 并确认 UI 可加载 `/api/config`。
- 可选：打开 `/api/version`，确认返回预期的后端元数据。

### Runbook：仅后端调试
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook：确定性 codegen smoke
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
scripts/pipeline_codegen/smoke_placeholders.sh
scripts/pipeline_codegen/smoke_conditional_steps.sh
scripts/pipeline_codegen/smoke_meta_round_v0.sh
```

## 📡 API 快照

核心 API 分组一览：

| 分类 | 端点 |
| --- | --- |
| 健康 + 运行时信息 | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan 模型 | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action 注册表 | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline 运行时 | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| 消息 + 日志 | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| Workspace 设置 | `GET/POST /api/workspaces/<name>/config` |

## 🧪 示例
### AAPS 示例
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

完整示例：
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### 确定性 runner 生成
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### 确定性演示流水线
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
然后使用 PWA 的 Start/Pause/Resume/Stop 控件并检查 `/api/logs`。

### 从带注释 shell 导入
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 开发说明
- 后端基于 Tornado，面向本地开发体验优化（包括 localhost 分端口时的宽松 CORS）。
- 持久化以 PostgreSQL 为主，并在 `backend/storage.py` 中提供兼容回退。
- PWA 的 block key 与脚本 `STEP.block` 值保持一致：`plan`、`work`、`debug`、`fix`、`summary`、`commit_push`。
- 内置动作为只读；编辑前请先 clone。
- `update_readme` action 受到路径安全限制，仅允许更新 `auto-apps/<workspace>/README.md` 下的 workspace README 目标。
- 某些文档/脚本中仍保留历史路径或命名（`HeyCyan`、`LightMind`），源于仓库演进。当前仓库的规范路径是本仓库根目录。
- 根目录 `i18n/` 已存在；多语言 README 文件在 `i18n/` 下维护。

### 工作模型与状态文件
- 运行时默认目录为 `./runtime`，可通过 `AUTOAPPDEV_RUNTIME_DIR` 覆盖。
- self-dev 自动化状态与历史记录保存在 `references/selfdev/`。
- README 流水线制品记录在 `.auto-readme-work/<timestamp>/`。

### 测试现状（当前）
- 仓库包含 smoke 检查和确定性演示脚本。
- 仓库根元数据尚未定义完整的顶层自动化测试套件/CI 清单。
- 假设验证主要通过脚本驱动（`scripts/pipeline_codegen/smoke_*.sh`、`backend.db_smoketest`、端到端检查清单）。

## 🔐 安全说明
- `update_readme` action 有意限制到工作区 README 目标（`auto-apps/<workspace>/README.md`），并有路径穿越防护。
- 动作注册表校验会对 action spec 字段进行规范化，并对支持的推理级别值进行边界控制。
- 仓库脚本默认假设在可信本地环境执行；在共享或接近生产环境运行前请先审阅脚本。
- `.env` 可能包含敏感值（`DATABASE_URL`、API keys）。请勿提交 `.env`，在本地开发之外使用合适的机密管理方式。

## 🔧 故障排查

| 症状 | 排查要点 |
| --- | --- |
| `tmux not found` | 安装 `tmux`，或手动分别启动 backend/PWA。 |
| 后端启动因缺失环境变量失败 | 对照 `.env.example` 与 `docs/env.md` 复查 `.env`。 |
| 数据库报错（连接/认证/schema） | 检查 `DATABASE_URL`；重跑 `conda run -n autoappdev python -m backend.apply_schema`；可选连接性检查：`conda run -n autoappdev python -m backend.db_smoketest`。 |
| PWA 可打开但无法调用 API | 确认 backend 在预期 host/port 监听；重新运行 `./scripts/run_autoappdev_tmux.sh` 以重新生成 `pwa/config.local.js`。 |
| Pipeline Start 返回 invalid transition | 先检查当前 pipeline 状态；从 `stopped` 状态启动。 |
| UI 无日志更新 | 确认 `runtime/logs/pipeline.log` 正在写入；直接使用 `/api/logs` 与 `/api/logs/tail` 定位是 UI 还是 backend 问题。 |
| LLM parse endpoint 显示 disabled | 设置 `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 并重启 backend。 |
| `conda run -n autoappdev ...` 失败 | 重跑 `./scripts/setup_autoappdev_env.sh`；确认 conda 环境 `autoappdev` 存在（`conda env list`）。 |
| 前端 API 指向错误 | 确认 `pwa/config.local.js` 存在并指向当前 backend host/port。 |

如果需要进行确定性手动验证路径，请使用 `docs/end-to-end-demo-checklist.md`。

## 🌐 README 与 i18n 工作流
- 根 README 是 README 自动化流水线的规范源。
- 多语言变体应放在 `i18n/` 目录下。
- i18n 目录状态：✅ 已在仓库中存在。
- 当前仓库语言清单：
  - `i18n/README.ar.md`
  - `i18n/README.de.md`
  - `i18n/README.es.md`
  - `i18n/README.fr.md`
  - `i18n/README.ja.md`
  - `i18n/README.ko.md`
  - `i18n/README.ru.md`
  - `i18n/README.vi.md`
  - `i18n/README.zh-Hans.md`
  - `i18n/README.zh-Hant.md`
- 每个 README 变体顶部仅保留一条语言导航行（不重复）。
- README 流水线入口：`prompt_tools/auto-readme-pipeline.sh`。

### i18n 生成约束（严格）
- 更新根 README 内容时，始终执行多语言生成。
- 逐个语言文件生成/更新（顺序执行，不要并行批量）。
- 每个变体顶部保持且仅保持一条语言导航行。
- 不要在同一文件重复语言栏。
- 翻译时保持规范命令片段、链接、API 路径和徽章语义不变。

建议顺序：
1. `README.md`
2. `i18n/README.ar.md`
3. `i18n/README.de.md`
4. `i18n/README.es.md`
5. `i18n/README.fr.md`
6. `i18n/README.ja.md`
7. `i18n/README.ko.md`
8. `i18n/README.ru.md`
9. `i18n/README.vi.md`
10. `i18n/README.zh-Hans.md`
11. `i18n/README.zh-Hant.md`

语言覆盖表：

| 语言 | 文件 |
| --- | --- |

## 📘 Readme 生成上下文

- 流水线运行时间戳：`20260301_064935`
- 触发条件：`./README.md` 首次完整草稿生成
- 输入用户提示：`probe prompt`
- 目标：生成完整、可读的 README 草稿，包含 required sections 与支持信息
- 使用的源码快照：
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- 本文件基于仓库内容生成并作为规范起点。

## ❓ FAQ

### PostgreSQL 是必须的吗？
推荐并且预计在正常运行时使用 PostgreSQL。存储层包含兼容回退，但生产类场景应假设 `DATABASE_URL` 可用并指向 PostgreSQL。

### 为什么同时有 `AUTOAPPDEV_PORT` 和 `PORT`？
`AUTOAPPDEV_PORT` 是项目专用变量；`PORT` 则是更通用的部署友好别名。除非有意覆盖启动路径行为，否则应保持二者一致。

### 只想查看 API 应该从哪里开始？
仅启动 backend（`conda run -n autoappdev python -m backend.app`），先访问 `/api/health`、`/api/version`、`/api/config`，再使用 `docs/api-contracts.md` 中列出的 script/action 端点。

### 多语言 README 会自动生成吗？
会。仓库包含 `prompt_tools/auto-readme-pipeline.sh`，语言变体维护在 `i18n/`，且每个文件顶部都保留一条语言导航。

## 🗺️ 路线图
- 完成当前 `51 / 55` 之外的 remaining self-dev 任务。
- 扩展 workspace/materials/context 工具与更严格的安全路径约束。
- 继续改进 action palette 的 UX 与可编辑动作流程。
- 加强 `i18n/` 与运行时语言切换的多语言 README/UI 支持。
- 强化 smoke/integration 检查与 CI 覆盖（目前已有脚本驱动的 smoke 检查，根目录尚无完整 CI 清单）。
- 围绕 AAPS v1 与标准 IR 进一步固化 parser/import/codegen 的确定性。

## 🤝 贡献
欢迎通过 issue 与 pull request 参与贡献。

建议流程：
1. Fork 并创建功能分支。
2. 保持改动聚焦、可复现。
3. 尽可能优先采用确定性脚本和测试。
4. 行为或契约变化时同步更新文档（`docs/*`、API 契约、示例）。
5. 提交 PR 时附上上下文、验证步骤与运行时假设。

仓库远程目前包括：
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 本地克隆中可能还包含与相关仓库关联的附加 remote（本工作区示例：`novel`）。

## 📄 许可证
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

当前仓库快照未检测到根目录 `LICENSE` 文件。

说明：
- 在添加许可证文件前，视使用和再分发条款为未明确，并向维护者确认。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
