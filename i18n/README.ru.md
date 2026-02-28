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

Переиспользуемые скрипты и руководства для поэтапного создания приложений из скриншотов и markdown с Codex как неинтерактивным инструментом.

> 🎯 **Миссия:** сделать пайплайны разработки приложений детерминированными, возобновляемыми и ориентированными на артефакты.
>
> 🧩 **Принцип проектирования:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Сигналы проекта

| Сигнал | Текущее направление |
| --- | --- |
| Модель выполнения | Tornado backend + статичный PWA-контроллер |
| Выполнение пайплайна | Детеминированное и возобновляемое (`start/pause/resume/stop`) |
| Стратегия хранения | PostgreSQL-first с совместимым fallback-режимом |
| Поток документации | Канонический root README + автоматизированные варианты в `i18n/` |

### 🔗 Быстрая навигация

| Что нужно | Перейти |
| --- | --- |
| Первый локальный запуск | [⚡ Quick Start](#-quick-start) |
| Конфигурация и переменные | [⚙️ Configuration](#-configuration) |
| Снимок API | [📡 API Snapshot](#-api-snapshot) |
| Runbooks эксплуатации | [🧭 Operational Runbooks](#-operational-runbooks) |
| Правила генерации README/i18n | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
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

## 🗂️ Оглавление
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
AutoAppDev — это контроллер для долгоживущих и возобновляемых пайплайнов разработки приложений. Он сочетает:

1. Tornado backend API с хранением в PostgreSQL (плюс локальное JSON fallback-поведение в коде хранения).
2. Scratch-подобный статичный PWA-контроллер.
3. Скрипты и документацию для авторинга пайплайнов, детерминированной генерации кода, self-development циклов и автоматизации README.

Проект оптимизирован для предсказуемого исполнения агентами с строгой последовательностью и историей артефактов в workflow.

### 🎨 Почему этот репозиторий существует

| Тема | Что это означает на практике |
| --- | --- |
| Детеминизм | Каноничная pipeline IR + pipeline/parser/import/codegen-процессы, рассчитанные на воспроизводимость |
| Возобновляемость | Явная state machine (`start/pause/resume/stop`) для длительных запусков |
| Эксплуатация | Runtime-логи, каналы inbox/outbox и проверки, управляемые скриптами |
| Documentation-first | Контракты/спеки/примеры живут в `docs/`, с автоматическим многоязычным README-потоком |

## 🧭 Philosophy
AutoAppDev рассматривает агентов как инструменты и поддерживает стабильную работу через строгий, возобновляемый цикл:

1. Plan
2. Implement
3. Debug/verify (с таймаутами)
4. Fix
5. Summarize + log
6. Commit + push

Контроллер пытается воплощать те же принципы в Scratch-подобных блоках и действиях (включая единое действие `update_readme`), чтобы каждый workspace оставался актуальным и воспроизводимым.

### 🔁 Цикл состояний жизненного цикла

| Переход состояния | Операционная цель |
| --- | --- |
| `start` | Запустить пайплайн из состояния stopped/ready |
| `pause` | Безопасно остановить длительное выполнение без потери контекста |
| `resume` | Возобновить выполнение из сохранённого runtime-состояния/артефактов |
| `stop` | Завершить выполнение и вернуться в нерабочее состояние |

## ✨ Features
- Возобновляемое управление жизненным циклом пайплайна: start, pause, resume, stop.
- API для Script library для AAPS pipeline-скриптов (`.aaps`) и канонической IR (`autoappdev_ir` v1).
- Детеминированная parser/import-pipeline:
  - Разбор отформатированных AAPS-скриптов.
  - Импорт аннотированного shell через комментарии `# AAPS:`.
  - Необязательный fallback парсинга с помощью Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Реестр действий с built-in и редактируемыми/кастомными action (поток clone/edit для readonly built-in).
- Scratch-подобные PWA-блоки и динамически загружаемая палитра действий (`GET /api/actions`).
- Каналы runtime-сообщений:
  - Inbox (`/api/inbox`) для указаний оператора пайплайну.
  - Outbox (`/api/outbox`) с ingest file-очереди из `runtime/outbox`.
- Инкрементальный стриминг логов из backend и pipeline-логов (`/api/logs`, `/api/logs/tail`).
- Детеминированный codegen runner из канонической IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev driver для итеративной эволюции репозитория (`scripts/auto-autoappdev-development.sh`).
- Автоматизация README с многоязычной генерацией в `i18n/`.

## 📌 At A Glance

| Область | Детали |
| --- | --- |
| Core runtime | Tornado backend + статичный PWA frontend |
| Persistence | PostgreSQL-first с совместимым fallback-поведением в `backend/storage.py` |
| Pipeline model | Каноническая IR (`autoappdev_ir` v1) и формат скриптов AAPS |
| Control flow | Жизненный цикл Start / Pause / Resume / Stop |
| Dev mode | Возобновляемый self-dev цикл + детеминированные скрипт/codegen workflow |
| README/i18n | Автоматизированный README pipeline с каркасом `i18n/` |

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
- Экспонирует API контроллера для скриптов, действий, плана, жизненного цикла pipeline, логов, inbox/outbox и конфигурации workspace.
- Валидирует и сохраняет assets скриптов пайплайна.
- Координирует состояние выполнения пайплайна и переходы статусов.
- Обеспечивает детеминированный fallback-поведение, когда пул БД недоступен.

### Frontend responsibilities
- Отрисовывает Scratch-подобный блоковый UI и поток редактирования пайплайна.
- Загружает палитру действий динамически из backend registry.
- Управляет lifecycle-контролами и мониторит статус/логи/сообщения.

## 📚 Contents
Карта ссылок на наиболее используемые документы, скрипты и примеры:

- `docs/auto-development-guide.md`: Bilingual (EN/ZH) философия и требования к долгоживущему, возобновляемому self-development агенту.
- `docs/ORDERING_RATIONALE.md`: Пример обоснования порядка screenshot-driven шагов.
- `docs/controller-mvp-scope.md`: Scope MVP контроллера (экраны + минимальные API).
- `docs/end-to-end-demo-checklist.md`: Детеминированный чеклист ручного end-to-end демо (happy path backend + PWA).
- `docs/env.md`: Конвенции переменных окружения (`.env`).
- `docs/api-contracts.md`: Контракты request/response для контроллера API.
- `docs/pipeline-formatted-script-spec.md`: Стандартный формат скриптов пайплайна (AAPS) и схема канонической IR (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Детеминированный генератор исполняемых bash pipeline-runner из канонической IR.
- `docs/common-actions.md`: Типовые контракты/actions (включая `update_readme`).
- `docs/workspace-layout.md`: Стандартные папки workspace и контракты (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Запуск приложения AutoAppDev (backend + PWA) в tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Запуск self-dev driver AutoAppDev в tmux.
- `scripts/app-auto-development.sh`: Линейный pipeline driver (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) с поддержкой resume/state.
- `scripts/generate_screenshot_docs.sh`: Генератор screenshot -> markdown описания (Codex-driven).
- `scripts/setup_autoappdev_env.sh`: Основной bootstrap-скрипт conda окружения для локальных запусков.
- `scripts/setup_backend_env.sh`: Скрипт-конфиг backend-окружения.
- `examples/ralph-wiggum-example.sh`: Пример помощника автоматизации Codex CLI.

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
- Conda (`conda`) для поставляемых setup-скриптов.
- `tmux` для one-command backend+PWA или self-dev сессий.
- PostgreSQL, доступный через `DATABASE_URL`.
- Optional: `codex` CLI для Codex-powered flows (self-dev, parse-llm fallback, auto-readme pipeline).

Краткая матрица требований:

| Компонент | Обязательно | Назначение |
| --- | --- | --- |
| `bash` | Да | Выполнение скриптов |
| Python `3.11+` | Да | Backend + codegen tooling |
| Conda | Да (рекомендуемый путь) | Скрипты bootstrap окружения |
| PostgreSQL | Да (предпочтительный режим) | Основная persistence через `DATABASE_URL` |
| `tmux` | Рекомендуется | Управляемые backend/PWA и self-dev сессии |
| `codex` CLI | По желанию | LLM-assisted parse и автоматизация README/self-dev |

## 🧩 Compatibility & Assumptions

| Тема | Текущее ожидание |
| --- | --- |
| Локальная ОС | Linux/macOS shell — основной таргет (`bash`-скрипты) |
| Python runtime | `3.11` (управляется `scripts/setup_autoappdev_env.sh`) |
| Режим персистентности | PostgreSQL предпочитается и считается каноническим |
| Fallback behavior | `backend/storage.py` включает JSON-совместимый fallback для деградации |
| Сетевая модель | Локальная разработка split-port (backend + статичный PWA) |
| Agent tooling | `codex` CLI опционален, кроме случаев LLM-assisted parse или self-dev automation |

Допущения в этом README:
- Команды выполняются из корня репозитория, если не указано иначе.
- `.env` настраивается до запуска backend-сервисов.
- `conda` и `tmux` доступны для рекомендуемых one-command workflow.

## 🛠️ Установка
### 1) Клонировать и перейти в репозиторий
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Настроить окружение
```bash
cp .env.example .env
```
Отредактируйте `.env` и задайте минимум:
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

### 5) Дополнительно: smoke test БД
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

Проверка одним вызовом:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Краткая карта endpoints:

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
Основной файл: `.env` (см. `docs/env.md` и `.env.example`).

### Важные переменные

| Переменная | Назначение |
| --- | --- |
| `SECRET_KEY` | Требуется по конвенции |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Backend bind-настройки |
| `DATABASE_URL` | PostgreSQL DSN (предпочтительный) |
| `AUTOAPPDEV_RUNTIME_DIR` | Переопределение runtime-директории (по умолчанию `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Цель запуска pipeline по умолчанию |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Включить `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Значения Codex по умолчанию для actions/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Зарезервировано для будущих интеграций |

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
| Запуск backend + PWA (рекомендуется) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Запуск только backend | `conda run -n autoappdev python -m backend.app` | Использует bind и DB настройки из `.env` |
| Запуск только статического PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Полезно для frontend-only проверок |
| Запуск self-dev драйвера в tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Возобновляемый цикл self-development |

### Частые опции скриптов
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Парсинг и сохранение скриптов
- Parse AAPS через API: `POST /api/scripts/parse`
- Import аннотированного shell: `POST /api/scripts/import-shell`
- Optional LLM parse: `POST /api/scripts/parse-llm` (requires `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### API управления пайплайном
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Другие часто используемые API
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Смотрите `docs/api-contracts.md` для форм request/response.

## 🧭 Operational Runbooks

### Runbook: поднять весь локальный стек
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Контрольные точки валидации:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Откройте `http://127.0.0.1:5173/` и убедитесь, что UI загрузил `/api/config`.
- Опционально: откройте `/api/version` и проверьте ожидаемые backend-metadata.

### Runbook: debugging только backend
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

Ключевые группы API на уровне обзора:

| Категория | Endpoints |
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
Затем используйте элементы управления Start/Pause/Resume/Stop в PWA и проверьте `/api/logs`.

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
- Backend основан на Tornado и заточен под локальную разработку (включая permissive CORS для localhost split-port).
- Storage строится как PostgreSQL-first с совместимым fallback-поведением в `backend/storage.py`.
- Ключи блоков PWA и значения `STEP.block` скриптов согласованы намеренно (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in actions доступны только для чтения; для правок используйте clone.
- Action `update_readme` имеет ограничения безопасности пути и нацелена на `auto-apps/<workspace>/README.md`.
- В некоторых документах/скриптах есть исторические ссылки на `HeyCyan`, `LightMind` — наследие эволюции проекта. Актуальный канонический путь — корень этого репозитория.
- Корневая директория `i18n/` присутствует. Языковые README-файлы ожидаются там в многоязычных запусках.

### Working model and state files
- Runtime по умолчанию `./runtime`, если его не переопределяет `AUTOAPPDEV_RUNTIME_DIR`.
- Состояние и история self-dev automation хранятся в `references/selfdev/`.
- Артефакты README pipeline лежат в `.auto-readme-work/<timestamp>/`.

### Testing posture (current)
- Репозиторий содержит smoke checks и детеминированные demo-скрипты.
- Полный top-level automated test suite/CI манифест сейчас не описан в метаданных root.
- Предположение: валидация сейчас преимущественно скрипт-ориентированная (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, end-to-end checklist).

## 🔐 Safety Notes
- Action `update_readme` намеренно ограничена targets workspace README (`auto-apps/<workspace>/README.md`) с защитой от path traversal.
- Валидация action registry нормализует spec-поля и ограничивает значения supported reasoning levels.
- Скрипты репозитория предполагают доверенный локальный запуск; просматривайте их перед выполнением в shared или production-подобных средах.
- `.env` может содержать чувствительные значения (`DATABASE_URL`, API keys). Не коммитьте `.env`, секреты храните во внешнем менеджменте.

## 🔧 Troubleshooting

| Симптом | Что проверить |
| --- | --- |
| `tmux not found` | Установите `tmux` или запустите backend/PWA вручную. |
| Backend не запускается из-за env | Проверьте `.env` с `.env.example` и `docs/env.md`. |
| Ошибки БД (connection/auth/schema) | Проверьте `DATABASE_URL`; повторно выполните `conda run -n autoappdev python -m backend.apply_schema`; опционально connectivity check: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA загружается, но не может вызывать API | Убедитесь, что backend слушает на нужном host/port; пересоздайте `pwa/config.local.js`, заново запустив `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start возвращает invalid transition | Сначала проверьте текущий статус пайплайна; стартовать нужно из состояния `stopped`. |
| Нет новых логов в UI | Проверьте, что `runtime/logs/pipeline.log` пишет; используйте напрямую `/api/logs` и `/api/logs/tail` для изоляции UI и backend-источника. |
| LLM parse endpoint возвращает disabled | Установите `AUTOAPPDEV_ENABLE_LLM_PARSE=1` и перезапустите backend. |
| `conda run -n autoappdev ...` fails | Повторно запустите `./scripts/setup_autoappdev_env.sh`; проверьте существование окружения `autoappdev` (`conda env list`). |
| Неверная API-цель во frontend | Убедитесь, что `pwa/config.local.js` существует и указывает на активный backend host/port. |

Для детерминированного ручного пути проверки используйте `docs/end-to-end-demo-checklist.md`.

## 🌐 README & i18n Workflow
- Корневой README — канонический источник для pipeline автоматизации README.
- Многоязычные версии ожидаются в `i18n/`.
- Статус директории i18n: ✅ присутствует в этом репозитории.
- Текущий язык-сет в этом репозитории:
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
- Языковая навигация должна оставаться единственной строкой вверху каждого варианта README (без дубликатов).
- Pipeline entrypoint: `prompt_tools/auto-readme-pipeline.sh`.

### i18n generation constraints (strict)
- Всегда выполняйте многоязычную генерацию при обновлении канонического README.
- Генерируйте и обновляйте языковые файлы по одному (последовательно), не в неявных bulk-батчах.
- Сохраняйте ровно одну строку language-options навигации в начале каждого варианта.
- Не дублируйте language bar в одном файле.
- Сохраняйте канонические snippets команд, ссылки, API-пути и смысл бейджей между переводами.

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
- Trigger: `./README.md`
- Input user prompt: `probe prompt`
- Goal: generate a complete, beautiful README draft with required sections and support information
- Source snapshot used:
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- This file was generated from repository contents and preserved as a canonical draft entry point.

## ❓ FAQ

### Is PostgreSQL mandatory?
Предпочтительно и ожидается для обычной работы. Уровень storage содержит fallback-совместимость, но production-like использование должно предполагать доступный PostgreSQL через `DATABASE_URL`.

### Why both `AUTOAPPDEV_PORT` and `PORT`?
`AUTOAPPDEV_PORT` — это project-specific переменная. `PORT` существует как deploy-friendly alias. Держите их согласованными, если намеренно не меняете путь запуска.

### Where should I start if I only want to inspect APIs?
Запустите backend-only (`conda run -n autoappdev python -m backend.app`) и используйте `/api/health`, `/api/version`, `/api/config`, затем endpoints скриптов/actions из `docs/api-contracts.md`.

### Are multilingual READMEs generated automatically?
Да. Репозиторий содержит `prompt_tools/auto-readme-pipeline.sh`, а языковые варианты поддерживаются в `i18n/` с одной строкой language-navigation наверху каждого файла.

## 🗺️ Roadmap
- Завершить оставшиеся задачи self-dev сверх текущего статуса `51 / 55`.
- Расширить workspace/materials/context tooling и более строгие safe-path контракты.
- Продолжать улучшать UX action palette и редактируемые action flows.
- Углубить поддержку многоязычного README/UI через `i18n/` и переключение языка во runtime.
- Укрепить smoke/integration checks и CI coverage (сейчас доступны smoke-скрипты, полный CI manifest не описан в корне).
- Продолжать повышать детерминизм parser/import/codegen вокруг AAPS v1 и канонической IR.

## 🤝 Contributing
Вклады приветствуются через issues и pull requests.

Рекомендуемый workflow:
1. Fork и создайте feature branch.
2. Держите изменения сконцентрированными и воспроизводимыми.
3. По возможности используйте детеминированные scripts/tests.
4. Обновляйте документацию при изменениях поведения/контрактов (`docs/*`, API contracts, examples).
5. Открывайте PR с контекстом, шагами валидации и runtime assumptions.

В репозитории сейчас доступны remotes:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Дополнительно в локальных клонах могут быть дополнительные remotes для смежных репозиториев (в этом workspace пример: `novel`).

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

В текущем снимке репозитория корневой `LICENSE` не обнаружен.

Примечание:
- Пока лицензия не добавлена, условия использования и распространения считаются неуточнёнными; уточните у maintainer.
