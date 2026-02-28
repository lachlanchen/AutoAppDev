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

Codex를 비대화형 도구로 활용해 스크린샷/마크다운으로부터 앱을 단계적으로 구축하기 위한 재사용 가능한 스크립트 + 가이드 모음입니다.

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev 상태 (자동 업데이트)

- 업데이트 시각: 2026-02-16T00:27:20Z
- Phase 커밋: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- 진행률: 55개 작업 중 51개 완료
- Codex 세션: `019c6056-f33a-7f31-b08f-0ca40c365351`
- 철학: Plan -> Work -> Verify -> Summary -> Commit/Push (선형, 재개 가능)

이 섹션은 `scripts/auto-autoappdev-development.sh`에서 업데이트됩니다.
마커 사이의 내용은 직접 수정하지 마세요.

<!-- AUTOAPPDEV:STATUS:END -->

## 🚀 개요
AutoAppDev는 장시간 실행되고 중단 후 재개 가능한 앱 개발 파이프라인을 위한 컨트롤러 프로젝트입니다. 다음 요소를 결합합니다.

1. Tornado 백엔드 API와 PostgreSQL 기반 영속성(스토리지 코드의 로컬 JSON 폴백 동작 포함)
2. Scratch 스타일의 정적 PWA 컨트롤러 UI
3. 파이프라인 작성, 결정적 코드 생성, 셀프 개발 루프, README 자동화를 위한 스크립트와 문서

### 한눈에 보기

| 영역 | 상세 |
| --- | --- |
| 핵심 런타임 | Tornado 백엔드 + 정적 PWA 프론트엔드 |
| 영속성 | PostgreSQL 우선, `backend/storage.py`의 호환 동작 포함 |
| 파이프라인 모델 | 정식 IR(`autoappdev_ir` v1) 및 AAPS 스크립트 포맷 |
| 제어 흐름 | Start / Pause / Resume / Stop 라이프사이클 |
| 개발 모드 | 재개 가능한 셀프 개발 루프 + 결정적 스크립트/코드생성 워크플로 |
| README/i18n | `i18n/` 스캐폴딩을 포함한 자동화 README 파이프라인 |

## 🧭 철학
AutoAppDev는 에이전트를 도구로 취급하고, 엄격하고 재개 가능한 루프를 통해 작업 안정성을 유지합니다:
1. 계획(Plan)
2. 구현(Implement)
3. 디버그/검증(Debug/verify, 타임아웃 포함)
4. 수정(Fix)
5. 요약 + 로그(Summarize + log)
6. 커밋 + 푸시(Commit + push)

컨트롤러 앱은 각 워크스페이스를 최신 상태이면서 재현 가능하게 유지하기 위해, 동일한 개념을 Scratch 스타일 블록/액션(공통 `update_readme` 액션 포함)으로 구현하는 것을 목표로 합니다.

## ✨ 기능
- 재개 가능한 파이프라인 라이프사이클 제어: start, pause, resume, stop.
- AAPS 파이프라인 스크립트(`.aaps`) 및 정식 IR(`autoappdev_ir` v1)을 위한 스크립트 라이브러리 API.
- 결정적 파서/임포트 파이프라인:
  - 포맷된 AAPS 스크립트 파싱
  - `# AAPS:` 주석을 통한 annotated shell 임포트
  - 선택적 Codex 보조 파싱 폴백(`AUTOAPPDEV_ENABLE_LLM_PARSE=1`)
- 빌트인 + 수정 가능/커스텀 액션을 포함한 액션 레지스트리(읽기 전용 빌트인은 clone/edit 흐름 사용).
- Scratch 스타일 PWA 블록과 런타임 로드 액션 팔레트(`GET /api/actions`).
- 런타임 메시징 채널:
  - 운영자 -> 파이프라인 가이드를 위한 Inbox(`/api/inbox`)
  - `runtime/outbox` 파일 큐 수집을 포함하는 Outbox(`/api/outbox`)
