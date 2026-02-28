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

使用 Codex 作為非互動工具，從截圖／Markdown 逐步建構應用的可重複使用腳本與指南。

> 🎯 **使命：** 讓應用開發流程具備可預測、可恢復、且以產物為導向的特性。
>
> 🧩 **設計原則：** Plan -> Work -> Verify -> Summary -> Commit/Push。

---

### 🎛️ 專案訊號

| 指標 | 當前方向 |
| --- | --- |
| 運行時模型 | Tornado 後端 + 靜態 PWA 控制器 |
| 流程執行 | 決定論且可恢復（`start/pause/resume/stop`） |
| 持久化策略 | PostgreSQL 優先，並具備相容降級行為 |
| 文件流程 | 以根 README 為規範來源，並使用自動化 `i18n/` 變體 |

### 🔗 快速導覽

| 需求 | 前往 |
| --- | --- |
| 首次本機執行 | [⚡ 快速開始](#-快速開始) |
| 環境與必要變數 | [⚙️ 設定](#-設定) |
| API 全貌 | [📡 API 快照](#-api-快照) |
| 運行與除錯手冊 | [🧭 作業手冊](#-作業手冊) |
| README / i18n 生成規則 | [🌐 README 與 i18n 工作流](#-readme-與-i18n-工作流) |
| 故障排查矩陣 | [🔧 疑難排解](#-疑難排解) |

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
- [🚀 概述](#-概述)
- [🧭 哲學](#-哲學)
- [✨ 功能](#-功能)
- [📌 一目了然](#-一目了然)
- [🏗️ 架構](#-架構)
- [📚 內容](#-內容)
- [🗂️ 專案結構](#-專案結構)
- [✅ 前置需求](#-前置需求)
- [🧩 相容性與假設](#-相容性與假設)
- [🛠️ 安裝](#-安裝)
- [⚡ 快速開始](#-快速開始)
- [⚙️ 設定](#-設定)
- [▶️ 使用方式](#-使用方式)
- [🧭 作業手冊](#-作業手冊)
- [📡 API 快照](#-api-快照)
- [🧪 範例](#-範例)
- [🧱 開發說明](#-開發說明)
- [🔐 安全說明](#-安全說明)
- [🔧 疑難排解](#-疑難排解)
- [🌐 README 與 i18n 工作流](#-readme-與-i18n-工作流)
- [📘 README 生成上下文](#-readme-生成上下文)
- [❓ 常見問題](#-faq)
- [🗺️ 路線圖](#-路線圖)
- [🤝 貢獻](#-貢獻)
- [❤️ Support](#-support)
- [📄 授權](#-授權)

## 🚀 概述
AutoAppDev 是一個面向長時間執行、可恢復之應用開發流水線的控制器專案。它結合了：

1. 一個以 PostgreSQL 為持久化後端的 Tornado API（儲存程式中含有本機 JSON 降級行為）。
2. 一個類似 Scratch 的靜態 PWA 控制器 UI。
3. 用於撰寫流程、決定論程式碼生成、self-dev 迴圈與 README 自動化的腳本與文件。

此專案針對可預測的代理執行進行最佳化，採用嚴格序列與以產物為導向的工作流程紀錄。

### 🎨 為何會有這個倉庫

| 主題 | 實際意涵 |
| --- | --- |
| 決定論 | 以標準化流程（pipeline IR + parser/import/codegen）設計，利於重複執行 |
| 可恢復性 | 對長時間執行任務提供明確生命週期狀態機（`start/pause/resume/stop`） |
| 可運維性 | 執行日誌、inbox/outbox 通道，以及腳本驅動的驗證迴圈 |
| 文件優先 | 規範與示例集中於 `docs/`，並搭配多語言 README 自動化 |

## 🧭 哲學
AutoAppDev 將代理視為執行工具，透過嚴格且可恢復的循環穩定工作：

1. Plan（規劃）
2. Implement（實作）
3. Debug/verify（含逾時控制）
4. Fix（修正）
5. Summarize + log（總結與紀錄）
6. Commit + push（提交與推送）

控制器應用旨在以 Scratch 式區塊/動作體現同樣原則（含通用 `update_readme` action），讓每個 workspace 維持最新且可重現。

### 🔁 生命週期狀態意圖

| 狀態轉換 | 運行意圖 |
| --- | --- |
| `start` | 從 stopped/ready 狀態啟動流水線 |
| `pause` | 在不遺失上下文的情況下安全暫停長時間執行 |
| `resume` | 從已儲存的執行時狀態/產物繼續 |
| `stop` | 結束執行並回到非執行狀態 |

## ✨ 功能
- 可恢復的流程生命週期控制：start、pause、resume、stop。
- AAPS 流程腳本（`.aaps`）與標準 IR（`autoappdev_ir` v1）腳本庫 API。
- 決定論式 parser/import 流程：
  - 解析格式化的 AAPS 腳本。
  - 透過 `# AAPS:` 註解匯入已標註的 shell。
  - 可選的 Codex 協助解析 fallback（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 行動登錄（action registry）包含內建動作與可編輯／自訂動作（唯讀內建動作可先 clone 再編輯）。
- Scratch 式 PWA 區塊與執行時載入的動作面板（`GET /api/actions`）。
- 執行時訊息管道：
  - Inbox（`/api/inbox`）供操作員向流程傳遞指引。
  - Outbox（`/api/outbox`）可從 `runtime/outbox` 讀取檔案佇列。
- 從後端與流程日誌輸出增量串流（`/api/logs`, `/api/logs/tail`）。
- 以標準 IR 進行決定論式 runner codegen（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用於儲存庫逐步演進的 self-dev driver（`scripts/auto-autoappdev-development.sh`）。
- README 自動化流程，含 `i18n/` 的多語言生成腳手架。

## 📌 一目了然

| 領域 | 說明 |
| --- | --- |
| 核心運行時 | Tornado 後端 + 靜態 PWA 前端 |
| 持久化 | PostgreSQL 優先，`backend/storage.py` 中具備相容降級 |
| 流程模型 | 標準 IR（`autoappdev_ir` v1）與 AAPS 腳本格式 |
| 控制流程 | Start / Pause / Resume / Stop 生命週期 |
| 開發模式 | 可恢復 self-dev 迴圈 + 決定論腳本/codegen 工作流 |
| README/i18n | 使用 `i18n/` 腳手架的自動化 README 流程 |

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
        +--> runtime (logs, outbox, llm_parse artifacts)
        +--> scripts (pipeline runner + codegen helpers)
```

### 後端職責
- 提供 scripts、actions、plan、流程生命週期、日誌、inbox/outbox、workspace config 等控制器 API。
- 驗證並持久化流程腳本資產。
- 協調流程執行狀態與轉換。
- 當資料庫連線池不可用時提供決定論式降級行為。

### 前端職責
- 呈現 Scratch 式區塊介面與流程編輯流程。
- 從後端動態載入行動面板（action palette）。
- 控制生命週期並監控狀態、日誌與訊息。

## 📚 內容
常用文件、腳本與範例索引：

- `docs/auto-development-guide.md`：雙語（EN/ZH）說明長時間、可恢復自動開發代理的觀念與需求。
- `docs/ORDERING_RATIONALE.md`：截圖驅動步驟排序的示例推理。
- `docs/controller-mvp-scope.md`：控制器 MVP 範圍（畫面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`：決定論式手動 E2E demo 檢查清單（backend + PWA happy path）。
- `docs/env.md`：環境變數（`.env`）規範。
- `docs/api-contracts.md`：控制器 API 的請求/回應契約。
- `docs/pipeline-formatted-script-spec.md`：標準流程腳本格式（AAPS）與標準 IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`：從標準 IR 決定論式產生可執行 Bash runner。
- `docs/common-actions.md`：通用 action 契約規格（含 `update_readme`）。
- `docs/workspace-layout.md`：標準 workspace 資料夾與約定（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`：在 tmux 中啟動 AutoAppDev（後端 + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`：在 tmux 中啟動 AutoAppDev self-dev driver。
- `scripts/app-auto-development.sh`：線性流程驅動（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`）並支援 resume/state。
- `scripts/generate_screenshot_docs.sh`：截圖 -> Markdown 說明生成器（Codex 驅動）。
- `scripts/setup_autoappdev_env.sh`：本機執行的主要 conda 環境初始化腳本。
- `scripts/setup_backend_env.sh`：後端環境輔助腳本。
- `examples/ralph-wiggum-example.sh`：Codex CLI 自動化輔助示例。

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

## ✅ 前置需求
- 支援 `bash` 的作業系統。
- Python `3.11+`。
- conda（`conda`）— 用於提供的設定腳本。
- `tmux`（供一鍵啟動後端 + PWA 或 self-dev 工作階段）。
- 可透過 `DATABASE_URL` 存取的 PostgreSQL。
- 可選：`codex` CLI（用於 Codex 驅動流程：self-dev、parse-llm fallback、auto-readme pipeline）。

快速需求矩陣：

| 元件 | 必要 | 用途 |
| --- | --- | --- |
| `bash` | 是 | 指令腳本執行 |
| Python `3.11+` | 是 | 後端與 codegen 工具 |
| Conda | 是（建議） | 環境初始化腳本 |
| PostgreSQL | 是（首選） | 以 `DATABASE_URL` 提供主要持久化 |
| `tmux` | 建議 | 管理後端/PWA 與 self-dev 工作階段 |
| `codex` CLI | 可選 | LLM 協助解析與 README/self-dev 自動化 |

## 🧩 相容性與假設

| 主題 | 目前預期 |
| --- | --- |
| 本機作業系統 | 以 Linux/macOS shell 為主（`bash` 腳本） |
| Python 執行環境 | `3.11`（由 `scripts/setup_autoappdev_env.sh` 管理） |
| 持久化模式 | PostgreSQL 為首選且作為標準 |
| 降級行為 | `backend/storage.py` 在降級情境包含 JSON 相容降級 |
| 網路模型 | 本機 `localhost` 分離埠開發（backend + static PWA） |
| 代理工具 | 除非使用 LLM 協助解析或 self-dev 自動化，否則 `codex` CLI 可選 |

本文檔假設如下：
- 除非該章節另有說明，否則命令從倉庫根目錄執行。
- 在啟動後端服務前已設定 `.env`。
- 一鍵工作流程預設可使用 `conda` 與 `tmux`。

## 🛠️ 安裝

### 1) 複製並進入專案
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) 設定環境
```bash
cp .env.example .env
```

編輯 `.env` 並至少設定：
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` 與 `AUTOAPPDEV_PORT`（或 `PORT`）

### 3) 建立/更新後端環境
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) 套用資料庫 schema
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

接著開啟：
- PWA：`http://127.0.0.1:5173/`
- Backend API base：`http://127.0.0.1:8788`
- 健康檢查：`http://127.0.0.1:8788/api/health`

只用一條指令做 smoke-check：
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

快速端點對照：

| 項目 | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| 健康端點 | `http://127.0.0.1:8788/api/health` |

## ⚙️ 設定

主要檔案：`.env`（請參閱 `docs/env.md` 與 `.env.example`）。

### 重要變數

| 變數 | 用途 |
| --- | --- |
| `SECRET_KEY` | 依慣例為必要值 |
| `AUTOAPPDEV_HOST`、`AUTOAPPDEV_PORT`、`PORT` | 後端綁定設定 |
| `DATABASE_URL` | PostgreSQL DSN（建議） |
| `AUTOAPPDEV_RUNTIME_DIR` | 覆寫 runtime 目錄（預設 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`、`AUTOAPPDEV_PIPELINE_SCRIPT` | 預設流程執行目標 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | 啟用 `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`、`AUTOAPPDEV_CODEX_REASONING`、`AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Codex 的 actions/endpoints 預設值 |
| `AI_API_BASE_URL`、`AI_API_KEY` | 預留給未來整合 |

快速驗證 `.env`：
```bash
bash -lc 'set -euo pipefail; test -f .env; set -a; source .env; set +a; \
python3 - <<"PY"
import os, sys
req = ["SECRET_KEY", "DATABASE_URL"]
missing = [k for k in req if not os.getenv(k)]
port_ok = bool(os.getenv("AUTOAPPDEV_PORT") or os.getenv("PORT"))
if not port_ok:
  missing.append("AUTOAPPDEV_PORT or PORT")
if missing:
  print("Missing env:", ", ".join(missing))
  sys.exit(1)
print("OK: env looks set")
PY'
```

## ▶️ 使用方式

| 模式 | 指令 | 說明 |
| --- | --- | --- |
| 啟動後端＋PWA（建議） | `./scripts/run_autoappdev_tmux.sh --restart` | 後端 `http://127.0.0.1:8788`，PWA `http://127.0.0.1:5173/` |
| 僅啟動後端 | `conda run -n autoappdev python -m backend.app` | 使用 `.env` 的 bind 與 DB 設定 |
| 僅啟動 PWA 靜態伺服器 | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | 適合前端單獨檢查 |
| 在 tmux 中執行 self-dev driver | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 可恢復的 self-dev 迴圈 |

### 常用腳本參數
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### 解析並儲存腳本
- 透過 API 解析 AAPS：`POST /api/scripts/parse`
- 匯入已標註 shell：`POST /api/scripts/import-shell`
- 可選的 LLM 解析：`POST /api/scripts/parse-llm`（需設 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### 流程控制 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 其他常用 API
- 健康／版本／設定：`/api/health`, `/api/version`, `/api/config`
- Plan 與腳本：`/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions：`/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- 訊息：`/api/chat`, `/api/inbox`, `/api/outbox`
- 日誌：`/api/logs`, `/api/logs/tail`

請參閱 `docs/api-contracts.md` 了解請求／回應格式。

## 🧭 作業手冊

### 手冊：啟動完整本機堆疊
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

驗證檢查點：
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- 開啟 `http://127.0.0.1:5173/`，確認 UI 能載入 `/api/config`。
- 可選：開啟 `/api/version`，確認回傳預期的後端中繼資料。

### 手冊：僅後端除錯
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### 手冊：決定論式 codegen smoke
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

核心 API 分組總覽：

| 分類 | 端點 |
| --- | --- |
| 健康與執行時資訊 | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan 模型 | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| 流程執行時 | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| 訊息與日誌 | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| Workspace 設定 | `GET/POST /api/workspaces/<name>/config` |

## 🧪 範例

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

### 決定論式 runner 生成
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### 決定論式 demo 流程
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```

接著使用 PWA 的 Start/Pause/Resume/Stop 控件並檢查 `/api/logs`。

### 從已標註 shell 匯入
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
- 後端基於 Tornado，針對本機開發體驗最佳化（包含 localhost 分 port 時較寬鬆的 CORS）。
- 持久化以 PostgreSQL 為主，並在 `backend/storage.py` 提供相容降級。
- PWA block key 與腳本 `STEP.block` 值刻意一致：`plan`、`work`、`debug`、`fix`、`summary`、`commit_push`。
- 內建 actions 為唯讀；編輯前請先 clone。
- `update_readme` action 限定於 workspace README 目標（`auto-apps/<workspace>/README.md`）且受路徑安全保護。
- 某些文件/腳本仍保留歷史路徑或命名（`HeyCyan`, `LightMind`），這些源於專案演進。現行的倉庫規範路徑是本倉庫根目錄。
- 根目錄 `i18n/` 已存在，預期多語言 README 存放於此。

### 工作模型與狀態檔
- 運行時預設目錄為 `./runtime`（可用 `AUTOAPPDEV_RUNTIME_DIR` 覆寫）。
- Self-dev 自動化狀態與歷史記錄位於 `references/selfdev/`。
- README pipeline 產物記錄於 `.auto-readme-work/<timestamp>/`。

### 測試現況（目前）
- 倉庫包含 smoke checks 與決定論式 demo 腳本。
- 尚未在根目錄定義完整的頂層自動化測試/CI 規格。
- 目前的驗證主要以腳本驅動為主（`scripts/pipeline_codegen/smoke_*.sh`、`backend.db_smoketest`、E2E 檢查清單）。

## 🔐 安全說明
- `update_readme` action 有意限制為 workspace README 目標（`auto-apps/<workspace>/README.md`），並具備路徑穿越防護。
- Action registry 驗證會標準化 action 規格欄位，並對支援的推理等級做界限控制。
- 倉庫腳本預設假設在可信本機環境執行；在共用環境或接近生產環境前請先審閱腳本。
- `.env` 可能含敏感值（如 `DATABASE_URL`、API 金鑰）。請勿提交 `.env`，並在本機開發以外使用適當的金鑰管理。

## 🔧 疑難排解

| 症狀 | 檢查項目 |
| --- | --- |
| `tmux not found` | 安裝 `tmux`，或改為手動各自啟動後端與 PWA。 |
| 後端因缺少 env 而啟動失敗 | 對照 `docs/env.md` 與 `.env.example` 檢查 `.env`。
| 資料庫錯誤（連線／認證／schema） | 檢查 `DATABASE_URL`；重跑 `conda run -n autoappdev python -m backend.apply_schema`；可選連線檢查：`conda run -n autoappdev python -m backend.db_smoketest`。 |
| PWA 可開啟但無法呼叫 API | 確認後端是否在預期 host/port 監聽；重新執行 `./scripts/run_autoappdev_tmux.sh` 以重建 `pwa/config.local.js`。 |
| Pipeline Start 回傳 invalid transition | 先確認目前 pipeline 狀態，務必從 `stopped` 狀態啟動。 |
| UI 沒有新日誌 | 確認 `runtime/logs/pipeline.log` 有在寫入；可直接呼叫 `/api/logs` 與 `/api/logs/tail` 以區隔 UI 與後端問題。 |
| LLM parse endpoint 顯示 disabled | 設定 `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 後重啟後端。 |
| `conda run -n autoappdev ...` 執行失敗 | 重跑 `./scripts/setup_autoappdev_env.sh`；確認 conda env `autoappdev` 存在（`conda env list`）。 |
| 前端 API 指向錯誤 | 確認 `pwa/config.local.js` 存在且指向目前後端 host/port。 |

需要可重複的手動驗證流程，請參考 `docs/end-to-end-demo-checklist.md`。

## 🌐 README 與 i18n 工作流
- 根 README 為 README 自動化流水線的規範來源。
- 多語言版本應放於 `i18n/`。
- i18n 目錄現況：✅ 於此 repo 中存在。
- 本專案目前語系：
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
- 每個 README 變體頂部僅保留一條語言導覽列，不得重複。
- README 流程入口：`prompt_tools/auto-readme-pipeline.sh`。

### i18n 生成限制（嚴格）
- 更新根 README 內容時，必須一併處理多語言生成。
- 多語言檔案需逐一生成/更新（循序，不可模糊批次）。
- 每個變體頂部保留且僅保留一條語言導覽。
- 不要在同一檔案重複語言列。
- 翻譯時保留規範命令片段、連結、API 路徑與徽章語意。

建議生成順序：
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

| 語言 | 檔案 |
| --- | --- |

## 📘 Readme 生成上下文

- 流水線執行時間戳：`20260301_064935`
- 觸發條件：`./README.md` 首次完整草稿生成
- 輸入使用者提示：`probe prompt`
- 目標：生成完整、清楚的 README 草稿，包含 required sections 與 support 內容
- 使用的來源快照：
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- 本檔案由倉庫內容生成，作為規範起點。

## ❓ 常見問題

### PostgreSQL 是必要的嗎？
建議並預期在一般運作時使用 PostgreSQL。儲存層有相容 fallback，但生產型使用仍建議 `DATABASE_URL` 可用且指向 PostgreSQL。

### 為什麼同時有 `AUTOAPPDEV_PORT` 和 `PORT`？
`AUTOAPPDEV_PORT` 是專案專用變數，`PORT` 是偏向部署的通用別名。除非刻意覆寫啟動行為，否則應保持一致。

### 只想查看 API，該從哪裡開始？
先只啟動後端（`conda run -n autoappdev python -m backend.app`），再用 `/api/health`、`/api/version`、`/api/config`，接著參閱 `docs/api-contracts.md` 的 script/action 端點。

### 多語言 README 會自動生成嗎？
會。倉庫有 `prompt_tools/auto-readme-pipeline.sh`，語系版本維護於 `i18n/`，每個檔案頂部都保留一條語言導覽。

## 🗺️ 路線圖
- 完成目前 `51 / 55` 之外剩餘的 self-dev 任務。
- 擴充 workspace/materials/context 工具與更強化的安全路徑限制。
- 持續改善 action palette UX 與可編輯動作流程。
- 加強 `i18n/` 及執行時語系切換的多語言 README/UI 支援。
- 加強 smoke/integration 檢查與 CI 覆蓋（目前以腳本驅動 smoke 檢查為主，根目錄尚未提供完整 CI 規格）。
- 深化 parser/import/codegen 決定論保障，持續圍繞 AAPS v1 與標準 IR。

## 🤝 貢獻
歡迎透過 issue 與 pull request 參與。

建議流程：
1. Fork 並建立功能分支。
2. 保持變更集中且可重現。
3. 優先採用決定論式腳本／測試。
4. 行為或契約改變時更新文件（`docs/*`、API 契約、範例）。
5. 提交 PR 時附上上下文、驗證步驟與執行條件。

本專案目前遠端如下：
- `origin`：`git@github.com:lachlanchen/AutoAppDev.git`
- 本地可能存在其他相關 repo 的 remote（本工作區示例：`novel`）。

---

## 📄 授權
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

此倉庫快照未偵測到根目錄 `LICENSE` 檔案。

補充：
- 在新增授權檔之前，請視使用／重分發條件為未明確，並向維護者確認。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
