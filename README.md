[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)


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

Reusable scripts + guides for building apps step-by-step from screenshots/markdown with Codex as a non-interactive tool.

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev Status (Auto-Updated)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

This section is updated by `scripts/auto-autoappdev-development.sh`.
Do not edit content between the markers.

<!-- AUTOAPPDEV:STATUS:END -->

## 🚀 Overview
AutoAppDev is a controller project for long-running, resumable app-development pipelines. It combines:

1. A Tornado backend API with PostgreSQL-backed persistence (plus local JSON fallback behavior in storage code).
2. A Scratch-like static PWA controller UI.
3. Scripts and docs for pipeline authoring, deterministic code generation, self-development loops, and README automation.

### At a glance

| Area | Details |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | PostgreSQL-first with compatibility behavior in `backend/storage.py` |
| Pipeline model | Canonical IR (`autoappdev_ir` v1) and AAPS script format |
| Control flow | Start / Pause / Resume / Stop lifecycle |
| Dev mode | Resumable self-dev loop + deterministic script/codegen workflows |
| README/i18n | Automated README pipeline with `i18n/` scaffolding |

## 🧭 Philosophy
AutoAppDev treats agents as tools and keeps work stable via a strict, resumable loop:
1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

The controller app aims to embody the same concepts as Scratch-like blocks/actions (including a common `update_readme` action) so each workspace stays current and reproducible.

