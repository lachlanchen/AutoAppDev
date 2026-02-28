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
![Control Flow](https://img.shields.io/badge/Control%20Flow-Plan%20%E2%86%92%20Work%20%E2%86%92%20Verify%20%E2%86%92%20Summary-0f766e)

---

스크린샷/마크다운 기반으로 앱을 단계별로 빌드할 때, Codex를 비대화형 도구로 활용하기 위한 재사용 가능한 스크립트와 가이드 모음입니다.

> 🎯 **Mission:** 앱 개발 파이프라인을 결정적이며 재개 가능하고, 아티팩트 기반으로 운영 가능하게 만듭니다.
>
> 🧩 **Design principle:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Project Signals

| Signal | Current Direction |
| --- | --- |
| Runtime model | Tornado backend + static PWA controller |
| Pipeline execution | Deterministic and resumable (`start/pause/resume/stop`) |
| Persistence strategy | PostgreSQL-first with compatibility fallback behavior |
| Documentation flow | Canonical root README + automated `i18n/` variants |

### 🔗 Quick Navigation

| Need | Go to |
| --- | --- |
| 로컬 첫 실행 | [⚡ Quick Start](#-quick-start) |
| 환경 변수 및 설정 | [⚙️ Configuration](#-configuration) |
| API 개요 | [📡 API Snapshot](#-api-snapshot) |
| 런타임/디버그 런북 | [🧭 Operational Runbooks](#-operational-runbooks) |
| README/i18n 생성 규칙 | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| 트러블슈팅 매트릭스 | [🔧 Troubleshooting](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev Status (Auto-Updated)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

이 섹션은 `scripts/auto-autoappdev-development.sh`가 자동 업데이트합니다.
마커 사이의 내용은 수정하지 마세요.

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

## 🧭 Repository Snapshot

| Focus | Current setup |
| --- | --- |
| Core loop | Plan → Work → Debug → Fix → Summary → Commit/Push |
| Runtime model | Tornado backend + static PWA controller |
| State machine | `start` / `pause` / `resume` / `stop` |
| Persistence | PostgreSQL-first with JSON fallback compatibility |
| Documentation | Canonical `README.md` plus multilingual `i18n/` outputs |

## 🚀 Overview
AutoAppDev는 장시간 실행되는 재개 가능한 앱 개발 파이프라인을 제어하는 프로젝트입니다. 다음을 결합합니다.

1. PostgreSQL 기반 영속성을 갖춘 Tornado 백엔드 API(스토리지 코드의 로컬 JSON 폴백 동작 포함).
2. Scratch 스타일의 정적 PWA 컨트롤러 UI.
3. 파이프라인 작성, 결정적 코드 생성, self-dev 루프, README 자동화를 위한 스크립트와 문서.

이 프로젝트는 엄격한 순차 실행과 아티팩트 중심 워크플로 이력을 전제로, 예측 가능한 에이전트 실행에 최적화되어 있습니다.

### 🎨 Why this repo exists

| Theme | What it means in practice |
| --- | --- |
| Determinism | Canonical pipeline IR + parser/import/codegen 워크플로를 반복 가능하게 설계 |
| Resumability | 장시간 실행을 위한 명시적 라이프사이클 상태 기계(`start/pause/resume/stop`) |
| Operability | 런타임 로그, inbox/outbox 채널, 스크립트 기반 검증 루프 |
| Documentation-first | 계약/명세/예제가 `docs/`에 있고 다국어 README 자동화 흐름이 함께 동작 |

## 🧭 Philosophy
AutoAppDev는 에이전트를 도구로 다루며, 엄격하고 재개 가능한 루프로 작업 안정성을 유지합니다.

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

컨트롤러 앱은 Scratch 유사 블록/액션(공통 `update_readme` 액션 포함)으로 동일한 개념을 구현해, 각 워크스페이스를 최신 상태이면서 재현 가능하게 유지합니다.

### 🔁 Lifecycle state intent

| State transition | Operational intent |
| --- | --- |
| `start` | Begin a pipeline from stopped/ready state |
| `pause` | Halt long-running execution safely without losing context |
| `resume` | Continue from saved runtime state/artifacts |
| `stop` | End execution and return to a non-running state |

## ✨ Features
- 재개 가능한 파이프라인 라이프사이클 제어: start, pause, resume, stop.
- AAPS 파이프라인 스크립트(`.aaps`)와 canonical IR(`autoappdev_ir` v1)를 위한 스크립트 라이브러리 API.
- 결정적 parser/import 파이프라인:
  - 포맷된 AAPS 스크립트 파싱.
  - `# AAPS:` 주석을 통한 주석 셸 import.
  - 선택적 Codex 보조 파싱 폴백(`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- 내장 액션 + 편집 가능한 커스텀 액션을 포함한 액션 레지스트리(읽기 전용 내장 액션은 clone/edit 흐름).
- Scratch 스타일 PWA 블록과 런타임에서 동적 로드되는 액션 팔레트(`GET /api/actions`).
- 런타임 메시징 채널:
  - Inbox (`/api/inbox`): 운영자 -> 파이프라인 지침 채널
  - Outbox (`/api/outbox`): `runtime/outbox` 파일 큐 수집 포함
- 백엔드/파이프라인 로그의 증분 스트리밍 (`/api/logs`, `/api/logs/tail`).
- canonical IR 기반 결정적 runner codegen(`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- 리포지토리 반복 진화를 위한 self-dev 드라이버(`scripts/auto-autoappdev-development.sh`).
- README 자동화 파이프라인 (i18n 생성 스캐폴딩) 지원 (`i18n/`).

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
- 스크립트, 액션, plan, pipeline lifecycle, logs, inbox/outbox, workspace config를 위한 컨트롤러 API 제공
- 파이프라인 스크립트 자산 검증 및 저장
- 파이프라인 실행 상태 및 전이 관리
- DB pool 사용 불가 시 결정적 폴백 동작 제공

### Frontend responsibilities
- Scratch 스타일 블록 UI와 파이프라인 편집 흐름 렌더링
- 백엔드 레지스트리에서 액션 팔레트 동적 로드
- 라이프사이클 제어 수행 및 상태/로그/메시지 모니터링

## 📚 Contents
자주 사용하는 문서, 스크립트, 예제에 대한 참조 지도:

- `docs/auto-development-guide.md`: 장시간 실행/재개 가능한 자동 개발 에이전트의 철학과 요구사항(영문/중문).
- `docs/ORDERING_RATIONALE.md`: 스크린샷 기반 단계 순서화의 근거 예시.
- `docs/controller-mvp-scope.md`: 컨트롤러 MVP 범위(화면 + 최소 API).
- `docs/end-to-end-demo-checklist.md`: 결정적 수동 엔드투엔드 데모 체크리스트(backend + PWA happy path).
- `docs/env.md`: 환경 변수(`.env`) 규약.
- `docs/api-contracts.md`: 컨트롤러 API 요청/응답 계약.
- `docs/pipeline-formatted-script-spec.md`: 표준 파이프라인 스크립트 형식(AAPS)과 canonical IR 스키마(TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: canonical IR에서 실행 가능한 bash 파이프라인 runner를 생성하는 결정적 코드 생성기.
- `docs/common-actions.md`: 공통 액션 계약/스펙(`update_readme` 포함).
- `docs/workspace-layout.md`: 표준 workspace 폴더와 계약(`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: tmux에서 AutoAppDev 앱(backend + PWA) 시작.
- `scripts/run_autoappdev_selfdev_tmux.sh`: tmux에서 AutoAppDev self-dev 드라이버 시작.
- `scripts/app-auto-development.sh`: resume/state 지원이 포함된 선형 파이프라인 드라이버(`plan -> backend -> PWA -> Android -> iOS -> review -> summary`).
- `scripts/generate_screenshot_docs.sh`: 스크린샷 → markdown 설명 생성기(Codex 구동).
- `scripts/setup_autoappdev_env.sh`: 로컬 실행을 위한 메인 conda 환경 부트스트랩 스크립트.
- `scripts/setup_backend_env.sh`: 백엔드 환경 도우미 스크립트.
- `examples/ralph-wiggum-example.sh`: Codex CLI 자동화 예시.

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
- `bash`가 있는 OS.
- Python `3.11+`.
- 제공된 setup 스크립트를 위한 Conda(`conda`).
- 백엔드+PWA 또는 self-dev를 한 번에 띄우는 `tmux`.
- `DATABASE_URL`로 접근 가능한 PostgreSQL.
- 선택 사항: Codex 기반 흐름(self-dev, parse-llm 폴백, auto-readme 파이프라인)을 위한 `codex` CLI.

빠른 요구사항 정리:

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
| Local OS | Linux/macOS shell이 1차 대상 (`bash` scripts) |
| Python runtime | `3.11` (`scripts/setup_autoappdev_env.sh`로 관리) |
| Persistence mode | PostgreSQL을 기본값으로 사용하며 canonical로 처리 |
| Fallback behavior | `backend/storage.py`에 장애 상황용 JSON 호환 폴백 포함 |
| Network model | localhost 분할 포트 개발 모델(backend + static PWA) |
| Agent tooling | LLM 보조 파싱 또는 self-dev 자동화 사용 시에만 `codex` CLI 필수 |

이 README의 가정:
- 별도 언급이 없으면 저장소 루트에서 명령을 실행합니다.
- 백엔드 서비스를 시작하기 전에 `.env`를 설정합니다.
- 권장 one-command 워크플로를 위해 `conda`와 `tmux`를 사용할 수 있어야 합니다.

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
`.env`를 편집하고 최소한 다음을 설정합니다.
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT` (또는 `PORT`)

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

그다음 열기:
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

원커맨드 smoke-check:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

빠른 엔드포인트 정리:

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
주요 파일: `.env` (`docs/env.md`, `.env.example` 참조).

### Important variables

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | 관례상 필수 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | 백엔드 바인딩 설정 |
| `DATABASE_URL` | PostgreSQL DSN (우선 사용) |
| `AUTOAPPDEV_RUNTIME_DIR` | 런타임 디렉터리 오버라이드(기본값 `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 기본 파이프라인 실행 대상 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | `/api/scripts/parse-llm` 활성화 |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | 액션/엔드포인트용 Codex 기본값 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 향후 통합을 위해 예약 |

`.env` 빠른 검증:
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
| 백엔드 + PWA 시작 (권장) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| 백엔드만 시작 | `conda run -n autoappdev python -m backend.app` | `.env`의 바인딩 + DB 설정 사용 |
| PWA 정적 서버만 시작 | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | 프론트엔드만 점검할 때 유용 |
| tmux에서 self-dev 드라이버 실행 | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 재개 가능한 self-development 루프 |

### Common script options
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parse and store scripts
- API로 AAPS 파싱: `POST /api/scripts/parse`
- 주석형 셸 import: `POST /api/scripts/import-shell`
- 선택적 LLM 파싱: `POST /api/scripts/parse-llm` (`AUTOAPPDEV_ENABLE_LLM_PARSE=1` 필요)

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

요청/응답 스키마는 `docs/api-contracts.md`를 참고하세요.

## 🧭 Operational Runbooks

### Runbook: bring up the full local stack
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

검증 체크포인트:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- `http://127.0.0.1:5173/`를 열고 UI가 `/api/config`를 로드할 수 있는지 확인.
- 선택 항목: `/api/version`을 열어 예상한 backend 메타데이터가 반환되는지 확인.

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

주요 API 그룹 한눈 정리:

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
그다음 PWA의 Start/Pause/Resume/Stop 제어를 사용하고 `/api/logs`를 확인합니다.

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
- 백엔드는 Tornado 기반이며 로컬 개발 용이성을 위해 설계되었고(로컬호스트 분할 포트 환경의 완화된 CORS 포함).
- 스토리지는 PostgreSQL 우선이며 `backend/storage.py`에 호환 동작이 포함되어 있습니다.
- PWA 블록 키와 스크립트 `STEP.block` 값이 의도적으로 정렬되어 있습니다(`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- 내장 액션은 readonly이므로 수정하려면 먼저 clone 합니다.
- `update_readme` 액션은 경로 안전성 제약으로 워크스페이스 README 대상(`auto-apps/<workspace>/README.md`)만 허용합니다.
- 일부 문서/스크립트에는 프로젝트 진화 과정의 과거 경로/이름(`HeyCyan`, `LightMind`)이 남아 있을 수 있습니다. 현재 canonical 경로는 이 저장소 루트입니다.
- 루트 `i18n/` 디렉터리가 존재하며, 다국어 README는 해당 디렉터리에 유지됩니다.

### Working model and state files
- 런타임 기본 경로는 `./runtime`이며 `AUTOAPPDEV_RUNTIME_DIR`로 오버라이드할 수 있습니다.
- self-dev 자동화 상태/히스토리는 `references/selfdev/` 하위에 기록됩니다.
- README 파이프라인 아티팩트는 `.auto-readme-work/<timestamp>/`에 기록됩니다.

### Testing posture (current)
- 저장소에는 스모크 체크와 결정적 데모 스크립트가 포함되어 있습니다.
- 루트 메타데이터 기준, 상단 자동 테스트/CI 매니페스트는 아직 완성되지 않았습니다.
- 현재 가정: 검증은 주로 스크립트 중심입니다(`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, 엔드투엔드 체크리스트).

## 🔐 Safety Notes
- `update_readme` 액션은 경로 순회 공격 방어와 함께 워크스페이스 README 대상(`auto-apps/<workspace>/README.md`)으로 의도적으로 제한됩니다.
- 액션 레지스트리 검증은 action spec 필드를 정규화하고 지원되는 reasoning 레벨의 값 범위를 제한합니다.
- 저장소 스크립트는 신뢰된 로컬 실행을 가정합니다. 공유 또는 운영 근접 환경에서는 실행 전 스크립트를 검토하세요.
- `.env`에는 민감한 값(`DATABASE_URL`, API keys)이 포함될 수 있습니다. `.env`는 커밋하지 말고 로컬 개발 외부에서는 별도 시크릿 관리 방식을 사용하세요.

## 🔧 Troubleshooting

| Symptom | What to check |
| --- | --- |
| `tmux not found` | `tmux`를 설치하거나 backend/PWA를 수동으로 실행하세요. |
| Backend starts fail due to missing env | `.env.example`와 `docs/env.md`로 `.env`를 재확인하세요. |
| Database errors (connection/auth/schema) | `DATABASE_URL`을 확인하고 `conda run -n autoappdev python -m backend.apply_schema`를 다시 실행하세요. (선택) 연결 점검: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA loads but cannot call API | backend가 기대 host/port에서 실행 중인지 확인하고, `./scripts/run_autoappdev_tmux.sh`를 다시 실행해 `pwa/config.local.js`를 재생성하세요. |
| Pipeline Start returns invalid transition | 현재 파이프라인 상태를 먼저 확인하고 `stopped`에서 시작하세요. |
| No log updates in UI | `runtime/logs/pipeline.log`가 쓰이는지 확인하고, UI 이슈 분리를 위해 `/api/logs`, `/api/logs/tail`을 직접 조회하세요. |
| LLM parse endpoint returns disabled | `AUTOAPPDEV_ENABLE_LLM_PARSE=1`로 설정 후 backend를 재시작하세요. |
| `conda run -n autoappdev ...` 실패 | `./scripts/setup_autoappdev_env.sh`를 재실행하고 conda env `autoappdev` 존재 여부를 `conda env list`로 확인하세요. |
| Wrong API target in frontend | `pwa/config.local.js` 존재 여부와 활성 backend host/port 지정 여부를 확인하세요. |

결정론적 수동 검증은 `docs/end-to-end-demo-checklist.md`를 이용하세요.

## 🌐 README & i18n Workflow
- root README는 README 자동화 파이프라인의 canonical 소스입니다.
- 다국어 README는 `i18n/` 아래에 있어야 합니다.
- i18n 디렉터리 상태: ✅ 현재 저장소에 존재.
- 현재 저장소 언어 목록:
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
- 각 README 변형의 첫 줄에는 언어 네비게이션을 딱 하나만 유지합니다(중복 언어 바 금지).
- README 파이프라인 진입점: `prompt_tools/auto-readme-pipeline.sh`.

### i18n generation constraints (strict)
- canonical README 내용이 바뀌면 반드시 다국어 생성도 처리해야 합니다.
- 언어 파일은 순차적으로 하나씩 생성/업데이트합니다(일괄이 아닌).
- 각 변형 상단에는 단일 언어 네비게이션 줄만 유지합니다.
- 동일 파일 내 언어 바 중복을 금지합니다.
- canonical 커맨드 스니펫, 링크, API 경로, 배지 의도는 유지하세요.

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
- 이 파일은 저장소 내용을 기반으로 생성되어 canonical 초안 진입점으로 보존됩니다.

## ❓ FAQ

### Is PostgreSQL mandatory?
운영에 권장되며 사실상 필수로 가정합니다. 스토리지 레이어에 폴백 호환 동작이 있지만, 운영 환경에서는 `DATABASE_URL`을 통해 PostgreSQL 사용 가능하다고 가정합니다.

### Why both `AUTOAPPDEV_PORT` and `PORT`?
`AUTOAPPDEV_PORT`는 프로젝트 전용 변수이고, `PORT`는 배포 친화적인 별칭입니다. 런칭 경로에서 의도적으로 오버라이드하지 않는 한 둘은 동일하게 맞춰 두는 것이 좋습니다.

### Where should I start if I only want to inspect APIs?
백엔드만 실행한 뒤(`conda run -n autoappdev python -m backend.app`) `/api/health`, `/api/version`, `/api/config`를 확인하고, 그다음 `docs/api-contracts.md`에 나열된 script/action 엔드포인트를 확인합니다.

### Are multilingual READMEs generated automatically?
예. 저장소에는 `prompt_tools/auto-readme-pipeline.sh`가 포함되어 있고, 각 언어 변형은 `i18n/`에서 관리되며 파일 맨 위에 언어 네비게이션이 1줄 존재합니다.

## 🗺️ Roadmap
- 현재 `51 / 55` 상태 이후 남은 self-dev 작업을 완료합니다.
- workspace/materials/context 도구를 확장하고 더 강한 safe-path 계약을 추가합니다.
- action palette UX와 편집 가능한 action 워크플로를 계속 개선합니다.
- `i18n/` 및 런타임 언어 전환 전반에서 다국어 README/UI 지원을 심화합니다.
- 스모크/통합 점검과 CI 커버리지를 강화합니다(현재는 스크립트 기반 스모크 점검이 있으며 루트에는 전체 CI 매니페스트 미기재).
- AAPS v1 및 canonical IR 주변 parser/import/codegen 결정론을 강화합니다.

## 🤝 Contributing
이슈와 PR을 통해 기여를 환영합니다.

권장 워크플로:
1. Fork 후 feature branch 생성
2. 변경사항은 집중적이고 재현 가능하게 유지
3. 가능한 경우 결정론적 스크립트/테스트 우선 사용
4. 동작/계약이 변경되면 문서 업데이트(`docs/*`, API contracts, examples)
5. PR에는 맥락, 검증 단계, 런타임 가정 사항을 포함

현재 저장소 remotes:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 로컬 클론에 따라 추가 리모트가 있을 수 있습니다(예시: 이 워크스페이스의 `novel`).

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

이 저장소 스냅샷에서 루트 `LICENSE` 파일이 감지되지 않았습니다.

Assumption note:
- 라이선스 파일이 추가될 때까지 사용/재배포 조건은 미확정 상태이며, 유지 관리자에게 확인하세요.
