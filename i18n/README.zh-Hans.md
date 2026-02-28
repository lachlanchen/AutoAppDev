[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/figs/banner.png" alt="LazyingArt banner" />
</p>

# AutoAppDev

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Backend](https://img.shields.io/badge/Backend-Tornado-222222)
![Frontend](https://img.shields.io/badge/Frontend-PWA-0A7EA4)
![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Self--Dev-51%2F55%20tasks%20done-2E8B57)
![i18n](https://img.shields.io/badge/i18n-11%20languages-1f6feb)

可复用脚本与指南：将 Codex 作为非交互式工具，基于截图/markdown 逐步构建应用。

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev 状态（自动更新）

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

此部分由 `scripts/auto-autoappdev-development.sh` 更新。
请勿编辑标记之间的内容。

<!-- AUTOAPPDEV:STATUS:END -->

## 🚀 概览
AutoAppDev 是一个用于长周期、可恢复应用开发流水线的控制器项目。它结合了：

1. 基于 Tornado 的后端 API，并使用 PostgreSQL 持久化（同时在存储代码中提供本地 JSON 回退行为）。
2. 类 Scratch 的静态 PWA 控制器 UI。
3. 用于流水线编写、确定性代码生成、自开发循环和 README 自动化的脚本与文档。

### 快速一览

| 区域 | 详情 |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | PostgreSQL-first with compatibility behavior in `backend/storage.py` |
| Pipeline model | Canonical IR (`autoappdev_ir` v1) and AAPS script format |
| Control flow | Start / Pause / Resume / Stop lifecycle |
| Dev mode | Resumable self-dev loop + deterministic script/codegen workflows |
| README/i18n | Automated README pipeline with `i18n/` scaffolding |

## 🧭 理念
AutoAppDev 将 agent 视为工具，并通过严格且可恢复的循环来保持工作稳定：
1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

控制器应用旨在用类似 Scratch 的块/动作来体现同样概念（包括通用的 `update_readme` action），让每个工作区保持最新且可复现。

## ✨ 功能
- 可恢复的流水线生命周期控制：start、pause、resume、stop。
- AAPS 流水线脚本（`.aaps`）与 canonical IR（`autoappdev_ir` v1）的脚本库 API。
- 确定性 parser/import 流程：
  - 解析格式化 AAPS 脚本。
  - 通过 `# AAPS:` 注释导入带标注的 shell。
  - 可选 Codex 辅助解析回退（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- Action 注册表：内置动作 + 可编辑/自定义动作（只读内置动作需先 clone/edit）。
- 类 Scratch 的 PWA 块，以及运行时加载的 action palette（`GET /api/actions`）。
- 运行时消息通道：
  - Inbox（`/api/inbox`）用于 operator -> pipeline 指导。
  - Outbox（`/api/outbox`），包含从 `runtime/outbox` 读取文件队列。
- 从后端与流水线日志增量流式读取（`/api/logs`、`/api/logs/tail`）。
- 从 canonical IR 进行确定性 runner 代码生成（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用于仓库迭代演进的 self-dev driver（`scripts/auto-autoappdev-development.sh`）。
- README 自动化流水线，并在 `i18n/` 下提供多语言生成脚手架。

## 📚 目录
- `docs/auto-development-guide.md`：面向长周期、可恢复自动开发 agent 的双语（EN/ZH）理念与要求。
- `docs/ORDERING_RATIONALE.md`：截图驱动步骤排序的示例依据。
- `docs/controller-mvp-scope.md`：控制器 MVP 范围（界面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`：确定性的手工端到端演示检查清单（backend + PWA happy path）。
- `docs/env.md`：环境变量（.env）约定。
- `docs/api-contracts.md`：控制器 API 请求/响应契约。
- `docs/pipeline-formatted-script-spec.md`：标准流水线脚本格式（AAPS）与 canonical IR 架构（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`：从 canonical IR 生成可运行 bash 流水线 runner 的确定性生成器。
- `docs/common-actions.md`：通用 action 契约/规范（包含 `update_readme`）。
- `docs/workspace-layout.md`：标准工作区目录与契约（materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps）。
- `scripts/run_autoappdev_tmux.sh`：在 tmux 中启动 AutoAppDev 应用（backend + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`：在 tmux 中启动 AutoAppDev self-dev driver。
- `scripts/app-auto-development.sh`：线性流水线 driver（plan -> backend -> PWA -> Android -> iOS -> review -> summary），支持恢复/状态。
- `scripts/generate_screenshot_docs.sh`：截图 -> markdown 描述生成器（Codex 驱动）。
- `scripts/setup_backend_env.sh`：本地运行的后端 conda 环境引导脚本。
- `examples/ralph-wiggum-example.sh`：Codex CLI 自动化辅助示例。

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
├── prompt_tools/
├── examples/
├── references/
├── i18n/
└── .auto-readme-work/
```

## ✅ 前置条件
- 具备 `bash` 的操作系统。
- Python `3.11+`。
- 用于已提供 setup 脚本的 Conda（`conda`）。
- 用于一键启动 backend+PWA 或 self-dev 会话的 `tmux`。
- 可由 `DATABASE_URL` 访问的 PostgreSQL。
- 可选：`codex` CLI（用于 Codex 驱动流程：self-dev、parse-llm 回退、auto-readme 流水线）。

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

## ⚙️ 配置
主配置文件：`.env`（见 `docs/env.md` 与 `.env.example`）。

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

## ▶️ 使用
### 一起启动 backend + PWA（推荐）
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
默认值：
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### 仅启动 backend
```bash
conda run -n autoappdev python -m backend.app
```

### 仅启动 PWA 静态服务
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### 在 tmux 中运行 self-dev driver
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### 解析并存储脚本
- 通过 API 解析 AAPS：`POST /api/scripts/parse`
- 导入带标注 shell：`POST /api/scripts/import-shell`
- 可选 LLM 解析：`POST /api/scripts/parse-llm`（需要 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### Pipeline 控制 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 其他常用 API
- Health/version/config：`/api/health`、`/api/version`、`/api/config`
- Plan/scripts：`/api/plan`、`/api/scripts`、`/api/scripts/<id>`
- Actions：`/api/actions`、`/api/actions/<id>`、`/api/actions/<id>/clone`、`/api/actions/update-readme`
- Messaging：`/api/chat`、`/api/inbox`、`/api/outbox`
- Logs：`/api/logs`、`/api/logs/tail`

请求/响应结构见 `docs/api-contracts.md`。

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

### Deterministic runner 生成
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Deterministic 演示流水线
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
然后使用 PWA 的 Start/Pause/Resume/Stop 控件，并查看 `/api/logs`。

## 🧱 开发说明
- 后端基于 Tornado，面向本地开发体验设计（包括对 localhost 分离端口的宽松 CORS）。
- 存储层以 PostgreSQL 为优先，并在 `backend/storage.py` 中提供兼容行为。
- PWA block key 与脚本 `STEP.block` 值是刻意对齐的（`plan`、`work`、`debug`、`fix`、`summary`、`commit_push`）。
- 内置 actions 为只读；编辑前请先 clone。
- `update_readme` action 受路径安全约束，仅允许工作区 README 目标 `auto-apps/<workspace>/README.md`。
- 部分文档/脚本中存在历史路径/名称引用（`HeyCyan`、`LightMind`），源自项目演进。当前仓库规范路径是本仓库根目录。
- 根目录 `i18n/` 已存在。多语言运行时应将各语言 README 文件放在该目录下。

## 🩺 故障排查
- `tmux not found`：
  - 安装 `tmux`，或手动运行 backend/PWA。
- 后端因缺少环境变量启动失败：
  - 对照 `.env.example` 与 `docs/env.md` 重新检查 `.env`。
- 数据库错误（连接/认证/schema）：
  - 校验 `DATABASE_URL`。
  - 重新运行 `conda run -n autoappdev python -m backend.apply_schema`。
  - 可选连通性检查：`conda run -n autoappdev python -m backend.db_smoketest`。
- PWA 能加载但无法调用 API：
  - 确认后端在预期 host/port 上监听。
  - 重新运行 `./scripts/run_autoappdev_tmux.sh` 以重新生成 `pwa/config.local.js`。
- Pipeline Start 返回 invalid transition：
  - 先检查当前 pipeline 状态；从 `stopped` 状态开始。
- UI 中没有日志更新：
  - 确认 `runtime/logs/pipeline.log` 正在写入。
  - 直接调用 `/api/logs` 与 `/api/logs/tail`，隔离 UI 与 backend 问题。
- LLM parse endpoint 返回 disabled：
  - 设置 `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 并重启后端。

如需确定性的手工验证路径，请使用 `docs/end-to-end-demo-checklist.md`。

## 🗺️ 路线图
- 完成当前 `51 / 55` 之外的剩余 self-dev 任务。
- 扩展 workspace/materials/context 工具，并强化安全路径契约。
- 持续优化 action palette UX 与可编辑 action 工作流。
- 深化 `i18n/` 与运行时语言切换的多语言 README/UI 支持。
- 加强 smoke/integration 检查与 CI 覆盖（当前已有脚本驱动的 smoke checks；根目录尚未记录完整 CI manifest）。

## 🤝 贡献
欢迎通过 issue 和 pull request 贡献。

建议流程：
1. Fork 并创建功能分支。
2. 保持改动聚焦且可复现。
3. 在可能情况下优先使用确定性脚本/测试。
4. 当行为/契约变更时更新文档（`docs/*`、API contracts、examples）。
5. 提交包含上下文、验证步骤和运行时假设的 PR。

当前仓库远端包含：
- `origin`：`git@github.com:lachlanchen/AutoAppDev.git`
- 本地克隆中可能还存在一个关联仓库的附加 remote。

## 📄 许可证
在当前仓库快照中未检测到根目录 `LICENSE` 文件。

假设说明：
- 在添加 license 文件之前，请将使用/再分发条款视为未明确，并与维护者确认。

## ❤️ Sponsor & Donate

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
