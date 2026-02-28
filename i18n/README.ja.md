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

Codex を非対話ツールとして活用し、スクリーンショットや markdown から段階的にアプリを構築するための再利用可能なスクリプトとガイド集です。

> 🎯 **Mission:** アプリ開発パイプラインを決定論的・再開可能・成果物駆動にする。
>
> 🧩 **Design principle:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ Project Signals

| Signal | Current Direction |
| --- | --- |
| Runtime model | Tornado backend + static PWA controller |
| Pipeline execution | 決定論的かつ再開可能（`start/pause/resume/stop`） |
| Persistence strategy | PostgreSQL-first と互換フォールバック動作 |
| Documentation flow | canonical なルート README + 自動生成 `i18n/` バリアント |

### 🔗 Quick Navigation

| Need | Go to |
| --- | --- |
| はじめてローカル実行する | [⚡ Quick Start](#-quick-start) |
| 環境と必須変数 | [⚙️ Configuration](#-configuration) |
| API の全体像 | [📡 API Snapshot](#-api-snapshot) |
| 実行/デバッグ手順 | [🧭 Operational Runbooks](#-operational-runbooks) |
| README/i18n 生成ルール | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| トラブル対応一覧 | [🔧 Troubleshooting](#-troubleshooting) |

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
- [❓ FAQ](#-faq)
- [🗺️ Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [❤️ Support](#-support)
- [📄 License](#-license)
- [❤️ Sponsor & Donate](#-sponsor--donate)

## 🚀 Overview
AutoAppDev は、長時間実行・再開可能なアプリ開発パイプライン向けのコントローラープロジェクトです。主に次の要素で構成されます。

1. PostgreSQL 永続化（およびストレージ層のローカル JSON フォールバック）を備えた Tornado バックエンド API。
2. Scratch ライクな静的 PWA コントローラー UI。
3. パイプライン作成、決定論的コード生成、自己開発ループ、README 自動化のためのスクリプトとドキュメント。

このプロジェクトは、厳密な順序制御と成果物指向のワークフロー履歴により、予測可能なエージェント実行に最適化されています。

### 🎨 Why this repo exists

| Theme | 実運用での意味 |
| --- | --- |
| Determinism | 再現性を重視した canonical pipeline IR + parser/import/codegen ワークフロー |
| Resumability | 長時間実行向けの明示的ライフサイクル状態機械（`start/pause/resume/stop`） |
| Operability | 実行ログ、inbox/outbox チャネル、スクリプト駆動の検証ループ |
| Documentation-first | 契約/仕様/例は `docs/` に集約し、多言語 README フローを自動化 |

## 🧭 Philosophy
AutoAppDev はエージェントを「ツール」として扱い、厳格で再開可能なループによって作業の安定性を維持します。

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

コントローラーアプリは、Scratch ライクなブロック/アクション（共通の `update_readme` アクションを含む）で同じ概念を体現し、各ワークスペースを常に最新かつ再現可能な状態に保つことを目指します。

### 🔁 Lifecycle state intent

| State transition | 運用上の意図 |
| --- | --- |
| `start` | 停止/準備状態からパイプラインを開始 |
| `pause` | コンテキストを失わず安全に長時間実行を一時停止 |
| `resume` | 保存済みランタイム状態/成果物から再開 |
| `stop` | 実行を終了し非実行状態に戻す |

## ✨ Features
- 再開可能なパイプラインライフサイクル制御: start, pause, resume, stop。
- AAPS パイプラインスクリプト（`.aaps`）と canonical IR（`autoappdev_ir` v1）のためのスクリプトライブラリ API。
- 決定論的 parser/import パイプライン:
  - 整形済み AAPS スクリプトを解析。
  - `# AAPS:` コメント経由で注釈付きシェルを取り込み。
  - 任意の Codex 補助解析フォールバック（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 組み込み + 編集可能/カスタムアクションのアクションレジストリ（読み取り専用組み込みを clone/edit するフロー）。
- Scratch ライクな PWA ブロックと実行時ロードされるアクションパレット（`GET /api/actions`）。
- ランタイムメッセージングチャネル:
  - オペレーター -> パイプライン指示の Inbox（`/api/inbox`）。
  - `runtime/outbox` からのファイルキュー取り込みを含む Outbox（`/api/outbox`）。
- バックエンドとパイプラインログの増分ストリーミング（`/api/logs`, `/api/logs/tail`）。
- canonical IR からの決定論的ランナーコード生成（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- リポジトリ反復進化のための self-dev ドライバー（`scripts/auto-autoappdev-development.sh`）。
- `i18n/` 配下の多言語生成足場を含む README 自動化パイプライン。

## 📌 At A Glance

| Area | Details |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | `backend/storage.py` に互換動作を持つ PostgreSQL-first |
| Pipeline model | Canonical IR (`autoappdev_ir` v1) と AAPS script format |
| Control flow | Start / Pause / Resume / Stop lifecycle |
| Dev mode | 再開可能な self-dev ループ + 決定論的 script/codegen ワークフロー |
| README/i18n | `i18n/` 足場を使う自動 README パイプライン |

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
- スクリプト、アクション、計画、パイプラインライフサイクル、ログ、inbox/outbox、ワークスペース設定向けのコントローラー API を提供。
- パイプラインスクリプト資産を検証して永続化。
- パイプライン実行状態とステータス遷移を調整。
- DB プール未使用時の決定論的フォールバック動作を提供。

### Frontend responsibilities
- Scratch ライクなブロック UI とパイプライン編集フローを描画。
- バックエンドレジストリからアクションパレットを動的ロード。
- ライフサイクル操作を駆動し、ステータス/ログ/メッセージを監視。

## 📚 Contents
よく使うドキュメント、スクリプト、サンプルへの参照マップです。

- `docs/auto-development-guide.md`: 長時間実行・再開可能な自己開発エージェント向けの二言語（EN/ZH）哲学と要件。
- `docs/ORDERING_RATIONALE.md`: スクリーンショット駆動ステップの順序付け rationale サンプル。
- `docs/controller-mvp-scope.md`: コントローラー MVP 範囲（画面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`: 決定論的な手動 E2E デモチェックリスト（backend + PWA happy path）。
- `docs/env.md`: 環境変数（`.env`）規約。
- `docs/api-contracts.md`: コントローラー API の request/response 契約。
- `docs/pipeline-formatted-script-spec.md`: 標準パイプラインスクリプト形式（AAPS）と canonical IR schema（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`: canonical IR から実行可能な bash pipeline runner を生成する決定論的ジェネレーター。
- `docs/common-actions.md`: 共通アクション契約/仕様（`update_readme` を含む）。
- `docs/workspace-layout.md`: 標準ワークスペースフォルダ + 契約（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`: tmux で AutoAppDev アプリ（backend + PWA）を起動。
- `scripts/run_autoappdev_selfdev_tmux.sh`: tmux で AutoAppDev self-dev driver を起動。
- `scripts/app-auto-development.sh`: resume/state 対応の線形パイプラインドライバー（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`）。
- `scripts/generate_screenshot_docs.sh`: スクリーンショット -> markdown 説明ジェネレーター（Codex 駆動）。
- `scripts/setup_autoappdev_env.sh`: ローカル実行向けメイン conda 環境ブートストラップスクリプト。
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
- 提供セットアップスクリプト向けの Conda（`conda`）。
- ワンコマンドで backend+PWA または self-dev セッションを管理する `tmux`。
- `DATABASE_URL` で到達可能な PostgreSQL。
- 任意: Codex 駆動フロー（self-dev、parse-llm フォールバック、auto-readme pipeline）向けの `codex` CLI。

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
| Local OS | Linux/macOS シェルが主対象（`bash` scripts） |
| Python runtime | `3.11`（`scripts/setup_autoappdev_env.sh` で管理） |
| Persistence mode | PostgreSQL を優先し canonical として扱う |
| Fallback behavior | `backend/storage.py` は劣化シナリオ向け JSON 互換フォールバックを含む |
| Network model | localhost の分割ポート開発（backend + static PWA） |
| Agent tooling | LLM 補助解析または self-dev 自動化を使う場合を除き `codex` CLI は任意 |

この README での前提:
- セクションで明示しない限り、コマンドはリポジトリルートで実行。
- backend サービス起動前に `.env` が設定済み。
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
`.env` を編集し、少なくとも以下を設定:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` and `AUTOAPPDEV_PORT` (or `PORT`)

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

その後に開く URL:
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

ワンコマンドのスモークチェック:
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
主ファイル: `.env`（`docs/env.md` と `.env.example` を参照）。

### Important variables

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | 慣例上必須 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | バックエンドのバインド設定 |
| `DATABASE_URL` | PostgreSQL DSN（推奨） |
| `AUTOAPPDEV_RUNTIME_DIR` | runtime dir を上書き（既定 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 既定のパイプライン実行ターゲット |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | `/api/scripts/parse-llm` を有効化 |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | actions/endpoints 向け Codex 既定値 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 将来統合用の予約値 |

`.env` の簡易検証:
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
| Start PWA static server only | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | フロントエンドのみ確認したい場合に有用 |
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
- 任意の LLM 解析: `POST /api/scripts/parse-llm`（`AUTOAPPDEV_ENABLE_LLM_PARSE=1` が必要）

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

request/response 形式は `docs/api-contracts.md` を参照してください。

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
- `http://127.0.0.1:5173/` を開き、UI から `/api/config` が読み込めることを確認。
- 任意: `/api/version` を開いて期待する backend metadata が返ることを確認。

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

主要 API グループの一覧:

| Category | Endpoints |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan model | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
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
その後、PWA の Start/Pause/Resume/Stop を操作し、`/api/logs` を確認してください。

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
- backend は Tornado ベースで、ローカル開発の扱いやすさを重視しています（localhost 分割ポート向けの緩和された CORS を含む）。
- ストレージは PostgreSQL-first で、`backend/storage.py` に互換動作があります。
- PWA ブロックキーと script の `STEP.block` 値は意図的に整合しています（`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`）。
- 組み込みアクションは readonly です。編集する場合は clone してください。
- `update_readme` アクションは、`auto-apps/<workspace>/README.md` 配下のワークスペース README のみを対象とする path-safety 制約があります。
- 一部 docs/scripts にはプロジェクト進化の経緯として過去のパス/名称参照（`HeyCyan`, `LightMind`）が残っています。現在の canonical path はこのリポジトリルートです。
- ルート `i18n/` ディレクトリは存在します。多言語実行時はここに言語 README を置く想定です。

### Working model and state files
- `AUTOAPPDEV_RUNTIME_DIR` で上書きしない限り、runtime の既定は `./runtime`。
- self-dev 自動化の state/history は `references/selfdev/` 配下に記録。
- README pipeline の成果物は `.auto-readme-work/<timestamp>/` 配下に記録。

### Testing posture (current)
- リポジトリにはスモークチェックと決定論的デモスクリプトが含まれます。
- ルートメタデータ上で完全なトップレベル自動テストスイート/CI マニフェストは現在定義されていません。
- 現在の前提: 検証は主にスクリプト駆動（`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, E2E チェックリスト）。

## 🔐 Safety Notes
- `update_readme` アクションは、path traversal 防止付きでワークスペース README ターゲット（`auto-apps/<workspace>/README.md`）に意図的に制限されています。
- action registry の検証では、action spec フィールドの正規化と、対応 reasoning レベルの値域制限を強制します。
- リポジトリスクリプトは信頼できるローカル実行を前提としています。共有環境や本番隣接環境で実行する前にスクリプト本文を確認してください。
- `.env` には機密値（`DATABASE_URL`, API keys）を含む可能性があります。`.env` はコミットせず、ローカル開発外では環境別シークレット管理を使用してください。

## 🔧 Troubleshooting

| Symptom | What to check |
| --- | --- |
| `tmux not found` | `tmux` をインストールするか、backend/PWA を手動で実行してください。 |
| Backend fails on startup due to missing env | `.env.example` と `docs/env.md` を基準に `.env` を再確認。 |
| Database errors (connection/auth/schema) | `DATABASE_URL` を確認し、`conda run -n autoappdev python -m backend.apply_schema` を再実行。任意の接続確認: `conda run -n autoappdev python -m backend.db_smoketest`。 |
| PWA loads but cannot call API | backend が期待 host/port で待受しているか確認。`./scripts/run_autoappdev_tmux.sh` を再実行して `pwa/config.local.js` を再生成。 |
| Pipeline Start returns invalid transition | 先に現在の pipeline status を確認し、`stopped` 状態から開始してください。 |
| No log updates in UI | `runtime/logs/pipeline.log` への書き込みを確認。UI か backend か切り分けるため `/api/logs` と `/api/logs/tail` を直接確認。 |
| LLM parse endpoint returns disabled | `AUTOAPPDEV_ENABLE_LLM_PARSE=1` を設定して backend を再起動。 |
| `conda run -n autoappdev ...` fails | `./scripts/setup_autoappdev_env.sh` を再実行し、conda env `autoappdev` の存在を確認（`conda env list`）。 |
| Wrong API target in frontend | `pwa/config.local.js` が存在し、稼働中 backend の host/port を指しているか確認。 |

決定論的な手動検証手順は `docs/end-to-end-demo-checklist.md` を参照してください。

## 🌐 README & i18n Workflow
- ルート README は README 自動化パイプラインの canonical source です。
- 多言語版は `i18n/` 配下に配置する想定です。
- i18n ディレクトリ状態: ✅ このリポジトリに存在。
- このリポジトリで現在対応している言語:
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
- 言語ナビゲーションは各 README 先頭に 1 行だけ保持してください（重複禁止）。
- README pipeline のエントリーポイント: `prompt_tools/auto-readme-pipeline.sh`。

### i18n generation constraints (strict)
- canonical README を更新する場合は、必ず多言語生成も処理する。
- 言語ファイルは一括ではなく 1 つずつ順次生成/更新する。
- 各バリアント先頭には言語オプションのナビゲーション行を 1 つだけ置く。
- 同一ファイル内で言語バーを重複させない。
- 翻訳後も canonical のコマンド断片、リンク、API パス、バッジ意図を保持する。

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

## ❓ FAQ

### Is PostgreSQL mandatory?
通常運用では推奨かつ前提です。ストレージ層にはフォールバック互換動作がありますが、本番相当の利用では `DATABASE_URL` 経由で PostgreSQL が利用可能である前提で扱ってください。

### Why both `AUTOAPPDEV_PORT` and `PORT`?
`AUTOAPPDEV_PORT` はプロジェクト固有です。`PORT` はデプロイ互換のエイリアスです。起動パスで意図的に上書きしない限り、両者は一致させてください。

### Where should I start if I only want to inspect APIs?
backend のみ起動（`conda run -n autoappdev python -m backend.app`）し、`/api/health`, `/api/version`, `/api/config` の順に確認した後、`docs/api-contracts.md` 記載の script/action エンドポイントへ進んでください。

### Are multilingual READMEs generated automatically?
はい。リポジトリには `prompt_tools/auto-readme-pipeline.sh` が含まれており、言語バリアントは `i18n/` 配下で、各ファイル先頭の単一言語ナビゲーション行ルールに従って管理されます。

## 🗺️ Roadmap
- 現在 `51 / 55` ステータスを超える残り self-dev タスクの完了。
- ワークスペース/素材/コンテキストツールの拡張と、より強い safe-path 契約。
- action palette UX と編集可能アクションワークフローの継続改善。
- `i18n/` と実行時言語切替を含む多言語 README/UI サポートの深化。
- スモーク/統合チェックと CI カバレッジの強化（現状はスクリプト駆動スモーク中心、ルートに完全 CI マニフェストは未記載）。
- AAPS v1 と canonical IR 周辺の parser/import/codegen 決定論性の継続的強化。

## 🤝 Contributing
Issue と Pull Request での貢献を歓迎します。

推奨ワークフロー:
1. Fork して feature branch を作成。
2. 変更は焦点を絞り再現可能に保つ。
3. 可能な限り決定論的な scripts/tests を優先。
4. 振る舞い/契約を変更したら docs を更新（`docs/*`, API contracts, examples）。
5. PR には背景、検証手順、ランタイム前提を記載。

現在のリポジトリ remotes:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- ローカル clone によっては関連リポジトリ用の追加 remote が存在する場合があります（この workspace で見つかった例: `novel`）。

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 License
このリポジトリスナップショットでは、ルートに `LICENSE` ファイルが見つかっていません。

Assumption note:
- ライセンスファイルが追加されるまでは、利用/再配布条件は未規定として扱い、メンテナーに確認してください。

## ❤️ Sponsor & Donate
| Channel | Link |
| --- | --- |
| GitHub Sponsors | https://github.com/sponsors/lachlanchen |
| Donate | https://chat.lazying.art/donate |
| PayPal | https://paypal.me/RongzhouChen |
| Stripe | https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400 |

このプロジェクトがあなたのワークフローに役立っている場合、スポンサー支援は self-dev タスク継続、ドキュメント品質向上、ツール堅牢化に直接つながります。
