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

Переиспользуемые скрипты и руководства для покадровой/по шагам сборки приложений из скриншотов и markdown с использованием Codex как неинтерактивного инструмента.

> 🎯 **Миссия:** сделать пайплайны разработки приложений детерминированными, возобновляемыми и ориентированными на артефакты.
>
> 🧩 **Принцип проектирования:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ Project Signals

| Сигнал | Текущее направление |
| --- | --- |
| Runtime model | Tornado backend + static PWA controller |
| Pipeline execution | Детеминированное и возобновляемое (`start/pause/resume/stop`) |
| Persistence strategy | PostgreSQL-first с fallback-совместимостью |
| Documentation flow | Канонический корневой README + автоматические варианты в `i18n/` |

### 🔗 Quick Navigation

| Нужна помощь | Перейти |
| --- | --- |
| Первый локальный запуск | [⚡ Quick Start](#-quick-start) |
| Окружение и обязательные переменные | [⚙️ Configuration](#-configuration) |
| Срез API | [📡 API Snapshot](#-api-snapshot) |
| Плейбуки запуска и диагностики | [🧭 Operational Runbooks](#-operational-runbooks) |
| Правила README/i18n | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| Матрица устранения неполадок | [🔧 Troubleshooting](#-troubleshooting) |

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

## 🚀 Overview
AutoAppDev — это управляющий проект для долгоживущих, возобновляемых пайплайнов разработки приложений. Он объединяет:

1. Backend API на Tornado с персистентностью в PostgreSQL (плюс локальное fallback-поведение JSON в коде хранилища).
2. Статический PWA-контроллер в стиле Scratch.
3. Скрипты и документацию для авторинга пайплайнов, детерминированной генерации кода, циклов self-development и автоматизации README.

Проект оптимизирован под предсказуемое выполнение агентами с строгой последовательностью и историей, ориентированной на артефакты.

### 🎨 Why this repo exists

| Тема | Что это означает на практике |
| --- | --- |
| Determinism | Канонический pipeline IR + parser/import/codegen-процессы, сконструированные для повторяемости |
| Resumability | Явная машина состояний (`start/pause/resume/stop`) для долгих прогонов |
| Operability | Runtime-логи, inbox/outbox каналы и скриптовые циклы верификации |
| Documentation-first | Контракты, спецификации и примеры в `docs/`, с автоматизированным многоязычным потоком README |

## 🧭 Philosophy
AutoAppDev рассматривает агентов как инструменты и поддерживает стабильную работу через строгий, возобновляемый цикл:

1. Plan
2. Implement
3. Debug/verify (с таймаутами)
4. Fix
5. Summarize + log
6. Commit + push

Контроллер-проект старается отражать те же принципы в Scratch-подобных блоках/действиях (включая общее действие `update_readme`), чтобы каждый workspace оставался актуальным и воспроизводимым.

### 🔁 Lifecycle state intent

| Переход состояния | Операционный смысл |
| --- | --- |
| `start` | Запустить пайплайн из состояния stopped/ready |
| `pause` | Безопасно приостановить длительное выполнение без потери контекста |
| `resume` | Возобновить выполнение из сохраненного runtime-состояния/артефактов |
| `stop` | Завершить выполнение и вернуться в неактивное состояние |

## ✨ Features
- Возобновляемое управление жизненным циклом пайплайна: start, pause, resume, stop.
- Script library API для AAPS pipeline scripts (`.aaps`) и канонического IR (`autoappdev_ir` v1).
- Детеминированный pipeline parser/import:
  - Разбор форматированных AAPS скриптов.
  - Импорт аннотированного shell через комментарии `# AAPS:`.
  - Опциональный fallback с использованием Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Реестр действий с встроенными и настраиваемыми action (clone/edit-поток для только для чтения built-ins).
- Scratch-подобные PWA-блоки и runtime-загружаемая палитра действий (`GET /api/actions`).
- Каналы runtime-сообщений:
  - Inbox (`/api/inbox`) для оператора -> указаний пайплайну.
  - Outbox (`/api/outbox`) с приёмом файловой очереди из `runtime/outbox`.
- Инкрементальная потоковая выдача логов backend и пайплайна (`/api/logs`, `/api/logs/tail`).
- Детеминированный codegen runner-а из канонического IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev драйвер для итеративного развития репозитория (`scripts/auto-autoappdev-development.sh`).
- Конвейер автоматизации README с каркасом многоязычной генерации в `i18n/`.

## 📌 At A Glance

| Область | Детали |
| --- | --- |
| Core runtime | Tornado backend + статический PWA frontend |
| Persistence | PostgreSQL-first с compatibility-поведением в `backend/storage.py` |
| Pipeline model | Канонический IR (`autoappdev_ir` v1) и формат скриптов AAPS |
| Control flow | Жизненный цикл Start / Pause / Resume / Stop |
| Dev mode | Возобновляемый self-dev цикл + детерминированные script/codegen процессы |
| README/i18n | Автоматизированный README-пайплайн с каркасом `i18n/` |

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
- Expose controller API для скриптов, действий, плана, жизненного цикла пайплайна, логов, inbox/outbox и конфигурации workspace.
- Проверять и сохранять assets скриптов пайплайна.
- Координировать выполнение и переходы состояний пайплайна.
- Обеспечивать детерминированное fallback-поведение при недоступности DB pool.

### Frontend responsibilities
- Отрисовывать Scratch-подобный UI блоков и поток редактирования пайплайна.
- Динамически загружать палитру действий из backend registry.
- Упаковывать и запускать lifecycle-контроли, следить за статусом/логами/сообщениями.

## 📚 Contents
Справочная карта наиболее используемых документов, скриптов и примеров:

- `docs/auto-development-guide.md`: двуязычная (EN/ZH) философия и требования к долгоживущему, возобновляемому self-development агенту.
- `docs/ORDERING_RATIONALE.md`: пример обоснования порядка screenshot-driven шагов.
- `docs/controller-mvp-scope.md`: границы Controller MVP (экраны + минимальные API).
- `docs/end-to-end-demo-checklist.md`: детерминированный ручной чеклист end-to-end демо (backend + PWA happy path).
- `docs/env.md`: соглашения по переменным окружения (`.env`).
- `docs/api-contracts.md`: контракты запросов/ответов API контроллера.
- `docs/pipeline-formatted-script-spec.md`: стандартный формат pipeline scripts (AAPS) и схема канонического IR (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: детерминированный генератор исполняемых bash pipeline runner из канонического IR.
- `docs/common-actions.md`: контракты/common action (включая `update_readme`).
- `docs/workspace-layout.md`: стандартные папки workspace + контракты (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: запуск AutoAppDev (backend + PWA) в tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: запуск self-dev драйвера AutoAppDev в tmux.
- `scripts/app-auto-development.sh`: линейный pipeline driver (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) с поддержкой resume/state.
- `scripts/generate_screenshot_docs.sh`: генератор описаний screenshot -> markdown (на основе Codex).
- `scripts/setup_autoappdev_env.sh`: основной bootstrap-скрипт conda окружения для локальных запусков.
- `scripts/setup_backend_env.sh`: вспомогательный скрипт окружения backend.
- `examples/ralph-wiggum-example.sh`: пример helper-скрипта автоматизации Codex CLI.

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
- ОС с `bash`.
- Python `3.11+`.
- Conda (`conda`) для предоставленных setup-скриптов.
- `tmux` для one-command запуска backend+PWA или self-dev сессий.
- PostgreSQL, доступный по `DATABASE_URL`.
- Optional: `codex` CLI для потоков на базе Codex (self-dev, parse-llm fallback, auto-readme pipeline).

Краткая матрица требований:

| Компонент | Обязательно | Назначение |
| --- | --- | --- |
| `bash` | Да | Выполнение скриптов |
| Python `3.11+` | Да | Backend + codegen-инструменты |
| Conda | Да (рекомендуемый путь) | Скрипты bootstrap окружения |
| PostgreSQL | Да (предпочтительный режим) | Основная персистентность через `DATABASE_URL` |
| `tmux` | Рекомендуется | Управляемые backend/PWA и self-dev сессии |
| `codex` CLI | По желанию | LLM-assisted parse и auto-readme/self-dev automation |

## 🧩 Compatibility & Assumptions

| Тема | Текущие ожидания |
| --- | --- |
| Локальная ОС | Основные таргеты: Linux/macOS (скрипты на `bash`) |
| Python runtime | `3.11` (управляется `scripts/setup_autoappdev_env.sh`) |
| Persistence mode | PostgreSQL предпочтителен и рассматривается как канонический |
| Fallback behavior | `backend/storage.py` включает fallback совместимость с JSON для деградированных сценариев |
| Network model | Локальная разработка с раздельными портами (backend + static PWA) |
| Agent tooling | `codex` CLI опционален, если не используются LLM-assisted parse и self-dev automation |

Допущения в этом README:
- Команды запускаются из корня репозитория, если раздел не указывает иначе.
- `.env` настроен до старта backend-сервисов.
- `conda` и `tmux` доступны для рекомендуемых one-command сценариев.

## 🛠️ Installation
### 1) Клонировать и перейти в репозиторий
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Настроить окружение
```bash
cp .env.example .env
```
Отредактируйте `.env` и задайте как минимум:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` и `AUTOAPPDEV_PORT` (или `PORT`)

### 3) Создать/обновить backend окружение
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Применить схему БД
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Optional: smoke test БД
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

Затем откройте:
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

Проверка в одной команде:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Краткая карта endpoint-ов:

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
Основной файл: `.env` (см. `docs/env.md` и `.env.example`).

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

Быстрая проверка `.env`:
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

| Режим | Команда | Примечания |
| --- | --- | --- |
| Start backend + PWA (recommended) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Start backend only | `conda run -n autoappdev python -m backend.app` | Использует bind-настройки и DB из `.env` |
| Start PWA static server only | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Полезно для проверки только frontend |
| Run self-dev driver in tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Возобновляемый self-development цикл |

### Common script options
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

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

См. `docs/api-contracts.md` для форматов запросов и ответов.

## 🧭 Operational Runbooks

### Runbook: bring up the full local stack
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Контрольные точки валидации:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Откройте `http://127.0.0.1:5173/` и убедитесь, что UI загрузил `/api/config`.
- Опционально: откройте `/api/version` и проверьте ожидаемые backend-метаданные.

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

Core API groups at a glance:

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

Полные примеры:
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
Затем используйте в PWA кнопки Start/Pause/Resume/Stop и проверьте `/api/logs`.

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
- Backend основан на Tornado и ориентирован на локальную разработку (включая permissive CORS для localhost с раздельными портами).
- Storage использует PostgreSQL-first с fallback-поведением в `backend/storage.py`.
- Ключи PWA блоков и значения `STEP.block` сознательно выровнены (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in actions доступны только для чтения; для редактирования используйте clone.
- `update_readme` действия ограничены безопасностью пути и работают только с `auto-apps/<workspace>/README.md`.
- В некоторых docs/scripts есть исторические пути/названия (`HeyCyan`, `LightMind`) из эволюции проекта. Текущий канонический путь — корень этого репозитория.
- Корневая директория `i18n/` присутствует. Языковые README ожидаются там во время многоязычных прогонов.

### Working model and state files
- Runtime по умолчанию `./runtime`, если не переопределён `AUTOAPPDEV_RUNTIME_DIR`.
- Состояние/история self-dev automation отслеживаются в `references/selfdev/`.
- Артефакты README-пайплайна сохраняются в `.auto-readme-work/<timestamp>/`.

### Testing posture (current)
- Репозиторий включает smoke-проверки и детерминированные demo-скрипты.
- Полноценный верхнеуровневый test suite/CI manifest пока не описан в метаданных корня.
- Предположение: валидация в основном скриптовая (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, end-to-end checklist).

## 🔐 Safety Notes
- Действие `update_readme` намеренно ограничено целями workspace README (`auto-apps/<workspace>/README.md`) с защитой от path traversal.
- Валидация action registry нормализует поля action spec и ограничивает диапазон значений для поддерживаемых reasoning levels.
- Скрипты репозитория предполагают доверенный локальный запуск; проверяйте содержимое скриптов перед использованием в общих/производственных окружениях.
- `.env` может содержать чувствительные значения (`DATABASE_URL`, API-ключи). Не коммитьте `.env`; используйте управление секретами на уровне окружения.

## 🔧 Troubleshooting

| Symptom | What to check |
| --- | --- |
| `tmux not found` | Установите `tmux` или запускайте backend/PWA вручную. |
| Backend fails on startup due to missing env | Перепроверьте `.env` относительно `.env.example` и `docs/env.md`. |
| Database errors (connection/auth/schema) | Проверьте `DATABASE_URL`; повторно выполните `conda run -n autoappdev python -m backend.apply_schema`; опционально проверьте подключение: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA loads but cannot call API | Убедитесь, что backend слушает нужные host/port; пересоздайте `pwa/config.local.js`, заново запустив `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start returns invalid transition | Сначала проверьте текущий статус пайплайна; запускайте только из `stopped`. |
| No log updates in UI | Проверьте, что `runtime/logs/pipeline.log` пишет; используйте `/api/logs` и `/api/logs/tail` для локализации проблемы UI vs backend. |
| LLM parse endpoint returns disabled | Установите `AUTOAPPDEV_ENABLE_LLM_PARSE=1` и перезапустите backend. |
| `conda run -n autoappdev ...` fails | Перезапустите `./scripts/setup_autoappdev_env.sh`; убедитесь, что окружение `autoappdev` существует (`conda env list`). |
| Wrong API target in frontend | Проверьте, что `pwa/config.local.js` существует и указывает на активный backend host/port. |

Для детерминированной ручной проверки используйте `docs/end-to-end-demo-checklist.md`.

## 🌐 README & i18n Workflow
- Корневой README является каноническим источником для конвейера автоматизации README.
- Многоязычные варианты должны находиться в `i18n/`.
- Статус директории i18n: ✅ присутствует в этом репозитории.
- Текущий языковой набор в репозитории:
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
- Языковая навигация должна быть единственной строкой вверху каждого варианта README (без дублей).
- Точка входа README pipeline: `prompt_tools/auto-readme-pipeline.sh`.

### i18n generation constraints (strict)
- При обновлении канонического README всегда запускайте многоязычную генерацию.
- Генерируйте/обновляйте файлы по одному (последовательно), а не пакетно.
- Сохраняйте ровно одну строку language-options вверху каждого варианта.
- Не дублируйте language bar внутри одного файла.
- Сохраняйте канонические snippets команд, ссылки, API-path и смысл бейджей во всех переводах.

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
Предпочтителен и ожидается для обычной эксплуатации. Уровень storage содержит fallback-совместимость, но для production-like сценариев лучше иметь PostgreSQL через `DATABASE_URL`.

### Why both `AUTOAPPDEV_PORT` and `PORT`?
`AUTOAPPDEV_PORT` — project-specific переменная. `PORT` существует как деплой-совместимый алиас. Держите их согласованными, если вы намеренно не меняете поведение запуска.

### Where should I start if I only want to inspect APIs?
Запустите только backend (`conda run -n autoappdev python -m backend.app`) и используйте `/api/health`, `/api/version`, `/api/config`, затем скриптами/endpoint-ами действий из `docs/api-contracts.md`.

### Are multilingual READMEs generated automatically?
Да. Репозиторий содержит `prompt_tools/auto-readme-pipeline.sh`, а языковые версии поддерживаются в `i18n/` с одной строкой language-navigation вверху каждого файла.

## 🗺️ Roadmap
- Завершить оставшиеся self-dev задачи поверх текущего статуса `51 / 55`.
- Расширить tooling workspace/materials/context и усилить safe-path контракты.
- Продолжить улучшение UX action palette и редактируемых action flows.
- Углубить поддержку многоязычного README/UI в `i18n/` и runtime-переключение языков.
- Усилить smoke/integration checks и CI coverage (сейчас доступны smoke-скрипты; полного CI manifest в корне не задокументировано).
- Продолжить укрепление детерминизма parser/import/codegen вокруг AAPS v1 и канонического IR.

## 🤝 Contributing
Вклады приветствуются через issues и pull requests.

Рекомендуемый workflow:
1. Сделайте fork и создайте feature branch.
2. Держите изменения локализованными и воспроизводимыми.
3. По возможности используйте детерминированные scripts/tests.
4. Обновляйте документацию при изменении поведения/контрактов (`docs/*`, API contracts, examples).
5. Открывайте PR с контекстом, шагами валидации и runtime предположениями.

Текущие remotes репозитория включают:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Дополнительно в локальных клонах могут присутствовать remotes для смежных репозиториев (в этом рабочем окружении пример: `novel`).

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
В текущем снимке репозитория корневой файл `LICENSE` не обнаружен.

Примечание:
- Пока лицензия не добавлена, условия использования и распространения считаются неуточнёнными; уточняйте у мейнтейнера.
