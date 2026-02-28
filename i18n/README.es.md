[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/figs/banner.png" alt="Banner de LazyingArt" />
</p>

# AutoAppDev

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Backend](https://img.shields.io/badge/Backend-Tornado-222222)
![Frontend](https://img.shields.io/badge/Frontend-PWA-0A7EA4)
![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Self--Dev-51%2F55%20tasks%20done-2E8B57)
![i18n](https://img.shields.io/badge/i18n-11%20languages-1f6feb)

Scripts reutilizables + guías para crear apps paso a paso desde capturas de pantalla/markdown usando Codex como herramienta no interactiva.

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Estado de Self-Dev (Actualización automática)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Esta sección se actualiza mediante `scripts/auto-autoappdev-development.sh`.
No edites contenido entre los marcadores.

<!-- AUTOAPPDEV:STATUS:END -->

## 🚀 Visión General
AutoAppDev es un proyecto controlador para pipelines de desarrollo de aplicaciones de larga duración y reanudables. Combina:

1. Una API backend en Tornado con persistencia respaldada por PostgreSQL (más comportamiento de compatibilidad con JSON local en el código de almacenamiento).
2. Una interfaz controladora PWA estática estilo Scratch.
3. Scripts y documentación para autoría de pipelines, generación de código determinista, ciclos de autodesarrollo y automatización de README.

### De un vistazo

| Área | Detalles |
| --- | --- |
| Runtime principal | Backend Tornado + frontend PWA estático |
| Persistencia | PostgreSQL primero, con comportamiento de compatibilidad en `backend/storage.py` |
| Modelo de pipeline | IR canónico (`autoappdev_ir` v1) y formato de script AAPS |
| Flujo de control | Ciclo de vida Start / Pause / Resume / Stop |
| Modo de desarrollo | Bucle self-dev reanudable + flujos deterministas de scripts/codegen |
| README/i18n | Pipeline automatizado de README con andamiaje `i18n/` |

## 🧭 Filosofía
AutoAppDev trata a los agentes como herramientas y mantiene la estabilidad del trabajo mediante un bucle estricto y reanudable:
1. Planificar
2. Implementar
3. Depurar/verificar (con timeouts)
4. Corregir
5. Resumir + registrar
6. Commit + push

La app controladora busca reflejar los mismos conceptos que los bloques/acciones estilo Scratch (incluyendo una acción común `update_readme`) para que cada workspace se mantenga actualizado y sea reproducible.

## ✨ Características
- Control reanudable del ciclo de vida del pipeline: start, pause, resume, stop.
- APIs de biblioteca de scripts para scripts de pipeline AAPS (`.aaps`) e IR canónico (`autoappdev_ir` v1).
- Pipeline determinista de parser/import:
  - Parseo de scripts AAPS formateados.
  - Importación de shell anotado mediante comentarios `# AAPS:`.
  - Fallback opcional de parseo asistido por Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Registro de acciones con acciones integradas + acciones editables/personalizadas (flujo clone/edit para integradas de solo lectura).
- Bloques PWA estilo Scratch y paleta de acciones cargada en runtime (`GET /api/actions`).
- Canales de mensajería en runtime:
  - Bandeja de entrada (`/api/inbox`) para guía operador -> pipeline.
  - Bandeja de salida (`/api/outbox`) que incluye ingesta de cola de archivos desde `runtime/outbox`.
- Streaming incremental de logs desde backend y logs del pipeline (`/api/logs`, `/api/logs/tail`).
- Codegen determinista de runner desde IR canónico (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev para evolución iterativa del repositorio (`scripts/auto-autoappdev-development.sh`).
- Pipeline de automatización de README con andamiaje de generación multilingüe bajo `i18n/`.

## 📚 Contenido
- `docs/auto-development-guide.md`: Filosofía y requisitos bilingües (EN/ZH) para un agente de autodesarrollo de larga duración y reanudable.
- `docs/ORDERING_RATIONALE.md`: Ejemplo de justificación para secuenciar pasos guiados por capturas.
- `docs/controller-mvp-scope.md`: Alcance del MVP del controlador (pantallas + APIs mínimas).
- `docs/end-to-end-demo-checklist.md`: Checklist manual determinista de demo end-to-end (ruta feliz backend + PWA).
- `docs/env.md`: Convenciones de variables de entorno (.env).
- `docs/api-contracts.md`: Contratos de request/response de la API del controlador.
- `docs/pipeline-formatted-script-spec.md`: Formato estándar de script de pipeline (AAPS) y esquema de IR canónico (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Generador determinista de runners bash ejecutables desde IR canónico.
- `docs/common-actions.md`: Contratos/especificaciones de acciones comunes (incluye `update_readme`).
- `docs/workspace-layout.md`: Carpetas estándar de workspace + contratos (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: Inicia la app AutoAppDev (backend + PWA) en tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Inicia el driver self-dev de AutoAppDev en tmux.
- `scripts/app-auto-development.sh`: Driver de pipeline lineal (plan -> backend -> PWA -> Android -> iOS -> review -> summary), con soporte de reanudación/estado.
- `scripts/generate_screenshot_docs.sh`: Generador de descripciones markdown desde capturas (impulsado por Codex).
- `scripts/setup_backend_env.sh`: Bootstrap del entorno conda del backend para ejecuciones locales.
- `examples/ralph-wiggum-example.sh`: Ejemplo de helper de automatización para Codex CLI.

## 🗂️ Estructura del Proyecto
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

## ✅ Requisitos Previos
- SO con `bash`.
- Python `3.11+`.
- Conda (`conda`) para los scripts de setup proporcionados.
- `tmux` para sesiones backend+PWA o self-dev con un solo comando.
- PostgreSQL accesible mediante `DATABASE_URL`.
- Opcional: CLI `codex` para flujos basados en Codex (self-dev, fallback parse-llm, pipeline auto-readme).

## 🛠️ Instalación
### 1) Clonar y entrar al repositorio
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

### 3) Crear/actualizar entorno de backend
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Aplicar esquema de base de datos
```bash
conda run -n autoappdev python -m backend.apply_schema
```

## ⚙️ Configuración
Archivo principal: `.env` (ver `docs/env.md` y `.env.example`).

### Variables importantes

| Variable | Propósito |
| --- | --- |
| `SECRET_KEY` | Requerida por convención |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Ajustes de bind del backend |
| `DATABASE_URL` | DSN de PostgreSQL (preferido) |
| `AUTOAPPDEV_RUNTIME_DIR` | Sobrescribe el directorio runtime (por defecto `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Objetivo por defecto para ejecutar pipeline |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Habilita `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Valores por defecto de Codex para acciones/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Reservadas para integraciones futuras |

Valida `.env` rápidamente:
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
### Iniciar backend + PWA juntos (recomendado)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
Valores por defecto:
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### Iniciar solo backend
```bash
conda run -n autoappdev python -m backend.app
```

### Iniciar solo servidor estático PWA
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### Ejecutar driver self-dev en tmux
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### Parsear y almacenar scripts
- Parsear AAPS vía API: `POST /api/scripts/parse`
- Importar shell anotado: `POST /api/scripts/import-shell`
- Parseo LLM opcional: `POST /api/scripts/parse-llm` (requiere `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### APIs de control del pipeline
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Otras APIs de uso frecuente
- Salud/versión/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Acciones: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Mensajería: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Consulta `docs/api-contracts.md` para las estructuras de request/response.

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

### Generación determinista de runner
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Pipeline de demo determinista
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Luego usa los controles Start/Pause/Resume/Stop de la PWA e inspecciona `/api/logs`.

## 🧱 Notas de Desarrollo
- El backend se basa en Tornado y está diseñado para ergonomía de desarrollo local (incluyendo CORS permisivo para puertos localhost separados).
- El almacenamiento es PostgreSQL-first con comportamiento de compatibilidad en `backend/storage.py`.
- Las keys de bloques de la PWA y los valores `STEP.block` del script están alineados intencionalmente (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Las acciones integradas son de solo lectura; clónalas antes de editarlas.
- La acción `update_readme` está restringida por seguridad de rutas a objetivos README del workspace en `auto-apps/<workspace>/README.md`.
- Existen referencias históricas de rutas/nombres en algunos docs/scripts (`HeyCyan`, `LightMind`) heredadas de la evolución del proyecto. La ruta canónica actual del repositorio es esta raíz.
- El directorio raíz `i18n/` existe. En ejecuciones multilingües, se esperan allí los archivos README por idioma.

## 🩺 Solución de Problemas
- `tmux not found`:
  - Instala `tmux` o ejecuta backend/PWA manualmente.
- El backend falla al iniciar por variables de entorno faltantes:
  - Revisa de nuevo `.env` contra `.env.example` y `docs/env.md`.
- Errores de base de datos (conexión/auth/esquema):
  - Verifica `DATABASE_URL`.
  - Vuelve a ejecutar `conda run -n autoappdev python -m backend.apply_schema`.
  - Verificación opcional de conectividad: `conda run -n autoappdev python -m backend.db_smoketest`.
- La PWA carga pero no puede llamar a la API:
  - Asegúrate de que el backend esté escuchando en el host/puerto esperado.
  - Regenera `pwa/config.local.js` volviendo a ejecutar `./scripts/run_autoappdev_tmux.sh`.
- Pipeline Start devuelve transición inválida:
  - Revisa primero el estado actual del pipeline; inicia desde `stopped`.
- No hay actualizaciones de logs en la UI:
  - Confirma que se esté escribiendo `runtime/logs/pipeline.log`.
  - Usa `/api/logs` y `/api/logs/tail` directamente para aislar problemas de UI vs backend.
- El endpoint de parseo LLM aparece deshabilitado:
  - Establece `AUTOAPPDEV_ENABLE_LLM_PARSE=1` y reinicia el backend.

Para una ruta de verificación manual determinista, usa `docs/end-to-end-demo-checklist.md`.

## 🗺️ Hoja de Ruta
- Completar las tareas restantes de self-dev más allá del estado actual `51 / 55`.
- Expandir el tooling de workspace/materiales/contexto y reforzar contratos de rutas seguras.
- Seguir mejorando la UX de la paleta de acciones y los flujos de acciones editables.
- Profundizar el soporte multilingüe de README/UI en `i18n/` y el cambio de idioma en runtime.
- Fortalecer checks de smoke/integración y cobertura de CI (actualmente hay checks smoke basados en scripts; no hay un manifiesto CI completo documentado en la raíz).

## 🤝 Contribuir
Las contribuciones son bienvenidas vía issues y pull requests.

Flujo sugerido:
1. Haz un fork y crea una rama de feature.
2. Mantén los cambios enfocados y reproducibles.
3. Prioriza scripts/tests deterministas cuando sea posible.
4. Actualiza la documentación cuando cambien comportamientos/contratos (`docs/*`, contratos de API, ejemplos).
5. Abre un PR con contexto, pasos de validación y cualquier supuesto de runtime.

Los remotos actuales del repositorio incluyen:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- puede haber un remoto adicional en clones locales para repos relacionados.

## 📄 Licencia
No se detectó un archivo `LICENSE` en la raíz en esta instantánea del repositorio.

Nota de supuesto:
- Hasta que se agregue un archivo de licencia, trata los términos de uso/redistribución como no especificados y confírmalos con el mantenedor.

## ❤️ Sponsor & Donate

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
