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
![Pipeline](https://img.shields.io/badge/Pipeline-Resumable-ff6b35)
![Docs](https://img.shields.io/badge/Docs-Workflow%20First-0e9f6e)
![Automation](https://img.shields.io/badge/Automation-README%20Pipeline-f97316)
![API](https://img.shields.io/badge/API-JSON%20HTTP-0ea5e9)
![State Machine](https://img.shields.io/badge/Lifecycle-start%2Fpause%2Fresume%2Fstop-f59e0b)

Переиспользуемые скрипты и руководства для поэтапной разработки приложений из скриншотов/markdown, где Codex используется как неинтерактивный инструмент.

> 🎯 **Миссия:** сделать пайплайны разработки приложений детерминированными, возобновляемыми и ориентированными на артефакты.
>
> 🧩 **Принцип дизайна:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🔗 Быстрая навигация

| Что нужно | Перейти к |
| --- | --- |
| Первый локальный запуск | [⚡ Quick Start](#-quick-start) |
| Окружение и обязательные переменные | [⚙️ Configuration](#-configuration) |
| Поверхность API | [📡 API Snapshot](#-api-snapshot) |
| Плейбуки запуска/отладки | [🧭 Operational Runbooks](#-operational-runbooks) |
| Правила генерации README/i18n | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| Матрица устранения неполадок | [🔧 Troubleshooting](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Статус Self-Dev (автообновляется)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Этот раздел обновляется скриптом `scripts/auto-autoappdev-development.sh`.
Не редактируйте содержимое между маркерами.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Содержание
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
- [🙌 Support](#-support)
- [📄 License](#-license)
- [❤️ Sponsor & Donate](#-sponsor--donate)

## 🚀 Overview
AutoAppDev — управляющий проект для долгоживущих и возобновляемых пайплайнов разработки приложений. Он объединяет:

1. Backend API на Tornado с PostgreSQL-персистентностью (плюс локальный JSON fallback в коде storage).
2. Статический управляющий PWA-интерфейс в стиле Scratch.
3. Скрипты и документацию для авторинга пайплайнов, детерминированной генерации кода, циклов self-dev и автоматизации README.

Проект оптимизирован под предсказуемое выполнение агентами со строгой последовательностью и историей, ориентированной на артефакты.

### 🎨 Зачем существует этот репозиторий

| Тема | Как это проявляется на практике |
| --- | --- |
| Детерминизм | Канонический pipeline IR + parser/import/codegen-процессы, спроектированные для повторяемости |
| Возобновляемость | Явная машина состояний жизненного цикла (`start/pause/resume/stop`) для долгих прогонов |
| Эксплуатация | Runtime-логи, inbox/outbox-каналы и циклы проверки, управляемые скриптами |
| Документация прежде всего | Контракты/спеки/примеры находятся в `docs/`, с автоматизированным многоязычным README-потоком |

## 🧭 Philosophy
AutoAppDev рассматривает агентов как инструменты и стабилизирует работу через строгий возобновляемый цикл:

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

Приложение-контроллер стремится воплощать те же идеи в Scratch-подобных блоках/действиях (включая общее действие `update_readme`), чтобы каждый workspace оставался актуальным и воспроизводимым.

### 🔁 Назначение состояний жизненного цикла

| Переход состояния | Операционный смысл |
| --- | --- |
| `start` | Запустить пайплайн из состояния stopped/ready |
| `pause` | Безопасно приостановить долгий запуск без потери контекста |
| `resume` | Продолжить из сохраненного runtime-состояния/артефактов |
| `stop` | Завершить выполнение и вернуться в состояние без запуска |

## ✨ Features
- Возобновляемое управление жизненным циклом пайплайна: start, pause, resume, stop.
- Скриптовые API-библиотеки для AAPS pipeline scripts (`.aaps`) и canonical IR (`autoappdev_ir` v1).
- Детерминированный parser/import-процесс:
  - Разбор форматированных AAPS-скриптов.
  - Импорт аннотированного shell через комментарии `# AAPS:`.
  - Опциональный Codex-assisted parse fallback (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Реестр действий со встроенными и редактируемыми/кастомными действиями (clone/edit-поток для readonly built-ins).
- Scratch-подобные PWA-блоки и палитра действий, подгружаемая в рантайме (`GET /api/actions`).
- Каналы сообщений runtime:
  - Inbox (`/api/inbox`) для инструкций от оператора к пайплайну.
  - Outbox (`/api/outbox`) с поддержкой ingest файловой очереди из `runtime/outbox`.
- Инкрементальный стриминг логов backend и pipeline (`/api/logs`, `/api/logs/tail`).
- Детерминированная генерация runner-кода из canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev драйвер для итеративного развития репозитория (`scripts/auto-autoappdev-development.sh`).
- Пайплайн автоматизации README с каркасом мультиязычной генерации в `i18n/`.

## 📌 At A Glance

| Область | Детали |
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

### Обязанности backend
- Предоставлять controller API для скриптов, действий, плана, жизненного цикла пайплайна, логов, inbox/outbox и конфигурации workspace.
- Валидировать и сохранять assets скриптов пайплайна.
- Координировать состояние выполнения пайплайна и переходы статуса.
- Давать детерминированное fallback-поведение, когда DB pool недоступен.

### Обязанности frontend
- Рендерить Scratch-подобный UI блоков и поток редактирования пайплайна.
- Динамически загружать палитру действий из backend-реестра.
- Управлять lifecycle-контролами и мониторить статус/логи/сообщения.

## 📚 Contents
Справочная карта наиболее используемых документов, скриптов и примеров:

- `docs/auto-development-guide.md`: Двуязычная (EN/ZH) философия и требования к долгоживущему, возобновляемому агенту auto-development.
- `docs/ORDERING_RATIONALE.md`: Пример обоснования последовательности шагов на основе скриншотов.
- `docs/controller-mvp-scope.md`: Scope MVP-контроллера (экраны + минимальные API).
- `docs/end-to-end-demo-checklist.md`: Детерминированный ручной чеклист сквозной демо-проверки (backend + happy path PWA).
- `docs/env.md`: Соглашения по переменным окружения (`.env`).
- `docs/api-contracts.md`: Контракты API запросов/ответов контроллера.
- `docs/pipeline-formatted-script-spec.md`: Стандартный формат pipeline script (AAPS) и схема canonical IR (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Детерминированный генератор исполняемых bash pipeline runner'ов из canonical IR.
- `docs/common-actions.md`: Контракты/спеки common actions (включая `update_readme`).
- `docs/workspace-layout.md`: Стандартные папки workspace + контракты (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Запуск приложения AutoAppDev (backend + PWA) в tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Запуск self-dev драйвера AutoAppDev в tmux.
- `scripts/app-auto-development.sh`: Линейный pipeline driver (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) с поддержкой resume/state.
- `scripts/generate_screenshot_docs.sh`: Генератор описаний screenshot -> markdown (на базе Codex).
- `scripts/setup_autoappdev_env.sh`: Основной скрипт bootstrap conda-среды для локальных запусков.
- `scripts/setup_backend_env.sh`: Вспомогательный скрипт окружения backend.
- `examples/ralph-wiggum-example.sh`: Пример helper-скрипта автоматизации Codex CLI.

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
- `tmux` для одно-командных backend+PWA или self-dev сессий.
- PostgreSQL, доступный по `DATABASE_URL`.
- Опционально: CLI `codex` для сценариев Codex-powered (self-dev, parse-llm fallback, auto-readme pipeline).

Быстрая матрица требований:

| Компонент | Обязательно | Назначение |
| --- | --- | --- |
| `bash` | Да | Выполнение скриптов |
| Python `3.11+` | Да | Backend + инструменты codegen |
| Conda | Да (рекомендуемый поток) | Скрипты bootstrap окружения |
| PostgreSQL | Да (предпочтительный режим) | Основная персистентность через `DATABASE_URL` |
| `tmux` | Рекомендуется | Управляемые сессии backend/PWA и self-dev |
| `codex` CLI | Опционально | LLM-assisted parse и README/self-dev automation |

## 🧩 Compatibility & Assumptions

| Тема | Текущее ожидание |
| --- | --- |
| Local OS | Linux/macOS shell'ы являются основной целью (`bash` scripts) |
| Python runtime | `3.11` (управляется `scripts/setup_autoappdev_env.sh`) |
| Persistence mode | PostgreSQL предпочитается и считается каноническим режимом |
| Fallback behavior | `backend/storage.py` включает JSON compatibility fallback для деградированных сценариев |
| Network model | Локальная split-port модель разработки (backend + static PWA) |
| Agent tooling | CLI `codex` опционален, кроме случаев LLM-assisted parse или self-dev automation |

Предположения, используемые в этом README:
- Вы выполняете команды из корня репозитория, если не указано иное.
- `.env` настроен до запуска backend-сервисов.
- `conda` и `tmux` доступны для рекомендуемых one-command workflow.

## 🛠️ Installation
### 1) Клонируйте репозиторий и перейдите в него
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Настройте окружение
```bash
cp .env.example .env
```
Отредактируйте `.env` и задайте как минимум:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` и `AUTOAPPDEV_PORT` (или `PORT`)

### 3) Создайте/обновите backend-окружение
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Примените схему базы данных
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Опционально: smoke-тест базы данных
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
- Базовый URL Backend API: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

Smoke-проверка одной командой:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Краткая карта endpoint'ов:

| Поверхность | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
Основной файл: `.env` (см. `docs/env.md` и `.env.example`).

### Важные переменные

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

Быстрая валидация `.env`:
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
| Запуск только backend | `conda run -n autoappdev python -m backend.app` | Использует `.env` bind + настройки БД |
| Запуск только статического сервера PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Удобно для проверок только фронтенда |
| Запуск self-dev драйвера в tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Возобновляемый цикл self-development |

### Часто используемые опции скриптов
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Разбор и сохранение скриптов
- Parse AAPS via API: `POST /api/scripts/parse`
- Import annotated shell: `POST /api/scripts/import-shell`
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

См. `docs/api-contracts.md` для форматов запросов/ответов.

## 🧭 Operational Runbooks

### Runbook: поднять полный локальный стек
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Контрольные точки валидации:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Откройте `http://127.0.0.1:5173/` и подтвердите, что UI может загрузить `/api/config`.
- Опционально: откройте `/api/version` и проверьте, что возвращаются ожидаемые backend-метаданные.

### Runbook: отладка только backend
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: детерминированный smoke codegen
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

Основные группы API в одном месте:

| Категория | Endpoints |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan model | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
| Workspace settings | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Examples
### Пример AAPS
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

### Детерминированная генерация runner
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Детерминированный demo pipeline
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Затем используйте в PWA контролы Start/Pause/Resume/Stop и проверьте `/api/logs`.

### Импорт из аннотированного shell
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
- Backend основан на Tornado и спроектирован для удобной локальной разработки (включая permissive CORS для localhost с разными портами).
- Storage работает в PostgreSQL-first режиме с compatibility behavior в `backend/storage.py`.
- Ключи блоков PWA и значения `STEP.block` в скриптах намеренно выровнены (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in actions readonly; перед редактированием сначала клонируйте.
- Действие `update_readme` ограничено path-safety: только README-цели workspace в `auto-apps/<workspace>/README.md`.
- В некоторых docs/scripts есть исторические ссылки на пути/имена (`HeyCyan`, `LightMind`), унаследованные в эволюции проекта. Текущий канонический путь — корень этого репозитория.
- Корневая директория `i18n/` существует. В мультиязычных прогонах языковые README ожидаются именно там.

### Рабочая модель и файлы состояния
- По умолчанию runtime находится в `./runtime`, если не переопределен `AUTOAPPDEV_RUNTIME_DIR`.
- Состояние/история self-dev automation отслеживаются в `references/selfdev/`.
- Артефакты README-пайплайна записываются в `.auto-readme-work/<timestamp>/`.

### Подход к тестированию (текущее состояние)
- Репозиторий включает smoke-проверки и детерминированные demo-скрипты.
- Полноценный верхнеуровневый набор автотестов/CI-манифест сейчас не определен в корневых метаданных.
- Предположение: валидация пока в основном script-driven (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, end-to-end checklist).

## 🔐 Safety Notes
- Действие `update_readme` намеренно ограничено целями workspace README (`auto-apps/<workspace>/README.md`) с защитой от path traversal.
- Валидация action registry принудительно нормализует поля action spec и ограничивает значения для поддерживаемых reasoning levels.
- Скрипты репозитория предполагают доверенную локальную среду выполнения; перед запуском в общих или около-прод средах проверяйте содержимое скриптов.
- `.env` может содержать чувствительные значения (`DATABASE_URL`, API keys). Не коммитьте `.env`; используйте управление секретами вне локальной разработки.

## 🔧 Troubleshooting

| Симптом | Что проверить |
| --- | --- |
| `tmux not found` | Установите `tmux` или запускайте backend/PWA вручную. |
| Backend не стартует из-за отсутствующих env | Снова проверьте `.env` по `.env.example` и `docs/env.md`. |
| Ошибки базы данных (connection/auth/schema) | Проверьте `DATABASE_URL`; повторно выполните `conda run -n autoappdev python -m backend.apply_schema`; опциональная проверка подключения: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA загружается, но не вызывает API | Убедитесь, что backend слушает ожидаемый host/port; пересоздайте `pwa/config.local.js`, повторно запустив `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start возвращает invalid transition | Сначала проверьте текущее состояние пайплайна; запуск должен идти из состояния `stopped`. |
| В UI нет обновлений логов | Подтвердите, что пишется `runtime/logs/pipeline.log`; используйте `/api/logs` и `/api/logs/tail` напрямую, чтобы отделить проблемы UI от backend. |
| LLM parse endpoint возвращает disabled | Установите `AUTOAPPDEV_ENABLE_LLM_PARSE=1` и перезапустите backend. |
| `conda run -n autoappdev ...` завершается с ошибкой | Повторно выполните `./scripts/setup_autoappdev_env.sh`; проверьте, что conda env `autoappdev` существует (`conda env list`). |
| Неверная API-цель во frontend | Проверьте, что `pwa/config.local.js` существует и указывает на активный backend host/port. |

Для детерминированного ручного пути валидации используйте `docs/end-to-end-demo-checklist.md`.

## 🌐 README & i18n Workflow
- Корневой README — канонический источник для пайплайна автоматизации README.
- Многоязычные варианты ожидаются в `i18n/`.
- Статус директории i18n: ✅ присутствует в этом репозитории.
- Текущий набор языков в репозитории:
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
- Языковая навигация должна оставаться одной строкой вверху каждого варианта README (без дублирующихся language bar).
- Entrypoint README-пайплайна: `prompt_tools/auto-readme-pipeline.sh`.

### Ограничения генерации i18n (строго)
- При обновлении канонического README всегда выполняйте многоязычную генерацию.
- Генерируйте/обновляйте языковые файлы по одному (последовательно), а не неоднозначными массовыми пакетами.
- Сохраняйте ровно одну строку language-options вверху каждого варианта.
- Не дублируйте language bar внутри одного файла.
- Сохраняйте канонические command snippets, ссылки, API-path и смысл badge'ей во всех переводах.

Рекомендуемый порядок по одному файлу:
1. `README.md` (канонический источник на английском)
2. `i18n/README.ar.md`
3. `i18n/README.de.md`
4. `i18n/README.es.md`
5. `i18n/README.fr.md`
6. `i18n/README.ja.md`
7. `i18n/README.ko.md`
8. `i18n/README.ru.md`
9. `i18n/README.vi.md`
10. `i18n/README.zh-Hans.md`
11. `i18n/README.zh-Hant.md`

Таблица покрытия языков:

| Язык | Файл |
| --- | --- |

## ❓ FAQ

### PostgreSQL обязателен?
Предпочтителен и ожидается для нормальной эксплуатации. Слой storage содержит fallback-совместимость, но для production-like использования предполагается доступный PostgreSQL через `DATABASE_URL`.

### Почему есть и `AUTOAPPDEV_PORT`, и `PORT`?
`AUTOAPPDEV_PORT` — project-specific переменная. `PORT` — deployment-friendly алиас. Держите их синхронизированными, если только вы намеренно не переопределяете поведение в своем сценарии запуска.

### С чего начать, если я хочу только посмотреть API?
Запустите только backend (`conda run -n autoappdev python -m backend.app`) и используйте `/api/health`, `/api/version`, `/api/config`, затем script/action endpoint'ы из `docs/api-contracts.md`.

### Многоязычные README генерируются автоматически?
Да. В репозитории есть `prompt_tools/auto-readme-pipeline.sh`, а языковые варианты поддерживаются в `i18n/` с одной строкой языковой навигации вверху каждого варианта.

## 🗺️ Roadmap
- Завершить оставшиеся self-dev задачи сверх текущего статуса `51 / 55`.
- Расширить инструменты workspace/materials/context и усилить safe-path контракты.
- Продолжать улучшать UX палитры действий и редактируемые workflows действий.
- Углубить поддержку многоязычного README/UI в `i18n/` и переключение языка в рантайме.
- Усилить smoke/integration проверки и покрытие CI (сейчас есть script-driven smoke checks; полный CI manifest в корне не задокументирован).
- Продолжить усиление детерминизма parser/import/codegen вокруг AAPS v1 и canonical IR.

## 🤝 Contributing
Вклад приветствуется через issues и pull requests.

Рекомендуемый workflow:
1. Сделайте fork и создайте feature branch.
2. Делайте изменения сфокусированными и воспроизводимыми.
3. По возможности предпочитайте детерминированные scripts/tests.
4. Обновляйте документацию при изменении поведения/контрактов (`docs/*`, API contracts, examples).
5. Откройте PR с контекстом, шагами валидации и предположениями о runtime.

Текущие удаленные репозитории включают:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- В локальных клонах могут присутствовать дополнительные remote для связанных репозиториев (пример в этом workspace: `novel`).

## 🙌 Support
- GitHub issues и pull requests для сообщений об ошибках и предложений функций.
- Ссылки sponsor/donate приведены ниже.

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 License
В этом снимке репозитория не обнаружен корневой файл `LICENSE`.

Примечание-предположение:
- Пока файл лицензии не добавлен, считайте условия использования/распространения неуточненными и уточняйте их у мейнтейнера.

## ❤️ Sponsor & Donate
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400

Если проект помогает вашему workflow, sponsorship напрямую поддерживает дальнейшие self-dev задачи, качество документации и усиление инструментов.