## ✨ Features
- Resumable pipeline lifecycle control: start, pause, resume, stop.
- Script library APIs for AAPS pipeline scripts (`.aaps`) and canonical IR (`autoappdev_ir` v1).
- Deterministic parser/import pipeline:
  - Parse formatted AAPS scripts.
  - Import annotated shell via `# AAPS:` comments.
  - Optional Codex-assisted parse fallback (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Action registry with built-ins + editable/custom actions (clone/edit flow for readonly built-ins).
- Scratch-like PWA blocks and runtime-loaded action palette (`GET /api/actions`).
- Runtime messaging channels:
  - Inbox (`/api/inbox`) for operator -> pipeline guidance.
  - Outbox (`/api/outbox`) including file-queue ingestion from `runtime/outbox`.
- Incremental log streaming from backend and pipeline logs (`/api/logs`, `/api/logs/tail`).
- Deterministic runner codegen from canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev driver for iterative repository evolution (`scripts/auto-autoappdev-development.sh`).
- README automation pipeline with multilingual generation scaffolding under `i18n/`.

## 📚 Contents
- `docs/auto-development-guide.md`: Bilingual (EN/ZH) philosophy and requirements for a long-running, resumable auto-development agent.
- `docs/ORDERING_RATIONALE.md`: Example rationale for sequencing screenshot-driven steps.
- `docs/controller-mvp-scope.md`: Controller MVP scope (screens + minimal APIs).
- `docs/end-to-end-demo-checklist.md`: Deterministic manual end-to-end demo checklist (backend + PWA happy path).
- `docs/env.md`: Environment variables (.env) conventions.
- `docs/api-contracts.md`: API request/response contracts for the controller.
- `docs/pipeline-formatted-script-spec.md`: Standard pipeline script format (AAPS) and canonical IR schema (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Deterministic generator for runnable bash pipeline runners from canonical IR.
- `docs/common-actions.md`: Common action contracts/specs (includes `update_readme`).
- `docs/workspace-layout.md`: Standard workspace folders + contracts (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: Start the AutoAppDev app (backend + PWA) in tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Start the AutoAppDev self-dev driver in tmux.
- `scripts/app-auto-development.sh`: The linear pipeline driver (plan -> backend -> PWA -> Android -> iOS -> review -> summary), with resume/state support.
- `scripts/generate_screenshot_docs.sh`: Screenshot -> markdown description generator (Codex-driven).
- `scripts/setup_backend_env.sh`: Backend conda env bootstrap for local runs.
- `examples/ralph-wiggum-example.sh`: Example Codex CLI automation helper.

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

## ✅ Prerequisites
- OS with `bash`.
- Python `3.11+`.
- Conda (`conda`) for the provided setup scripts.
- `tmux` for one-command backend+PWA or self-dev sessions.
- PostgreSQL reachable by `DATABASE_URL`.
- Optional: `codex` CLI for Codex-powered flows (self-dev, parse-llm fallback, auto-readme pipeline).

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
Edit `.env` and set at least:
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

## ⚙️ Configuration
Primary file: `.env` (see `docs/env.md` and `.env.example`).

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

Validate `.env` quickly:
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
### Start backend + PWA together (recommended)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
Defaults:
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### Start backend only
```bash
conda run -n autoappdev python -m backend.app
```

### Start PWA static server only
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### Run self-dev driver in tmux
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### Parse and store scripts
- Parse AAPS via API: `POST /api/scripts/parse`
- Import annotated shell: `POST /api/scripts/import-shell`
- Optional LLM parse: `POST /api/scripts/parse-llm` (requires `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

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

See `docs/api-contracts.md` for request/response shapes.

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
Then use the PWA Start/Pause/Resume/Stop controls and inspect `/api/logs`.

## 🧱 Development Notes
- The backend is Tornado-based and designed for local dev ergonomics (including permissive CORS for localhost split ports).
- Storage is PostgreSQL-first with compatibility behavior in `backend/storage.py`.
- PWA block keys and script `STEP.block` values are intentionally aligned (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in actions are readonly; clone before editing.
- `update_readme` action is path-safety constrained to workspace README targets under `auto-apps/<workspace>/README.md`.
- There are historical path/name references in some docs/scripts (`HeyCyan`, `LightMind`) inherited from project evolution. Current repo canonical path is this repository root.
- The root `i18n/` directory exists. Language README files are expected there in multilingual runs.

## 🩺 Troubleshooting
- `tmux not found`:
  - Install `tmux` or run backend/PWA manually.
- Backend fails on startup due to missing env:
  - Recheck `.env` against `.env.example` and `docs/env.md`.
- Database errors (connection/auth/schema):
  - Verify `DATABASE_URL`.
  - Re-run `conda run -n autoappdev python -m backend.apply_schema`.
  - Optional connectivity check: `conda run -n autoappdev python -m backend.db_smoketest`.
- PWA loads but cannot call API:
  - Ensure backend is listening on expected host/port.
  - Regenerate `pwa/config.local.js` by re-running `./scripts/run_autoappdev_tmux.sh`.
- Pipeline Start returns invalid transition:
  - Check current pipeline status first; start from `stopped` state.
- No log updates in UI:
  - Confirm `runtime/logs/pipeline.log` is being written.
  - Use `/api/logs` and `/api/logs/tail` directly to isolate UI vs backend issues.
- LLM parse endpoint returns disabled:
  - Set `AUTOAPPDEV_ENABLE_LLM_PARSE=1` and restart backend.

For a deterministic manual verification path, use `docs/end-to-end-demo-checklist.md`.

## 🗺️ Roadmap
- Complete remaining self-dev tasks beyond current `51 / 55` status.
- Expand workspace/materials/context tooling and stronger safe-path contracts.
- Continue improving action palette UX and editable action workflows.
- Deepen multilingual README/UI support across `i18n/` and runtime language switching.
- Strengthen smoke/integration checks and CI coverage (currently script-driven smoke checks are present; no full CI manifest is documented at root).

## 🤝 Contributing
Contributions are welcome via issues and pull requests.

Suggested workflow:
1. Fork and create a feature branch.
2. Keep changes focused and reproducible.
3. Prefer deterministic scripts/tests where possible.
4. Update docs when behavior/contracts change (`docs/*`, API contracts, examples).
5. Open a PR with context, validation steps, and any runtime assumptions.

Repository remotes currently include:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- an additional remote may be present in local clones for related repos.

## 📄 License
No root `LICENSE` file was detected in this repository snapshot.

Assumption note:
- Until a license file is added, treat usage/redistribution terms as unspecified and confirm with the maintainer.

## ❤️ Sponsor & Donate

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
