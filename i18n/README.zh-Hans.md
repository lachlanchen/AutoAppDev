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

可复用脚本与指南，使用 Codex 作为非交互式工具，从截图/Markdown 逐步构建应用。

> 🎯 **使命：** 让应用开发流水线具备确定性、可恢复、并以工件为驱动。
>
> 🧩 **设计原则：** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ 项目信号

| 信号 | 当前方向 |
| --- | --- |
| 运行时模型 | Tornado backend + static PWA controller |
| 流水线执行 | 确定性且可恢复（`start/pause/resume/stop`） |
| 持久化策略 | PostgreSQL 优先，并带兼容回退行为 |
| 文档流 | 规范根 README + 自动化 `i18n/` 变体 |

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
- [✨ 功能特性](#-功能特性)
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
- [❓ FAQ](#-faq)
- [🗺️ 路线图](#️-路线图)
- [🤝 贡献](#-贡献)
- [❤️ Support](#-support)
- [📄 许可证](#-许可证)
- [❤️ 赞助与捐赠](#️-赞助与捐赠)

## 🚀 概览
AutoAppDev 是一个面向长时间运行、可恢复的应用开发流水线控制器项目，组合了：

1. 使用 PostgreSQL 持久化（并在存储代码中提供本地 JSON 回退行为）的 Tornado 后端 API。
2. 类 Scratch 的静态 PWA 控制器界面。
3. 用于流水线编写、确定性代码生成、自研循环与 README 自动化的脚本和文档。

该项目针对可预测的代理执行进行了优化，采用严格顺序和面向工件的工作流历史。

### 🎨 为什么存在这个仓库

| 主题 | 实际含义 |
| --- | --- |
| 确定性 | 规范化流水线 IR + parser/import/codegen 工作流，强调可重复性 |
| 可恢复 | 对长时间运行任务使用显式生命周期状态机（`start/pause/resume/stop`） |
| 可运维性 | 运行日志、inbox/outbox 通道，以及脚本驱动的验证循环 |
| 文档优先 | 合同/规范/示例位于 `docs/`，并配套自动化多语言 README 流程 |

## 🧭 方法论
AutoAppDev 将代理视为工具，通过严格、可恢复的循环来保持工作稳定：

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

控制器应用旨在以类 Scratch 的块/动作体现同样概念（包括通用 `update_readme` action），从而让每个工作区都保持最新且可复现。

### 🔁 生命周期状态意图

| 状态迁移 | 运行意图 |
| --- | --- |
| `start` | 从 stopped/ready 状态开始流水线 |
| `pause` | 在不丢失上下文的前提下安全暂停长任务 |
| `resume` | 从保存的运行时状态/工件继续执行 |
| `stop` | 结束执行并回到非运行状态 |

## ✨ 功能特性
- 可恢复的流水线生命周期控制：start、pause、resume、stop。
- 面向 AAPS 流水线脚本（`.aaps`）和规范 IR（`autoappdev_ir` v1）的脚本库 API。
- 确定性的 parser/import 流程：
  - 解析格式化 AAPS 脚本。
  - 通过 `# AAPS:` 注释导入标注过的 shell。
  - 可选的 Codex 辅助解析回退（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 动作注册表支持内置动作 + 可编辑/自定义动作（只读内置动作可 clone/edit）。
- 类 Scratch PWA 积木与运行时加载动作面板（`GET /api/actions`）。
- 运行时消息通道：
  - Inbox（`/api/inbox`）用于操作员 -> 流水线指导。
  - Outbox（`/api/outbox`）包含从 `runtime/outbox` 的文件队列摄取。
- 后端与流水线日志增量流式输出（`/api/logs`, `/api/logs/tail`）。
- 从规范 IR 进行确定性 runner 代码生成（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用于仓库迭代演进的自研驱动（`scripts/auto-autoappdev-development.sh`）。
- README 自动化流水线及 `i18n/` 下的多语言生成脚手架。

## 📌 一览

| 区域 | 详情 |
| --- | --- |
| 核心运行时 | Tornado backend + static PWA frontend |
| 持久化 | PostgreSQL 优先，并在 `backend/storage.py` 内提供兼容行为 |
| 流水线模型 | 规范 IR（`autoappdev_ir` v1）与 AAPS 脚本格式 |
| 控制流 | Start / Pause / Resume / Stop 生命周期 |
| 开发模式 | 可恢复自研循环 + 确定性脚本/codegen 工作流 |
| README/i18n | 带 `i18n/` 脚手架的自动化 README 流水线 |

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

### Backend 职责
- 暴露控制器 API：scripts、actions、plan、pipeline lifecycle、logs、inbox/outbox、workspace config。
- 校验并持久化流水线脚本资产。
- 协调流水线执行状态与状态迁移。
- 在 DB 连接池不可用时提供确定性回退行为。

### Frontend 职责
- 渲染类 Scratch 积木 UI 与流水线编辑流程。
- 从后端注册表动态加载动作面板。
- 驱动生命周期控制并监控状态/日志/消息。

## 📚 内容索引
最常用文档、脚本与示例的参考映射：

- `docs/auto-development-guide.md`：长期运行、可恢复自动开发代理的方法论与要求（中英双语）。
- `docs/ORDERING_RATIONALE.md`：截图驱动步骤排序的示例依据。
- `docs/controller-mvp-scope.md`：控制器 MVP 范围（页面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`：确定性手动端到端演示检查清单（backend + PWA happy path）。
- `docs/env.md`：环境变量（`.env`）约定。
- `docs/api-contracts.md`：控制器 API 请求/响应契约。
- `docs/pipeline-formatted-script-spec.md`：标准流水线脚本格式（AAPS）与规范 IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`：从规范 IR 生成可运行 bash pipeline runner 的确定性生成器。
- `docs/common-actions.md`：通用 action 契约/规范（含 `update_readme`）。
- `docs/workspace-layout.md`：标准工作区目录 + 契约（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`：在 tmux 中启动 AutoAppDev 应用（backend + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`：在 tmux 中启动 AutoAppDev 自研驱动。
- `scripts/app-auto-development.sh`：线性流水线驱动（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`），支持 resume/state。
- `scripts/generate_screenshot_docs.sh`：截图 -> Markdown 描述生成器（Codex 驱动）。
- `scripts/setup_autoappdev_env.sh`：本地运行主 conda 环境引导脚本。
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
- 具备 `bash` 的操作系统。
- Python `3.11+`。
- 用于安装脚本的 Conda（`conda`）。
- 用于一键 backend+PWA 或自研会话的 `tmux`。
- `DATABASE_URL` 可达的 PostgreSQL。
- 可选：`codex` CLI（用于 Codex 驱动流程：self-dev、parse-llm 回退、auto-readme 流水线）。

快速要求矩阵：

| 组件 | 必需性 | 用途 |
| --- | --- | --- |
| `bash` | 是 | 脚本执行 |
| Python `3.11+` | 是 | 后端 + codegen 工具 |
| Conda | 是（推荐流程） | 环境引导脚本 |
| PostgreSQL | 是（首选模式） | 通过 `DATABASE_URL` 进行主持久化 |
| `tmux` | 推荐 | 托管 backend/PWA 与 self-dev 会话 |
| `codex` CLI | 可选 | LLM 辅助解析与 README/self-dev 自动化 |

## 🧩 兼容性与假设

| 主题 | 当前预期 |
| --- | --- |
| 本地 OS | 主要目标为 Linux/macOS shell（`bash` 脚本） |
| Python 运行时 | `3.11`（由 `scripts/setup_autoappdev_env.sh` 管理） |
| 持久化模式 | PostgreSQL 为首选并视为规范方案 |
| 回退行为 | `backend/storage.py` 在降级场景中包含 JSON 兼容回退 |
| 网络模型 | 本地 localhost 分端口开发（backend + static PWA） |
| 代理工具 | 除非使用 LLM 辅助解析或 self-dev 自动化，否则 `codex` CLI 为可选 |

本 README 使用的假设：
- 除非章节另有说明，你在仓库根目录执行命令。
- 启动后端服务前，`.env` 已完成配置。
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
- `AUTOAPPDEV_HOST` 和 `AUTOAPPDEV_PORT`（或 `PORT`）

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
- Health check: `http://127.0.0.1:8788/api/health`

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
主配置文件：`.env`（参见 `docs/env.md` 与 `.env.example`）。

### 重要变量

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Required by convention |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Backend bind settings |
| `DATABASE_URL` | PostgreSQL DSN (preferred) |
| `AUTOAPPDEV_RUNTIME_DIR` | Override runtime dir (default `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Default pipeline run target |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Enable `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Codex defaults for actions/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Reserved for future integrations |

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
| 仅启动 backend | `conda run -n autoappdev python -m backend.app` | 使用 `.env` 里的绑定与 DB 设置 |
| 仅启动 PWA 静态服务 | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | 适合仅前端检查 |
| 在 tmux 运行 self-dev 驱动 | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 可恢复自研循环 |

### 常用脚本参数
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### 解析并存储脚本
- 通过 API 解析 AAPS：`POST /api/scripts/parse`
- 导入带注释 shell：`POST /api/scripts/import-shell`
- 可选 LLM 解析：`POST /api/scripts/parse-llm`（需要 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### 流水线控制 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 其他高频 API
- 健康/版本/配置：`/api/health`, `/api/version`, `/api/config`
- 计划/脚本：`/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- 动作：`/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- 消息：`/api/chat`, `/api/inbox`, `/api/outbox`
- 日志：`/api/logs`, `/api/logs/tail`

请求/响应结构见 `docs/api-contracts.md`。

## 🧭 运维 Runbook

### Runbook：拉起完整本地栈
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

验证检查点：
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- 打开 `http://127.0.0.1:5173/`，确认 UI 能加载 `/api/config`。
- 可选：打开 `/api/version`，确认返回预期后端元数据。

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
| 消息 + 日志 | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
| 工作区设置 | `GET/POST /api/workspaces/<name>/config` |

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
然后使用 PWA 的 Start/Pause/Resume/Stop 控件，并检查 `/api/logs`。

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
- 后端基于 Tornado，针对本地开发体验设计（包括对 localhost 分端口的宽松 CORS）。
- 存储层为 PostgreSQL 优先，并在 `backend/storage.py` 中提供兼容行为。
- PWA 的 block key 与脚本 `STEP.block` 值有意保持一致（`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`）。
- 内置动作为只读；编辑前请先 clone。
- `update_readme` action 受到路径安全约束，仅允许更新 `auto-apps/<workspace>/README.md` 下的工作区 README 目标。
- 部分文档/脚本仍保留历史路径或命名（`HeyCyan`, `LightMind`），继承于项目演进过程。当前仓库规范路径是本仓库根目录。
- 根目录 `i18n/` 已存在。多语言运行期望语言 README 文件放在此目录。

### 工作模型与状态文件
- 运行时默认目录为 `./runtime`，可通过 `AUTOAPPDEV_RUNTIME_DIR` 覆盖。
- 自研自动化状态/历史记录位于 `references/selfdev/`。
- README 流水线工件记录在 `.auto-readme-work/<timestamp>/`。

### 测试现状（当前）
- 仓库包含 smoke 检查与确定性演示脚本。
- 根元数据中目前未定义完整的顶层自动化测试套件/CI 清单。
- 当前假设：验证主要由脚本驱动（`scripts/pipeline_codegen/smoke_*.sh`、`backend.db_smoketest`、端到端检查清单）。

## 🔐 安全说明
- `update_readme` action 被有意限制为工作区 README 目标（`auto-apps/<workspace>/README.md`），并带有路径穿越防护。
- Action 注册表校验会强制规范化 action spec 字段，并对支持的 reasoning level 值做边界限制。
- 仓库脚本假设在可信本地环境执行；在共享环境或接近生产的环境运行前请先审阅脚本内容。
- `.env` 可能包含敏感值（`DATABASE_URL`、API keys）。请勿提交 `.env`，并在本地开发之外使用环境级密钥管理。

## 🔧 故障排查

| 症状 | 检查项 |
| --- | --- |
| `tmux not found` | 安装 `tmux`，或手动分别运行 backend/PWA。 |
| 后端启动因缺少环境变量失败 | 对照 `.env.example` 与 `docs/env.md` 复查 `.env`。 |
| 数据库错误（连接/认证/schema） | 检查 `DATABASE_URL`；重新执行 `conda run -n autoappdev python -m backend.apply_schema`；可选连通性检查：`conda run -n autoappdev python -m backend.db_smoketest`。 |
| PWA 能打开但无法调用 API | 确认 backend 在预期 host/port 监听；重新执行 `./scripts/run_autoappdev_tmux.sh` 生成 `pwa/config.local.js`。 |
| Pipeline Start 返回 invalid transition | 先检查当前 pipeline 状态；从 `stopped` 状态启动。 |
| UI 没有日志更新 | 确认 `runtime/logs/pipeline.log` 正在写入；直接调用 `/api/logs` 与 `/api/logs/tail` 以隔离 UI 或 backend 问题。 |
| LLM parse endpoint 显示 disabled | 设置 `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 并重启 backend。 |
| `conda run -n autoappdev ...` 失败 | 重新执行 `./scripts/setup_autoappdev_env.sh`；确认 conda 环境 `autoappdev` 存在（`conda env list`）。 |
| 前端 API 目标错误 | 确认 `pwa/config.local.js` 存在且指向当前 backend host/port。 |

如需确定性的手动验证路径，请使用 `docs/end-to-end-demo-checklist.md`。

## 🌐 README 与 i18n 工作流
- 根 README 是 README 自动化流水线使用的规范来源。
- 多语言变体应放在 `i18n/` 下。
- i18n 目录状态：✅ 本仓库已存在。
- 本仓库当前语言集合：
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
- 每个 README 变体顶部都应保持单行语言导航（不要重复语言栏）。
- README 流水线入口：`prompt_tools/auto-readme-pipeline.sh`。

### i18n 生成约束（严格）
- 更新规范 README 内容时，始终要处理多语言生成。
- 逐个语言文件顺序生成/更新，不要批量混合处理。
- 每个变体顶部保持且仅保持一条 language-options 导航行。
- 不要在同一个文件中重复语言栏。
- 在翻译中保留规范命令片段、链接、API 路径和徽章意图。

建议逐个生成顺序：
1. `README.md`（规范英文源）
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

| Language | File |
| --- | --- |

## ❓ FAQ

### PostgreSQL 是必须的吗？
正常运行场景下推荐且默认应使用 PostgreSQL。存储层包含回退兼容行为，但类生产使用应假设 `DATABASE_URL` 可用并指向 PostgreSQL。

### 为什么同时有 `AUTOAPPDEV_PORT` 和 `PORT`？
`AUTOAPPDEV_PORT` 是项目专用变量。`PORT` 作为更通用的部署别名存在。除非你有意在启动路径中覆盖行为，否则应保持两者一致。

### 如果我只想查看 API，从哪里开始？
仅启动 backend（`conda run -n autoappdev python -m backend.app`），然后依次访问 `/api/health`、`/api/version`、`/api/config`，再查看 `docs/api-contracts.md` 中列出的 script/action 端点。

### 多语言 README 会自动生成吗？
会。仓库包含 `prompt_tools/auto-readme-pipeline.sh`，语言变体维护在 `i18n/` 下，并在每个变体顶部保留单行语言导航。

## 🗺️ 路线图
- 完成当前 `51 / 55` 之外的剩余 self-dev 任务。
- 扩展 workspace/materials/context 工具与更强的安全路径契约。
- 继续改进 action palette UX 与可编辑 action 工作流。
- 持续增强 `i18n/` 与运行时语言切换的多语言 README/UI 支持。
- 强化 smoke/integration 检查与 CI 覆盖（当前已有脚本驱动 smoke 检查；根目录尚无完整 CI 清单文档）。
- 持续加固围绕 AAPS v1 与规范 IR 的 parser/import/codegen 确定性。

## 🤝 贡献
欢迎通过 issue 和 pull request 参与贡献。

建议流程：
1. Fork 并创建功能分支。
2. 保持改动聚焦且可复现。
3. 尽可能优先使用确定性脚本/测试。
4. 当行为/契约变化时同步更新文档（`docs/*`、API 契约、示例）。
5. 提交 PR 时附上背景、验证步骤与任何运行时假设。

当前仓库远程包含：
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 在本地克隆中可能还存在与相关仓库关联的附加 remote（本工作区示例：`novel`）。

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 许可证
当前仓库快照中未检测到根目录 `LICENSE` 文件。

假设说明：
- 在补充许可证文件前，请将使用/再分发条款视为未明确，并与维护者确认。

## ❤️ 赞助与捐赠
| 渠道 | 链接 |
| --- | --- |
| GitHub Sponsors | https://github.com/sponsors/lachlanchen |
| Donate | https://chat.lazying.art/donate |
| PayPal | https://paypal.me/RongzhouChen |
| Stripe | https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400 |

如果这个项目对你的工作流有帮助，赞助将直接支持持续的 self-dev 任务、文档质量提升和工具链加固。
