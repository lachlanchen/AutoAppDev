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

可重用的腳本與指南，使用 Codex 作為非互動工具，從截圖/Markdown 逐步建構應用程式。

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

## 🚀 概覽
AutoAppDev 是一個用於長時間執行、可續跑（resumable）應用開發流程的控制器專案。它結合了：

1. Tornado 後端 API，搭配 PostgreSQL 持久化（並在儲存程式碼中提供本機 JSON fallback 行為）。
2. 類 Scratch 的靜態 PWA 控制器介面。
3. 用於流程撰寫、確定性程式碼生成、自我開發迴圈與 README 自動化的腳本與文件。

### 一覽

| 區域 | 說明 |
| --- | --- |
| 核心執行環境 | Tornado 後端 + 靜態 PWA 前端 |
| 持久化 | 以 PostgreSQL 為主，並在 `backend/storage.py` 具備相容行為 |
| 流程模型 | Canonical IR（`autoappdev_ir` v1）與 AAPS script 格式 |
| 控制流程 | Start / Pause / Resume / Stop 生命週期 |
| 開發模式 | 可續跑 self-dev 迴圈 + 確定性 script/codegen 工作流 |
| README/i18n | 含 `i18n/` scaffolding 的 README 自動化流程 |

## 🧭 設計理念
AutoAppDev 將 agent 視為工具，並透過嚴格、可續跑的迴圈維持工作穩定：
1. Plan
2. Implement
3. Debug/verify（含 timeout）
4. Fix
5. Summarize + log
6. Commit + push

控制器應用程式目標是以類 Scratch 的 blocks/actions 呈現相同概念（包含共用 `update_readme` action），讓每個 workspace 都能保持最新且可重現。

## ✨ 功能
- 可續跑的流程生命週期控制：start、pause、resume、stop。
- AAPS 流程腳本（`.aaps`）與 canonical IR（`autoappdev_ir` v1）的腳本庫 API。
- 確定性 parser/import 流程：
  - 解析格式化 AAPS scripts。
  - 透過 `# AAPS:` 註解匯入 shell。
  - 可選 Codex 輔助解析 fallback（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- Action registry，包含內建 actions + 可編輯/自訂 actions（唯讀內建 action 可透過 clone/edit 流程調整）。
- 類 Scratch 的 PWA 積木，以及執行期載入的 action palette（`GET /api/actions`）。
- 執行期訊息通道：
  - Inbox（`/api/inbox`）用於 operator -> pipeline 指引。
  - Outbox（`/api/outbox`）包含來自 `runtime/outbox` 的檔案佇列匯入。
- 後端與流程日誌的增量串流（`/api/logs`、`/api/logs/tail`）。
- 從 canonical IR 進行確定性 runner codegen（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 用於儲存庫迭代演進的 self-dev driver（`scripts/auto-autoappdev-development.sh`）。
- README 自動化流程，含 `i18n/` 多語生成 scaffolding。

## 📚 內容
- `docs/auto-development-guide.md`：長時間執行、可續跑自動開發 agent 的雙語（EN/ZH）理念與需求。
- `docs/ORDERING_RATIONALE.md`：截圖驅動步驟排序的範例理據。
- `docs/controller-mvp-scope.md`：控制器 MVP 範圍（畫面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`：確定性的手動端到端 demo 檢核清單（backend + PWA happy path）。
- `docs/env.md`：環境變數（`.env`）慣例。
- `docs/api-contracts.md`：控制器 API 請求/回應契約。
- `docs/pipeline-formatted-script-spec.md`：標準流程腳本格式（AAPS）與 canonical IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`：從 canonical IR 生成可執行 bash pipeline runner 的確定性產生器。
- `docs/common-actions.md`：通用 action 契約/規格（包含 `update_readme`）。
- `docs/workspace-layout.md`：標準 workspace 資料夾 + 契約（materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps）。
- `scripts/run_autoappdev_tmux.sh`：在 tmux 中啟動 AutoAppDev 應用（backend + PWA）。
- `scripts/run_autoappdev_selfdev_tmux.sh`：在 tmux 中啟動 AutoAppDev self-dev driver。
- `scripts/app-auto-development.sh`：線性流程 driver（plan -> backend -> PWA -> Android -> iOS -> review -> summary），支援續跑/狀態。
- `scripts/generate_screenshot_docs.sh`：截圖 -> markdown 描述生成器（Codex 驅動）。
- `scripts/setup_backend_env.sh`：本機執行用的 backend conda 環境初始化。
- `examples/ralph-wiggum-example.sh`：Codex CLI 自動化輔助範例。

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

## ✅ 先決條件
- 具備 `bash` 的作業系統。
- Python `3.11+`。
- 提供腳本所需的 Conda（`conda`）。
- 可一鍵啟動 backend+PWA 或 self-dev session 的 `tmux`。
- `DATABASE_URL` 可連線的 PostgreSQL。
- 可選：用於 Codex 驅動流程的 `codex` CLI（self-dev、parse-llm fallback、auto-readme pipeline）。

## 🛠️ 安裝
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
- `AUTOAPPDEV_HOST` 與 `AUTOAPPDEV_PORT`（或 `PORT`）

