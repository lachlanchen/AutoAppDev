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

可複用指令碼與指南，使用 Codex 作為非互動式工具，從截圖/Markdown 逐步構建應用。

> 🎯 **使命：** 讓應用開發流水線具備確定性、可恢復、並以工件為驅動。
>
> 🧩 **設計原則：** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ 專案訊號

| 訊號 | 目前方向 |
| --- | --- |
| 執行時模型 | Tornado backend + static PWA controller |
| 流水線執行 | 確定性且可恢復（`start/pause/resume/stop`） |
| 持久化策略 | PostgreSQL 優先，並帶相容回退行為 |
| 文件流程 | 以根 README 為規範來源，並自動生成 `i18n/` 變體 |

### 🔗 快速導航

| 需求 | 前往 |
| --- | --- |
| 首次本地執行 | [⚡ 快速開始](#-快速開始) |
| 環境與必需變數 | [⚙️ 配置](#️-配置) |
| API 總覽 | [📡 API 快照](#-api-快照) |
| 執行/除錯手冊 | [🧭 運維 Runbook](#-運維-runbook) |
| README/i18n 生成規則 | [🌐 README 與 i18n 工作流](#-readme-與-i18n-工作流) |
| 故障排查矩陣 | [🔧 故障排查](#-故障排查) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## 自研狀態（自動更新）

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

本節由 `scripts/auto-autoappdev-development.sh` 自動更新。
請勿編輯標記之間的內容。

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ 目錄
- [🚀 概覽](#-概覽)
- [🧭 方法論](#-方法論)
- [✨ 功能特性](#-功能特性)
- [📌 一覽](#-一覽)
- [🏗️ 架構](#️-架構)
- [📚 內容索引](#-內容索引)
- [🗂️ 專案結構](#️-專案結構)
- [✅ 前置要求](#-前置要求)
- [🧩 相容性與假設](#-相容性與假設)
- [🛠️ 安裝](#️-安裝)
- [⚡ 快速開始](#-快速開始)
- [⚙️ 配置](#️-配置)
- [▶️ 使用方式](#️-使用方式)
- [🧭 運維 Runbook](#-運維-runbook)
- [📡 API 快照](#-api-快照)
- [🧪 示例](#-示例)
- [🧱 開發說明](#-開發說明)
- [🔐 安全說明](#-安全說明)
- [🔧 故障排查](#-故障排查)
- [🌐 README 與 i18n 工作流](#-readme-與-i18n-工作流)
- [❓ FAQ](#-faq)
- [🗺️ 路線圖](#️-路線圖)
- [🤝 貢獻](#-貢獻)
- [❤️ Support](#-support)
- [📄 許可證](#-許可證)
- [❤️ 贊助與捐贈](#️-贊助與捐贈)

## 🚀 概覽
AutoAppDev 是一個面向長時間執行、可恢復的應用開發流水線控制器專案，組合了：

1. 使用 PostgreSQL 持久化（並在儲存程式碼中提供本地 JSON 回退行為）的 Tornado 後端 API。
2. 類 Scratch 的靜態 PWA 控制器介面。
3. 用於流水線編寫、確定性程式碼生成、自研迴圈與 README 自動化的指令碼和文件。

該專案針對可預測的代理執行進行了最佳化，採用嚴格順序和麵向工件的工作流歷史。

### 🎨 為什麼存在這個倉庫

| 主題 | 實際含義 |
| --- | --- |
| 確定性 | 規範化流水線 IR + parser/import/codegen 工作流，強調可重複性 |
| 可恢復 | 對長時間執行任務使用顯式生命週期狀態機（`start/pause/resume/stop`） |
| 可運維性 | 執行日誌、inbox/outbox 通道，以及指令碼驅動的驗證迴圈 |
| 文件優先 | 合同/規範/示例位於 `docs/`，並配套自動化多語言 README 流程 |

## 🧭 方法論
AutoAppDev 將代理視為工具，透過嚴格、可恢復的迴圈來保持工作穩定：

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

控制器應用旨在以類 Scratch 的塊/動作體現同樣概念（包括通用 `update_readme` action），從而讓每個工作區都保持最新且可復現。

### 🔁 生命週期狀態意圖

| 狀態遷移 | 執行意圖 |
| --- | --- |
| `start` | 從 stopped/ready 狀態開始流水線 |
| `pause` | 在不丟失上下文的前提下安全暫停長任務 |
| `resume` | 從儲存的執行時狀態/工件繼續執行 |
| `stop` | 結束執行並回到非執行狀態 |

## ✨ 功能特性
- 可恢復的流水線生命週期控制：start、pause、resume、stop。
- 面向 AAPS 流水線指令碼（`.aaps`）和規範 IR（`autoappdev_ir` v1）的指令碼庫 API。
- 確定性的 parser/import 流程：
  - 解析格式化 AAPS 指令碼。
  - 透過 `# AAPS:` 註釋匯入標註過的 shell。
  - 可選的 Codex 輔助解析回退（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 動作登錄檔支援內建動作 + 可編輯/自定義動作（只讀內建動作可 clone/edit）。
- 類 Scratch PWA 積木與執行時載入動作面板（`GET /api/actions`）。
- 執行時訊息通道：
  - Inbox（`/api/inbox`）用於操作員 -> 流水線指導。
  - Outbox（`/api/outbox`）包含從 `runtime/outbox` 的檔案佇列攝取。
- 後端與流水線日誌增量流式輸出（`/api/logs`, `/api/logs/tail`）。
- 從規範 IR 進行確定性 runner 程式碼生成（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用於倉庫迭代演進的自研驅動（`scripts/auto-autoappdev-development.sh`）。
- README 自動化流水線及 `i18n/` 下的多語言生成腳手架。

## 📌 一覽

| 區域 | 詳情 |
| --- | --- |
| 核心執行時 | Tornado backend + static PWA frontend |
| 持久化 | PostgreSQL 優先，並在 `backend/storage.py` 內提供相容行為 |
| 流水線模型 | 規範 IR（`autoappdev_ir` v1）與 AAPS 指令碼格式 |
| 控制流 | Start / Pause / Resume / Stop 生命週期 |
| 開發模式 | 可恢復自研迴圈 + 確定性指令碼/codegen 工作流 |
| README/i18n | 帶 `i18n/` 腳手架的自動化 README 流水線 |

## 🏗️ 架構

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

### Backend 職責
- 暴露控制器 API：scripts、actions、plan、pipeline lifecycle、logs、inbox/outbox、workspace config。
- 校驗並持久化流水線指令碼資產。
- 協調流水線執行狀態與狀態遷移。
- 在 DB 連線池不可用時提供確定性回退行為。

### Frontend 職責
- 渲染類 Scratch 積木 UI 與流水線編輯流程。
- 從後端登錄檔動態載入動作面板。
- 驅動生命週期控制並監控狀態/日誌/訊息。

## 📚 內容索引
最常用文件、指令碼與示例的參考對映：

- `docs/auto-development-guide.md`：長期執行、可恢復自動開發代理的方法論與要求（中英雙語）。
- `docs/ORDERING_RATIONALE.md`：截圖驅動步驟排序的示例依據。
- `docs/controller-mvp-scope.md`：控制器 MVP 範圍（頁面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`：確定性手動端到端演示檢查清單（backend + PWA happy path）。
- `docs/env.md`：環境變數（`.env`）約定。
- `docs/api-contracts.md`：控制器 API 請求/響應契約。
- `docs/pipeline-formatted-script-spec.md`：標準流水線指令碼格式（AAPS）與規範 IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`：從規範 IR 生成可執行 bash pipeline runner 的確定性生成器。
- `docs/common-actions.md`：通用 action 契約/規範（含 `update_readme`）。
- `docs/workspace-layout.md`：標準工作區目錄 + 契約（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`：在 tmux 中啟動 AutoAppDev 應用（backend + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`：在 tmux 中啟動 AutoAppDev 自研驅動。
- `scripts/app-auto-development.sh`：線性流水線驅動（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`），支援 resume/state。
- `scripts/generate_screenshot_docs.sh`：截圖 -> Markdown 描述生成器（Codex 驅動）。
- `scripts/setup_autoappdev_env.sh`：本地執行主 conda 環境引導指令碼。
- `scripts/setup_backend_env.sh`：後端環境輔助指令碼。
- `examples/ralph-wiggum-example.sh`：Codex CLI 自動化助手示例。

## 🗂️ 專案結構
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
- 具備 `bash` 的作業系統。
- Python `3.11+`。
- 用於安裝指令碼的 Conda（`conda`）。
- 用於一鍵 backend+PWA 或自研會話的 `tmux`。
- `DATABASE_URL` 可達的 PostgreSQL。
- 可選：`codex` CLI（用於 Codex 驅動流程：self-dev、parse-llm 回退、auto-readme 流水線）。

快速要求矩陣：

| 元件 | 必需性 | 用途 |
| --- | --- | --- |
| `bash` | 是 | 指令碼執行 |
| Python `3.11+` | 是 | 後端 + codegen 工具 |
| Conda | 是（推薦流程） | 環境引導指令碼 |
| PostgreSQL | 是（首選模式） | 透過 `DATABASE_URL` 進行主持久化 |
| `tmux` | 推薦 | 託管 backend/PWA 與 self-dev 會話 |
| `codex` CLI | 可選 | LLM 輔助解析與 README/self-dev 自動化 |

## 🧩 相容性與假設

| 主題 | 當前預期 |
| --- | --- |
| 本地 OS | 主要目標為 Linux/macOS shell（`bash` 指令碼） |
| Python 執行時 | `3.11`（由 `scripts/setup_autoappdev_env.sh` 管理） |
| 持久化模式 | PostgreSQL 為首選並視為規範方案 |
| 回退行為 | `backend/storage.py` 在降級場景中包含 JSON 相容回退 |
| 網路模型 | 本地 localhost 分埠開發（backend + static PWA） |
| 代理工具 | 除非使用 LLM 輔助解析或 self-dev 自動化，否則 `codex` CLI 為可選 |

本 README 使用的假設：
- 除非章節另有說明，你在倉庫根目錄執行命令。
- 啟動後端服務前，`.env` 已完成配置。
- 推薦的一鍵工作流依賴 `conda` 與 `tmux`。

## 🛠️ 安裝
### 1) 克隆並進入倉庫
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) 配置環境
```bash
cp .env.example .env
```
編輯 `.env` 並至少設定：
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` 和 `AUTOAPPDEV_PORT`（或 `PORT`）

### 3) 建立/更新後端環境
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) 應用資料庫 schema
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) 可選：資料庫 smoke test
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ 快速開始
```bash
# from repo root
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

然後開啟：
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

一條命令做 smoke-check：
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

快速端點對映：

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ 配置
主配置檔案：`.env`（參見 `docs/env.md` 與 `.env.example`）。

### 重要變數

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

快速校驗 `.env`：
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

| 模式 | 命令 | 說明 |
| --- | --- | --- |
| 啟動 backend + PWA（推薦） | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`，PWA `http://127.0.0.1:5173/` |
| 僅啟動 backend | `conda run -n autoappdev python -m backend.app` | 使用 `.env` 裡的繫結與 DB 設定 |
| 僅啟動 PWA 靜態服務 | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | 適合僅前端檢查 |
| 在 tmux 執行 self-dev 驅動 | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 可恢復自研迴圈 |

### 常用指令碼引數
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### 解析並儲存指令碼
- 透過 API 解析 AAPS：`POST /api/scripts/parse`
- 匯入帶註釋 shell：`POST /api/scripts/import-shell`
- 可選 LLM 解析：`POST /api/scripts/parse-llm`（需要 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### 流水線控制 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 其他高頻 API
- 健康/版本/配置：`/api/health`, `/api/version`, `/api/config`
- 計劃/指令碼：`/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- 動作：`/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- 訊息：`/api/chat`, `/api/inbox`, `/api/outbox`
- 日誌：`/api/logs`, `/api/logs/tail`

請求/響應結構見 `docs/api-contracts.md`。

## 🧭 運維 Runbook

### Runbook：拉起完整本地棧
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

驗證檢查點：
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- 開啟 `http://127.0.0.1:5173/`，確認 UI 能載入 `/api/config`。
- 可選：開啟 `/api/version`，確認返回預期後端後設資料。

### Runbook：僅後端除錯
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook：確定性 codegen smoke
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

核心 API 分組一覽：

| 分類 | 端點 |
| --- | --- |
| 健康 + 執行時資訊 | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan 模型 | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action 登錄檔 | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline 執行時 | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| 訊息 + 日誌 | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
| 工作區設定 | `GET/POST /api/workspaces/<name>/config` |

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

### 確定性 runner 生成
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### 確定性演示流水線
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
然後使用 PWA 的 Start/Pause/Resume/Stop 控制元件，並檢查 `/api/logs`。

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

## 🧱 開發說明
- 後端基於 Tornado，針對本地開發體驗設計（包括對 localhost 分埠的寬鬆 CORS）。
- 儲存層為 PostgreSQL 優先，並在 `backend/storage.py` 中提供相容行為。
- PWA 的 block key 與指令碼 `STEP.block` 值有意保持一致（`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`）。
- 內建動作為只讀；編輯前請先 clone。
- `update_readme` action 受到路徑安全約束，僅允許更新 `auto-apps/<workspace>/README.md` 下的工作區 README 目標。
- 部分文件/指令碼仍保留歷史路徑或命名（`HeyCyan`, `LightMind`），繼承於專案演進過程。當前倉庫規範路徑是本倉庫根目錄。
- 根目錄 `i18n/` 已存在。多語言執行期望語言 README 檔案放在此目錄。

### 工作模型與狀態檔案
- 執行時預設目錄為 `./runtime`，可透過 `AUTOAPPDEV_RUNTIME_DIR` 覆蓋。
- 自研自動化狀態/歷史記錄位於 `references/selfdev/`。
- README 流水線工件記錄在 `.auto-readme-work/<timestamp>/`。

### 測試現狀（當前）
- 倉庫包含 smoke 檢查與確定性演示指令碼。
- 根後設資料中目前未定義完整的頂層自動化測試套件/CI 清單。
- 當前假設：驗證主要由指令碼驅動（`scripts/pipeline_codegen/smoke_*.sh`、`backend.db_smoketest`、端到端檢查清單）。

## 🔐 安全說明
- `update_readme` action 被有意限制為工作區 README 目標（`auto-apps/<workspace>/README.md`），並帶有路徑穿越防護。
- Action 登錄檔校驗會強制規範化 action spec 欄位，並對支援的 reasoning level 值做邊界限制。
- 倉庫指令碼假設在可信本地環境執行；在共享環境或接近生產的環境執行前請先審閱指令碼內容。
- `.env` 可能包含敏感值（`DATABASE_URL`、API keys）。請勿提交 `.env`，並在本地開發之外使用環境級金鑰管理。

## 🔧 故障排查

| 症狀 | 檢查項 |
| --- | --- |
| `tmux not found` | 安裝 `tmux`，或手動分別執行 backend/PWA。 |
| 後端啟動因缺少環境變數失敗 | 對照 `.env.example` 與 `docs/env.md` 複查 `.env`。 |
| 資料庫錯誤（連線/認證/schema） | 檢查 `DATABASE_URL`；重新執行 `conda run -n autoappdev python -m backend.apply_schema`；可選連通性檢查：`conda run -n autoappdev python -m backend.db_smoketest`。 |
| PWA 能開啟但無法呼叫 API | 確認 backend 在預期 host/port 監聽；重新執行 `./scripts/run_autoappdev_tmux.sh` 生成 `pwa/config.local.js`。 |
| Pipeline Start 返回 invalid transition | 先檢查當前 pipeline 狀態；從 `stopped` 狀態啟動。 |
| UI 沒有日誌更新 | 確認 `runtime/logs/pipeline.log` 正在寫入；直接呼叫 `/api/logs` 與 `/api/logs/tail` 以隔離 UI 或 backend 問題。 |
| LLM parse endpoint 顯示 disabled | 設定 `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 並重啟 backend。 |
| `conda run -n autoappdev ...` 失敗 | 重新執行 `./scripts/setup_autoappdev_env.sh`；確認 conda 環境 `autoappdev` 存在（`conda env list`）。 |
| 前端 API 目標錯誤 | 確認 `pwa/config.local.js` 存在且指向當前 backend host/port。 |

如需確定性的手動驗證路徑，請使用 `docs/end-to-end-demo-checklist.md`。

## 🌐 README 與 i18n 工作流
- 根 README 是 README 自動化流水線使用的規範來源。
- 多語言變體應放在 `i18n/` 下。
- i18n 目錄狀態：✅ 本倉庫已存在。
- 本倉庫當前語言集合：
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
- 每個 README 變體頂部都應保持單行語言導航（不要重複語言欄）。
- README 流水線入口：`prompt_tools/auto-readme-pipeline.sh`。

### i18n 生成約束（嚴格）
- 更新規範 README 內容時，始終要處理多語言生成。
- 逐個語言檔案順序生成/更新，不要批次混合處理。
- 每個變體頂部保持且僅保持一條 language-options 導航行。
- 不要在同一個檔案中重複語言欄。
- 在翻譯中保留規範命令片段、連結、API 路徑和徽章意圖。

建議逐個生成順序：
1. `README.md`（規範英文源）
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

語言覆蓋表：

| Language | File |
| --- | --- |

## ❓ FAQ

### PostgreSQL 是必須的嗎？
正常執行場景下推薦且預設應使用 PostgreSQL。儲存層包含回退相容行為，但類生產使用應假設 `DATABASE_URL` 可用並指向 PostgreSQL。

### 為什麼同時有 `AUTOAPPDEV_PORT` 和 `PORT`？
`AUTOAPPDEV_PORT` 是專案專用變數。`PORT` 作為更通用的部署別名存在。除非你有意在啟動路徑中覆蓋行為，否則應保持兩者一致。

### 如果我只想檢視 API，從哪裡開始？
僅啟動 backend（`conda run -n autoappdev python -m backend.app`），然後依次訪問 `/api/health`、`/api/version`、`/api/config`，再檢視 `docs/api-contracts.md` 中列出的 script/action 端點。

### 多語言 README 會自動生成嗎？
會。倉庫包含 `prompt_tools/auto-readme-pipeline.sh`，語言變體維護在 `i18n/` 下，並在每個變體頂部保留單行語言導航。

## 🗺️ 路線圖
- 完成當前 `51 / 55` 之外的剩餘 self-dev 任務。
- 擴充套件 workspace/materials/context 工具與更強的安全路徑契約。
- 繼續改進 action palette UX 與可編輯 action 工作流。
- 持續增強 `i18n/` 與執行時語言切換的多語言 README/UI 支援。
- 強化 smoke/integration 檢查與 CI 覆蓋（當前已有指令碼驅動 smoke 檢查；根目錄尚無完整 CI 清單文件）。
- 持續加固圍繞 AAPS v1 與規範 IR 的 parser/import/codegen 確定性。

## 🤝 貢獻
歡迎透過 issue 和 pull request 參與貢獻。

建議流程：
1. Fork 並建立功能分支。
2. 保持改動聚焦且可復現。
3. 儘可能優先使用確定性指令碼/測試。
4. 當行為/契約變化時同步更新文件（`docs/*`、API 契約、示例）。
5. 提交 PR 時附上背景、驗證步驟與任何執行時假設。

當前倉庫遠端包含：
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 在本地克隆中可能還存在與相關倉庫關聯的附加 remote（本工作區示例：`novel`）。

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 許可證
當前倉庫快照中未檢測到根目錄 `LICENSE` 檔案。

假設說明：
- 在補充許可證檔案前，請將使用/再分發條款視為未明確，並與維護者確認。

## ❤️ 贊助與捐贈
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400

如果這個專案對你的工作流有幫助，贊助將直接支援持續的 self-dev 任務、文件質量提升和工具鏈加固。
