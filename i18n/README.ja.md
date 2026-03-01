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

スクリーンショット/Markdown からアプリを段階的に構築するための、再利用可能なスクリプトとガイド集です。Codex を非対話ツールとして利用します。

> 🎯 **ミッション:** アプリ開発パイプラインを決定論的・再開可能・成果物駆動にする。
>
> 🧩 **設計原則:** Plan -> Work -> Verify -> Summary -> Commit/Push。

---

### 🎛️ プロジェクトシグナル

| Signal | 現在の方向性 |
| --- | --- |
| Runtime model | Tornado backend + static PWA controller |
| Pipeline execution | 決定論的かつ再開可能 (`start/pause/resume/stop`) |
| Persistence strategy | PostgreSQL 優先 + 互換フォールバック動作 |
| Documentation flow | Canonical なルート README + 自動 `i18n/` バリアント |

### 🔗 クイックナビゲーション

| 必要なもの | 移動先 |
| --- | --- |
| 最初のローカル起動 | [⚡ Quick Start](#-quick-start) |
| 環境と必須変数 | [⚙️ Configuration](#-configuration) |
| API 全体像 | [📡 API Snapshot](#-api-snapshot) |
| 実行/デバッグ運用手順 | [🧭 Operational Runbooks](#-operational-runbooks) |
| README/i18n 生成ルール | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| トラブルシューティング一覧 | [🔧 Troubleshooting](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev ステータス（自動更新）

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

このセクションは `scripts/auto-autoappdev-development.sh` により更新されます。
マーカー間の内容は編集しないでください。

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ 目次
- [🚀 概要](#-概要)
- [🧭 リポジトリスナップショット](#-リポジトリスナップショット)
- [🧭 哲学](#-哲学)
- [✨ 特徴](#-特徴)
- [📌 ひと目でわかる要点](#-ひと目でわかる要点)
- [🏗️ アーキテクチャ](#-アーキテクチャ)
- [📚 内容](#-内容)
- [🗂️ プロジェクト構成](#-プロジェクト構成)
- [✅ 前提条件](#-前提条件)
- [🧩 互換性と前提](#-互換性と前提)
- [🛠️ インストール](#-インストール)
- [⚡ クイックスタート](#-クイックスタート)
- [⚙️ 設定](#-設定)
- [▶️ 使い方](#-使い方)
- [🧭 運用ランブック](#-運用ランブック)
- [📡 API スナップショット](#-api-スナップショット)
- [🧪 例](#-例)
- [🧱 開発メモ](#-開発メモ)
- [🔐 セーフティノート](#-セーフティノート)
- [🔧 トラブルシューティング](#-トラブルシューティング)
- [🌐 README と i18n ワークフロー](#-readme-と-i18n-ワークフロー)
- [📘 README 生成コンテキスト](#-readme-生成コンテキスト)
- [❓ FAQ](#-faq)
- [🗺️ ロードマップ](#-ロードマップ)
- [🤝 コントリビュート](#-コントリビュート)
- [❤️ Support](#-support)
- [📄 ライセンス](#-ライセンス)

## 🧭 リポジトリスナップショット

| Focus | 現在の構成 |
| --- | --- |
| Core loop | Plan → Work → Debug → Fix → Summary → Commit/Push |
| Runtime model | Tornado backend + static PWA controller |
| State machine | `start` / `pause` / `resume` / `stop` |
| Persistence | PostgreSQL 優先 + JSON フォールバック互換 |
| Documentation | Canonical `README.md` + 多言語 `i18n/` 出力 |

## 🚀 概要
AutoAppDev は、長時間実行かつ再開可能なアプリ開発パイプライン向けのコントローラープロジェクトです。以下を組み合わせています。

1. PostgreSQL 永続化対応の Tornado バックエンド API（ストレージコードにローカル JSON フォールバック互換あり）。
2. Scratch 風の静的 PWA コントローラー UI。
3. パイプライン記述、決定論的コード生成、自己開発ループ、README 自動化のためのスクリプトとドキュメント。

本プロジェクトは、厳密な順序制御と成果物中心の履歴管理により、予測可能なエージェント実行に最適化されています。

### 🎨 このリポジトリの存在理由

| テーマ | 実運用での意味 |
| --- | --- |
| Determinism | Canonical pipeline IR + parser/import/codegen による再現性重視設計 |
| Resumability | 長時間実行向けの明示的ライフサイクル状態機械 (`start/pause/resume/stop`) |
| Operability | 実行ログ、inbox/outbox チャネル、スクリプト駆動検証ループ |
| Documentation-first | `docs/` に契約/仕様/例を集約し、多言語 README フローを自動化 |

## 🧭 哲学
AutoAppDev はエージェントを「ツール」として扱い、厳密かつ再開可能なループで作業を安定化します。

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

コントローラーアプリは、Scratch 風ブロック/アクション（共通の `update_readme` アクションを含む）で同じ概念を表現し、各ワークスペースを最新かつ再現可能に保つことを目指します。

### 🔁 ライフサイクル状態の意図

| 状態遷移 | 運用上の意図 |
| --- | --- |
| `start` | stopped/ready 状態からパイプラインを開始 |
| `pause` | コンテキストを失わずに長時間実行を安全停止 |
| `resume` | 保存済みの実行状態/成果物から再開 |
| `stop` | 実行を終了して非実行状態へ戻す |

## ✨ 特徴
- 再開可能なパイプライン制御: start, pause, resume, stop。
- AAPS パイプラインスクリプト（`.aaps`）と canonical IR（`autoappdev_ir` v1）向けスクリプトライブラリ API。
- 決定論的 parser/import パイプライン:
  - 整形済み AAPS スクリプトの解析。
  - `# AAPS:` コメントによる注釈付き shell の取り込み。
  - 任意の Codex 補助パースフォールバック（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 組み込み + 編集可能/カスタムアクション対応のアクションレジストリ（読み取り専用組み込みは clone/edit フロー）。
- Scratch 風 PWA ブロックと実行時ロード型アクションパレット（`GET /api/actions`）。
- 実行時メッセージチャネル:
  - Inbox（`/api/inbox`）: オペレーター -> パイプライン指示。
  - Outbox（`/api/outbox`）: `runtime/outbox` からのファイルキュー取り込みを含む。
- バックエンドおよびパイプラインログの増分ストリーミング（`/api/logs`, `/api/logs/tail`）。
- Canonical IR からの決定論的 runner codegen（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- 反復的なリポジトリ進化のための self-dev ドライバー（`scripts/auto-autoappdev-development.sh`）。
- `i18n/` 配下の多言語 README 生成スキャフォールディング。

## 📌 ひと目でわかる要点

| 領域 | 詳細 |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | PostgreSQL 優先、`backend/storage.py` に互換動作 |
| Pipeline model | Canonical IR (`autoappdev_ir` v1) と AAPS スクリプト形式 |
| Control flow | Start / Pause / Resume / Stop ライフサイクル |
| Dev mode | 再開可能 self-dev ループ + 決定論的 script/codegen ワークフロー |
| README/i18n | `i18n/` スキャフォールディング付き自動 README パイプライン |

## 🏗️ アーキテクチャ

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

### バックエンドの責務
- スクリプト、アクション、計画、パイプラインライフサイクル、ログ、inbox/outbox、ワークスペース設定の controller API を提供。
- パイプラインスクリプト資産を検証して永続化。
- パイプライン実行状態と状態遷移を調整。
- DB プールが利用不可の場合に決定論的フォールバック動作を提供。

### フロントエンドの責務
- Scratch 風ブロック UI とパイプライン編集フローを描画。
- バックエンドレジストリからアクションパレットを動的ロード。
- ライフサイクル操作を実行し、状態/ログ/メッセージを監視。

## 📚 内容
最もよく使うドキュメント、スクリプト、サンプルの参照マップ:

- `docs/auto-development-guide.md`: 長時間実行・再開可能な自動開発エージェント向けの思想と要件（英中バイリンガル）。
- `docs/ORDERING_RATIONALE.md`: スクリーンショット駆動ステップの順序付け根拠サンプル。
- `docs/controller-mvp-scope.md`: Controller MVP 範囲（画面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`: 決定論的な手動 E2E デモチェックリスト（backend + PWA ハッピーパス）。
- `docs/env.md`: 環境変数（`.env`）規約。
- `docs/api-contracts.md`: controller の API リクエスト/レスポンス契約。
- `docs/pipeline-formatted-script-spec.md`: 標準パイプラインスクリプト形式（AAPS）と canonical IR スキーマ（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`: canonical IR から実行可能 bash runner を生成する決定論的ジェネレーター。
- `docs/common-actions.md`: 共通アクション契約/仕様（`update_readme` を含む）。
- `docs/workspace-layout.md`: 標準ワークスペースフォルダ + 契約（`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`）。
- `scripts/run_autoappdev_tmux.sh`: tmux で AutoAppDev アプリ（backend + PWA）を起動。
- `scripts/run_autoappdev_selfdev_tmux.sh`: tmux で AutoAppDev self-dev ドライバーを起動。
- `scripts/app-auto-development.sh`: 線形パイプラインドライバー（`plan -> backend -> PWA -> Android -> iOS -> review -> summary`、resume/state 対応）。
- `scripts/generate_screenshot_docs.sh`: スクリーンショット -> Markdown 説明生成（Codex 駆動）。
- `scripts/setup_autoappdev_env.sh`: ローカル実行向けメイン conda 環境ブートストラップ。
- `scripts/setup_backend_env.sh`: backend 環境ヘルパー。
- `examples/ralph-wiggum-example.sh`: Codex CLI 自動化ヘルパーの例。

## 🗂️ プロジェクト構成
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

## ✅ 前提条件
- `bash` が使える OS。
- Python `3.11+`。
- 提供セットアップスクリプト用に Conda（`conda`）。
- backend+PWA または self-dev セッションをワンコマンドで動かすための `tmux`。
- `DATABASE_URL` で到達可能な PostgreSQL。
- 任意: Codex 駆動フロー用の `codex` CLI（self-dev、parse-llm フォールバック、auto-readme pipeline）。

クイック要件マトリクス:

| コンポーネント | 必須 | 目的 |
| --- | --- | --- |
| `bash` | はい | スクリプト実行 |
| Python `3.11+` | はい | backend + codegen ツール |
| Conda | はい（推奨フロー） | 環境ブートストラップスクリプト |
| PostgreSQL | はい（推奨モード） | `DATABASE_URL` 経由の主永続化 |
| `tmux` | 推奨 | 管理された backend/PWA と self-dev セッション |
| `codex` CLI | 任意 | LLM 補助パースと README/self-dev 自動化 |

## 🧩 互換性と前提

| トピック | 現在の想定 |
| --- | --- |
| ローカル OS | Linux/macOS シェルが主対象（`bash` スクリプト） |
| Python ランタイム | `3.11`（`scripts/setup_autoappdev_env.sh` で管理） |
| 永続化モード | PostgreSQL を優先・正規系として扱う |
| フォールバック動作 | `backend/storage.py` には劣化シナリオ向け JSON 互換フォールバックを実装 |
| ネットワークモデル | localhost 分離ポート開発（backend + static PWA） |
| エージェントツール | LLM 補助パースや self-dev 自動化を使う場合のみ `codex` CLI が必要 |

この README での前提:
- 特記がない限り、リポジトリルートからコマンドを実行します。
- backend 起動前に `.env` を設定します。
- 推奨のワンコマンドワークフローでは `conda` と `tmux` が利用可能です。

## 🛠️ インストール
### 1) リポジトリをクローンして移動
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) 環境を設定
```bash
cp .env.example .env
```
`.env` を編集して、少なくとも以下を設定:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` と `AUTOAPPDEV_PORT`（または `PORT`）

### 3) backend 環境を作成/更新
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) データベーススキーマを適用
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) 任意: DB スモークテスト
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ クイックスタート
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

クイックエンドポイントマップ:

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ 設定
主設定ファイル: `.env`（`docs/env.md` と `.env.example` を参照）。

### 重要な変数

| 変数 | 目的 |
| --- | --- |
| `SECRET_KEY` | 規約上必須 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | backend バインド設定 |
| `DATABASE_URL` | PostgreSQL DSN（推奨） |
| `AUTOAPPDEV_RUNTIME_DIR` | runtime ディレクトリ上書き（既定 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | デフォルトパイプライン実行対象 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | `/api/scripts/parse-llm` を有効化 |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | action/endpoint 用 Codex 既定値 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 将来統合用に予約 |

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

## ▶️ 使い方

| モード | コマンド | メモ |
| --- | --- | --- |
| backend + PWA を起動（推奨） | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| backend のみ起動 | `conda run -n autoappdev python -m backend.app` | `.env` のバインド + DB 設定を使用 |
| PWA 静的サーバーのみ起動 | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | フロントエンド単体確認に便利 |
| tmux で self-dev ドライバー実行 | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 再開可能 self-development ループ |

### よく使うスクリプトオプション
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### スクリプトの解析と保存
- API で AAPS を解析: `POST /api/scripts/parse`
- 注釈付き shell を取り込み: `POST /api/scripts/import-shell`
- 任意の LLM 解析: `POST /api/scripts/parse-llm`（`AUTOAPPDEV_ENABLE_LLM_PARSE=1` が必要）

### パイプライン制御 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### その他よく使う API
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

リクエスト/レスポンス形状は `docs/api-contracts.md` を参照してください。

## 🧭 運用ランブック

### ランブック: ローカルフルスタックを起動
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

検証チェックポイント:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- `http://127.0.0.1:5173/` を開き、UI が `/api/config` を読み込めることを確認。
- 任意: `/api/version` を開き、想定どおりの backend メタデータが返ることを確認。

### ランブック: backend 単体デバッグ
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### ランブック: 決定論的 codegen スモーク
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

## 📡 API スナップショット

主要 API グループの一覧:

| カテゴリ | エンドポイント |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan model | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET /api/logs/tail` |
| Workspace settings | `GET/POST /api/workspaces/<name>/config` |

## 🧪 例
### AAPS 例
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

完全なサンプル:
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### 決定論的 runner 生成
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### 決定論的デモパイプライン
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
その後、PWA の Start/Pause/Resume/Stop を操作し、`/api/logs` を確認してください。

### 注釈付き shell から取り込み
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 開発メモ
- backend は Tornado ベースで、ローカル開発の扱いやすさを重視した設計です（localhost 分離ポート向けの緩い CORS を含む）。
- 永続化は PostgreSQL 優先で、`backend/storage.py` に互換動作があります。
- PWA ブロックキーとスクリプト `STEP.block` 値は意図的に揃えています（`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`）。
- 組み込みアクションは読み取り専用です。編集前に clone してください。
- `update_readme` アクションは `auto-apps/<workspace>/README.md` 配下のワークスペース README のみに対して安全パス制約があります。
- 一部 docs/scripts には、プロジェクト進化過程で残った過去のパス/名称参照（`HeyCyan`, `LightMind`）が含まれます。現在の canonical パスはこのリポジトリルートです。
- ルート `i18n/` ディレクトリは存在し、多言語実行ではそこに各言語 README を配置します。

### 作業モデルと状態ファイル
- `AUTOAPPDEV_RUNTIME_DIR` で上書きしない限り、runtime は `./runtime` を使用。
- self-dev 自動化の state/history は `references/selfdev/` に記録。
- README パイプライン成果物は `.auto-readme-work/<timestamp>/` に記録。

### 現在のテスト体制
- リポジトリにはスモークチェックと決定論的デモスクリプトが含まれます。
- ルートメタデータとして、完全なトップレベル自動テストスイート/CI マニフェストは現時点で未定義です。
- 想定: 現在は主にスクリプト駆動で検証（`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, E2E チェックリスト）。

## 🔐 セーフティノート
- `update_readme` アクションは、ワークスペース README ターゲット（`auto-apps/<workspace>/README.md`）のみに意図的に制約され、パストラバーサル保護があります。
- Action registry の検証では、action spec フィールドの正規化と、対応 reasoning レベルの境界値チェックを実施します。
- リポジトリスクリプトは信頼済みローカル実行を前提としています。共有環境や本番隣接環境で実行する前にスクリプト本文を確認してください。
- `.env` には機密値（`DATABASE_URL`、API キー等）が入る可能性があります。`.env` はコミットせず、ローカル以外では環境別シークレット管理を使用してください。

## 🔧 トラブルシューティング

| 症状 | 確認ポイント |
| --- | --- |
| `tmux not found` | `tmux` をインストールするか、backend/PWA を手動起動。 |
| 環境変数不足で backend 起動失敗 | `.env.example` と `docs/env.md` を基準に `.env` を再確認。 |
| データベースエラー（接続/認証/スキーマ） | `DATABASE_URL` を確認し、`conda run -n autoappdev python -m backend.apply_schema` を再実行。任意で接続確認: `conda run -n autoappdev python -m backend.db_smoketest`。 |
| PWA は表示されるが API 呼び出し不可 | backend が想定 host/port で待受中か確認し、`./scripts/run_autoappdev_tmux.sh` 再実行で `pwa/config.local.js` を再生成。 |
| Pipeline Start が invalid transition を返す | 先に現在の pipeline status を確認し、`stopped` から開始。 |
| UI にログ更新が出ない | `runtime/logs/pipeline.log` が書き込まれているか確認し、`/api/logs` と `/api/logs/tail` を直接呼んで UI 側か backend 側か切り分け。 |
| LLM parse endpoint が disabled を返す | `AUTOAPPDEV_ENABLE_LLM_PARSE=1` を設定して backend を再起動。 |
| `conda run -n autoappdev ...` が失敗 | `./scripts/setup_autoappdev_env.sh` を再実行し、conda 環境 `autoappdev` の存在を確認（`conda env list`）。 |
| フロントエンドの API 接続先が誤り | `pwa/config.local.js` が存在し、稼働中 backend の host/port を指しているか確認。 |

決定論的な手動検証パスは `docs/end-to-end-demo-checklist.md` を参照してください。

## 🌐 README と i18n ワークフロー
- ルート README は README 自動化パイプラインが参照する canonical ソースです。
- 多言語バリアントは `i18n/` 配下に配置します。
- i18n ディレクトリ状態: ✅ このリポジトリに存在。
- このリポジトリの現在の言語セット:
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
- 言語ナビゲーションは各 README バリアントの先頭に 1 行のみ維持してください（重複禁止）。
- README パイプラインのエントリポイント: `prompt_tools/auto-readme-pipeline.sh`。

### i18n 生成制約（厳格）
- Canonical README 更新時は、常に多言語生成も処理すること。
- 言語ファイルは一括曖昧処理ではなく、1 言語ずつ順番に生成/更新すること。
- 各バリアント先頭には言語オプションナビ行をちょうど 1 行だけ置くこと。
- 同一ファイル内で言語バーを重複させないこと。
- 翻訳後も canonical のコマンドスニペット、リンク、API パス、バッジ意図を維持すること。

推奨の 1 言語ずつ生成順序:
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

言語カバレッジ表:

| Language | File |
| --- | --- |
| Arabic | `i18n/README.ar.md` |

観測済みワークスペースメモ:
- `i18n/README.zh-Hant.md.tmp` は一時翻訳成果物として現れる場合があります。最終 canonical ファイルは `README.<lang>.md` を維持してください。

## 📘 README 生成コンテキスト

- Pipeline run timestamp: `20260301_095119`
- Trigger: `./README.md` first complete draft generation (canonical-base incremental update)
- Input user prompt: `Use current README as canonical base. No reduction: only increment and improve. Preserve existing content, links, badges, commands, and details. Always process multilingual generation (do not skip): ensure i18n exists and generate/update language files one-by-one with a single language-options line at the top and no duplicates.`
- Goal: generate a complete, beautiful README draft with required sections and support information
- 使用したソーススナップショット:
  - `./.auto-readme-work/20260301_095119/pipeline-context.md`
  - `./.auto-readme-work/20260301_095119/repo-structure-analysis.md`
- このファイルはリポジトリ内容から生成され、canonical ドラフトの出発点として保持されます。

## ❓ FAQ

### PostgreSQL は必須ですか？
通常運用では推奨かつ想定されています。ストレージ層にはフォールバック互換動作がありますが、本番相当の利用では `DATABASE_URL` 経由で PostgreSQL が利用可能である前提を推奨します。

### なぜ `AUTOAPPDEV_PORT` と `PORT` の両方があるのですか？
`AUTOAPPDEV_PORT` はプロジェクト固有、`PORT` はデプロイ互換向けのエイリアスです。起動経路で意図的に上書きしない限り、同じ値に揃えてください。

### API だけ確認したい場合はどこから始めればよいですか？
backend 単体で起動（`conda run -n autoappdev python -m backend.app`）し、`/api/health`、`/api/version`、`/api/config` の順に確認後、`docs/api-contracts.md` に記載の script/action エンドポイントへ進んでください。

### 多言語 README は自動生成ですか？
はい。リポジトリには `prompt_tools/auto-readme-pipeline.sh` が含まれ、言語バリアントは `i18n/` 配下で管理されます。各ファイル先頭の言語ナビ行は 1 行のみです。

## 🗺️ ロードマップ
- 現在の `51 / 55` ステータス以降の残タスクを完了。
- workspace/materials/context ツールを拡張し、より強固な safe-path 契約を整備。
- アクションパレット UX と編集可能アクションワークフローを継続改善。
- `i18n/` とランタイム言語切り替えを含む多言語 README/UI 対応を強化。
- スモーク/統合チェックと CI カバレッジを強化（現状はスクリプト駆動スモークが中心で、ルートに完全 CI マニフェストは未記載）。
- AAPS v1 と canonical IR 周辺の parser/import/codegen 決定論を継続的に強化。

## 🤝 コントリビュート
Issue や Pull Request による貢献を歓迎します。

推奨ワークフロー:
1. Fork して feature ブランチを作成。
2. 変更は焦点を絞り、再現可能性を維持。
3. 可能な限り決定論的なスクリプト/テストを優先。
4. 挙動/契約が変わる場合は関連ドキュメントを更新（`docs/*`、API 契約、サンプル）。
5. 背景、検証手順、実行時前提を添えて PR を作成。

このリポジトリに現在設定されている remote:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- ローカルクローンによっては関連リポジトリ向け追加 remote が存在する場合があります（この workspace での例: `novel`）。

---

## 📄 ライセンス
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

このリポジトリスナップショットのルートに `LICENSE` ファイルは検出されませんでした。

前提メモ:
- ライセンスファイルが追加されるまで、利用/再配布条件は未定義として扱い、メンテナーに確認してください。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