### 3) 建立/更新 backend 環境
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) 套用資料庫 schema
```bash
conda run -n autoappdev python -m backend.apply_schema
```

## ⚙️ 設定
主要檔案：`.env`（請見 `docs/env.md` 與 `.env.example`）。

### 重要變數

| 變數 | 用途 |
| --- | --- |
| `SECRET_KEY` | 依慣例必填 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | 後端綁定位址設定 |
| `DATABASE_URL` | PostgreSQL DSN（建議） |
| `AUTOAPPDEV_RUNTIME_DIR` | 覆寫 runtime 目錄（預設 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 預設流程執行目標 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | 啟用 `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | actions/endpoints 的 Codex 預設值 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 預留給未來整合 |

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

## ▶️ 使用方式
### 一起啟動 backend + PWA（建議）
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
預設：
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### 僅啟動 backend
```bash
conda run -n autoappdev python -m backend.app
```

### 僅啟動 PWA 靜態伺服器
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### 在 tmux 執行 self-dev driver
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### 解析並儲存 scripts
- 透過 API 解析 AAPS：`POST /api/scripts/parse`
- 匯入帶註解的 shell：`POST /api/scripts/import-shell`
- 可選 LLM 解析：`POST /api/scripts/parse-llm`（需要 `AUTOAPPDEV_ENABLE_LLM_PARSE=1`）

### 流程控制 API
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

請參考 `docs/api-contracts.md` 了解請求/回應結構。

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

### 確定性 runner 生成
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### 確定性 demo 流程
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
接著使用 PWA 的 Start/Pause/Resume/Stop 控制，並檢查 `/api/logs`。

## 🧱 開發備註
- 後端基於 Tornado，並為本機開發體驗設計（包含 localhost 分離連接埠的寬鬆 CORS）。
- 儲存層以 PostgreSQL 為主，並在 `backend/storage.py` 提供相容行為。
- PWA block keys 與 script `STEP.block` 值刻意對齊（`plan`、`work`、`debug`、`fix`、`summary`、`commit_push`）。
- 內建 actions 為唯讀；如需修改請先 clone。
- `update_readme` action 受路徑安全限制，只能指向 `auto-apps/<workspace>/README.md` 下的 workspace README 目標。
- 某些文件/腳本仍有歷史路徑/名稱參照（`HeyCyan`、`LightMind`），這是專案演進遺留。當前 canonical path 為本儲存庫根目錄。
- 根目錄 `i18n/` 已存在；多語流程預期在此放置各語言 README 檔案。

## 🩺 疑難排解
- `tmux not found`：
  - 安裝 `tmux`，或手動執行 backend/PWA。
- Backend 啟動因缺少環境變數失敗：
  - 對照 `.env.example` 與 `docs/env.md` 重新檢查 `.env`。
- 資料庫錯誤（連線/驗證/schema）：
  - 確認 `DATABASE_URL`。
  - 重新執行 `conda run -n autoappdev python -m backend.apply_schema`。
  - 可選連線檢查：`conda run -n autoappdev python -m backend.db_smoketest`。
- PWA 可載入但無法呼叫 API：
  - 確認 backend 正在預期 host/port 監聽。
  - 重新執行 `./scripts/run_autoappdev_tmux.sh` 以重建 `pwa/config.local.js`。
- Pipeline Start 回傳 invalid transition：
  - 先檢查目前 pipeline 狀態；從 `stopped` 狀態開始。
- UI 無日誌更新：
  - 確認 `runtime/logs/pipeline.log` 有持續寫入。
  - 直接呼叫 `/api/logs` 與 `/api/logs/tail`，隔離 UI 與 backend 問題。
- LLM parse endpoint 顯示 disabled：
  - 設定 `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 並重啟 backend。

若需確定性的手動驗證路徑，請使用 `docs/end-to-end-demo-checklist.md`。

## 🗺️ 路線圖
- 完成目前 `51 / 55` 之外的剩餘 self-dev 任務。
- 擴充 workspace/materials/context 工具與更強的安全路徑契約。
- 持續改善 action palette UX 與可編輯 action 工作流。
- 深化 `i18n/` 與執行期語言切換的多語 README/UI 支援。
- 強化 smoke/integration 檢查與 CI 覆蓋（目前已有腳本驅動 smoke checks；根目錄尚無完整 CI manifest 文件）。

## 🤝 貢獻
歡迎透過 issue 與 pull request 參與。

建議流程：
1. Fork 並建立功能分支。
2. 保持變更聚焦且可重現。
3. 盡可能優先使用確定性腳本/測試。
4. 行為或契約有變更時同步更新文件（`docs/*`、API 契約、範例）。
5. 開 PR 時附上背景、驗證步驟與任何執行期假設。

儲存庫目前的遠端包含：
- `origin`：`git@github.com:lachlanchen/AutoAppDev.git`
- 本機 clone 可能還有額外遠端指向相關儲存庫。

## 📄 授權
在此儲存庫快照中未偵測到根目錄 `LICENSE` 檔案。

Assumption note:
- 在新增授權檔案前，請將使用/再散布條款視為未明確，並向維護者確認。

## ❤️ 贊助與捐贈

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
