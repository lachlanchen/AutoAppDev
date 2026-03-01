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

Scripts reutilizables + guías para construir aplicaciones paso a paso desde capturas/Markdown con Codex como herramienta no interactiva.

> 🎯 **Misión:** Hacer que las pipelines de desarrollo de apps sean deterministas, reanudables y orientadas a artefactos.
>
> 🧩 **Principio de diseño:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Señales del proyecto

| Señal | Dirección actual |
| --- | --- |
| Modelo de ejecución | Backend de Tornado + controlador PWA estático |
| Ejecución de pipeline | Determinista y reanudable (`start/pause/resume/stop`) |
| Estrategia de persistencia | PostgreSQL-first con comportamiento de fallback compatible |
| Flujo de documentación | README raíz canónico + variantes automatizadas en `i18n/` |

### 🔗 Navegación rápida

| Necesidad | Ir a |
| --- | --- |
| Primera ejecución local | [⚡ Inicio rápido](#-inicio-rápido) |
| Entorno y variables requeridas | [⚙️ Configuración](#-configuración) |
| Superficie API | [📡 Resumen de API](#-resumen-de-api) |
| Procedimientos operativos/depuración | [🧭 Runbooks operativos](#-runbooks-operativos) |
| Reglas de generación de README/i18n | [🌐 Flujo README e i18n](#-flujo-readme-e-i18n) |
| Matriz de solución de problemas | [🔧 Solución de problemas](#-solución-de-problemas) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Estado de Self-Dev (Actualizado automáticamente)

- Actualizado: 2026-02-16T00:27:20Z
- Commit de fase: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progreso: 51 / 55 tareas completadas
- Sesión de Codex: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Filosofía: Plan -> Work -> Verify -> Summary -> Commit/Push (lineal, reanudable)

Esta sección se actualiza con `scripts/auto-autoappdev-development.sh`.
No edite el contenido entre los marcadores.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Tabla de contenidos
- [🧭 Resumen del repositorio](#-resumen-del-repositorio)
- [🚀 Visión general](#-visión-general)
- [🧭 Filosofía](#-filosofía)
- [✨ Características](#-características)
- [📌 En resumen](#-en-resumen)
- [🏗️ Arquitectura](#-arquitectura)
- [📚 Contenido](#-contenido)
- [🗂️ Estructura del proyecto](#-estructura-del-proyecto)
- [✅ Requisitos previos](#-requisitos-previos)
- [🧩 Compatibilidad y supuestos](#-compatibilidad-y-supuestos)
- [🛠️ Instalación](#-instalación)
- [⚡ Inicio rápido](#-inicio-rápido)
- [⚙️ Configuración](#-configuración)
- [▶️ Uso](#-uso)
- [🧭 Runbooks operativos](#-runbooks-operativos)
- [📡 Resumen de API](#-resumen-de-api)
- [🧪 Ejemplos](#-ejemplos)
- [🧱 Notas de desarrollo](#-notas-de-desarrollo)
- [🔐 Notas de seguridad](#-notas-de-seguridad)
- [🔧 Solución de problemas](#-solución-de-problemas)
- [🌐 Flujo README e i18n](#-flujo-readme-e-i18n)
- [📘 Contexto de generación del README](#-contexto-de-generación-del-readme)
- [❓ FAQ](#-faq)
- [🗺️ Hoja de ruta](#-hoja-de-ruta)
- [🤝 Contribuciones](#-contribuciones)
- [❤️ Support](#-support)
- [📄 License](#-license)

## 🧭 Resumen del repositorio

| Enfoque | Configuración actual |
| --- | --- |
| Bucle principal | Plan → Work → Debug → Fix → Summary → Commit/Push |
| Modelo de ejecución | Backend Tornado + controlador PWA estático |
| Máquina de estados | `start` / `pause` / `resume` / `stop` |
| Persistencia | PostgreSQL-first con compatibilidad de fallback JSON |
| Documentación | `README.md` canónico + salidas multilingües en `i18n/` |

## 🚀 Visión general
AutoAppDev es un proyecto controlador para pipelines de desarrollo de apps de larga duración y reanudables. Combina:

1. Un backend API Tornado con persistencia en PostgreSQL (más comportamiento de fallback JSON local en el código de almacenamiento).
2. Una interfaz de control PWA estática al estilo Scratch.
3. Scripts y documentación para la autoría de pipelines, generación determinista de código, ciclos de auto-desarrollo y automatización del README.

El proyecto está optimizado para la ejecución predecible de agentes con secuenciación estricta e historial de trabajo orientado a artefactos.

### 🎨 Por qué existe este repositorio

| Tema | Qué significa en la práctica |
| --- | --- |
| Determinismo | IR canónico + flujos parser/import/codegen diseñados para repetibilidad |
| Reanudabilidad | Máquina de estados de ciclo de vida explícita (`start/pause/resume/stop`) para ejecuciones largas |
| Operabilidad | Logs runtime, canales inbox/outbox y bucles de verificación guiados por scripts |
| Documentación primero | Contratos/especificaciones/ejemplos viven en `docs/`, con flujo de README multilingüe automatizado |

## 🧭 Filosofía
AutoAppDev trata los agentes como herramientas y mantiene el trabajo estable mediante un bucle estricto y reanudable:

1. Plan
2. Implementar
3. Depurar/verificar (con timeouts)
4. Corregir
5. Resumir + registrar
6. Commit + push

La app controladora busca reflejar los mismos conceptos que los bloques/acciones tipo Scratch (incluida una acción común `update_readme`) para que cada workspace permanezca vigente y reproducible.

### 🔁 Intención del estado de ciclo de vida

| Transición de estado | Intención operacional |
| --- | --- |
| `start` | Iniciar una pipeline desde estado detenido/listo |
| `pause` | Detener la ejecución prolongada con seguridad sin perder contexto |
| `resume` | Continuar desde estado/artefactos de ejecución guardados |
| `stop` | Finalizar la ejecución y volver a un estado no en ejecución |

## ✨ Características
- Control reanudable del ciclo de vida de la pipeline: start, pause, resume, stop.
- APIs de biblioteca de scripts para pipelines AAPS (`.aaps`) e IR canónico (`autoappdev_ir` v1).
- Pipeline determinista parser/import:
  - Parsear scripts AAPS formateados.
  - Importar shell anotado vía comentarios `# AAPS:`.
  - Fallback opcional de parseo asistido por Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Registro de acciones con built-ins + acciones editables/personalizadas (flujo clonar/editar para built-ins de solo lectura).
- Bloques PWA al estilo Scratch y paleta de acciones cargada en runtime (`GET /api/actions`).
- Canales de mensajería de runtime:
  - Inbox (`/api/inbox`) para guía de operador -> pipeline.
  - Outbox (`/api/outbox`) incluyendo ingesta de cola de archivos desde `runtime/outbox`.
- Streaming incremental de logs desde backend y logs de pipeline (`/api/logs`, `/api/logs/tail`).
- Generación determinista del runner desde IR canónico (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev para evolución iterativa del repositorio (`scripts/auto-autoappdev-development.sh`).
- Pipeline de automatización de README con andamiaje de generación multilingüe en `i18n/`.

## 📌 En resumen

| Área | Detalles |
| --- | --- |
| Runtime principal | Backend Tornado + frontend PWA estático |
| Persistencia | PostgreSQL-first con comportamiento de compatibilidad en `backend/storage.py` |
| Modelo de pipeline | IR canónico (`autoappdev_ir` v1) y formato de script AAPS |
| Flujo de control | Ciclo de vida Start / Pause / Resume / Stop |
| Modo de desarrollo | Bucle self-dev reanudable + flujos deterministas de script/codegen |
| README/i18n | Pipeline de README automatizado con scaffolding en `i18n/` |

## 🏗️ Arquitectura

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

### Responsabilidades del backend
- Exponer APIs de control para scripts, acciones, plan, ciclo de vida de pipeline, logs, inbox/outbox y configuración de workspace.
- Validar y persistir activos de scripts de pipeline.
- Coordinar estado de ejecución del pipeline y transiciones de estado.
- Proveer comportamiento de fallback determinista cuando el pool de DB no está disponible.

### Responsabilidades del frontend
- Renderizar la UI de bloques tipo Scratch y el flujo de edición del pipeline.
- Cargar la paleta de acciones dinámicamente desde el registro del backend.
- Ejecutar controles de ciclo de vida y monitorear estado/logs/mensajes.

## 📚 Contenido
Referencia principal para los docs, scripts y ejemplos más usados:

- `docs/auto-development-guide.md`: Filosofía y requisitos bilingües (EN/ZH) para un agente de auto-desarrollo de ejecución prolongada y reanudable.
- `docs/ORDERING_RATIONALE.md`: Ejemplo de razonamiento para secuenciar pasos guiados por capturas.
- `docs/controller-mvp-scope.md`: Alcance MVP del controlador (pantallas + APIs mínimas).
- `docs/end-to-end-demo-checklist.md`: Checklist manual determinista de demo end-to-end (backend + happy path de PWA).
- `docs/env.md`: Convenciones de variables de entorno (`.env`).
- `docs/api-contracts.md`: Contratos de request/response de API para el controlador.
- `docs/pipeline-formatted-script-spec.md`: Formato estándar de script de pipeline (AAPS) y esquema IR canónico (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Generador determinista de runners bash ejecutables desde IR canónico.
- `docs/common-actions.md`: Contratos/especificaciones de acciones comunes (incluye `update_readme`).
- `docs/workspace-layout.md`: Carpetas y contratos estándar de workspace (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Arranca AutoAppDev (backend + PWA) en tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Arranca el driver self-dev de AutoAppDev en tmux.
- `scripts/app-auto-development.sh`: Driver de pipeline lineal (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) con soporte resume/estado.
- `scripts/generate_screenshot_docs.sh`: Generador de descripciones markdown desde capturas (Con Codex).
- `scripts/setup_autoappdev_env.sh`: Script principal de bootstrap de entorno conda para ejecuciones locales.
- `scripts/setup_backend_env.sh`: Script auxiliar de entorno backend.
- `examples/ralph-wiggum-example.sh`: Ejemplo de helper de automatización de Codex CLI.

## 🗂️ Estructura del proyecto
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

## ✅ Requisitos previos
- SO con `bash`.
- Python `3.11+`.
- Conda (`conda`) para los scripts de setup proporcionados.
- `tmux` para una sesión de backend + PWA o self-dev en un comando.
- PostgreSQL accesible por `DATABASE_URL`.
- Opcional: CLI de `codex` para flujos con Codex (self-dev, parse-llm fallback, pipeline auto-readme).

Matriz rápida de requisitos:

| Componente | Requerido | Propósito |
| --- | --- | --- |
| `bash` | Sí | Ejecución de scripts |
| Python `3.11+` | Sí | Backend + herramientas de codegen |
| Conda | Sí (flujo recomendado) | Scripts de bootstrap de entorno |
| PostgreSQL | Sí (modo preferido) | Persistencia primaria via `DATABASE_URL` |
| `tmux` | Recomendado | Sesiones gestionadas de backend/PWA y self-dev |
| CLI `codex` | Opcional | Parseo LLM asistido y automatización README/self-dev |

## 🧩 Compatibilidad y supuestos

| Tema | Expectativa actual |
| --- | --- |
| SO local | Linux/macOS con shells de `bash` son el objetivo principal |
| Runtime Python | `3.11` (gestionado por `scripts/setup_autoappdev_env.sh`) |
| Modo de persistencia | PostgreSQL es preferido y tratado como canónico |
| Comportamiento de fallback | `backend/storage.py` incluye fallback JSON compatible para escenarios degradados |
| Modelo de red | Desarrollo split-port localhost (backend + PWA estático) |
| Herramientas del agente | CLI `codex` es opcional salvo uso de parseo LLM o automatización self-dev |

Supuestos usados en este README:
- Ejecutas comandos desde la raíz del repositorio salvo que una sección diga lo contrario.
- `.env` está configurado antes de arrancar los servicios backend.
- `conda` y `tmux` están disponibles para los workflows recomendados.

## 🛠️ Instalación
### 1) Clonar y entrar al repo
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Configurar entorno
```bash
cp .env.example .env
```

Edita `.env` y establece al menos:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` y `AUTOAPPDEV_PORT` (o `PORT`)

### 3) Crear/actualizar entorno backend
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Aplicar esquema de BD
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Opcional: prueba de humo de BD
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Inicio rápido
```bash
# from repo root
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Luego abre:
- PWA: `http://127.0.0.1:5173/`
- API base backend: `http://127.0.0.1:8788`
- Verificación de salud: `http://127.0.0.1:8788/api/health`

Chequeo rápido con un comando:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Mapa rápido de endpoints:

| Superficie | URL |
| --- | --- |
| Interfaz PWA | `http://127.0.0.1:5173/` |
| API backend | `http://127.0.0.1:8788` |
| Endpoint health | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuración
Archivo principal: `.env` (ver `docs/env.md` y `.env.example`).

### Variables importantes

| Variable | Propósito |
| --- | --- |
| `SECRET_KEY` | Requerida por convención |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Ajustes de bind del backend |
| `DATABASE_URL` | DSN de PostgreSQL (preferido) |
| `AUTOAPPDEV_RUNTIME_DIR` | Sobrescribir runtime dir (default `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Objetivo de ejecución de pipeline por defecto |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Habilita `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Defaults de Codex para acciones/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Reservados para integraciones futuras |

Validar `.env` rápidamente:
```bash
bash -lc 'set -euo pipefail; test -f .env; set -a; source .env; set +a; \
python3 - <<"PY"\
import os, sys\
req = ["SECRET_KEY", "DATABASE_URL"]\
missing = [k for k in req if not os.getenv(k)]\
port_ok = bool(os.getenv("AUTOAPPDEV_PORT") or os.getenv("PORT"))\
if not port_ok: missing.append("AUTOAPPDEV_PORT o PORT")\
if missing:\
  print("Missing env:", ", ".join(missing))\
  sys.exit(1)\
print("OK: env looks set")\
PY'
```

## ▶️ Uso

| Modo | Comando | Notas |
| --- | --- | --- |
| Iniciar backend + PWA (recomendado) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Iniciar solo backend | `conda run -n autoappdev python -m backend.app` | Usa configuración `.env` para bind + BD |
| Servidor estático solo PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Útil para checks frontend-only |
| Ejecutar driver self-dev en tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Bucle self-development reanudable |

### Opciones comunes de scripts
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parsear y guardar scripts
- Parseo de AAPS via API: `POST /api/scripts/parse`
- Importar shell anotado: `POST /api/scripts/import-shell`
- Parse LLM opcional: `POST /api/scripts/parse-llm` (requiere `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### APIs de control de pipeline
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Otras APIs usadas frecuentemente
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Acciones: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Mensajería: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Ver `docs/api-contracts.md` para formas request/response.

## 🧭 Runbooks operativos

### Runbook: levantar stack local completo
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Puntos de validación:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Abrir `http://127.0.0.1:5173/` y confirmar que la UI pueda cargar `/api/config`.
- Opcional: abrir `/api/version` y verificar que se devuelvan metadatos esperados del backend.

### Runbook: depuración solo backend
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: smoke determinista de codegen
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

## 📡 Resumen de API

Grupos de API en un vistazo:

| Categoría | Endpoints |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Modelo de plan | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Registro de acciones | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Runtime pipeline | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Mensajería + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| Configuración de workspace | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Ejemplos
### Ejemplo de AAPS
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

Ejemplos completos:
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### Generación determinista de runner
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Pipeline demo determinista
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Luego usa los controles Start/Pause/Resume/Stop del PWA y revisa `/api/logs`.

### Importar desde shell anotado
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 Notas de desarrollo
- El backend está basado en Tornado y pensado para ergonomía local (incluyendo CORS permisivo para puertos split en localhost).
- El almacenamiento es PostgreSQL-first con comportamiento compatible en `backend/storage.py`.
- Las claves de bloque del PWA y los valores de `STEP.block` están alineados intencionalmente (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Las acciones built-in son de solo lectura; clona antes de editar.
- La acción `update_readme` tiene restricciones de seguridad de rutas para objetivos de README en `auto-apps/<workspace>/README.md`.
- Hay referencias históricas de rutas/nombres en algunos docs/scripts (`HeyCyan`, `LightMind`) heredadas de la evolución del proyecto. La ruta canónica actual del repo es la raíz de este repositorio.
- El directorio raíz `i18n/` existe. En corridas multilingües se esperan archivos README de idiomas allí.

### Modelo de trabajo y archivos de estado
- Runtime usa `./runtime` por defecto salvo sobrescritura por `AUTOAPPDEV_RUNTIME_DIR`.
- El estado/historial de automatización self-dev se rastrea en `references/selfdev/`.
- Los artefactos del pipeline README se registran en `.auto-readme-work/<timestamp>/`.

### Postura de tests (actual)
- El repositorio incluye smoke checks y scripts deterministas de demo.
- Un suite de pruebas/CI de nivel superior todavía no está definida en metadatos raíz.
- Suposición: la validación sigue siendo principalmente impulsada por scripts por ahora (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, checklist end-to-end).

## 🔐 Notas de seguridad
- La acción `update_readme` está restringida intencionalmente a objetivos README de workspace (`auto-apps/<workspace>/README.md`) con protecciones de path traversal.
- La validación del registry de acciones fuerza campos normalizados y valores acotados para los niveles de razonamiento soportados.
- Los scripts del repositorio asumen ejecución local confiable; revisa los cuerpos de script antes de ejecutarlos en entornos compartidos o cercanos a producción.
- `.env` puede contener valores sensibles (`DATABASE_URL`, claves API). Mantén `.env` fuera de commits y usa gestión de secretos acorde al entorno.

## 🔧 Solución de problemas

| Síntoma | Qué verificar |
| --- | --- |
| `tmux not found` | Instalar `tmux` o ejecutar backend/PWA manualmente. |
| El backend falla al iniciar por env faltante | Revisa `.env` contra `.env.example` y `docs/env.md`. |
| Errores de BD (conexión/autenticación/schema) | Verifica `DATABASE_URL`; ejecuta nuevamente `conda run -n autoappdev python -m backend.apply_schema`; verificación opcional: `conda run -n autoappdev python -m backend.db_smoketest`. |
| La PWA carga pero no puede llamar a la API | Asegúrate de que backend escuche en host/puerto esperado; regenera `pwa/config.local.js` relanzando `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start devuelve transición inválida | Revisa estado actual del pipeline; inicia desde estado `stopped`. |
| No hay actualizaciones de log en la UI | Confirma que `runtime/logs/pipeline.log` se esté escribiendo; usa `/api/logs` y `/api/logs/tail` directamente para aislar problema de UI vs backend. |
| Endpoint de parseo LLM está deshabilitado | Configura `AUTOAPPDEV_ENABLE_LLM_PARSE=1` y reinicia backend. |
| `conda run -n autoappdev ...` falla | Vuelve a ejecutar `./scripts/setup_autoappdev_env.sh`; confirma que exista el entorno conda `autoappdev` (`conda env list`). |
| API objetivo incorrecta en frontend | Confirma que `pwa/config.local.js` exista y apunte al host/puerto activo del backend. |

Para una verificación manual determinista, usa `docs/end-to-end-demo-checklist.md`.

## 🌐 Flujo README e i18n
- El README raíz es la fuente canónica usada por el pipeline de automatización.
- Se esperan variantes multilingües en `i18n/`.
- Estado del directorio i18n: ✅ presente en este repositorio.
- Conjunto actual de idiomas en este repositorio:
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
- La navegación de idiomas debe permanecer como una sola línea al inicio de cada variante README (sin barras de idioma duplicadas).
- Punto de entrada del pipeline README: `prompt_tools/auto-readme-pipeline.sh`.

### Restricciones de generación i18n (estrictas)
- Procesar siempre generación multilingüe al actualizar contenido canónico del README.
- Generar/actualizar archivos de idioma uno por uno (secuencialmente), no en lotes ambiguos.
- Mantener exactamente una línea de navegación de idiomas al tope de cada variante.
- No duplicar barras de idioma dentro del mismo archivo.
- Preservar comandos canónicos, enlaces, rutas de API y la intención de badges a través de traducciones.

Sugerencia de orden uno a uno:
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

Tabla de cobertura de idiomas:

| Idioma | Archivo |
| --- | --- |

## 📘 Contexto de generación del README

- Marca temporal de ejecución de pipeline: `20260301_064935`
- Disparador: `./README.md` generación inicial del borrador completo
- Prompt de entrada del usuario: `probe prompt`
- Objetivo: generar un borrador de README completo y pulido con secciones requeridas e información de soporte
- Snapshot de fuente usado:
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- Este archivo se generó de contenidos del repositorio y quedó como punto de entrada canónico del borrador.

## ❓ FAQ

### ¿PostgreSQL es obligatorio?
Preferido y esperado para operación normal. La capa de almacenamiento tiene comportamiento de fallback de compatibilidad, pero el uso tipo producción asume que PostgreSQL está disponible vía `DATABASE_URL`.

### ¿Por qué ambos `AUTOAPPDEV_PORT` y `PORT`?
`AUTOAPPDEV_PORT` es específico del proyecto. `PORT` existe como alias amigable a despliegue. Mantenlos alineados salvo que intencionalmente quieras sobrescribir el comportamiento de arranque.

### ¿Por dónde empiezo si solo quiero inspeccionar APIs?
Ejecuta backend-only (`conda run -n autoappdev python -m backend.app`) y usa `/api/health`, `/api/version`, `/api/config`, luego endpoints y acciones listadas en `docs/api-contracts.md`.

### ¿Los README multilingües se generan automáticamente?
Sí. El repositorio incluye `prompt_tools/auto-readme-pipeline.sh`, y las variantes de idioma se mantienen en `i18n/` con una línea única de navegación de idiomas al inicio de cada variante.

## 🗺️ Hoja de ruta
- Completar tareas restantes más allá del estado actual `51 / 55`.
- Expandir el tooling de workspace/materials/context y contratos de rutas seguras.
- Mejorar la UX del action palette y flujos de acciones editables.
- Profundizar soporte de README/UI multilingüe en `i18n/` y cambio de idioma runtime.
- Fortalecer checks smoke/integración y cobertura CI (actualmente hay smoke checks impulsados por scripts; no hay manifiesto de CI completo documentado en raíz).
- Seguir endureciendo la determinismo de parser/import/codegen en torno a AAPS v1 y IR canónico.

## 🤝 Contribuciones
Las contribuciones son bienvenidas vía issues y pull requests.

Flujo sugerido:
1. Haz fork y crea una rama de función.
2. Mantén los cambios enfocados y reproducibles.
3. Prefiere scripts/pruebas deterministas cuando sea posible.
4. Actualiza docs cuando cambien comportamientos/contratos (`docs/*`, contratos API, ejemplos).
5. Abre un PR con contexto, pasos de validación y supuestos de runtime.

Remotos del repositorio actualmente incluyen:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Puede haber remotos adicionales en clones locales para repositorios relacionados (ejemplo hallado en este workspace: `novel`).

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

No se detectó un archivo `LICENSE` en este snapshot del repositorio.

Nota de supuesto:
- Hasta que se agregue una licencia, considera los términos de uso/redistribución como no especificados y confírmalo con el maintainer.
