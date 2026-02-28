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

Переиспользуемые скрипты и руководства для пошаговой разработки приложений по скриншотам/markdown с использованием Codex как неинтерактивного инструмента.

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

## 🚀 Обзор
AutoAppDev — это управляющий проект для долгоживущих, возобновляемых пайплайнов разработки приложений. Он объединяет:

1. Backend API на Tornado с персистентностью в PostgreSQL (плюс поведение локального JSON fallback в коде storage).
2. Статический управляющий PWA-интерфейс в стиле Scratch.
3. Скрипты и документацию для создания пайплайнов, детерминированной генерации кода, циклов self-development и автоматизации README.

### Кратко

| Область | Детали |
| --- | --- |
| Core runtime | Tornado backend + static PWA frontend |
| Persistence | PostgreSQL-first with compatibility behavior in `backend/storage.py` |
| Pipeline model | Canonical IR (`autoappdev_ir` v1) and AAPS script format |
| Control flow | Start / Pause / Resume / Stop lifecycle |
| Dev mode | Resumable self-dev loop + deterministic script/codegen workflows |
| README/i18n | Automated README pipeline with `i18n/` scaffolding |

## 🧭 Философия
AutoAppDev рассматривает агентов как инструменты и сохраняет стабильность работы через строгий, возобновляемый цикл:
1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

Управляющее приложение нацелено на воплощение этих же концепций в виде блоков/действий в стиле Scratch (включая общее действие `update_readme`), чтобы каждое workspace оставалось актуальным и воспроизводимым.

## ✨ Возможности
- Возобновляемое управление жизненным циклом пайплайна: start, pause, resume, stop.
- API библиотеки скриптов для AAPS pipeline scripts (`.aaps`) и canonical IR (`autoappdev_ir` v1).
- Детерминированный parser/import pipeline:
  - Разбор форматированных AAPS-скриптов.
  - Импорт аннотированного shell через комментарии `# AAPS:`.
  - Опциональный fallback разбора с помощью Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Реестр действий со встроенными + редактируемыми/кастомными действиями (clone/edit-поток для readonly встроенных).
- Scratch-подобные блоки PWA и палитра действий, загружаемая во время выполнения (`GET /api/actions`).
- Каналы сообщений рантайма:
  - Inbox (`/api/inbox`) для руководящих сообщений оператор -> pipeline.
  - Outbox (`/api/outbox`), включая ingest очереди файлов из `runtime/outbox`.
- Инкрементальный стриминг логов из backend и pipeline logs (`/api/logs`, `/api/logs/tail`).
- Детерминированная генерация runner-кода из canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev драйвер для итеративного развития репозитория (`scripts/auto-autoappdev-development.sh`).
- Пайплайн автоматизации README с каркасом мультиязычной генерации в `i18n/`.

