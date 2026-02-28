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

スクリーンショットや markdown から、Codex を非対話型ツールとして使ってアプリを段階的に構築するための、再利用可能なスクリプトとガイド集です。

> 🎯 **Mission:** アプリ開発パイプラインを決定論的、再開可能、成果物主導にする。
>
> 🧩 **Design principle:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Project Signals

| Signal | Current Direction |
| --- | --- |
| Runtime model | Tornado backend + static PWA controller |
| Pipeline execution | 決定論的で再開可能（`start/pause/resume/stop`） |
| Persistence strategy | PostgreSQL first + 互換フォールバック |
| Documentation flow | canonical root README + 自動化された `i18n/` 派生 |

### 🔗 Quick Navigation

| Need | Go to |
| --- | --- |
| 初回のローカル実行 | [⚡ Quick Start](#-quick-start) |
| 環境設定と必須変数 | [⚙️ Configuration](#-configuration) |
| API 全体像 | [📡 API Snapshot](#-api-snapshot) |
| 実行・デバッグ手順 | [🧭 Operational Runbooks](#-operational-runbooks) |
| README/i18n 生成ルール | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| トラブルシューティング | [🔧 Troubleshooting](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev Status (Auto-Updated)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

このセクションは `scripts/auto-autoappdev-development.sh` により更新されます。
マーカー間の内容は編集しないでください。

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Table of Contents
- [🚀 Overview](#-overview)
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

## 🚀 Overview
AutoAppDev は、長時間実行で再開可能なアプリ開発パイプライン用のコントローラー・プロジェクトです。主な構成は以下の通りです。

1. PostgreSQL 永続化（`storage` 側にはローカル JSON 互換フォールバックも含む）を備えた Tornado のバックエンド API。
2. Scratch のような静的 PWA コントローラー UI。
3. パイプライン作成、決定論的なコード生成、自己開発ループ、README 自動化のためのスクリプトとドキュメント。

このプロジェクトは、厳格な順序制御と成果物ベースのワークフロー履歴により、予測可能なエージェント実行を実現するよう最適化されています。

### 🎨 Why this repo exists

| Theme | What it means in practice |
| --- | --- |
| Determinism | canonical pipeline IR + parser/import/codegen ワークフローで再現性を担保 |
| Resumability | 長時間実行を想定し `start/pause/resume/stop` の明示的状態遷移を採用 |
| Operability | ランタイムログ、inbox/outbox、スクリプト主導の検証ループ |
| Documentation-first | 契約・仕様・サンプルを `docs/` に集約し、多言語 README を自動生成 |

## 🧭 Philosophy
AutoAppDev はエージェントを「道具」と見なし、厳格かつ再開可能なループで作業を安定化します。

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

コントローラーアプリは Scratch 風のブロック/アクション（共通の `update_readme` アクションを含む）を通じて同様の考え方を実装し、各ワークスペースを常に最新かつ再現可能な状態に保ちます。

### 🔁 Lifecycle state intent

| State transition | Operational intent |
| --- | --- |
| `start` | 停止/待機状態からパイプラインを開始 |
| `pause` | コンテキストを失わずに長時間実行を一時停止 |
| `resume` | 保存されたランタイム状態や成果物から再開 |
| `stop` | 実行を停止して非実行状態に復帰 |

## ✨ Features
- 再開可能なパイプライン状態制御: start, pause, resume, stop。
- AAPS パイプラインスクリプト（`.aaps`）と canonical IR（`autoappdev_ir` v1）向けスクリプト API。
- 決定論的 parser/import パイプライン:
  - フォーマット済み AAPS スクリプトを解析。
  - `# AAPS:` コメント経由で注釈付きシェルを取り込み。
  - 任意の Codex 補助解析フォールバック (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`)。
- 組み込みアクション + 編集可能/カスタムアクションのアクションレジストリ（読み取り専用の組み込みを clone/edit して利用）。
- Scratch 風 PWA ブロックと実行時ロードされるアクションパレット（`GET /api/actions`）。
- ランタイム通信チャネル:
  - オペレーターからパイプライン指示を送る Inbox（`/api/inbox`）。
  - `runtime/outbox` のファイルキュー取り込みを含む Outbox（`/api/outbox`）。
- バックエンドとパイプラインログの増分ストリーミング（`/api/logs`, `/api/logs/tail`）。
- canonical IR からの決定論的ランナーコード生成（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- リポジトリの反復進化を担う self-dev ドライバー（`scripts/auto-autoappdev-development.sh`）。
- `i18n/` 配下で多言語生成スケルトンを提供する README 自動化パイプライン。

## 📌 At A Glance

| Area | Details |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | PostgreSQL-first と `backend/storage.py` の互換動作 |
| Pipeline model | canonical IR（`autoappdev_ir` v1）と AAPS スクリプト形式 |
| Control flow | Start / Pause / Resume / Stop の状態機構 |
| Dev mode | 再開可能な self-dev ループ + 決定論的 script/codegen ワークフロー |
| README/i18n | `i18n/` で自動化された README パイプライン |

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
- scripts, actions, plan, pipeline lifecycle, logs, inbox/outbox, workspace config 用のコントローラー API を公開。
- パイプラインスクリプト資産の検証と永続化。
- パイプライン実行状態とステータス遷移を調整。
- DB プールが利用不可のときに決定論的フォールバック動作を提供。

### Frontend responsibilities
- Scratch 風のブロック UI とパイプライン編集フローを描画。
- バックエンドレジストリからアクションパレットを動的にロード。
- ライフサイクル制御を操作し、ステータス/ログ/メッセージを監視。

## 📚 Contents
最頻出のドキュメント、スクリプト、サンプルへの参照マップ:

- `docs/auto-development-guide.md`: EN/ZH の二言語で、長時間実行・再開可能な自己開発エージェントの思想と要件。
- `docs/ORDERING_RATIONALE.md`: スクリーンショット主導のステップ順序に関する事例。
- `docs/controller-mvp-scope.md`: コントローラー MVP の範囲（画面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`: 決定論的な手動 E2E デモチェックリスト（backend + PWA happy path）。
- `docs/env.md`: 環境変数（`.env`）の取り決め。
- `docs/api-contracts.md`: コントローラー API のリクエスト/レスポンス契約。
- `docs/pipeline-formatted-script-spec.md`: 標準パイプラインスクリプト形式（AAPS）と canonical IR スキーマ（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`: canonical IR から実行可能な Bash ランナーを生成する決定論的コードジェネレーター。
- `docs/common-actions.md`: 共通アクション契約/仕様（`update_readme` を含む）。
- `docs/workspace-layout.md`: 標準ワークスペース構成 + 契約（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`: tmux で AutoAppDev（backend + PWA）を起動。
- `scripts/run_autoappdev_selfdev_tmux.sh`: tmux で AutoAppDev self-dev driver を起動。
- `scripts/app-auto-development.sh`: 線形パイプラインドライバー（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`）で resume/state 対応。
- `scripts/generate_screenshot_docs.sh`: スクリーンショット -> markdown 説明生成（Codex 駆動）。
- `scripts/setup_autoappdev_env.sh`: ローカル実行向けメイン conda 環境のセットアップ。
- `scripts/setup_backend_env.sh`: backend 環境ヘルパースクリプト。
- `examples/ralph-wiggum-example.sh`: Codex CLI 自動化ヘルパー例。

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
- `bash` が使える OS。
- Python `3.11+`。
- conda (`conda`)（提供されているセットアップに必要）。
- backend+PWA または self-dev セッションを管理するための `tmux`。
- `DATABASE_URL` で到達可能な PostgreSQL。
- 任意: Codex CLI（self-dev、parse-llm フォールバック、auto-readme パイプライン）。

Quick requirement matrix:

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
| Local OS | Linux/macOS の `bash` スクリプトを主対象 |
| Python runtime | `3.11`（`scripts/setup_autoappdev_env.sh` で管理） |
| Persistence mode | PostgreSQL を優先し canonical として扱う |
| Fallback behavior | `backend/storage.py` は劣化シナリオ向け JSON 互換フォールバックを含む |
| Network model | localhost 分離ポート構成（backend + static PWA） |
| Agent tooling | LLM 補助解析または self-dev 自動化を使う場合を除き `codex` CLI は任意 |

この README の前提:
- セクションに明示がない場合は、コマンドはリポジトリのルートで実行。
- backend 起動前に `.env` を設定済みにしておく。
- 推奨ワークフローでは `conda` と `tmux` が利用可能。

## 🛠️ Installation
### 1) Clone and enter repo
```bash
 git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Configure environment
```bash
cp .env.example .env
```
`.env` を編集して最低限次を設定:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` と `AUTOAPPDEV_PORT`（または `PORT`）

### 3) Create/update backend environment
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Apply database schema
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Optional: database smoke test
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

次を開きます:
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

1 コマンド検証:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Quick endpoint map:

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
主要ファイル: `.env`（`docs/env.md` と `.env.example` を参照）。

### Important variables

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | 規約上必須 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | バックエンドのバインド設定 |
| `DATABASE_URL` | PostgreSQL DSN（推奨） |
| `AUTOAPPDEV_RUNTIME_DIR` | runtime ディレクトリの上書き（既定 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 既定のパイプライン実行対象 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | `/api/scripts/parse-llm` を有効化 |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | actions/endpoints 用の Codex デフォルト |
| `AI_API_BASE_URL`, `AI_API_KEY` | 将来の連携用に予約 |

`.env` を簡単に検証:
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
| Start backend only | `conda run -n autoappdev python -m backend.app` | `.env` の bind + DB 設定を使用 |
| Start PWA static server only | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | フロントエンドのみの確認に有用 |
| Run self-dev driver in tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 再開可能な self-development ループ |

### Common script options
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parse and store scripts
- API で AAPS を解析: `POST /api/scripts/parse`
- 注釈付きシェルを取り込み: `POST /api/scripts/import-shell`
- 任意で LLM 解析: `POST /api/scripts/parse-llm`（`AUTOAPPDEV_ENABLE_LLM_PARSE=1` が必要）

### Pipeline control APIs
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Other frequently used APIs
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

リクエスト/レスポンスの形式は `docs/api-contracts.md` を参照。

## 🧭 Operational Runbooks

### Runbook: bring up the full local stack
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

検証チェックポイント:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- `http://127.0.0.1:5173/` を開き、UI が `/api/config` を読めることを確認。
- 任意: `/api/version` を開き、期待される backend metadata が返ることを確認。

### Runbook: backend-only debugging
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: deterministic codegen smoke
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

主要 API の概要:

| Category | Endpoints |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan model | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| Workspace settings | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Examples
### AAPS example
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

Full examples:
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### Deterministic runner generation
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Deterministic demo pipeline
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
その後、PWA の Start/Pause/Resume/Stop 操作を行い、`/api/logs` を確認します。

### Import from annotated shell
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
- backend は Tornado ベースで、ローカル開発向けに扱いやすく設計されています（localhost 分割ポート向けの許容的 CORS を含む）。
- ストレージは PostgreSQL-first で、`backend/storage.py` に互換動作が組み込まれています。
- PWA のブロックキーと `STEP.block` の値は意図的に合わせています（`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`）。
- 組み込みアクションは読み取り専用で、編集前に clone が必要です。
- `update_readme` アクションは path-safety 制約により対象は `auto-apps/<workspace>/README.md` 配下の workspace README に限定。
- 一部の docs/scripts には旧プロジェクト経緯由来の歴史的な path/name 記述（`HeyCyan`, `LightMind`）が残ります。現在の canonical path はこのリポジトリのルートです。
- ルートの `i18n/` ディレクトリが存在し、多言語 README はここに配置されます。

### Working model and state files
- runtime ディレクトリは既定で `AUTOAPPDEV_RUNTIME_DIR` が未設定なら `./runtime`。
- self-dev 自動化の状態履歴は `references/selfdev/` で追跡。
- README パイプラインの成果物は `.auto-readme-work/<timestamp>/` に記録。

### Testing posture (current)
- リポジトリにはスモークチェックと決定論的デモスクリプトが含まれます。
- リポジトリ上の top-level 自動テスト/CI マニフェストは現時点では未定義です。
- 前提: 検証は主にスクリプト駆動（`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, E2E チェックリスト）。

## 🔐 Safety Notes
- `update_readme` アクションは、ワークスペース README ターゲット（`auto-apps/<workspace>/README.md`）への path traversal 保護付き制限を持ちます。
- action registry の検証では、action spec の正規化とサポート reasoning レベルの範囲制御が行われます。
- リポジトリのスクリプトは信頼できるローカル実行を前提としています。共有環境や本番近接環境で実行する際は事前にスクリプト内容を確認してください。
- `.env` は機密情報（`DATABASE_URL`、API キー）を含む可能性があります。`.env` はコミットせず、環境ごとの秘密管理を採用してください。

## 🔧 Troubleshooting

| Symptom | What to check |
| --- | --- |
| `tmux not found` | `tmux` をインストールするか、backend/PWA を手動で起動してください。 |
| Backend fails on startup due to missing env | `.env.example` と `docs/env.md` を基準に `.env` を再確認してください。 |
| Database errors (connection/auth/schema) | `DATABASE_URL` を確認し、`conda run -n autoappdev python -m backend.apply_schema` を再実行。任意の疎通確認として `conda run -n autoappdev python -m backend.db_smoketest`。
| PWA loads but cannot call API | backend が想定 host/port で待機しているか確認。`./scripts/run_autoappdev_tmux.sh` を再実行して `pwa/config.local.js` を再生成。 |
| Pipeline Start returns invalid transition | まず現在の pipeline status を確認し、`stopped` 状態から開始。 |
| No log updates in UI | `runtime/logs/pipeline.log` が書き込まれているか確認。UI 側か backend 側か切り分けるため `/api/logs` と `/api/logs/tail` を直接確認。 |
| LLM parse endpoint returns disabled | `AUTOAPPDEV_ENABLE_LLM_PARSE=1` を設定して backend を再起動。 |
| `conda run -n autoappdev ...` fails | `./scripts/setup_autoappdev_env.sh` を再実行し、conda env `autoappdev` が存在するか（`conda env list`）確認。 |
| Wrong API target in frontend | `pwa/config.local.js` が存在し、起動中の backend host/port を指しているか確認。 |

決定論的な手動検証手順は `docs/end-to-end-demo-checklist.md` を参照してください。

## 🌐 README & i18n Workflow
- ルートの README は README 自動化パイプラインの canonical source です。
- 多言語版は `i18n/` に配置されます。
- i18n ディレクトリの状態: ✅ 本リポジトリに存在。
- 現在このリポジトリで対応している言語:
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
- 各 README 先頭には言語ナビゲーション行を 1 行だけ置く（重複禁止）。
- README パイプラインのエントリーポイント: `prompt_tools/auto-readme-pipeline.sh`。

### i18n generation constraints (strict)
- canonical README の更新時は、必ず多言語生成処理を行う。
- 言語ファイルは一括ではなく 1 つずつ順次更新。
- 各変種の先頭に単一の言語ナビゲーション行を置く。
- 同一ファイル内で言語バーを重複させない。
- canonical コマンドスニペット、リンク、API パス、バッジ意図は維持する。

Suggested one-by-one generation order:
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

Language coverage table:

| Language | File |
| --- | --- |

## 📘 Readme Generation Context

- Pipeline run timestamp: `20260301_064935`
- Trigger: `./README.md` first complete draft generation
- Input user prompt: `probe prompt`
- Goal: generate a complete, beautiful README draft with required sections and support information
- Source snapshot used:
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- This file was generated from repository contents and preserved as a canonical draft entry point.

## ❓ FAQ

### Is PostgreSQL mandatory?
通常運用では推奨かつ想定される前提です。ストレージ層にフォールバック互換動作はあるものの、本番相当の利用では `DATABASE_URL` を通じて PostgreSQL が利用可能な前提で扱います。

### Why both `AUTOAPPDEV_PORT` and `PORT`?
`AUTOAPPDEV_PORT` はプロジェクト固有、`PORT` はデプロイ互換エイリアスです。意図的に起動経路を変更しない限り、同じ値を合わせてください。

### Where should I start if I only want to inspect APIs?
まず backend のみ起動します（`conda run -n autoappdev python -m backend.app`）、続けて `/api/health`, `/api/version`, `/api/config` を確認し、`docs/api-contracts.md` に記載の script/action エンドポイントに進みます。

### Are multilingual READMEs generated automatically?
はい。リポジトリには `prompt_tools/auto-readme-pipeline.sh` が含まれており、多言語版は `i18n/` 配下で、各 README の先頭には単一の言語ナビゲーション行ルールを守って管理されます。

## 🗺️ Roadmap
- `51 / 55` ステータスを超える残タスクの解消。
- ワークスペース/素材/コンテキスト工具の拡張、より強い safe-path 契約。
- action palette の UX 改善と編集可能アクションワークフローの向上。
- `i18n/` と実行時言語切替を含む多言語 README/UI サポートを強化。
- スモーク/統合チェックと CI カバレッジ強化（現状はスクリプト駆動スモークが中心、ルートには完全な CI マニフェストなし）。
- AAPS v1 と canonical IR 周辺で parser/import/codegen の決定論をさらに強化。

## 🤝 Contributing
Issue / PR でのコントリビューションを歓迎します。

推奨ワークフロー:
1. Fork して feature branch を作成。
2. 変更を絞り、再現性を保つ。
3. 可能であれば決定論的な scripts/tests を優先。
4. 挙動や契約が変わったらドキュメントを更新（`docs/*`、API 契約、examples）。
5. PR には背景・検証手順・実行前提を記載。

このリポジトリの remotes:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- ローカル環境では関連リポジトリ向けに追加 remote が存在する場合があります（この workspace の例: `novel`）。

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

このリポジトリスナップショットでは、ルートに `LICENSE` ファイルは検出されませんでした。

Assumption note:
- ライセンスが追加されるまでは、利用/再配布条件は未定義として扱い、メンテナーに確認してください。
