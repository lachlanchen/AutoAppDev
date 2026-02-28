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

Codex を非対話ツールとして使い、スクリーンショット/markdown からアプリを段階的に構築するための再利用可能なスクリプトとガイド集です。

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

## 🚀 概要
AutoAppDev は、長時間実行かつ再開可能なアプリ開発パイプライン向けのコントローラープロジェクトです。次の要素を組み合わせています。

1. Tornado バックエンド API と PostgreSQL ベースの永続化（加えて、ストレージコード内にローカル JSON フォールバック挙動）。
2. Scratch ライクな静的 PWA コントローラー UI。
3. パイプライン作成、決定論的コード生成、自己開発ループ、README 自動化のためのスクリプトとドキュメント。

### ひと目で分かるポイント

| 領域 | 詳細 |
| --- | --- |
| コア実行基盤 | Tornado バックエンド + 静的 PWA フロントエンド |
| 永続化 | PostgreSQL 優先、`backend/storage.py` に互換挙動あり |
| パイプラインモデル | 正規 IR（`autoappdev_ir` v1）と AAPS スクリプト形式 |
| 制御フロー | Start / Pause / Resume / Stop ライフサイクル |
| 開発モード | 再開可能な self-dev ループ + 決定論的スクリプト/コード生成ワークフロー |
| README/i18n | `i18n/` スキャフォールドを含む README 自動化パイプライン |

## 🧭 哲学
AutoAppDev はエージェントを「ツール」として扱い、厳格で再開可能なループで作業の安定性を維持します。
1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

コントローラーアプリは、Scratch ライクなブロック/アクションとして同じ概念（共通 `update_readme` アクションを含む）を体現し、各ワークスペースを常に最新かつ再現可能に保つことを目指します。

## ✨ 主な機能
- 再開可能なパイプラインライフサイクル制御: start, pause, resume, stop。
- AAPS パイプラインスクリプト（`.aaps`）と正規 IR（`autoappdev_ir` v1）向けのスクリプトライブラリ API。
- 決定論的 parser/import パイプライン:
  - 整形済み AAPS スクリプトを解析。
  - `# AAPS:` コメント経由で注釈付き shell を取り込み。
  - 任意の Codex 補助 parse フォールバック（`AUTOAPPDEV_ENABLE_LLM_PARSE=1`）。
- 組み込み + 編集可能/カスタムアクションを備えたアクションレジストリ（readonly な組み込みは clone/edit フローで編集）。
- Scratch ライク PWA ブロックと実行時読み込みアクションパレット（`GET /api/actions`）。
- 実行時メッセージチャネル:
  - Inbox（`/api/inbox`）で operator -> pipeline ガイダンス。
  - Outbox（`/api/outbox`）には `runtime/outbox` からのファイルキュー取り込みを含む。
- バックエンドとパイプラインログからのインクリメンタルログストリーミング（`/api/logs`, `/api/logs/tail`）。
- 正規 IR からの決定論的 runner codegen（`scripts/pipeline_codegen/generate_runner_from_ir.py`）。
- リポジトリを反復的に進化させる self-dev ドライバー（`scripts/auto-autoappdev-development.sh`）。
- `i18n/` 配下の多言語生成スキャフォールドを備えた README 自動化パイプライン。

## 📚 目次
- `docs/auto-development-guide.md`: 長時間実行・再開可能な自動開発エージェントに関するバイリンガル（EN/ZH）の哲学と要件。
- `docs/ORDERING_RATIONALE.md`: スクリーンショット駆動ステップの順序付け理由の例。
- `docs/controller-mvp-scope.md`: コントローラー MVP スコープ（画面 + 最小 API）。
- `docs/end-to-end-demo-checklist.md`: 決定論的な手動 end-to-end デモチェックリスト（バックエンド + PWA ハッピーパス）。
- `docs/env.md`: 環境変数（.env）の規約。
- `docs/api-contracts.md`: コントローラー向け API リクエスト/レスポンス契約。
- `docs/pipeline-formatted-script-spec.md`: 標準パイプラインスクリプト形式（AAPS）と正規 IR スキーマ（TASK -> STEP -> ACTION）。
- `docs/pipeline-runner-codegen.md`: 正規 IR から実行可能な bash パイプライン runner を生成する決定論的ジェネレーター。
- `docs/common-actions.md`: 共通アクション契約/仕様（`update_readme` を含む）。
- `docs/workspace-layout.md`: 標準ワークスペースフォルダ + 契約（materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps）。
- `scripts/run_autoappdev_tmux.sh`: tmux で AutoAppDev アプリ（バックエンド + PWA）を起動。
- `scripts/run_autoappdev_selfdev_tmux.sh`: tmux で AutoAppDev self-dev ドライバーを起動。
- `scripts/app-auto-development.sh`: 線形パイプラインドライバー（plan -> backend -> PWA -> Android -> iOS -> review -> summary、再開/状態対応）。
- `scripts/generate_screenshot_docs.sh`: スクリーンショット -> markdown 説明生成（Codex 駆動）。
- `scripts/setup_backend_env.sh`: ローカル実行向けバックエンド conda 環境ブートストラップ。
- `examples/ralph-wiggum-example.sh`: Codex CLI 自動化ヘルパー例。

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

