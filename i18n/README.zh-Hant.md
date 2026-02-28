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

可復用腳本和指南，使用 Codex 作為非交互式工具，從截圖/Markdown 逐步構建應用。

> 🎯 **使命：** 讓應用開發流水線具備確定性、可恢復、且以工件為驅動。
>
> 🧩 **設計原則：** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ 項目信號

| 信號 | 當前方向 |
| --- | --- |
| 運行時模型 | Tornado backend + static PWA controller |
| 流水線執行 | 確定性且可恢復（`start/pause/resume/stop`） |
| 持久化策略 | PostgreSQL 優先，並帶兼容回退行為 |
| 文檔流程 | 以根 README 為規範來源，配套自動化 `i18n/` 變體 |

### 🔗 快速導航

| 需求 | 前往 |
| --- | --- |
| 首次本地運行 | [⚡ 快速開始](#-快速開始) |
| 環境與必需變量 | [⚙️ 配置](#️-配置) |
| API 總覽 | [📡 API 快照](#-api-快照) |
| 運行/調試手冊 | [🧭 運維 Runbook](#-運維-runbook) |
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
- [✨ 特性](#-特性)
- [📌 一覽](#-一覽)
- [🏗️ 架構](#️-架構)
- [📚 內容索引](#-內容索引)
- [🗂️ 項目結構](#️-項目結構)
- [✅ 前置要求](#-前置要求)
- [🧩 兼容性與假設](#-兼容性與假設)
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
- [📘 README 生成上下文](#-readme-生成上下文)
- [❓ FAQ](#-faq)
- [🗺️ 路線圖](#️-路線圖)
- [🤝 貢獻](#-貢獻)
- [❤️ Support](#-support)
- [📄 許可證](#-許可證)

## 🚀 概覽
AutoAppDev 是一個面向長時間運行、可恢復的應用開發流水線控制器項目，結合了：

1. 一個基於 PostgreSQL 持久化的 Tornado 後端 API（存儲代碼中包含本地 JSON 回退行為）。
2. 一個 Scratch 風格的靜態 PWA 控制器界面。
3. 一套用於流水線編寫、確定性代碼生成、self-dev 循環與 README 自動化的腳本與文檔。

該項目專為可預測的代理執行進行優化，採用嚴格順序和以工件為導向的工作流歷史。

### 🎨 為甚麼有這個倉庫

| 主題 | 實際含義 |
| --- | --- |
| 確定性 | 規範化流水線 IR + parser/import/codegen 流程，面向可復現結果 |
| 可恢復性 | 對長時間運行任務提供顯式生命週期狀態機（`start/pause/resume/stop`） |
| 可運維性 | 運行日誌、inbox/outbox 通道，以及腳本驅動的驗證循環 |
| 文檔優先 | 規範與示例位於 `docs/`，並配套多語言 README 流程 |

## 🧭 方法論
AutoAppDev 將 agent 視作執行工具，通過嚴格且可恢復的循環保持工作穩定：

1. Plan（規劃）
2. Implement（實現）
3. Debug/verify（帶超時）
4. Fix（修復）
5. Summarize + log（總結 + 日誌）
6. Commit + push（提交 + 推送）

控制器應用目標是通過 Scratch 風格的塊/動作體現同樣的理念（含通用 `update_readme` action），確保每個 workspace 保持同步且可復現。

### 🔁 生命週期狀態意圖

| 狀態遷移 | 運行意圖 |
| --- | --- |
| `start` | 從 stopped/ready 狀態啓動流水線 |
| `pause` | 在不丟失上下文的前提下安全暫停長期執行 |
| `resume` | 從已保存運行時狀態/工件繼續執行 |
| `stop` | 結束執行並回到非運行狀態 |

## ✨ 特性
- 可恢復的流水線生命週期控制：start、pause、resume、stop。
- 腳本庫 API，支持 AAPS 流水線腳本（`.aaps`）和標準 IR（`autoappdev_ir` v1）。
- 確定性的 parser/import 流程：
  - 解析格式化的 AAPS 腳本。
  - 通過 `# AAPS:` 注釋導入帶注解的 shell。
  - 可選的 Codex 輔助解析回退（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 動作注冊表包含內置動作與可編輯/自定義動作（只讀內置動作支持 clone/edit）。
- Scratch 風格的 PWA 塊與運行時加載動作面板（`GET /api/actions`）。
- 運行時消息通道：
  - Inbox（`/api/inbox`）用於操作者到流水線的指引。
  - Outbox（`/api/outbox`）支持從 `runtime/outbox` 的文件隊列攝取。
- 來自後端與流水線日誌的增量流式輸出（`/api/logs`, `/api/logs/tail`）。
- 基於標準 IR 的確定性 runner 代碼生成（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用於倉庫迭代演進的 self-dev 驅動（`scripts/auto-autoappdev-development.sh`）。
- 具備多語言生成腳手架的 README 自動化流水線（`i18n/`）。

## 📌 一覽

| 領域 | 說明 |
| --- | --- |
| 核心運行時 | Tornado backend + static PWA 前端 |
| 持久化 | PostgreSQL 優先，`backend/storage.py` 中兼容回退 |
| 流水線模型 | 標準 IR（`autoappdev_ir` v1）與 AAPS 腳本格式 |
| 控制流 | Start / Pause / Resume / Stop 生命週期 |
| 開發模式 | 可恢復 self-dev 循環 + 確定性腳本/codegen 工作流 |
| README/i18n | 基於 `i18n/` 腳手架的自動化 README 流程 |

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

### 後端職責
- 提供 scripts、actions、plan、pipeline lifecycle、logs、inbox/outbox、workspace config 等控制器 API。
- 校驗並持久化流水線腳本資產。
- 協調流水線執行狀態及其狀態變更。
- 當數據庫連接池不可用時提供確定性回退。

### 前端職責
- 渲染 Scratch 風格的塊式 UI 與流水線編輯流程。
- 從後端動態加載動作面板（action palette）。
- 驅動生命週期控制並監控狀態、日誌、消息。

## 📚 內容索引
常用文檔、腳本和示例的快速映射：

- `docs/auto-development-guide.md`：Bilingual（EN/ZH）長時間運行、可恢復自動開發代理的理念與要求。
- `docs/ORDERING_RATIONALE.md`：截圖驅動步驟順序示例依據。
- `docs/controller-mvp-scope.md`：控制器 MVP 範圍（頁面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`：確定性的人工端到端演示檢查清單（backend + PWA happy path）。
- `docs/env.md`：環境變量（`.env`）約定。
- `docs/api-contracts.md`：控制器 API 請求與響應契約。
- `docs/pipeline-formatted-script-spec.md`：標準流水線腳本格式（AAPS）與標準 IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`：從標準 IR 生成可執行 bash runner 的確定性生成器。
- `docs/common-actions.md`：通用 action 契約與規範（含 `update_readme`）。
- `docs/workspace-layout.md`：標準 workspace 目錄與約定（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`：在 tmux 中啓動 AutoAppDev（backend + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`：在 tmux 中啓動 AutoAppDev self-dev 驅動。
- `scripts/app-auto-development.sh`：線性流水線驅動（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`），支持 resume/state。
- `scripts/generate_screenshot_docs.sh`：截圖 -> markdown 描述生成器（由 Codex 驅動）。
- `scripts/setup_autoappdev_env.sh`：本地運行主 conda 環境初始化腳本。
- `scripts/setup_backend_env.sh`：後端環境輔助腳本。
- `examples/ralph-wiggum-example.sh`：Codex CLI 自動化助手示例。

## 🗂️ 項目結構
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
- 支持 `bash` 的操作系統。
- Python `3.11+`。
- Conda（`conda`）用於提供的設置腳本。
- `tmux`，用於一鍵啓動 backend+PWA 或 self-dev 會話。
- 可通過 `DATABASE_URL` 訪問的 PostgreSQL。
- 可選：`codex` CLI（用於 Codex 驅動流程：self-dev、parse-llm 回退、auto-readme 流水線）。

快速需求矩陣：

| 組件 | 必需 | 用途 |
| --- | --- | --- |
| `bash` | 是 | 腳本執行 |
| Python `3.11+` | 是 | 後端 + codegen 工具 |
| Conda | 是（推薦） | 環境初始化腳本 |
| PostgreSQL | 是（首選） | 通過 `DATABASE_URL` 提供主持久化 |
| `tmux` | 推薦 | 托管 backend/PWA 與 self-dev 會話 |
| `codex` CLI | 可選 | LLM 輔助解析與 README/self-dev 自動化 |

## 🧩 兼容性與假設

| 主題 | 當前預期 |
| --- | --- |
| 本地操作系統 | 以 Linux/macOS shell 為主（`bash` 腳本） |
| Python 運行時 | `3.11`（由 `scripts/setup_autoappdev_env.sh` 管理） |
| 持久化模式 | PostgreSQL 為首選並作為標準 |
| 回退行為 | `backend/storage.py` 在降級場景中包含 JSON 兼容回退 |
| 網絡模型 | 本地 localhost 分端口開發（backend + static PWA） |
| 代理工具 | 除非使用 LLM 輔助解析或 self-dev 自動化，否則 `codex` CLI 可選 |

本文檔所依據的假設：
- 除非章節另有說明，命令均在倉庫根目錄執行。
- 啓動後端服務前已配置 `.env`。
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
編輯 `.env` 並至少設置：
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` 與 `AUTOAPPDEV_PORT`（或 `PORT`）

### 3) 創建/更新後端環境
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) 應用數據庫 schema
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) 可選：數據庫 smoke test
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

然後打開：
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- 健康檢查: `http://127.0.0.1:8788/api/health`

一條命令做 smoke-check：
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

快速端點映射：

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ 配置
主配置文件：`.env`（見 `docs/env.md` 和 `.env.example`）。

### 重要變量

| 變量 | 用途 |
| --- | --- |
| `SECRET_KEY` | 約定上的必需值 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | 後端綁定設置 |
| `DATABASE_URL` | PostgreSQL DSN（推薦） |
| `AUTOAPPDEV_RUNTIME_DIR` | 覆蓋運行時目錄（默認 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 默認流水線運行目標 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | 啓用 `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Codex 的 actions/endpoints 默認值 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 預留給未來集成 |

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
| 啓動 backend + PWA（推薦） | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`，PWA `http://127.0.0.1:5173/` |
| 僅啓動 backend | `conda run -n autoappdev python -m backend.app` | 使用 `.env` 里的 bind 與 DB 配置 |
| 僅啓動 PWA 靜態服務 | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | 適用於前端單獨檢查 |
| 在 tmux 中運行 self-dev 驅動 | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 可恢復的 self-dev 循環 |

### 常用腳本參數
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### 解析並存儲腳本
- 通過 API 解析 AAPS：`POST /api/scripts/parse`
- 導入帶注釋 shell：`POST /api/scripts/import-shell`
- 可選的 LLM 解析：`POST /api/scripts/parse-llm`（需要 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### 流水線控制 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 其他高頻 API
- 健康/版本/配置：`/api/health`, `/api/version`, `/api/config`
- Plan 和腳本：`/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions：`/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- 消息：`/api/chat`, `/api/inbox`, `/api/outbox`
- 日誌：`/api/logs`, `/api/logs/tail`

詳細請求/響應結構見 `docs/api-contracts.md`。

## 🧭 運維 Runbook

### Runbook：啓動完整本地棧
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

驗證檢查點：
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- 打開 `http://127.0.0.1:5173/` 並確認 UI 可加載 `/api/config`。
- 可選：打開 `/api/version`，確認返回預期的後端元數據。

### Runbook：僅後端調試
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
| 健康 + 運行時信息 | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan 模型 | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action 注冊表 | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline 運行時 | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| 消息 + 日誌 | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| Workspace 設置 | `GET/POST /api/workspaces/<name>/config` |

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
然後使用 PWA 的 Start/Pause/Resume/Stop 控件並檢查 `/api/logs`。

### 從帶注釋 shell 導入
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
- 後端基於 Tornado，面向本地開發體驗優化（包括 localhost 分端口時的寬松 CORS）。
- 持久化以 PostgreSQL 為主，並在 `backend/storage.py` 中提供兼容回退。
- PWA 的 block key 與腳本 `STEP.block` 值保持一致：`plan`、`work`、`debug`、`fix`、`summary`、`commit_push`。
- 內置動作為只讀；編輯前請先 clone。
- `update_readme` action 受到路徑安全限制，僅允許更新 `auto-apps/<workspace>/README.md` 下的 workspace README 目標。
- 某些文檔/腳本中仍保留歷史路徑或命名（`HeyCyan`、`LightMind`），源於倉庫演進。當前倉庫的規範路徑是本倉庫根目錄。
- 根目錄 `i18n/` 已存在；多語言 README 文件在 `i18n/` 下維護。

### 工作模型與狀態文件
- 運行時默認目錄為 `./runtime`，可通過 `AUTOAPPDEV_RUNTIME_DIR` 覆蓋。
- self-dev 自動化狀態與歷史記錄保存在 `references/selfdev/`。
- README 流水線製品記錄在 `.auto-readme-work/<timestamp>/`。

### 測試現狀（當前）
- 倉庫包含 smoke 檢查和確定性演示腳本。
- 倉庫根元數據尚未定義完整的頂層自動化測試套件/CI 清單。
- 假設驗證主要通過腳本驅動（`scripts/pipeline_codegen/smoke_*.sh`、`backend.db_smoketest`、端到端檢查清單）。

## 🔐 安全說明
- `update_readme` action 有意限制到工作區 README 目標（`auto-apps/<workspace>/README.md`），並有路徑穿越防護。
- 動作注冊表校驗會對 action spec 字段進行規範化，並對支持的推理級別值進行邊界控制。
- 倉庫腳本默認假設在可信本地環境執行；在共享或接近生產環境運行前請先審閱腳本。
- `.env` 可能包含敏感值（`DATABASE_URL`、API keys）。請勿提交 `.env`，在本地開發之外使用合適的機密管理方式。

## 🔧 故障排查

| 症狀 | 排查要點 |
| --- | --- |
| `tmux not found` | 安裝 `tmux`，或手動分別啓動 backend/PWA。 |
| 後端啓動因缺失環境變量失敗 | 對照 `.env.example` 與 `docs/env.md` 復查 `.env`。 |
| 數據庫報錯（連接/認證/schema） | 檢查 `DATABASE_URL`；重跑 `conda run -n autoappdev python -m backend.apply_schema`；可選連接性檢查：`conda run -n autoappdev python -m backend.db_smoketest`。 |
| PWA 可打開但無法調用 API | 確認 backend 在預期 host/port 監聽；重新運行 `./scripts/run_autoappdev_tmux.sh` 以重新生成 `pwa/config.local.js`。 |
| Pipeline Start 返回 invalid transition | 先檢查當前 pipeline 狀態；從 `stopped` 狀態啓動。 |
| UI 無日誌更新 | 確認 `runtime/logs/pipeline.log` 正在寫入；直接使用 `/api/logs` 與 `/api/logs/tail` 定位是 UI 還是 backend 問題。 |
| LLM parse endpoint 顯示 disabled | 設置 `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 並重啓 backend。 |
| `conda run -n autoappdev ...` 失敗 | 重跑 `./scripts/setup_autoappdev_env.sh`；確認 conda 環境 `autoappdev` 存在（`conda env list`）。 |
| 前端 API 指向錯誤 | 確認 `pwa/config.local.js` 存在並指向當前 backend host/port。 |

如果需要進行確定性手動驗證路徑，請使用 `docs/end-to-end-demo-checklist.md`。

## 🌐 README 與 i18n 工作流
- 根 README 是 README 自動化流水線的規範源。
- 多語言變體應放在 `i18n/` 目錄下。
- i18n 目錄狀態：✅ 已在倉庫中存在。
- 當前倉庫語言清單：
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
- 每個 README 變體頂部僅保留一條語言導航行（不重復）。
- README 流水線入口：`prompt_tools/auto-readme-pipeline.sh`。

### i18n 生成約束（嚴格）
- 更新根 README 內容時，始終執行多語言生成。
- 逐個語言文件生成/更新（順序執行，不要並行批量）。
- 每個變體頂部保持且僅保持一條語言導航行。
- 不要在同一文件重復語言欄。
- 翻譯時保持規範命令片段、鏈接、API 路徑和徽章語義不變。

建議順序：
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

語言覆蓋表：

| 語言 | 文件 |
| --- | --- |

## 📘 Readme 生成上下文

- 流水線運行時間戳：`20260301_064935`
- 觸發條件：`./README.md` 首次完整草稿生成
- 輸入用戶提示：`probe prompt`
- 目標：生成完整、可讀的 README 草稿，包含 required sections 與支持信息
- 使用的源碼快照：
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- 本文件基於倉庫內容生成並作為規範起點。

## ❓ FAQ

### PostgreSQL 是必須的嗎？
推薦並且預計在正常運行時使用 PostgreSQL。存儲層包含兼容回退，但生產類場景應假設 `DATABASE_URL` 可用並指向 PostgreSQL。

### 為甚麼同時有 `AUTOAPPDEV_PORT` 和 `PORT`？
`AUTOAPPDEV_PORT` 是項目專用變量；`PORT` 則是更通用的部署友好別名。除非有意覆蓋啓動路徑行為，否則應保持二者一致。

### 只想查看 API 應該從哪裡開始？
僅啓動 backend（`conda run -n autoappdev python -m backend.app`），先訪問 `/api/health`、`/api/version`、`/api/config`，再使用 `docs/api-contracts.md` 中列出的 script/action 端點。

### 多語言 README 會自動生成嗎？
會。倉庫包含 `prompt_tools/auto-readme-pipeline.sh`，語言變體維護在 `i18n/`，且每個文件頂部都保留一條語言導航。

## 🗺️ 路線圖
- 完成當前 `51 / 55` 之外的 remaining self-dev 任務。
- 擴展 workspace/materials/context 工具與更嚴格的安全路徑約束。
- 繼續改進 action palette 的 UX 與可編輯動作流程。
- 加強 `i18n/` 與運行時語言切換的多語言 README/UI 支持。
- 強化 smoke/integration 檢查與 CI 覆蓋（目前已有腳本驅動的 smoke 檢查，根目錄尚無完整 CI 清單）。
- 圍繞 AAPS v1 與標準 IR 進一步固化 parser/import/codegen 的確定性。

## 🤝 貢獻
歡迎通過 issue 與 pull request 參與貢獻。

建議流程：
1. Fork 並創建功能分支。
2. 保持改動聚焦、可復現。
3. 盡可能優先採用確定性腳本和測試。
4. 行為或契約變化時同步更新文檔（`docs/*`、API 契約、示例）。
5. 提交 PR 時附上上下文、驗證步驟與運行時假設。

倉庫遠程目前包括：
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 本地克隆中可能還包含與相關倉庫關聯的附加 remote（本工作區示例：`novel`）。



## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