## 📚 Содержание
- `docs/auto-development-guide.md`: Двуязычное (EN/ZH) описание философии и требований к долгоживущему, возобновляемому агенту auto-development.
- `docs/ORDERING_RATIONALE.md`: Пример обоснования для последовательности шагов на основе скриншотов.
- `docs/controller-mvp-scope.md`: Область MVP контроллера (экраны + минимальные API).
- `docs/end-to-end-demo-checklist.md`: Детерминированный ручной checklist сквозной демонстрации (backend + happy path PWA).
- `docs/env.md`: Соглашения по переменным окружения (.env).
- `docs/api-contracts.md`: Контракты API запросов/ответов контроллера.
- `docs/pipeline-formatted-script-spec.md`: Стандартный формат pipeline script (AAPS) и схема canonical IR (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Детерминированный генератор исполняемых bash pipeline runner-скриптов из canonical IR.
- `docs/common-actions.md`: Контракты/спеки общих действий (включая `update_readme`).
- `docs/workspace-layout.md`: Стандартные папки workspace + контракты (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: Запуск приложения AutoAppDev (backend + PWA) в tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Запуск self-dev драйвера AutoAppDev в tmux.
- `scripts/app-auto-development.sh`: Линейный pipeline driver (plan -> backend -> PWA -> Android -> iOS -> review -> summary) с поддержкой resume/state.
- `scripts/generate_screenshot_docs.sh`: Генератор описаний screenshot -> markdown (на базе Codex).
- `scripts/setup_backend_env.sh`: Bootstrap conda-среды backend для локальных запусков.
- `examples/ralph-wiggum-example.sh`: Пример помощника автоматизации Codex CLI.

## 🗂️ Структура проекта
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

## ✅ Предварительные требования
- ОС с `bash`.
- Python `3.11+`.
- Conda (`conda`) для предоставленных setup-скриптов.
- `tmux` для одно-командных сессий backend+PWA или self-dev.
- PostgreSQL, доступный по `DATABASE_URL`.
- Опционально: CLI `codex` для Codex-driven сценариев (self-dev, parse-llm fallback, auto-readme pipeline).

## 🛠️ Установка
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

### 3) Создайте/обновите backend-среду
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Примените схему базы данных
```bash
conda run -n autoappdev python -m backend.apply_schema
```

## ⚙️ Конфигурация
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

## ▶️ Использование
### Запустить backend + PWA вместе (рекомендуется)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
По умолчанию:
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### Запустить только backend
```bash
conda run -n autoappdev python -m backend.app
```

### Запустить только статический сервер PWA
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### Запустить self-dev драйвер в tmux
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

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

Смотрите `docs/api-contracts.md` для форматов запросов/ответов.

## 🧪 Примеры
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
Затем используйте в PWA элементы управления Start/Pause/Resume/Stop и проверьте `/api/logs`.

## 🧱 Заметки по разработке
- Backend основан на Tornado и рассчитан на удобную локальную разработку (включая permissive CORS для localhost с разными портами).
- Хранилище ориентировано на PostgreSQL-first с compatibility behavior в `backend/storage.py`.
- Ключи блоков PWA и значения `STEP.block` в скриптах намеренно согласованы (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Встроенные действия readonly; перед редактированием выполняйте clone.
- Действие `update_readme` ограничено path-safety: только README-цели workspace в `auto-apps/<workspace>/README.md`.
- В некоторых docs/scripts встречаются исторические ссылки на пути/имена (`HeyCyan`, `LightMind`), унаследованные в ходе эволюции проекта. Текущий канонический путь репозитория — корень этого репозитория.
- Корневая директория `i18n/` существует. В мультиязычных прогонах ожидаются языковые README-файлы именно там.

## 🩺 Устранение неполадок
- `tmux not found`:
  - Установите `tmux` или запускайте backend/PWA вручную.
- Backend не стартует из-за отсутствующих env:
  - Сверьте `.env` с `.env.example` и `docs/env.md`.
- Ошибки базы данных (connection/auth/schema):
  - Проверьте `DATABASE_URL`.
  - Повторно выполните `conda run -n autoappdev python -m backend.apply_schema`.
  - Опциональная проверка подключения: `conda run -n autoappdev python -m backend.db_smoketest`.
- PWA загружается, но не может вызвать API:
  - Убедитесь, что backend слушает ожидаемый host/port.
  - Пересоздайте `pwa/config.local.js`, повторно запустив `./scripts/run_autoappdev_tmux.sh`.
- Pipeline Start возвращает invalid transition:
  - Сначала проверьте текущее состояние пайплайна; запуск должен идти из состояния `stopped`.
- В UI нет обновлений логов:
  - Подтвердите, что `runtime/logs/pipeline.log` действительно записывается.
  - Используйте `/api/logs` и `/api/logs/tail` напрямую, чтобы отделить проблемы UI от backend.
- LLM parse endpoint возвращает disabled:
  - Установите `AUTOAPPDEV_ENABLE_LLM_PARSE=1` и перезапустите backend.

Для детерминированного ручного пути проверки используйте `docs/end-to-end-demo-checklist.md`.

## 🗺️ Дорожная карта
- Завершить оставшиеся self-dev задачи сверх текущего статуса `51 / 55`.
- Расширить инструменты workspace/materials/context и усилить безопасные path-контракты.
- Продолжить улучшение UX палитры действий и редактируемых workflows действий.
- Углубить поддержку мультиязычного README/UI в `i18n/` и переключение языков в рантайме.
- Усилить smoke/integration проверки и покрытие CI (в настоящее время присутствуют script-driven smoke checks; полноценный CI manifest в корне не задокументирован).

## 🤝 Участие
Вклад приветствуется через issues и pull requests.

Рекомендуемый workflow:
1. Сделайте fork и создайте feature-ветку.
2. Поддерживайте изменения сфокусированными и воспроизводимыми.
3. По возможности предпочитайте детерминированные скрипты/тесты.
4. Обновляйте документацию при изменении поведения/контрактов (`docs/*`, API-контракты, примеры).
5. Откройте PR с контекстом, шагами валидации и любыми предположениями о рантайме.

Текущие удалённые репозитории включают:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- в локальных клонах может присутствовать дополнительный remote для связанных репозиториев.

## 📄 Лицензия
В этом снимке репозитория не обнаружен корневой файл `LICENSE`.

Примечание-предположение:
- Пока файл лицензии не добавлен, считайте условия использования/распространения неуточнёнными и уточняйте их у мейнтейнера.

## ❤️ Sponsor & Donate

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