- 백엔드/파이프라인 로그의 점진적 스트리밍(`/api/logs`, `/api/logs/tail`).
- 정식 IR 기반 결정적 러너 코드 생성(`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- 저장소 반복 진화를 위한 셀프 개발 드라이버(`scripts/auto-autoappdev-development.sh`).
- `i18n/` 하위 다국어 생성 스캐폴딩을 갖춘 README 자동화 파이프라인.

## 📚 구성
- `docs/auto-development-guide.md`: 장시간 실행, 재개 가능한 자동 개발 에이전트를 위한 이중언어(EN/ZH) 철학 및 요구사항.
- `docs/ORDERING_RATIONALE.md`: 스크린샷 기반 단계 순서화 예시 근거.
- `docs/controller-mvp-scope.md`: 컨트롤러 MVP 범위(화면 + 최소 API).
- `docs/end-to-end-demo-checklist.md`: 결정적 수동 E2E 데모 체크리스트(백엔드 + PWA 해피패스).
- `docs/env.md`: 환경 변수(.env) 규약.
- `docs/api-contracts.md`: 컨트롤러 API 요청/응답 계약.
- `docs/pipeline-formatted-script-spec.md`: 표준 파이프라인 스크립트 포맷(AAPS) 및 정식 IR 스키마(TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: 정식 IR로부터 실행 가능한 bash 파이프라인 러너를 생성하는 결정적 제너레이터.
- `docs/common-actions.md`: 공통 액션 계약/스펙(`update_readme` 포함).
- `docs/workspace-layout.md`: 표준 워크스페이스 폴더 + 계약(materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: tmux에서 AutoAppDev 앱(백엔드 + PWA) 시작.
- `scripts/run_autoappdev_selfdev_tmux.sh`: tmux에서 AutoAppDev 셀프 개발 드라이버 시작.
- `scripts/app-auto-development.sh`: 선형 파이프라인 드라이버(plan -> backend -> PWA -> Android -> iOS -> review -> summary), resume/state 지원 포함.
- `scripts/generate_screenshot_docs.sh`: 스크린샷 -> 마크다운 설명 생성기(Codex 기반).
- `scripts/setup_backend_env.sh`: 로컬 실행용 백엔드 conda 환경 부트스트랩.
- `examples/ralph-wiggum-example.sh`: Codex CLI 자동화 헬퍼 예시.

## 🗂️ 프로젝트 구조
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

## ✅ 사전 요구사항
- `bash`를 사용할 수 있는 OS.
- Python `3.11+`.
- 제공된 설정 스크립트를 위한 Conda(`conda`).
- 한 번에 백엔드+PWA 또는 셀프 개발 세션을 실행하기 위한 `tmux`.
- `DATABASE_URL`로 접근 가능한 PostgreSQL.
- 선택 사항: Codex 기반 플로우(셀프 개발, parse-llm 폴백, auto-readme 파이프라인)를 위한 `codex` CLI.

## 🛠️ 설치
### 1) 저장소 클론 및 진입
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) 환경 설정
```bash
cp .env.example .env
```
`.env`를 편집해 최소한 다음을 설정하세요:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` 및 `AUTOAPPDEV_PORT`(또는 `PORT`)

### 3) 백엔드 환경 생성/업데이트
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) 데이터베이스 스키마 적용
```bash
conda run -n autoappdev python -m backend.apply_schema
```

## ⚙️ 설정
주요 파일: `.env` (`docs/env.md` 및 `.env.example` 참고).

### 주요 변수

| 변수 | 용도 |
| --- | --- |
| `SECRET_KEY` | 관례상 필수 |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | 백엔드 바인딩 설정 |
| `DATABASE_URL` | PostgreSQL DSN(권장) |
| `AUTOAPPDEV_RUNTIME_DIR` | 런타임 디렉터리 재정의(기본값 `./runtime`) |
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

## ▶️ 사용법
### 백엔드 + PWA 동시 시작 (권장)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
기본값:
- 백엔드: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### 백엔드만 시작
```bash
conda run -n autoappdev python -m backend.app
```

### PWA 정적 서버만 시작
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### tmux에서 셀프 개발 드라이버 실행
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### 스크립트 파싱 및 저장
- API로 AAPS 파싱: `POST /api/scripts/parse`
- 주석된 쉘 임포트: `POST /api/scripts/import-shell`
- 선택적 LLM 파싱: `POST /api/scripts/parse-llm` (`AUTOAPPDEV_ENABLE_LLM_PARSE=1` 필요)

### 파이프라인 제어 API
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### 그 외 자주 쓰는 API
- 헬스/버전/설정: `/api/health`, `/api/version`, `/api/config`
- 계획/스크립트: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- 액션: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- 메시징: `/api/chat`, `/api/inbox`, `/api/outbox`
- 로그: `/api/logs`, `/api/logs/tail`

요청/응답 형태는 `docs/api-contracts.md`를 참고하세요.

## 🧪 예시
### AAPS 예시
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

