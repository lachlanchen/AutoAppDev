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

스크린샷/마크다운으로부터 앱을 단계적으로 구축할 때, Codex를 비대화형 도구로 활용하기 위한 재사용 가능한 스크립트와 가이드 모음입니다.

> 🎯 **Mission:** 앱 개발 파이프라인을 결정적(deterministic)이고, 재개 가능하며, 아티팩트 중심으로 만드는 것.
>
> 🧩 **Design principle:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ Project Signals

| 신호 | 현재 방향 |
| --- | --- |
| Runtime model | Tornado backend + static PWA controller |
| Pipeline execution | 결정적이며 재개 가능 (`start/pause/resume/stop`) |
| Persistence strategy | PostgreSQL 우선 + 호환성 폴백 동작 |
| Documentation flow | 루트 README를 기준으로 자동 생성되는 `i18n/` 변형 |

### 🔗 Quick Navigation

| 필요 | 이동 |
| --- | --- |
| 로컬에서 처음 실행 | [⚡ Quick Start](#-quick-start) |
| 환경 및 필수 변수 | [⚙️ Configuration](#-configuration) |
| API 표면 개요 | [📡 API Snapshot](#-api-snapshot) |
| 런타임/디버그 플레이북 | [🧭 Operational Runbooks](#-operational-runbooks) |
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
- [❓ FAQ](#-faq)
- [🗺️ Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [❤️ Support](#-support)
- [📄 License](#-license)
- [❤️ Sponsor & Donate](#-sponsor--donate)

## 🚀 Overview
AutoAppDev는 장시간 실행되고 중간 재개가 가능한 앱 개발 파이프라인을 제어하는 프로젝트입니다. 다음을 결합합니다.

1. Tornado 백엔드 API + PostgreSQL 기반 영속성(스토리지 코드의 로컬 JSON 폴백 동작 포함)
2. Scratch 스타일의 정적 PWA 컨트롤러 UI
3. 파이프라인 작성, 결정적 코드 생성, self-dev 루프, README 자동화를 위한 스크립트/문서

이 프로젝트는 엄격한 순서 제어와 아티팩트 중심 워크플로 이력을 전제로, 예측 가능한 에이전트 실행에 최적화되어 있습니다.

### 🎨 Why this repo exists

| 테마 | 실제 의미 |
| --- | --- |
| Determinism | Canonical pipeline IR + parser/import/codegen 워크플로를 반복 가능하게 설계 |
| Resumability | 장시간 실행을 위한 명시적 라이프사이클 상태 기계(`start/pause/resume/stop`) |
| Operability | 런타임 로그, inbox/outbox 채널, 스크립트 기반 검증 루프 |
| Documentation-first | 계약/스펙/예제가 `docs/`에 존재하고 다국어 README 흐름 자동화 |

## 🧭 Philosophy
AutoAppDev는 에이전트를 도구로 다루며, 엄격하고 재개 가능한 루프로 작업 안정성을 유지합니다.

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

컨트롤러 앱은 Scratch 유사 블록/액션(공통 `update_readme` 액션 포함)으로 같은 개념을 구현해, 각 워크스페이스를 최신 상태이면서 재현 가능하도록 유지하는 것을 목표로 합니다.

### 🔁 Lifecycle state intent

| 상태 전이 | 운영 의도 |
| --- | --- |
| `start` | stopped/ready 상태에서 파이프라인 실행 시작 |
| `pause` | 컨텍스트를 잃지 않고 장시간 실행을 안전하게 일시 중지 |
| `resume` | 저장된 런타임 상태/아티팩트에서 이어서 실행 |
| `stop` | 실행을 종료하고 비실행 상태로 복귀 |

## ✨ Features
- 재개 가능한 파이프라인 라이프사이클 제어: start, pause, resume, stop.
- AAPS 파이프라인 스크립트(`.aaps`)와 canonical IR(`autoappdev_ir` v1)을 위한 스크립트 라이브러리 API.
- 결정적 parser/import 파이프라인:
  - 포맷된 AAPS 스크립트 파싱.
  - `# AAPS:` 주석을 통한 annotated shell import.
  - 선택적 Codex 보조 파싱 폴백(`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- 내장 액션 + 수정 가능한 커스텀 액션을 포함한 액션 레지스트리(readonly 내장 액션은 clone/edit 흐름).
- Scratch 스타일 PWA 블록 + 런타임 로드 액션 팔레트(`GET /api/actions`).
- 런타임 메시징 채널:
  - Inbox (`/api/inbox`): 운영자 -> 파이프라인 가이드.
  - Outbox (`/api/outbox`): `runtime/outbox` 파일 큐 수집 포함.
- 백엔드 및 파이프라인 로그 증분 스트리밍(`/api/logs`, `/api/logs/tail`).
- canonical IR 기반 결정적 runner codegen(`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- 저장소의 반복적 진화를 위한 self-dev 드라이버(`scripts/auto-autoappdev-development.sh`).
- `i18n/` 하위 다국어 생성 스캐폴딩을 포함한 README 자동화 파이프라인.

## 📌 At A Glance

| 영역 | 상세 |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | PostgreSQL 우선, `backend/storage.py`의 호환 동작 포함 |
| Pipeline model | Canonical IR (`autoappdev_ir` v1) + AAPS 스크립트 형식 |
| Control flow | Start / Pause / Resume / Stop 라이프사이클 |
| Dev mode | 재개 가능한 self-dev 루프 + 결정적 script/codegen 워크플로 |
| README/i18n | `i18n/` 스캐폴딩 기반 README 자동화 파이프라인 |

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
- scripts, actions, plan, pipeline lifecycle, logs, inbox/outbox, workspace config용 controller API 노출.
- 파이프라인 스크립트 자산 검증 및 저장.
- 파이프라인 실행 상태와 상태 전이를 조정.
- DB pool이 없을 때도 결정적 폴백 동작 제공.

### Frontend responsibilities
- Scratch 스타일 블록 UI 및 파이프라인 편집 흐름 렌더링.
- 백엔드 레지스트리에서 액션 팔레트를 동적으로 로드.
- 라이프사이클 제어 + 상태/로그/메시지 모니터링.

## 📚 Contents
가장 자주 쓰는 문서/스크립트/예제를 빠르게 찾기 위한 참조 맵입니다.

- `docs/auto-development-guide.md`: 장시간 실행/재개 가능한 자동 개발 에이전트를 위한 이중 언어(EN/ZH) 철학 및 요구사항.
- `docs/ORDERING_RATIONALE.md`: 스크린샷 기반 단계 순서화의 근거 예시.
- `docs/controller-mvp-scope.md`: 컨트롤러 MVP 범위(화면 + 최소 API).
- `docs/end-to-end-demo-checklist.md`: 결정적 수동 end-to-end 데모 체크리스트(backend + PWA happy path).
- `docs/env.md`: 환경 변수(`.env`) 규약.
- `docs/api-contracts.md`: 컨트롤러의 API 요청/응답 계약.
- `docs/pipeline-formatted-script-spec.md`: 표준 파이프라인 스크립트 형식(AAPS) 및 canonical IR 스키마(TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: canonical IR에서 실행 가능한 bash 파이프라인 runner를 생성하는 결정적 생성기.
- `docs/common-actions.md`: 공통 action 계약/스펙(`update_readme` 포함).
- `docs/workspace-layout.md`: 표준 workspace 폴더 + 계약(`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: tmux에서 AutoAppDev 앱(backend + PWA) 시작.
- `scripts/run_autoappdev_selfdev_tmux.sh`: tmux에서 AutoAppDev self-dev 드라이버 시작.
- `scripts/app-auto-development.sh`: resume/state 지원 선형 파이프라인 드라이버(`plan -> backend -> PWA -> Android -> iOS -> review -> summary`).
- `scripts/generate_screenshot_docs.sh`: 스크린샷 -> markdown 설명 생성기(Codex 기반).
- `scripts/setup_autoappdev_env.sh`: 로컬 실행용 메인 conda 환경 bootstrap 스크립트.
- `scripts/setup_backend_env.sh`: 백엔드 환경 helper 스크립트.
- `examples/ralph-wiggum-example.sh`: Codex CLI 자동화 helper 예시.

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
- `bash`를 사용할 수 있는 OS.
- Python `3.11+`.
- 제공된 setup 스크립트를 위한 Conda(`conda`).
- 원커맨드 backend+PWA 또는 self-dev 세션용 `tmux`.
- `DATABASE_URL`로 접근 가능한 PostgreSQL.
- 선택 사항: Codex 기반 흐름(self-dev, parse-llm 폴백, auto-readme 파이프라인)을 위한 `codex` CLI.

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
| Local OS | Linux/macOS shell이 1차 대상(`bash` scripts) |
| Python runtime | `3.11` (`scripts/setup_autoappdev_env.sh`로 관리) |
| Persistence mode | PostgreSQL이 권장되며 canonical로 취급 |
| Fallback behavior | `backend/storage.py`는 장애 시나리오용 JSON 호환 폴백 포함 |
| Network model | localhost 분리 포트 개발 모델(backend + static PWA) |
| Agent tooling | LLM parse 보조나 self-dev 자동화를 쓸 때만 `codex` CLI 필수 |

이 README의 기본 가정:
- 별도 언급이 없으면 저장소 루트에서 명령을 실행합니다.
- 백엔드 시작 전에 `.env`가 설정되어 있습니다.
- 권장 원커맨드 워크플로를 위해 `conda`와 `tmux`를 사용할 수 있습니다.

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
`.env`를 편집하고 최소 다음을 설정하세요:
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

그다음 열기:
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

원커맨드 스모크 체크:
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
주요 파일: `.env` (`docs/env.md`, `.env.example` 참고).

### Important variables

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | 관례상 필수 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | 백엔드 바인딩 설정 |
| `DATABASE_URL` | PostgreSQL DSN (권장) |
| `AUTOAPPDEV_RUNTIME_DIR` | 런타임 디렉터리 재정의 (기본 `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | 기본 파이프라인 실행 대상 |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | `/api/scripts/parse-llm` 활성화 |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | action/endpoint용 Codex 기본값 |
| `AI_API_BASE_URL`, `AI_API_KEY` | 향후 통합을 위해 예약됨 |

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
| Start backend + PWA (recommended) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Start backend only | `conda run -n autoappdev python -m backend.app` | `.env`의 bind + DB 설정 사용 |
| Start PWA static server only | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | 프런트엔드만 점검할 때 유용 |
| Run self-dev driver in tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | 재개 가능한 self-development 루프 |

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
- 선택 사항: `/api/version`을 열어 예상한 backend 메타데이터가 반환되는지 확인.

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

핵심 API 그룹 한눈에 보기:

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

전체 예시:
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
그다음 PWA의 Start/Pause/Resume/Stop 제어를 사용하고 `/api/logs`를 확인하세요.

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
- 백엔드는 Tornado 기반이며 로컬 개발 편의성(로컬호스트 분리 포트에서의 완화된 CORS 포함)을 고려해 설계되었습니다.
- 스토리지는 PostgreSQL 우선이며 `backend/storage.py`에 호환 동작이 포함되어 있습니다.
- PWA 블록 키와 스크립트 `STEP.block` 값은 의도적으로 일치시켰습니다(`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- 내장 액션은 readonly이며 수정하려면 먼저 clone해야 합니다.
- `update_readme` 액션은 경로 안전성 제약으로 workspace README 대상(`auto-apps/<workspace>/README.md`)에만 허용됩니다.
- 일부 문서/스크립트에는 프로젝트 진화 과정에서 남은 과거 경로/이름 참조(`HeyCyan`, `LightMind`)가 있습니다. 현재 canonical 경로는 이 저장소 루트입니다.
- 루트 `i18n/` 디렉터리는 존재하며, 다국어 실행 시 그 위치의 언어별 README 파일을 기대합니다.

### Working model and state files
- 런타임 기본 경로는 `./runtime`이며 `AUTOAPPDEV_RUNTIME_DIR`로 오버라이드할 수 있습니다.
- self-dev 자동화의 상태/히스토리는 `references/selfdev/` 아래에 기록됩니다.
- README 파이프라인 아티팩트는 `.auto-readme-work/<timestamp>/` 아래에 기록됩니다.

### Testing posture (current)
- 저장소에는 스모크 체크와 결정적 데모 스크립트가 포함되어 있습니다.
- 루트 메타데이터 기준, 상위 레벨의 완전한 자동 테스트 스위트/CI 매니페스트는 아직 정의되어 있지 않습니다.
- 현재 가정: 검증은 주로 스크립트 중심(`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, end-to-end checklist)입니다.

## 🔐 Safety Notes
- `update_readme` 액션은 경로 순회 방어와 함께 workspace README 대상(`auto-apps/<workspace>/README.md`)으로 의도적으로 제한되어 있습니다.
- action registry 검증은 action spec 필드를 정규화하고 지원되는 reasoning 수준의 값 범위를 제한합니다.
- 저장소 스크립트는 신뢰된 로컬 실행을 가정합니다. 공유/프로덕션 인접 환경에서 실행 전 스크립트 본문을 검토하세요.
- `.env`에는 민감 값(`DATABASE_URL`, API keys)이 들어갈 수 있습니다. `.env`는 커밋하지 말고 로컬 개발 외 환경에서는 별도 시크릿 관리를 사용하세요.

## 🔧 Troubleshooting

| Symptom | What to check |
| --- | --- |
| `tmux not found` | `tmux`를 설치하거나 backend/PWA를 수동으로 실행하세요. |
| Backend fails on startup due to missing env | `.env.example`, `docs/env.md`를 기준으로 `.env`를 다시 확인하세요. |
| Database errors (connection/auth/schema) | `DATABASE_URL` 확인 후 `conda run -n autoappdev python -m backend.apply_schema`를 재실행하고, 필요 시 `conda run -n autoappdev python -m backend.db_smoketest`로 연결을 점검하세요. |
| PWA loads but cannot call API | backend가 예상 host/port에서 리슨 중인지 확인하고 `./scripts/run_autoappdev_tmux.sh` 재실행으로 `pwa/config.local.js`를 재생성하세요. |
| Pipeline Start returns invalid transition | 현재 파이프라인 상태를 먼저 확인하고 `stopped` 상태에서 시작하세요. |
| No log updates in UI | `runtime/logs/pipeline.log`가 기록되는지 확인하고, UI/백엔드 분리를 위해 `/api/logs`, `/api/logs/tail`을 직접 호출하세요. |
| LLM parse endpoint returns disabled | `AUTOAPPDEV_ENABLE_LLM_PARSE=1` 설정 후 backend를 재시작하세요. |
| `conda run -n autoappdev ...` fails | `./scripts/setup_autoappdev_env.sh`를 다시 실행하고 conda env `autoappdev` 존재 여부(`conda env list`)를 확인하세요. |
| Wrong API target in frontend | `pwa/config.local.js`가 존재하며 활성 backend host/port를 가리키는지 확인하세요. |

결정적인 수동 검증 경로는 `docs/end-to-end-demo-checklist.md`를 사용하세요.

## 🌐 README & i18n Workflow
- 루트 README는 README 자동화 파이프라인의 canonical 소스입니다.
- 다국어 변형본은 `i18n/` 아래에 있어야 합니다.
- i18n 디렉터리 상태: ✅ 이 저장소에 존재합니다.
- 이 저장소의 현재 언어 세트:
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
- 언어 네비게이션은 각 README 변형본 상단에 한 줄로 유지해야 합니다(언어 바 중복 금지).
- README 파이프라인 진입점: `prompt_tools/auto-readme-pipeline.sh`.

### i18n generation constraints (strict)
- canonical README 내용이 바뀌면 항상 다국어 생성을 처리해야 합니다.
- 언어 파일은 한 번에 하나씩 순차적으로 생성/업데이트하세요(대량 일괄 처리 금지).
- 각 변형본 상단에는 언어 옵션 네비게이션 라인을 정확히 1개만 유지하세요.
- 동일 파일 안에 언어 바를 중복하지 마세요.
- 번역본에서도 canonical 명령 스니펫, 링크, API 경로, 배지 의도를 보존하세요.

권장 one-by-one 생성 순서:
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
권장되며 일반 운영에서 사실상 필수로 가정합니다. 스토리지 레이어에 폴백 호환 동작은 있지만, 프로덕션에 가까운 사용에서는 `DATABASE_URL`을 통한 PostgreSQL 가용성을 전제로 하세요.

### Why both `AUTOAPPDEV_PORT` and `PORT`?
`AUTOAPPDEV_PORT`는 프로젝트 전용 변수이고, `PORT`는 배포 친화적 별칭입니다. 실행 경로에서 의도적으로 오버라이드하지 않는다면 둘을 동일하게 유지하세요.

### Where should I start if I only want to inspect APIs?
backend-only로 실행(`conda run -n autoappdev python -m backend.app`)한 뒤 `/api/health`, `/api/version`, `/api/config`부터 확인하고 `docs/api-contracts.md`에 나열된 script/action 엔드포인트로 진행하면 됩니다.

### Are multilingual READMEs generated automatically?
예. 저장소에 `prompt_tools/auto-readme-pipeline.sh`가 포함되어 있고, 각 언어 변형본은 `i18n/` 아래에서 파일 상단 1줄 언어 네비게이션 규칙과 함께 유지됩니다.

## 🗺️ Roadmap
- 현재 `51 / 55` 상태 이후 남은 self-dev 작업 완료.
- workspace/materials/context 도구 확장 및 더 강한 safe-path 계약 추가.
- action palette UX 및 편집 가능한 action 워크플로 지속 개선.
- `i18n/`과 런타임 언어 전환 전반에서 다국어 README/UI 지원 심화.
- 스모크/통합 점검 및 CI 커버리지 강화(현재는 스크립트 기반 스모크 점검 중심이며, 루트에 전체 CI 매니페스트는 문서화되어 있지 않음).
- AAPS v1 + canonical IR 주변 parser/import/codegen의 결정성 강화 지속.

## 🤝 Contributing
이슈와 Pull Request를 통한 기여를 환영합니다.

권장 워크플로:
1. Fork 후 기능 브랜치를 생성합니다.
2. 변경은 집중도 높고 재현 가능하게 유지합니다.
3. 가능하면 결정적 스크립트/테스트를 우선합니다.
4. 동작/계약이 바뀌면 문서(`docs/*`, API contracts, examples)를 함께 업데이트합니다.
5. 맥락, 검증 절차, 런타임 가정을 포함해 PR을 생성합니다.

현재 저장소 remote에는 다음이 포함되어 있습니다.
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 관련 저장소를 위해 로컬 clone에 추가 remote가 있을 수 있습니다(이 워크스페이스에서 발견된 예: `novel`).

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 License
이 저장소 스냅샷에서 루트 `LICENSE` 파일은 감지되지 않았습니다.

Assumption note:
- 라이선스 파일이 추가되기 전까지 사용/재배포 조건은 미지정 상태로 보고, 유지관리자에게 확인하세요.

## ❤️ Sponsor & Donate
| 채널 | 링크 |
| --- | --- |
| GitHub Sponsors | https://github.com/sponsors/lachlanchen |
| Donate | https://chat.lazying.art/donate |
| PayPal | https://paypal.me/RongzhouChen |
| Stripe | https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400 |

이 프로젝트가 워크플로에 도움이 되었다면, 후원은 self-dev 작업 지속, 문서 품질 개선, 툴링 강화에 직접적인 도움이 됩니다.