## ✅ 前提条件
- `bash` が使える OS。
- Python `3.11+`。
- 提供セットアップスクリプト用の Conda（`conda`）。
- バックエンド+PWA または self-dev セッションを 1 コマンドで起動するための `tmux`。
- `DATABASE_URL` で到達可能な PostgreSQL。
- 任意: Codex 駆動フロー（self-dev、parse-llm フォールバック、auto-readme パイプライン）向けの `codex` CLI。

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
`.env` を編集し、少なくとも以下を設定してください。
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` と `AUTOAPPDEV_PORT`（または `PORT`）

### 3) バックエンド環境を作成/更新
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) データベーススキーマを適用
```bash
conda run -n autoappdev python -m backend.apply_schema
```

## ⚙️ 設定
主要ファイル: `.env`（`docs/env.md` と `.env.example` を参照）。

### 重要な変数

| 変数 | 用途 |
| --- | --- |
| `SECRET_KEY` | 規約上必須 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | バックエンドの bind 設定 |
| `DATABASE_URL` | PostgreSQL DSN（推奨） |
| `AUTOAPPDEV_RUNTIME_DIR` | runtime ディレクトリを上書き（既定 `./runtime`） |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 既定のパイプライン実行ターゲット |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | `/api/scripts/parse-llm` を有効化 |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | actions/endpoints 向け Codex 既定値 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 将来連携用に予約 |

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
### バックエンド + PWA を同時起動（推奨）
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
既定値:
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### バックエンドのみ起動
```bash
conda run -n autoappdev python -m backend.app
```

### PWA 静的サーバーのみ起動
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### tmux で self-dev ドライバーを起動
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### スクリプトの解析と保存
- API 経由で AAPS を解析: `POST /api/scripts/parse`
- 注釈付き shell を取り込み: `POST /api/scripts/import-shell`
- 任意の LLM 解析: `POST /api/scripts/parse-llm`（`AUTOAPPDEV_ENABLE_LLM_PARSE=1` が必要）

### パイプライン制御 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### よく使うその他 API
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

リクエスト/レスポンスの形は `docs/api-contracts.md` を参照してください。

## 🧪 例
### AAPS 例
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

完全な例:
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
その後、PWA の Start/Pause/Resume/Stop コントロールを操作し、`/api/logs` を確認してください。

## 🧱 開発メモ
- バックエンドは Tornado ベースで、ローカル開発の使いやすさを重視して設計されています（localhost の分離ポートを想定した緩めの CORS を含む）。
- ストレージは PostgreSQL 優先で、`backend/storage.py` に互換挙動があります。
- PWA ブロックキーとスクリプト `STEP.block` 値は意図的に揃えています（`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`）。
- 組み込みアクションは readonly です。編集前に clone してください。
- `update_readme` アクションは、`auto-apps/<workspace>/README.md` 配下のワークスペース README ターゲットに対して path-safety 制約があります。
- 一部 docs/scripts には、プロジェクト進化の過程で引き継がれた過去のパス/名称参照（`HeyCyan`, `LightMind`）が残っています。現在の正規パスはこのリポジトリルートです。
- ルート `i18n/` ディレクトリは存在します。多言語実行時の README 言語ファイルはここに配置される想定です。

## 🩺 トラブルシューティング
- `tmux not found`:
  - `tmux` をインストールするか、バックエンド/PWA を手動で起動してください。
- 環境変数不足でバックエンド起動に失敗:
  - `.env.example` と `docs/env.md` を基に `.env` を再確認してください。
- データベースエラー（接続/認証/スキーマ）:
  - `DATABASE_URL` を確認。
  - `conda run -n autoappdev python -m backend.apply_schema` を再実行。
  - 任意の接続チェック: `conda run -n autoappdev python -m backend.db_smoketest`。
- PWA は開くが API を呼べない:
  - バックエンドが想定 host/port で待受しているか確認。
  - `./scripts/run_autoappdev_tmux.sh` を再実行して `pwa/config.local.js` を再生成。
- Pipeline Start が invalid transition を返す:
  - 先に現在の pipeline status を確認し、`stopped` 状態から開始してください。
- UI でログ更新が見えない:
  - `runtime/logs/pipeline.log` へ書き込みがあるか確認。
  - UI とバックエンドの切り分けのため、`/api/logs` と `/api/logs/tail` を直接使用。
- LLM parse endpoint が disabled を返す:
  - `AUTOAPPDEV_ENABLE_LLM_PARSE=1` を設定し、バックエンドを再起動。

決定論的な手動検証パスとして `docs/end-to-end-demo-checklist.md` を利用してください。

## 🗺️ ロードマップ
- 現在の `51 / 55` ステータスを超え、残りの self-dev タスクを完了。
- ワークスペース/マテリアル/コンテキストのツールを拡充し、より強い safe-path 契約を整備。
- アクションパレット UX と編集可能アクションのワークフローを継続改善。
- `i18n/` とランタイム言語切替にまたがる多言語 README/UI サポートを強化。
- スモーク/統合チェックと CI カバレッジを強化（現状はスクリプト駆動のスモークチェックあり。ルートに完全な CI マニフェストは未記載）。

## 🤝 コントリビューション
Issue と Pull Request での貢献を歓迎します。

推奨ワークフロー:
1. Fork して機能ブランチを作成。
2. 変更は焦点を絞り、再現可能に保つ。
3. 可能な限り決定論的なスクリプト/テストを優先。
4. 挙動/契約が変わる場合は docs を更新（`docs/*`、API 契約、examples）。
5. コンテキスト、検証手順、ランタイム前提を添えて PR を作成。

現在のリポジトリリモート:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- ローカルクローンによっては、関連リポジトリ向け追加リモートが存在する場合があります。

## 📄 ライセンス
このリポジトリスナップショットでは、ルート `LICENSE` ファイルは検出されませんでした。

前提メモ:
- ライセンスファイルが追加されるまで、利用/再配布条件は未指定として扱い、メンテナーに確認してください。

## ❤️ Sponsor & Donate

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