### 결정적 러너 생성
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### 결정적 데모 파이프라인
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
그 후 PWA의 Start/Pause/Resume/Stop 제어를 사용하고 `/api/logs`를 확인하세요.

## 🧱 개발 노트
- 백엔드는 Tornado 기반이며, 로컬 개발 편의성을 위해 설계되었습니다(로컬호스트 분리 포트에서 동작하는 관대한 CORS 포함).
- 스토리지는 PostgreSQL 우선이며 `backend/storage.py`에 호환 동작이 있습니다.
- PWA 블록 키와 스크립트 `STEP.block` 값은 의도적으로 정렬되어 있습니다(`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- 빌트인 액션은 읽기 전용이며, 수정 전 clone이 필요합니다.
- `update_readme` 액션은 워크스페이스의 README 대상(`auto-apps/<workspace>/README.md`)으로 경로 안전성이 제한됩니다.
- 일부 문서/스크립트에는 프로젝트 진화 과정에서 이어진 과거 경로/이름 참조(`HeyCyan`, `LightMind`)가 있습니다. 현재 저장소의 정식 경로는 이 저장소 루트입니다.
- 루트 `i18n/` 디렉터리가 존재하며, 다국어 실행에서는 해당 위치의 언어별 README 파일이 기대됩니다.

## 🩺 문제 해결
- `tmux not found`:
  - `tmux`를 설치하거나 백엔드/PWA를 수동 실행하세요.
- 환경 변수 누락으로 백엔드 시작 실패:
  - `.env.example`, `docs/env.md`를 기준으로 `.env`를 다시 확인하세요.
- 데이터베이스 오류(연결/인증/스키마):
  - `DATABASE_URL`을 확인하세요.
  - `conda run -n autoappdev python -m backend.apply_schema`를 다시 실행하세요.
  - 선택적 연결 확인: `conda run -n autoappdev python -m backend.db_smoketest`.
- PWA는 로드되지만 API 호출 실패:
  - 백엔드가 예상 host/port에서 수신 중인지 확인하세요.
  - `./scripts/run_autoappdev_tmux.sh`를 다시 실행해 `pwa/config.local.js`를 재생성하세요.
- Pipeline Start가 invalid transition 반환:
  - 먼저 현재 파이프라인 상태를 확인하세요. `stopped` 상태에서 시작해야 합니다.
- UI에서 로그 업데이트 없음:
  - `runtime/logs/pipeline.log`가 실제로 쓰이고 있는지 확인하세요.
  - `/api/logs`, `/api/logs/tail`을 직접 호출해 UI 문제인지 백엔드 문제인지 분리하세요.
- LLM parse endpoint가 disabled 반환:
  - `AUTOAPPDEV_ENABLE_LLM_PARSE=1`을 설정하고 백엔드를 재시작하세요.

결정적인 수동 검증 경로는 `docs/end-to-end-demo-checklist.md`를 사용하세요.

## 🗺️ 로드맵
- 현재 `51 / 55` 상태 이후 남은 셀프 개발 작업 완료.
- 워크스페이스/materials/context 도구 확장 및 안전 경로 계약 강화.
- 액션 팔레트 UX 및 수정 가능한 액션 워크플로 지속 개선.
- `i18n/` 및 런타임 언어 전환 전반에서 다국어 README/UI 지원 심화.
- 스모크/통합 점검과 CI 커버리지 강화(현재는 스크립트 기반 스모크 점검이 존재하며, 루트에 전체 CI 매니페스트는 문서화되어 있지 않음).

## 🤝 기여
이슈와 Pull Request를 통한 기여를 환영합니다.

권장 워크플로:
1. 포크 후 기능 브랜치를 생성하세요.
2. 변경 사항은 집중적이고 재현 가능하게 유지하세요.
3. 가능하면 결정적 스크립트/테스트를 우선하세요.
4. 동작/계약이 변경되면 문서(`docs/*`, API 계약, 예시)를 업데이트하세요.
5. 맥락, 검증 단계, 런타임 가정을 포함해 PR을 열어 주세요.

현재 저장소 리모트에는 다음이 포함됩니다:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- 로컬 클론에는 관련 저장소를 위한 추가 리모트가 있을 수 있습니다.

## 📄 라이선스
이 저장소 스냅샷의 루트에서는 `LICENSE` 파일이 감지되지 않았습니다.

가정 참고:
- 라이선스 파일이 추가되기 전까지 사용/재배포 조건은 명시되지 않은 것으로 보고, 유지관리자에게 확인하세요.

## ❤️ 스폰서 및 후원

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
