[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# AutoAppDev 🚀

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
![Control Flow](https://img.shields.io/badge/Control%20Flow-Plan%20%E2%86%92%20Work%20%E2%86%92%20Verify%20%E2%86%92%20Summary-0f766e)
![GitHub stars](https://img.shields.io/github/stars/lachlanchen/AutoAppDev?style=flat&logo=github&logoColor=white&color=%231DA1F2)
![GitHub forks](https://img.shields.io/github/forks/lachlanchen/AutoAppDev?style=flat&logo=github&logoColor=white&color=%2300A4A6)
![GitHub issues](https://img.shields.io/github/issues/lachlanchen/AutoAppDev?style=flat&logo=github&logoColor=white&color=%23ef4444)

---

可重用腳本與指南，搭配 Codex 作為非互動式工具，從截圖／Markdown 逐步建置應用程式。

> 🎯 **使命：** 讓應用開發 pipeline 具備可決定性、可恢復、且以產出物為核心。
>
> 🧩 **設計原則：** Plan -> Work -> Verify -> Summary -> Commit/Push。

---

### 🎛️ 專案訊號

| Signal | Current Direction |
| --- | --- |
| Runtime model | Tornado backend + static PWA controller |
| Pipeline execution | Deterministic and resumable (`start/pause/resume/stop`) |
| Persistence strategy | PostgreSQL-first with compatibility fallback behavior |
| Documentation flow | Canonical root README + automated `i18n/` variants |

### 🔗 快速導覽

| 需求 | 前往 |
| --- | --- |
| 首次本機啟動 | [⚡ Quick Start](#-quick-start) |
| 環境與必要變數 | [⚙️ Configuration](#-configuration) |
| API 介面總覽 | [📡 API Snapshot](#-api-snapshot) |
| 執行／除錯操作手冊 | [🧭 Operational Runbooks](#-operational-runbooks) |
| README/i18n 生成規範 | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| 疑難排解矩陣 | [🔧 Troubleshooting](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev 狀態（自動更新）

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

此區段由 `scripts/auto-autoappdev-development.sh` 更新。
請勿編輯標記之間的內容。

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ 目錄
- [🚀 Overview](#-overview)
- [🧭 Repository Snapshot](#-repository-snapshot)
- [🧭 Philosophy](#-philosophy)
- [✨ Features](#-features)
- [📌 At A Glance](#-at-a-glance)
- [🏗️ Architecture](#-architecture)
- [📚 Contents](#-contents)
- [🗂️ Project Structure](#-project-structure)
- [✅ Prerequisites](#-prerequisites)
- [🧩 Compatibility & Assumptions](#-compatibility--assumptions)
- [🛠️ Installation](#-installation)
- [⚡ Quick Start](#-quick-start)
- [⚙️ Configuration](#-configuration)
- [▶️ Usage](#-usage)
- [🧭 Operational Runbooks](#-operational-runbooks)
- [📡 API Snapshot](#-api-snapshot)
- [🧪 Examples](#-examples)
- [🧱 Development Notes](#-development-notes)
- [🔐 Safety Notes](#-safety-notes)
- [🔧 Troubleshooting](#-troubleshooting)
- [🌐 README & i18n Workflow](#-readme--i18n-workflow)
- [📘 Readme Generation Context](#-readme-generation-context)
- [❓ FAQ](#-faq)
- [🗺️ Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [❤️ Support](#-support)
- [📄 License](#-license)

## 🧭 Repository Snapshot

| Focus | Current setup |
| --- | --- |
| Core loop | Plan → Work → Debug → Fix → Summary → Commit/Push |
| Runtime model | Tornado backend + static PWA controller |
| State machine | `start` / `pause` / `resume` / `stop` |
| Persistence | PostgreSQL-first with JSON fallback compatibility |
| Documentation | Canonical `README.md` plus multilingual `i18n/` outputs |

## 🚀 Overview
AutoAppDev 是一個面向長時間執行且可恢復的應用開發 pipeline 控制器專案，整合了：

1. 以 Tornado 為基礎、並由 PostgreSQL 支援持久化的後端 API（儲存層同時包含本機 JSON fallback 相容行為）。
2. 類 Scratch 的靜態 PWA 控制介面。
3. 用於 pipeline 編寫、可決定性程式碼生成、自我開發循環與 README 自動化的腳本與文件。

本專案針對可預測的 agent 執行進行最佳化，採用嚴格順序與以產出物為導向的工作流歷史。

### 🎨 為何建立這個儲存庫

| Theme | 實務上的意義 |
| --- | --- |
| Determinism | 透過 Canonical pipeline IR + parser/import/codegen 工作流，追求可重現性 |
| Resumability | 以明確 lifecycle state machine（`start/pause/resume/stop`）支援長流程執行 |
| Operability | 具備 runtime 日誌、inbox/outbox 通道與腳本化驗證循環 |
| Documentation-first | 契約／規格／範例集中於 `docs/`，並搭配自動化多語 README 流程 |

## 🧭 Philosophy
AutoAppDev 將 agent 視為工具，並透過嚴格且可恢復的循環維持工作穩定：

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

控制器應用程式也希望以類 Scratch 的區塊／動作體現同一套概念（包含共用 `update_readme` action），讓每個 workspace 都能保持最新且可重現。

### 🔁 Lifecycle 狀態意圖

| State transition | Operational intent |
| --- | --- |
| `start` | 從停止／就緒狀態啟動 pipeline |
| `pause` | 安全暫停長時間執行，且不遺失上下文 |
| `resume` | 從已保存的執行狀態／產出物繼續 |
| `stop` | 結束執行並回到非執行狀態 |

## ✨ Features
- 可恢復的 pipeline 生命週期控制：start、pause、resume、stop。
- AAPS pipeline script（`.aaps`）與 canonical IR（`autoappdev_ir` v1）的腳本庫 API。
- 可決定性的 parser/import pipeline：
  - 解析格式化 AAPS scripts。
  - 透過 `# AAPS:` 註解匯入帶註釋 shell。
  - 可選的 Codex 輔助 parse fallback（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- Action registry：內建動作 + 可編輯／自定義動作（內建唯讀需 clone/edit）。
- 類 Scratch PWA 區塊與執行期載入 action palette（`GET /api/actions`）。
- Runtime 訊息通道：
  - Inbox（`/api/inbox`）用於 operator -> pipeline 指示。
  - Outbox（`/api/outbox`）包含從 `runtime/outbox` 佇列檔案的匯入。
- 後端與 pipeline 日誌增量串流（`/api/logs`, `/api/logs/tail`）。
- 從 canonical IR 進行可決定性 runner codegen（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用於儲存庫迭代演進的 self-dev driver（`scripts/auto-autoappdev-development.sh`）。
- `i18n/` 下具備多語生成框架的 README 自動化 pipeline。

## 📌 At A Glance

| Area | Details |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | PostgreSQL-first with compatibility behavior in `backend/storage.py` |
| Pipeline model | Canonical IR (`autoappdev_ir` v1) and AAPS script format |
| Control flow | Start / Pause / Resume / Stop lifecycle |
| Dev mode | Resumable self-dev loop + deterministic script/codegen workflows |
| README/i18n | Automated README pipeline with `i18n/` scaffolding |

## 🏗️ Architecture

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

### Backend responsibilities
- 對外提供控制器 API：scripts、actions、plan、pipeline lifecycle、logs、inbox/outbox、workspace config。
- 驗證並持久化 pipeline script 產出物。
- 協調 pipeline 執行狀態與狀態轉換。
- 在 DB pool 不可用時，提供可決定性的 fallback 行為。

### Frontend responsibilities
- 呈現類 Scratch 區塊 UI 與 pipeline 編輯流程。
- 由後端 registry 動態載入 action palette。
- 驅動 lifecycle 控制並監控 status/logs/messages。

## 📚 Contents
常用文件、腳本與範例的參考地圖：

- `docs/auto-development-guide.md`: 長時間、可恢復自動開發 agent 的雙語（EN/ZH）理念與需求。
- `docs/ORDERING_RATIONALE.md`: 截圖驅動步驟排序的示例說明。
- `docs/controller-mvp-scope.md`: 控制器 MVP 範圍（畫面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`: 可決定性的手動端到端 Demo 清單（backend + PWA happy path）。
- `docs/env.md`: 環境變數（`.env`）慣例。
- `docs/api-contracts.md`: 控制器 API 請求／回應契約。
- `docs/pipeline-formatted-script-spec.md`: 標準 pipeline script 格式（AAPS）與 canonical IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`: 從 canonical IR 產生可執行 bash pipeline runner 的可決定性生成器。
- `docs/common-actions.md`: 常見 action 契約／規格（包含 `update_readme`）。
- `docs/workspace-layout.md`: 標準 workspace 目錄與契約（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`: 在 tmux 中啟動 AutoAppDev app（backend + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`: 在 tmux 中啟動 AutoAppDev self-dev driver。
- `scripts/app-auto-development.sh`: 線性 pipeline driver（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`），支援 resume/state。
- `scripts/generate_screenshot_docs.sh`: 截圖 -> Markdown 描述生成器（Codex 驅動）。
- `scripts/setup_autoappdev_env.sh`: 本機執行主要 conda 環境建置腳本。
- `scripts/setup_backend_env.sh`: 後端環境輔助腳本。
- `examples/ralph-wiggum-example.sh`: Codex CLI 自動化輔助範例。

## 🗂️ Project Structure
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

## ✅ Prerequisites
- 具備 `bash` 的作業系統。
- Python `3.11+`。
- 用於既有 setup scripts 的 Conda（`conda`）。
- 用於一鍵 backend+PWA 或 self-dev session 的 `tmux`。
- `DATABASE_URL` 可連線的 PostgreSQL。
- 選配：`codex` CLI（用於 Codex 流程：self-dev、parse-llm fallback、auto-readme pipeline）。

快速需求矩陣：

| Component | Required | Purpose |
| --- | --- | --- |
| `bash` | Yes | Script execution |
| Python `3.11+` | Yes | Backend + codegen tooling |
| Conda | Yes (recommended flow) | Environment bootstrap scripts |
| PostgreSQL | Yes (preferred mode) | Primary persistence via `DATABASE_URL` |
| `tmux` | Recommended | Managed backend/PWA and self-dev sessions |
| `codex` CLI | Optional | LLM-assisted parse and README/self-dev automation |

## 🧩 Compatibility & Assumptions

| Topic | Current expectation |
| --- | --- |
| Local OS | Linux/macOS shells are the primary target (`bash` scripts) |
| Python runtime | `3.11` (managed by `scripts/setup_autoappdev_env.sh`) |
| Persistence mode | PostgreSQL is preferred and treated as canonical |
| Fallback behavior | `backend/storage.py` includes JSON compatibility fallback for degraded scenarios |
| Network model | Localhost split-port development (backend + static PWA) |
| Agent tooling | `codex` CLI is optional unless using LLM-assisted parse or self-dev automation |

本 README 使用以下假設：
- 除非章節另有說明，否則你會在儲存庫根目錄執行命令。
- 啟動 backend 服務前，`.env` 已完成設定。
- 建議的一鍵流程假設 `conda` 與 `tmux` 可用。

## 🛠️ Installation
### 1) Clone 並進入儲存庫
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) 設定環境
```bash
cp .env.example .env
```
編輯 `.env`，至少設定：
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` and `AUTOAPPDEV_PORT` (or `PORT`)

### 3) 建立／更新 backend 環境
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) 套用資料庫 schema
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) 選配：資料庫 smoke test
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Quick Start
```bash
# from repo root
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

接著開啟：
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

一行命令進行 smoke-check：
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

快速端點地圖：

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
主要檔案：`.env`（參見 `docs/env.md` 與 `.env.example`）。

### Important variables

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

快速驗證 `.env`：
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

## ▶️ Usage

| Mode | Command | Notes |
| --- | --- | --- |
| Start backend + PWA (recommended) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Start backend only | `conda run -n autoappdev python -m backend.app` | Uses `.env` bind + DB settings |
| Start PWA static server only | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Useful for frontend-only checks |
| Run self-dev driver in tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Resumable self-development loop |

### 常用腳本選項
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### 解析並儲存 scripts
- 透過 API 解析 AAPS：`POST /api/scripts/parse`
- 匯入帶註釋 shell：`POST /api/scripts/import-shell`
- 選配 LLM parse：`POST /api/scripts/parse-llm`（需 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### Pipeline 控制 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 其他常用 API
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

請參閱 `docs/api-contracts.md` 了解請求／回應格式。

## 🧭 Operational Runbooks

### Runbook: 啟動完整本機堆疊
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

驗證檢查點：
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- 開啟 `http://127.0.0.1:5173/`，確認 UI 可載入 `/api/config`。
- 選配：開啟 `/api/version`，確認回傳預期後端 metadata。

### Runbook: 僅 backend 除錯
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: 可決定性 codegen smoke
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

## 📡 API Snapshot

核心 API 群組一覽：

| Category | Endpoints |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan model | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET /api/logs/tail` |
| Workspace settings | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Examples
### AAPS 範例
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

完整範例：
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### 可決定性 runner 生成
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### 可決定性 demo pipeline
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
接著使用 PWA 的 Start/Pause/Resume/Stop 控制，並檢查 `/api/logs`。

### 從帶註釋 shell 匯入
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 Development Notes
- Backend 基於 Tornado，並針對本機開發體驗設計（包含針對 localhost 分離連接埠的寬鬆 CORS）。
- 儲存層採 PostgreSQL-first，並在 `backend/storage.py` 提供相容 fallback 行為。
- PWA block keys 與 script `STEP.block` 值刻意對齊（`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`）。
- 內建 actions 為唯讀；修改前請先 clone。
- `update_readme` action 受路徑安全限制，只允許工作區 `auto-apps/<workspace>/README.md` 目標。
- 某些 docs/scripts 仍有歷史路徑／名稱參考（`HeyCyan`, `LightMind`），源於專案演進。當前 canonical path 為本儲存庫根目錄。
- 根目錄 `i18n/` 已存在，多語 README 預期放置於此。

### 工作模型與狀態檔
- Runtime 預設為 `./runtime`，除非以 `AUTOAPPDEV_RUNTIME_DIR` 覆寫。
- Self-dev 自動化狀態／歷史記錄於 `references/selfdev/`。
- README pipeline 產出物記錄於 `.auto-readme-work/<timestamp>/`。

### 測試現況（目前）
- 儲存庫包含 smoke checks 與可決定性 demo scripts。
- 根目錄 metadata 目前尚未定義完整頂層自動化測試套件／CI manifest。
- 假設：目前驗證主要以腳本驅動（`scripts/pipeline_codegen/smoke_*.sh`、`backend.db_smoketest`、端到端 checklist）。

## 🔐 Safety Notes
- `update_readme` action 明確限制於工作區 README 目標（`auto-apps/<workspace>/README.md`），並具備路徑穿越防護。
- Action registry 驗證會強制 action spec 欄位正規化，並限制支援推理等級的值範圍。
- 儲存庫腳本假設在受信任本機環境執行；若在共享或接近正式環境使用，請先審閱腳本內容。
- `.env` 可能包含敏感值（`DATABASE_URL`、API keys）。請勿提交 `.env`，並在本機開發之外採用環境級秘密管理。

## 🔧 Troubleshooting

| Symptom | What to check |
| --- | --- |
| `tmux not found` | Install `tmux` or run backend/PWA manually. |
| Backend fails on startup due to missing env | Recheck `.env` against `.env.example` and `docs/env.md`. |
| Database errors (connection/auth/schema) | Verify `DATABASE_URL`; re-run `conda run -n autoappdev python -m backend.apply_schema`; optional connectivity check: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA loads but cannot call API | Ensure backend is listening on expected host/port; regenerate `pwa/config.local.js` by re-running `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start returns invalid transition | Check current pipeline status first; start from `stopped` state. |
| No log updates in UI | Confirm `runtime/logs/pipeline.log` is being written; use `/api/logs` and `/api/logs/tail` directly to isolate UI vs backend issues. |
| LLM parse endpoint returns disabled | Set `AUTOAPPDEV_ENABLE_LLM_PARSE=1` and restart backend. |
| `conda run -n autoappdev ...` fails | Re-run `./scripts/setup_autoappdev_env.sh`; confirm conda env `autoappdev` exists (`conda env list`). |
| Wrong API target in frontend | Confirm `pwa/config.local.js` exists and points to active backend host/port. |

如需可決定性的手動驗證路徑，請使用 `docs/end-to-end-demo-checklist.md`。

## 🌐 README & i18n Workflow
- 根 README 是 README 自動化 pipeline 的 canonical source。
- 多語版本預期位於 `i18n/`。
- i18n 目錄狀態：✅ 此儲存庫已存在。
- 目前此儲存庫的語言集合：
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
- 每個 README 變體頂部都應保持單一語言導覽列（不可重複）。
- README pipeline 入口：`prompt_tools/auto-readme-pipeline.sh`。

### i18n 生成限制（嚴格）
- 更新 canonical README 內容時，必須始終處理多語生成。
- 語言檔需逐一（序列式）生成／更新，不得使用模糊的批次流程。
- 每個變體頂部只能有一行 language-options 導覽列。
- 同一檔案中不得重複語言列。
- 翻譯時保留 canonical 命令片段、連結、API 路徑與 badge 意圖。

建議逐一生成順序：
1. `i18n/README.ar.md`
2. `i18n/README.de.md`
3. `i18n/README.es.md`
4. `i18n/README.fr.md`
5. `i18n/README.ja.md`
6. `i18n/README.ko.md`
7. `i18n/README.ru.md`
8. `i18n/README.vi.md`
9. `i18n/README.zh-Hans.md`
10. `i18n/README.zh-Hant.md`

語言覆蓋表：

| Language | File |
| --- | --- |
| Arabic | `i18n/README.ar.md` |

觀察到的 workspace 備註：
- `i18n/README.zh-Hant.md.tmp` 可能作為暫存翻譯產物出現；最終 canonical 檔案需維持為 `README.<lang>.md`。

## 📘 Readme Generation Context

- Pipeline run timestamp: `20260301_095119`
- Trigger: `./README.md` first complete draft generation (canonical-base incremental update)
- Input user prompt: `Use current README as canonical base. No reduction: only increment and improve. Preserve existing content, links, badges, commands, and details. Always process multilingual generation (do not skip): ensure i18n exists and generate/update language files one-by-one with a single language-options line at the top and no duplicates.`
- Goal: generate a complete, beautiful README draft with required sections and support information
- Source snapshot used:
  - `./.auto-readme-work/20260301_095119/pipeline-context.md`
  - `./.auto-readme-work/20260301_095119/repo-structure-analysis.md`
- 此檔案由儲存庫內容生成，並作為 canonical draft 入口保留。

## ❓ FAQ

### PostgreSQL 是強制的嗎？
一般運作建議且預期使用 PostgreSQL。儲存層雖有 fallback 相容行為，但在接近正式的使用情境下，仍應假設 `DATABASE_URL` 可用。

### 為什麼同時有 `AUTOAPPDEV_PORT` 與 `PORT`？
`AUTOAPPDEV_PORT` 是專案專用設定；`PORT` 是部署友善別名。除非你有意覆寫啟動行為，否則建議保持一致。

### 若我只想看 API，該從哪開始？
以 backend-only 方式啟動（`conda run -n autoappdev python -m backend.app`），先檢查 `/api/health`、`/api/version`、`/api/config`，再依 `docs/api-contracts.md` 查看 scripts/actions 端點。

### 多語 README 會自動生成嗎？
會。儲存庫提供 `prompt_tools/auto-readme-pipeline.sh`，語言版本維護於 `i18n/`，且每個版本頂部都維持單一語言導覽列。

## 🗺️ Roadmap
- 完成目前 `51 / 55` 之外的剩餘 self-dev 任務。
- 擴展 workspace/materials/context 工具與更強的安全路徑契約。
- 持續改進 action palette UX 與可編輯 action 工作流。
- 深化 `i18n/` 與 runtime 語言切換的多語 README/UI 支援。
- 強化 smoke/integration 檢查與 CI 覆蓋（目前已有腳本化 smoke checks，根目錄尚無完整 CI manifest）。
- 持續強化 AAPS v1 與 canonical IR 的 parser/import/codegen 可決定性。

## 🤝 Contributing
歡迎透過 issue 與 pull request 參與貢獻。

建議流程：
1. Fork 並建立 feature branch。
2. 讓變更保持聚焦且可重現。
3. 優先提供可決定性的 scripts/tests。
4. 行為或契約變更時同步更新文件（`docs/*`、API contracts、examples）。
5. 提交 PR 並附上背景、驗證步驟與任何 runtime 假設。

目前儲存庫 remote 包含：
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 本機 clone 可能含有其他相關儲存庫 remote（此 workspace 觀察到範例：`novel`）。

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

在此儲存庫快照中，未偵測到根目錄 `LICENSE` 檔案。

假設說明：
- 在新增授權檔之前，使用／再散佈條款視為未明確，請先向維護者確認。
