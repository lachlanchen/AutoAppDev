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

Scripts reutilizables + guías para crear apps paso a paso desde capturas/markdown usando Codex como herramienta no interactiva.

> 🎯 **Misión:** Hacer que los pipelines de desarrollo de apps sean deterministas, reanudables y orientados a artefactos.
>
> 🧩 **Principio de diseño:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ Señales del proyecto

| Señal | Dirección actual |
| --- | --- |
| Modelo de ejecución | Backend Tornado + controlador PWA estático |
| Ejecución de pipelines | Determinista y reanudable (`start/pause/resume/stop`) |
| Estrategia de persistencia | PostgreSQL-first con comportamiento de fallback compatible |
| Flujo de documentación | README raíz canónico + variantes automatizadas en `i18n/` |

### 🔗 Navegación rápida

| Necesidad | Ir a |
| --- | --- |
| Primera ejecución local | [⚡ Inicio rápido](#-inicio-rápido) |
| Entorno y variables requeridas | [⚙️ Configuración](#-configuración) |
| Superficie API | [📡 Resumen de API](#-resumen-de-api) |
| Runbooks de operación/depuración | [🧭 Runbooks operativos](#-runbooks-operativos) |
| Reglas de generación README/i18n | [🌐 Flujo README e i18n](#-flujo-readme-e-i18n) |
| Matriz de solución de problemas | [🔧 Solución de problemas](#-solución-de-problemas) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Estado de Self-Dev (autoactualizado)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Esta sección se actualiza con `scripts/auto-autoappdev-development.sh`.
No edites el contenido entre los marcadores.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Tabla de contenidos
- [🚀 Visión general](#-visión-general)
- [🧭 Filosofía](#-filosofía)
- [✨ Características](#-características)
- [📌 Resumen rápido](#-resumen-rápido)
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
- [❓ FAQ](#-faq)
- [🗺️ Hoja de ruta](#-hoja-de-ruta)
- [🤝 Contribuciones](#-contribuciones)
- [❤️ Support](#-support)
- [📄 Licencia](#-licencia)
- [❤️ Patrocinio y donaciones](#-patrocinio-y-donaciones)

## 🚀 Visión general
AutoAppDev es un proyecto controlador para pipelines de desarrollo de apps de larga duración y reanudables. Combina:

1. Una API backend en Tornado con persistencia respaldada por PostgreSQL (más comportamiento de fallback JSON local en el código de almacenamiento).
2. Una UI controladora PWA estática estilo Scratch.
3. Scripts y documentación para autoría de pipelines, generación de código determinista, bucles de auto-desarrollo y automatización de README.

El proyecto está optimizado para ejecución de agentes predecible con secuenciación estricta e historial de trabajo orientado a artefactos.

### 🎨 Por qué existe este repositorio

| Tema | Qué significa en la práctica |
| --- | --- |
| Determinismo | Flujos canónicos IR + parser/import/codegen diseñados para repetibilidad |
| Reanudabilidad | Máquina de estados de ciclo de vida explícita (`start/pause/resume/stop`) para ejecuciones largas |
| Operabilidad | Logs de ejecución, canales de inbox/outbox y bucles de verificación guiados por scripts |
| Documentación primero | Contratos/especificaciones/ejemplos viven en `docs/`, con flujo README multilingüe automatizado |

## 🧭 Filosofía
AutoAppDev trata a los agentes como herramientas y mantiene el trabajo estable mediante un bucle estricto y reanudable:

1. Planificar
2. Implementar
3. Depurar/verificar (con timeouts)
4. Corregir
5. Resumir + registrar
6. Commit + push

La app controladora busca reflejar los mismos conceptos que los bloques/acciones tipo Scratch (incluida una acción común `update_readme`) para que cada workspace se mantenga actual y reproducible.

### 🔁 Intención de los estados del ciclo de vida

| Transición de estado | Intención operativa |
| --- | --- |
| `start` | Iniciar un pipeline desde estado detenido/listo |
| `pause` | Detener con seguridad una ejecución larga sin perder contexto |
| `resume` | Continuar desde estado/artefactos de ejecución guardados |
| `stop` | Finalizar la ejecución y volver a un estado no activo |

## ✨ Características
- Control reanudable del ciclo de vida del pipeline: start, pause, resume, stop.
- APIs de librería de scripts para scripts pipeline AAPS (`.aaps`) e IR canónico (`autoappdev_ir` v1).
- Pipeline determinista de parser/import:
  - Parsear scripts AAPS formateados.
  - Importar shell anotado vía comentarios `# AAPS:`.
  - Fallback opcional de parseo asistido por Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Registro de acciones con acciones integradas + acciones editables/personalizadas (flujo clonar/editar para integradas de solo lectura).
- Bloques PWA tipo Scratch y paleta de acciones cargada en runtime (`GET /api/actions`).
- Canales de mensajería de runtime:
  - Inbox (`/api/inbox`) para guía operador -> pipeline.
  - Outbox (`/api/outbox`) incluyendo ingestión de cola de archivos desde `runtime/outbox`.
- Streaming incremental de logs desde backend y logs de pipeline (`/api/logs`, `/api/logs/tail`).
- Codegen determinista del runner desde IR canónico (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev para evolución iterativa del repositorio (`scripts/auto-autoappdev-development.sh`).
- Pipeline de automatización de README con andamiaje de generación multilingüe en `i18n/`.

## 📌 Resumen rápido

| Área | Detalles |
| --- | --- |
| Runtime principal | Backend Tornado + frontend PWA estático |
| Persistencia | PostgreSQL-first con comportamiento de compatibilidad en `backend/storage.py` |
| Modelo de pipeline | IR canónico (`autoappdev_ir` v1) y formato de script AAPS |
| Flujo de control | Ciclo de vida Start / Pause / Resume / Stop |
| Modo de desarrollo | Bucle self-dev reanudable + flujos deterministas de script/codegen |
| README/i18n | Pipeline README automatizado con andamiaje `i18n/` |

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
- Exponer APIs de control para scripts, acciones, plan, ciclo de vida de pipeline, logs, inbox/outbox, configuración de workspace.
- Validar y persistir assets de scripts de pipeline.
- Coordinar estado de ejecución de pipeline y transiciones de estado.
- Proporcionar fallback determinista cuando el pool de DB no está disponible.

### Responsabilidades del frontend
- Renderizar UI de bloques tipo Scratch y el flujo de edición de pipeline.
- Cargar dinámicamente la paleta de acciones desde el registro del backend.
- Gestionar controles del ciclo de vida y monitorear estado/logs/mensajes.

## 📚 Contenido
Mapa de referencia de la documentación, scripts y ejemplos más usados:

- `docs/auto-development-guide.md`: Filosofía y requisitos bilingües (EN/ZH) para un agente de auto-desarrollo de larga duración y reanudable.
- `docs/ORDERING_RATIONALE.md`: Ejemplo de razonamiento para secuenciar pasos guiados por capturas.
- `docs/controller-mvp-scope.md`: Alcance del MVP del controlador (pantallas + APIs mínimas).
- `docs/end-to-end-demo-checklist.md`: Checklist manual determinista para demo end-to-end (backend + happy path PWA).
- `docs/env.md`: Convenciones de variables de entorno (`.env`).
- `docs/api-contracts.md`: Contratos de request/response de API para el controlador.
- `docs/pipeline-formatted-script-spec.md`: Formato estándar de script pipeline (AAPS) y esquema IR canónico (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Generador determinista de runners bash ejecutables desde IR canónico.
- `docs/common-actions.md`: Contratos/especificaciones de acciones comunes (incluye `update_readme`).
- `docs/workspace-layout.md`: Carpetas estándar de workspace + contratos (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Inicia la app AutoAppDev (backend + PWA) en tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Inicia el driver self-dev de AutoAppDev en tmux.
- `scripts/app-auto-development.sh`: Driver de pipeline lineal (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) con soporte de reanudación/estado.
- `scripts/generate_screenshot_docs.sh`: Generador de descripciones markdown desde capturas (guiado por Codex).
- `scripts/setup_autoappdev_env.sh`: Script principal de bootstrap de entorno conda para ejecución local.
- `scripts/setup_backend_env.sh`: Script auxiliar de entorno backend.
- `examples/ralph-wiggum-example.sh`: Ejemplo de helper de automatización con Codex CLI.

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
- Conda (`conda`) para los scripts de configuración proporcionados.
- `tmux` para sesiones backend+PWA o self-dev con un solo comando.
- PostgreSQL accesible desde `DATABASE_URL`.
- Opcional: CLI `codex` para flujos impulsados por Codex (self-dev, fallback parse-llm, pipeline auto-readme).

Matriz rápida de requisitos:

| Componente | Requerido | Propósito |
| --- | --- | --- |
| `bash` | Sí | Ejecución de scripts |
| Python `3.11+` | Sí | Backend + herramientas de codegen |
| Conda | Sí (flujo recomendado) | Scripts de bootstrap de entorno |
| PostgreSQL | Sí (modo preferido) | Persistencia primaria vía `DATABASE_URL` |
| `tmux` | Recomendado | Sesiones gestionadas backend/PWA y self-dev |
| CLI `codex` | Opcional | Parseo asistido por LLM y automatización README/self-dev |

## 🧩 Compatibilidad y supuestos

| Tema | Expectativa actual |
| --- | --- |
| SO local | Shells Linux/macOS son el objetivo principal (scripts `bash`) |
| Runtime de Python | `3.11` (gestionado por `scripts/setup_autoappdev_env.sh`) |
| Modo de persistencia | PostgreSQL es preferido y tratado como canónico |
| Comportamiento de fallback | `backend/storage.py` incluye fallback de compatibilidad JSON para escenarios degradados |
| Modelo de red | Desarrollo localhost con puertos separados (backend + PWA estática) |
| Tooling de agente | CLI `codex` es opcional salvo para parseo asistido por LLM o automatización self-dev |

Supuestos usados en este README:
- Ejecutas comandos desde la raíz del repositorio salvo que una sección indique lo contrario.
- `.env` está configurado antes de iniciar servicios backend.
- `conda` y `tmux` están disponibles para los flujos recomendados de un solo comando.

## 🛠️ Instalación
### 1) Clona y entra al repositorio
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Configura el entorno
```bash
cp .env.example .env
```
Edita `.env` y define al menos:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` y `AUTOAPPDEV_PORT` (o `PORT`)

### 3) Crea/actualiza el entorno backend
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Aplica el esquema de base de datos
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Opcional: smoke test de base de datos
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
- Base API backend: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

Comprobación rápida con un solo comando:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Mapa rápido de endpoints:

| Superficie | URL |
| --- | --- |
| UI PWA | `http://127.0.0.1:5173/` |
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
| `AUTOAPPDEV_RUNTIME_DIR` | Sobrescribe directorio runtime (por defecto `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Objetivo por defecto de ejecución de pipeline |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Habilita `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Valores por defecto de Codex para acciones/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Reservadas para futuras integraciones |

Validar `.env` rápidamente:
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

## ▶️ Uso

| Modo | Comando | Notas |
| --- | --- | --- |
| Iniciar backend + PWA (recomendado) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Iniciar solo backend | `conda run -n autoappdev python -m backend.app` | Usa ajustes de bind + DB desde `.env` |
| Iniciar solo servidor estático PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Útil para validaciones solo frontend |
| Ejecutar driver self-dev en tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Bucle de auto-desarrollo reanudable |

### Opciones comunes de scripts
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parsear y almacenar scripts
- Parsear AAPS vía API: `POST /api/scripts/parse`
- Importar shell anotado: `POST /api/scripts/import-shell`
- Parseo LLM opcional: `POST /api/scripts/parse-llm` (requiere `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### APIs de control de pipeline
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Otras APIs usadas con frecuencia
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Mensajería: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Consulta `docs/api-contracts.md` para las formas request/response.

## 🧭 Runbooks operativos

### Runbook: levantar el stack local completo
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Puntos de validación:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Abre `http://127.0.0.1:5173/` y confirma que la UI puede cargar `/api/config`.
- Opcional: abre `/api/version` y verifica que se devuelva la metadata esperada del backend.

### Runbook: depuración solo backend
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: smoke de codegen determinista
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

Grupos principales de API, de un vistazo:

| Categoría | Endpoints |
| --- | --- |
| Salud + información runtime | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Modelo de plan | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Registro de acciones | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Runtime de pipeline | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Mensajería + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
| Configuración de workspace | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Ejemplos
### Ejemplo AAPS
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

### Generación de runner determinista
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Demo de pipeline determinista
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Luego usa los controles Start/Pause/Resume/Stop en la PWA e inspecciona `/api/logs`.

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
- El backend está basado en Tornado y diseñado para ergonomía de desarrollo local (incluye CORS permisivo para localhost con puertos separados).
- El almacenamiento es PostgreSQL-first con comportamiento de compatibilidad en `backend/storage.py`.
- Las claves de bloques de la PWA y los valores `STEP.block` del script están alineados intencionalmente (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Las acciones integradas son de solo lectura; clónalas antes de editarlas.
- La acción `update_readme` está restringida por seguridad de ruta a objetivos README del workspace bajo `auto-apps/<workspace>/README.md`.
- Existen referencias históricas de rutas/nombres en algunos docs/scripts (`HeyCyan`, `LightMind`) heredadas de la evolución del proyecto. La ruta canónica actual del repositorio es esta raíz.
- El directorio raíz `i18n/` existe. En ejecuciones multilingües se esperan archivos README de idioma allí.

### Modelo de trabajo y archivos de estado
- Runtime usa por defecto `./runtime`, salvo que se sobrescriba con `AUTOAPPDEV_RUNTIME_DIR`.
- El estado/historial de la automatización self-dev se registra en `references/selfdev/`.
- Los artefactos del pipeline README se guardan en `.auto-readme-work/<timestamp>/`.

### Postura de pruebas (actual)
- El repositorio incluye smoke checks y scripts de demo determinista.
- Actualmente no hay una suite de pruebas automatizada/manifest CI completa definida en los metadatos raíz.
- Supuesto: por ahora la validación es principalmente guiada por scripts (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, checklist end-to-end).

## 🔐 Notas de seguridad
- La acción `update_readme` está intencionalmente limitada a objetivos README de workspace (`auto-apps/<workspace>/README.md`) con protecciones contra path traversal.
- La validación del registro de acciones aplica campos de especificación normalizados y valores acotados para niveles de razonamiento soportados.
- Los scripts del repositorio asumen ejecución local confiable; revisa su contenido antes de ejecutarlos en entornos compartidos o cercanos a producción.
- `.env` puede contener valores sensibles (`DATABASE_URL`, API keys). Mantén `.env` fuera de commits y usa gestión de secretos por entorno fuera del desarrollo local.

## 🔧 Solución de problemas

| Síntoma | Qué revisar |
| --- | --- |
| `tmux not found` | Instala `tmux` o ejecuta backend/PWA manualmente. |
| Backend falla al iniciar por variables faltantes | Revisa `.env` contra `.env.example` y `docs/env.md`. |
| Errores de base de datos (conexión/auth/esquema) | Verifica `DATABASE_URL`; vuelve a ejecutar `conda run -n autoappdev python -m backend.apply_schema`; chequeo opcional de conectividad: `conda run -n autoappdev python -m backend.db_smoketest`. |
| La PWA carga pero no puede llamar a la API | Confirma que el backend escucha en host/puerto esperados; regenera `pwa/config.local.js` volviendo a ejecutar `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start devuelve transición inválida | Revisa primero el estado actual del pipeline; inicia desde estado `stopped`. |
| No hay actualizaciones de logs en UI | Confirma que `runtime/logs/pipeline.log` se está escribiendo; usa `/api/logs` y `/api/logs/tail` directamente para aislar problemas UI vs backend. |
| El endpoint de parseo LLM devuelve disabled | Define `AUTOAPPDEV_ENABLE_LLM_PARSE=1` y reinicia backend. |
| Falla `conda run -n autoappdev ...` | Vuelve a ejecutar `./scripts/setup_autoappdev_env.sh`; confirma que existe el entorno conda `autoappdev` (`conda env list`). |
| Objetivo API incorrecto en frontend | Confirma que `pwa/config.local.js` existe y apunta al host/puerto backend activo. |

Para una ruta de verificación manual determinista, usa `docs/end-to-end-demo-checklist.md`.

## 🌐 Flujo README e i18n
- El README raíz es la fuente canónica usada por el pipeline de automatización de README.
- Las variantes multilingües se esperan bajo `i18n/`.
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
- La navegación de idiomas debe mantenerse como una sola línea en la parte superior de cada variante README (sin barras de idioma duplicadas).
- Punto de entrada del pipeline README: `prompt_tools/auto-readme-pipeline.sh`.

### Restricciones de generación i18n (estrictas)
- Procesa siempre la generación multilingüe al actualizar el contenido canónico del README.
- Genera/actualiza archivos de idioma uno por uno (secuencialmente), no en lotes ambiguos.
- Mantén exactamente una línea de navegación de idiomas en la parte superior de cada variante.
- No dupliques barras de idioma dentro del mismo archivo.
- Conserva snippets de comandos canónicos, enlaces, rutas API e intención de badges en todas las traducciones.

Orden sugerido de generación, uno por uno:
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

## ❓ FAQ

### ¿Es obligatorio PostgreSQL?
Es preferido y esperado para operación normal. La capa de almacenamiento contiene comportamiento de fallback compatible, pero el uso tipo producción debe asumir PostgreSQL disponible vía `DATABASE_URL`.

### ¿Por qué existen `AUTOAPPDEV_PORT` y `PORT`?
`AUTOAPPDEV_PORT` es específico del proyecto. `PORT` existe como alias amigable para despliegues. Mantenlos alineados salvo que quieras sobreescribir el comportamiento de lanzamiento intencionalmente.

### ¿Por dónde empezar si solo quiero inspeccionar APIs?
Ejecuta solo backend (`conda run -n autoappdev python -m backend.app`) y usa `/api/health`, `/api/version`, `/api/config`, luego los endpoints de scripts/acciones listados en `docs/api-contracts.md`.

### ¿Los READMEs multilingües se generan automáticamente?
Sí. El repositorio incluye `prompt_tools/auto-readme-pipeline.sh`, y las variantes de idioma se mantienen en `i18n/` con una sola línea de navegación de idioma en la parte superior de cada variante.

## 🗺️ Hoja de ruta
- Completar las tareas self-dev restantes más allá del estado actual `51 / 55`.
- Expandir tooling de workspace/materiales/contexto y contratos de ruta segura más sólidos.
- Seguir mejorando la UX de la paleta de acciones y los flujos de acciones editables.
- Profundizar el soporte multilingüe README/UI en `i18n/` y el cambio de idioma en runtime.
- Fortalecer smoke/integration checks y cobertura CI (actualmente hay smoke checks guiados por scripts; no hay un manifiesto CI completo documentado en la raíz).
- Seguir reforzando el determinismo de parser/import/codegen en torno a AAPS v1 e IR canónico.

## 🤝 Contribuciones
Las contribuciones son bienvenidas vía issues y pull requests.

Flujo sugerido:
1. Haz fork y crea una rama de feature.
2. Mantén los cambios enfocados y reproducibles.
3. Prioriza scripts/tests deterministas cuando sea posible.
4. Actualiza docs cuando cambien comportamientos/contratos (`docs/*`, contratos API, ejemplos).
5. Abre un PR con contexto, pasos de validación y cualquier supuesto de runtime.

Los remotos del repositorio actualmente incluyen:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Puede haber remotos adicionales en clones locales para repos relacionados (ejemplo encontrado en este workspace: `novel`).

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 Licencia
No se detectó un archivo `LICENSE` en la raíz en esta instantánea del repositorio.

Nota de supuesto:
- Hasta que se agregue un archivo de licencia, trata los términos de uso/redistribución como no especificados y confírmalos con el mantenedor.

## ❤️ Patrocinio y donaciones
| Canal | Enlace |
| --- | --- |
| GitHub Sponsors | https://github.com/sponsors/lachlanchen |
| Donate | https://chat.lazying.art/donate |
| PayPal | https://paypal.me/RongzhouChen |
| Stripe | https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400 |

Si este proyecto ayuda a tu flujo de trabajo, el patrocinio apoya directamente la continuidad de tareas self-dev, la calidad de la documentación y el refuerzo del tooling.
