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

Wiederverwendbare Skripte und Leitfäden, um Apps schrittweise aus Screenshots/Markdown zu erstellen, wobei Codex als nicht-interaktives Tool eingesetzt wird.

> 🎯 **Mission:** App-Entwicklungs-Pipelines deterministisch, fortsetzbar und artefaktgetrieben machen.
>
> 🧩 **Designprinzip:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Projektsignale

| Signal | Aktuelle Richtung |
| --- | --- |
| Laufzeitmodell | Tornado-Backend + statischer PWA-Controller |
| Pipeline-Ausführung | Deterministisch und fortsetzbar (`start/pause/resume/stop`) |
| Persistenzstrategie | PostgreSQL-first mit kompatiblem Fallback-Verhalten |
| Dokumentationsfluss | Kanonische Root-README + automatisierte `i18n/`-Varianten |

### 🔗 Schnelle Navigation

| Bedarf | Gehe zu |
| --- | --- |
| Erster lokaler Start | [⚡ Quick Start](#-quick-start) |
| Umgebung und Pflichtvariablen | [⚙️ Konfiguration](#-configuration) |
| API-Überblick | [📡 API Snapshot](#-api-snapshot) |
| Laufzeit-/Debug-Playbooks | [🧭 Operative Runbooks](#-operational-runbooks) |
| README/i18n-Generierungsregeln | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| Troubleshooting-Matrix | [🔧 Troubleshooting](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev-Status (automatisch aktualisiert)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Dieser Abschnitt wird durch `scripts/auto-autoappdev-development.sh` aktualisiert.
Inhalte zwischen den Markern nicht manuell bearbeiten.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Inhaltsverzeichnis
- [🚀 Überblick](#-overview)
- [🧭 Philosophie](#-philosophy)
- [✨ Features](#-features)
- [📌 Auf einen Blick](#-at-a-glance)
- [🏗️ Architektur](#-architecture)
- [📚 Inhalte](#-contents)
- [🗂️ Projektstruktur](#-project-structure)
- [✅ Voraussetzungen](#-prerequisites)
- [🧩 Kompatibilität & Annahmen](#-compatibility--assumptions)
- [🛠️ Installation](#-installation)
- [⚡ Quick Start](#-quick-start)
- [⚙️ Konfiguration](#-configuration)
- [▶️ Nutzung](#-usage)
- [🧭 Operative Runbooks](#-operational-runbooks)
- [📡 API Snapshot](#-api-snapshot)
- [🧪 Beispiele](#-examples)
- [🧱 Entwicklungshinweise](#-development-notes)
- [🔐 Sicherheitshinweise](#-safety-notes)
- [🔧 Troubleshooting](#-troubleshooting)
- [🌐 README & i18n Workflow](#-readme--i18n-workflow)
- [📘 Readme Generation Context](#-readme-generation-context)
- [❓ FAQ](#-faq)
- [🗺️ Roadmap](#-roadmap)
- [🤝 Mitwirken](#-contributing)
- [❤️ Support](#-support)
- [📄 Lizenz](#-license)

## 🚀 Überblick
AutoAppDev ist ein Controller-Projekt für langlebige, fortsetzbare App-Entwicklungs-Pipelines. Es kombiniert:

1. Eine Tornado-Backend-API mit PostgreSQL-gestützter Persistenz (plus lokalem JSON-Fallback-Verhalten im Storage-Code).
2. Eine Scratch-ähnliche statische PWA-Controller-UI.
3. Skripte und Dokumentation für Pipeline-Authoring, deterministische Code-Generierung, Self-Development-Loops und README-Automatisierung.

Das Projekt ist für vorhersehbare Agent-Ausführung mit strikter Sequenzierung und artefaktorientierter Workflow-Historie optimiert.

### 🎨 Warum dieses Repository existiert

| Thema | Bedeutung in der Praxis |
| --- | --- |
| Determinismus | Kanonische Pipeline-IR + Parser/Import/Codegen-Workflows für Wiederholbarkeit |
| Fortsetzbarkeit | Explizite Lifecycle-State-Machine (`start/pause/resume/stop`) für lange Läufe |
| Betriebsfähigkeit | Laufzeitlogs, Inbox/Outbox-Kanäle und skriptgetriebene Verifikationsschleifen |
| Dokumentation zuerst | Verträge/Spezifikationen/Beispiele liegen in `docs/`, mit automatisiertem mehrsprachigem README-Flow |

## 🧭 Philosophie
AutoAppDev behandelt Agents als Werkzeuge und stabilisiert die Arbeit über einen strikten, fortsetzbaren Zyklus:

1. Plan
2. Implement
3. Debug/verify (mit Timeouts)
4. Fix
5. Summarize + log
6. Commit + push

Die Controller-App soll dieselben Konzepte als Scratch-ähnliche Blöcke/Aktionen verkörpern (einschließlich einer gemeinsamen `update_readme`-Action), damit jeder Workspace aktuell und reproduzierbar bleibt.

### 🔁 Zielbild der Lifecycle-States

| Zustandsübergang | Operative Absicht |
| --- | --- |
| `start` | Pipeline aus gestopptem/bereitem Zustand starten |
| `pause` | Laufende Ausführung sicher anhalten, ohne Kontextverlust |
| `resume` | Von gespeichertem Laufzeitstatus/Artefakten fortsetzen |
| `stop` | Ausführung beenden und in einen nicht laufenden Zustand zurückkehren |

## ✨ Features
- Fortsetzbare Pipeline-Lifecycle-Steuerung: start, pause, resume, stop.
- Script-Library-APIs für AAPS-Pipeline-Skripte (`.aaps`) und kanonische IR (`autoappdev_ir` v1).
- Deterministische Parser/Import-Pipeline:
  - Formatierte AAPS-Skripte parsen.
  - Annotierte Shell über `# AAPS:`-Kommentare importieren.
  - Optionaler Codex-gestützter Parse-Fallback (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Action Registry mit Built-ins + editierbaren/custom Actions (clone/edit-Flow für readonly-Built-ins).
- Scratch-ähnliche PWA-Blöcke und zur Laufzeit geladene Action-Palette (`GET /api/actions`).
- Laufzeit-Messaging-Kanäle:
  - Inbox (`/api/inbox`) für Operator -> Pipeline-Hinweise.
  - Outbox (`/api/outbox`) inkl. File-Queue-Ingestion aus `runtime/outbox`.
- Inkrementelles Log-Streaming aus Backend- und Pipeline-Logs (`/api/logs`, `/api/logs/tail`).
- Deterministische Runner-Codegenerierung aus kanonischer IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev-Treiber für iterative Repository-Weiterentwicklung (`scripts/auto-autoappdev-development.sh`).
- README-Automatisierungspipeline mit mehrsprachigem Gerüst unter `i18n/`.

## 📌 Auf einen Blick

| Bereich | Details |
| --- | --- |
| Kernlaufzeit | Tornado-Backend + statisches PWA-Frontend |
| Persistenz | PostgreSQL-first mit kompatiblem Verhalten in `backend/storage.py` |
| Pipeline-Modell | Kanonische IR (`autoappdev_ir` v1) und AAPS-Skriptformat |
| Kontrollfluss | Start / Pause / Resume / Stop-Lifecycle |
| Dev-Modus | Fortsetzbare Self-Dev-Schleife + deterministische Script/Codegen-Workflows |
| README/i18n | Automatisierte README-Pipeline mit `i18n/`-Gerüst |

## 🏗️ Architektur

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

### Backend-Verantwortlichkeiten
- Controller-APIs für Skripte, Aktionen, Plan, Pipeline-Lifecycle, Logs, Inbox/Outbox und Workspace-Konfiguration bereitstellen.
- Pipeline-Skript-Assets validieren und persistieren.
- Pipeline-Ausführungszustand und Statusübergänge koordinieren.
- Deterministisches Fallback-Verhalten bereitstellen, wenn der DB-Pool nicht verfügbar ist.

### Frontend-Verantwortlichkeiten
- Scratch-ähnliche Block-UI und Pipeline-Editing-Flow rendern.
- Action-Palette dynamisch aus der Backend-Registry laden.
- Lifecycle-Steuerung ausführen und Status/Logs/Nachrichten überwachen.

## 📚 Inhalte
Referenzkarte für die am häufigsten verwendeten Dokus, Skripte und Beispiele:

- `docs/auto-development-guide.md`: Zweisprachige (EN/ZH) Philosophie und Anforderungen für einen langlebigen, fortsetzbaren Auto-Development-Agent.
- `docs/ORDERING_RATIONALE.md`: Beispielbegründung für die Reihenfolge screenshot-gesteuerter Schritte.
- `docs/controller-mvp-scope.md`: Controller-MVP-Umfang (Screens + minimale APIs).
- `docs/end-to-end-demo-checklist.md`: Deterministische manuelle End-to-End-Demo-Checkliste (Backend + PWA Happy Path).
- `docs/env.md`: Konventionen für Umgebungsvariablen (`.env`).
- `docs/api-contracts.md`: API-Request/Response-Verträge für den Controller.
- `docs/pipeline-formatted-script-spec.md`: Standard-Pipeline-Skriptformat (AAPS) und kanonisches IR-Schema (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Deterministischer Generator für ausführbare Bash-Pipeline-Runner aus kanonischer IR.
- `docs/common-actions.md`: Häufige Action-Verträge/Spezifikationen (inkl. `update_readme`).
- `docs/workspace-layout.md`: Standard-Workspace-Ordner + Verträge (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Startet die AutoAppDev-App (Backend + PWA) in tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Startet den AutoAppDev-Self-Dev-Treiber in tmux.
- `scripts/app-auto-development.sh`: Linearer Pipeline-Treiber (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) mit Resume/State-Unterstützung.
- `scripts/generate_screenshot_docs.sh`: Generator für Screenshot -> Markdown-Beschreibung (Codex-gestützt).
- `scripts/setup_autoappdev_env.sh`: Hauptskript zum Bootstrappen der conda-Umgebung für lokale Läufe.
- `scripts/setup_backend_env.sh`: Hilfsskript für Backend-Umgebung.
- `examples/ralph-wiggum-example.sh`: Beispielhafter Codex-CLI-Automationshelfer.

## 🗂️ Projektstruktur
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

## ✅ Voraussetzungen
- Betriebssystem mit `bash`.
- Python `3.11+`.
- Conda (`conda`) für die bereitgestellten Setup-Skripte.
- `tmux` für Ein-Kommando-Sitzungen mit Backend+PWA oder Self-Dev.
- PostgreSQL erreichbar über `DATABASE_URL`.
- Optional: `codex` CLI für Codex-gestützte Flows (Self-Dev, parse-llm-Fallback, Auto-README-Pipeline).

Quick requirement matrix:

| Komponente | Erforderlich | Zweck |
| --- | --- | --- |
| `bash` | Ja | Skriptausführung |
| Python `3.11+` | Ja | Backend + Codegen-Tooling |
| Conda | Ja (empfohlener Flow) | Environment-Bootstrap-Skripte |
| PostgreSQL | Ja (bevorzugter Modus) | Primäre Persistenz über `DATABASE_URL` |
| `tmux` | Empfohlen | Verwaltete Backend/PWA- und Self-Dev-Sessions |
| `codex` CLI | Optional | LLM-gestütztes Parsing und README/Self-Dev-Automatisierung |

## 🧩 Kompatibilität & Annahmen

| Thema | Aktuelle Erwartung |
| --- | --- |
| Lokales OS | Linux/macOS-Shells sind primäres Ziel (`bash`-Skripte) |
| Python-Laufzeit | `3.11` (verwaltet durch `scripts/setup_autoappdev_env.sh`) |
| Persistenzmodus | PostgreSQL ist bevorzugt und gilt als kanonisch |
| Fallback-Verhalten | `backend/storage.py` enthält JSON-Kompatibilitäts-Fallback für degradierte Szenarien |
| Netzwerkmodell | Lokale Split-Port-Entwicklung (Backend + statische PWA) |
| Agent-Tooling | `codex` CLI ist optional, außer bei LLM-Parsing oder Self-Dev-Automatisierung |

Annahmen in dieser README:
- Befehle werden vom Repository-Root ausgeführt, sofern nicht anders angegeben.
- `.env` ist konfiguriert, bevor Backend-Services gestartet werden.
- `conda` und `tmux` sind für die empfohlenen One-Command-Workflows verfügbar.

## 🛠️ Installation
### 1) Repo klonen und betreten
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Umgebung konfigurieren
```bash
cp .env.example .env
```
Bearbeite `.env` und setze mindestens:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` und `AUTOAPPDEV_PORT` (oder `PORT`)

### 3) Backend-Umgebung erstellen/aktualisieren
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Datenbankschema anwenden
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Optional: Datenbank-Smoke-Test
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

Dann öffnen:
- PWA: `http://127.0.0.1:5173/`
- Backend API Base: `http://127.0.0.1:8788`
- Health Check: `http://127.0.0.1:8788/api/health`

Smoke-Check mit einem Befehl:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Schnelle Endpoint-Übersicht:

| Oberfläche | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health-Endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Konfiguration
Primäre Datei: `.env` (siehe `docs/env.md` und `.env.example`).

### Wichtige Variablen

| Variable | Zweck |
| --- | --- |
| `SECRET_KEY` | Konventionsgemäß erforderlich |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Backend-Bind-Einstellungen |
| `DATABASE_URL` | PostgreSQL-DSN (bevorzugt) |
| `AUTOAPPDEV_RUNTIME_DIR` | Runtime-Verzeichnis überschreiben (Standard `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Standardziel für Pipeline-Ausführung |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Aktiviert `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Codex-Defaults für Actions/Endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Für zukünftige Integrationen reserviert |

`.env` schnell validieren:
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

## ▶️ Nutzung

| Modus | Befehl | Hinweise |
| --- | --- | --- |
| Backend + PWA starten (empfohlen) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Nur Backend starten | `conda run -n autoappdev python -m backend.app` | Nutzt `.env`-Bind- + DB-Einstellungen |
| Nur PWA-Static-Server starten | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Nützlich für Frontend-only-Checks |
| Self-Dev-Treiber in tmux starten | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Fortsetzbare Self-Development-Schleife |

### Häufige Skriptoptionen
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Skripte parsen und speichern
- AAPS per API parsen: `POST /api/scripts/parse`
- Annotierte Shell importieren: `POST /api/scripts/import-shell`
- Optionales LLM-Parsing: `POST /api/scripts/parse-llm` (benötigt `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### Pipeline-Control-APIs
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Weitere häufig genutzte APIs
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Siehe `docs/api-contracts.md` für Request/Response-Strukturen.

## 🧭 Operative Runbooks

### Runbook: vollständigen lokalen Stack hochfahren
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Validierungs-Checkpoints:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- `http://127.0.0.1:5173/` öffnen und bestätigen, dass die UI `/api/config` laden kann.
- Optional: `/api/version` öffnen und prüfen, ob erwartete Backend-Metadaten zurückkommen.

### Runbook: Backend-only-Debugging
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: deterministischer Codegen-Smoke
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

Kern-API-Gruppen auf einen Blick:

| Kategorie | Endpoints |
| --- | --- |
| Health + Laufzeitinfo | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan-Modell | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action Registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline-Laufzeit | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + Logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| Workspace-Einstellungen | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Beispiele
### AAPS-Beispiel
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

Vollständige Beispiele:
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### Deterministische Runner-Generierung
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Deterministische Demo-Pipeline
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Danach die PWA-Steuerung Start/Pause/Resume/Stop nutzen und `/api/logs` prüfen.

### Import aus annotierter Shell
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 Entwicklungshinweise
- Das Backend basiert auf Tornado und ist auf lokale Dev-Ergonomie ausgelegt (inklusive permissivem CORS für localhost-Split-Ports).
- Storage ist PostgreSQL-first mit kompatiblem Verhalten in `backend/storage.py`.
- PWA-Block-Keys und Script-`STEP.block`-Werte sind absichtlich synchronisiert (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in-Actions sind readonly; vor dem Bearbeiten klonen.
- Die `update_readme`-Action ist aus Pfadsicherheitsgründen auf Workspace-README-Ziele unter `auto-apps/<workspace>/README.md` begrenzt.
- In manchen Docs/Skripten gibt es historische Pfad-/Namensreferenzen (`HeyCyan`, `LightMind`), geerbt aus der Projektentwicklung. Der kanonische aktuelle Repo-Pfad ist dieses Repository-Root.
- Das Root-Verzeichnis `i18n/` existiert. Sprach-READMEs werden dort für mehrsprachige Läufe erwartet.

### Arbeitsmodell und State-Dateien
- Runtime ist standardmäßig `./runtime`, außer `AUTOAPPDEV_RUNTIME_DIR` überschreibt dies.
- Self-Dev-Automationsstatus/-historie wird unter `references/selfdev/` geführt.
- README-Pipeline-Artefakte werden unter `.auto-readme-work/<timestamp>/` abgelegt.

### Test-Posten (aktuell)
- Das Repository enthält Smoke-Checks und deterministische Demo-Skripte.
- Eine vollständige top-level Test-Suite/CI-Manifest ist in den Root-Metadaten aktuell nicht definiert.
- Annahme: Verifikation ist derzeit primär skriptgetrieben (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, End-to-End-Checkliste).

## 🔐 Sicherheitshinweise
- Die `update_readme`-Action ist absichtlich auf Workspace-README-Ziele (`auto-apps/<workspace>/README.md`) begrenzt, inklusive Schutz gegen Path Traversal.
- Die Action-Registry-Validierung erzwingt normalisierte Action-Spec-Felder und begrenzte Werte für unterstützte Reasoning-Levels.
- Repository-Skripte setzen vertrauenswürdige lokale Ausführung voraus; prüfe Skriptinhalte vor Ausführung in geteilten oder produktionsnahen Umgebungen.
- `.env` kann sensible Werte enthalten (`DATABASE_URL`, API keys). `.env` nicht committen und außerhalb lokaler Entwicklung umgebungsspezifisches Secret-Management verwenden.

## 🔧 Troubleshooting

| Symptom | Was prüfen |
| --- | --- |
| `tmux not found` | `tmux` installieren oder Backend/PWA manuell starten. |
| Backend-Start scheitert wegen fehlender Env | `.env` gegen `.env.example` und `docs/env.md` prüfen. |
| Datenbankfehler (Verbindung/Auth/Schema) | `DATABASE_URL` prüfen; `conda run -n autoappdev python -m backend.apply_schema` erneut ausführen; optionaler Connectivity-Check: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA lädt, kann API aber nicht aufrufen | Sicherstellen, dass Backend auf erwartetem Host/Port lauscht; `pwa/config.local.js` durch erneutes Ausführen von `./scripts/run_autoappdev_tmux.sh` regenerieren. |
| Pipeline Start liefert invalid transition | Zuerst aktuellen Pipeline-Status prüfen; aus Zustand `stopped` starten. |
| Keine Log-Updates in der UI | Prüfen, ob `runtime/logs/pipeline.log` beschrieben wird; `/api/logs` und `/api/logs/tail` direkt verwenden, um UI- vs Backend-Problem zu isolieren. |
| LLM-Parse-Endpoint meldet disabled | `AUTOAPPDEV_ENABLE_LLM_PARSE=1` setzen und Backend neu starten. |
| `conda run -n autoappdev ...` schlägt fehl | `./scripts/setup_autoappdev_env.sh` erneut ausführen; prüfen, ob conda-env `autoappdev` existiert (`conda env list`). |
| Falsches API-Ziel im Frontend | Prüfen, ob `pwa/config.local.js` existiert und auf aktiven Backend-Host/Port zeigt. |

Für einen deterministischen manuellen Verifikationspfad siehe `docs/end-to-end-demo-checklist.md`.

## 🌐 README & i18n Workflow
- Die Root-README ist die kanonische Quelle der README-Automatisierungspipeline.
- Mehrsprachige Varianten werden unter `i18n/` erwartet.
- i18n-Verzeichnisstatus: ✅ in diesem Repository vorhanden.
- Aktueller Sprachsatz in diesem Repository:
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
- Die Sprach-Navigation muss als einzelne Zeile am Anfang jeder README-Variante bleiben (keine duplizierten Sprachleisten).
- Einstiegspunkt der README-Pipeline: `prompt_tools/auto-readme-pipeline.sh`.

### i18n-Generierungsvorgaben (strict)
- Bei Aktualisierungen der kanonischen README immer mehrsprachige Generierung ausführen.
- Sprachdateien einzeln und sequenziell generieren/aktualisieren, nicht in mehrdeutigen Bulk-Batches.
- Genau eine Sprachoptions-Navigationszeile am Anfang jeder Variante behalten.
- Sprachleisten innerhalb derselben Datei nicht duplizieren.
- Kanonische Befehls-Snippets, Links, API-Pfade und Badge-Intention über Übersetzungen hinweg erhalten.

Empfohlene Reihenfolge für die Einzelgenerierung:
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

Sprachabdeckungstabelle:

| Sprache | Datei |
| --- | --- |

## 📘 Readme Generation Context

- Pipeline-Durchlauf-Zeitstempel: `20260301_064935`
- Auslöser: `./README.md`
- Eingabe-User-Prompt: `probe prompt`
- Ziel: vollständigen, schön formatierten README-Entwurf mit erforderlichen Abschnitten und Support-Informationen erzeugen
- Eingabesnapshot verwendet:
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- Diese Datei wurde aus Repository-Inhalten generiert und als kanonischer Eingangs-Entwurf gespeichert.

## ❓ FAQ

### Ist PostgreSQL zwingend?
Bevorzugt und für den normalen Betrieb erwartet. Die Storage-Schicht enthält kompatibles Fallback-Verhalten, aber produktionsähnliche Nutzung sollte davon ausgehen, dass PostgreSQL über `DATABASE_URL` verfügbar ist.

### Warum sowohl `AUTOAPPDEV_PORT` als auch `PORT`?
`AUTOAPPDEV_PORT` ist projektspezifisch. `PORT` existiert als deployment-freundlicher Alias. Halte beide synchron, außer du überschreibst das Verhalten in deinem Startpfad bewusst.

### Wo starte ich, wenn ich nur die APIs prüfen möchte?
Backend-only starten (`conda run -n autoappdev python -m backend.app`) und dann `/api/health`, `/api/version`, `/api/config` sowie die Script/Action-Endpoints aus `docs/api-contracts.md` nutzen.

### Werden mehrsprachige READMEs automatisch erzeugt?
Ja. Das Repository enthält `prompt_tools/auto-readme-pipeline.sh`, und Sprachvarianten werden unter `i18n/` mit einer einzelnen Sprach-Navigationszeile am Dateianfang gepflegt.

## 🗺️ Roadmap
- Verbleibende Self-Dev-Tasks jenseits des aktuellen Status `51 / 55` abschließen.
- Workspace/Materials/Context-Tooling und stärkere Safe-Path-Verträge ausbauen.
- UX der Action-Palette und editierbare Action-Workflows weiter verbessern.
- Mehrsprachige README/UI-Unterstützung über `i18n/` und Laufzeit-Sprachumschaltung vertiefen.
- Smoke/Integration-Checks und CI-Abdeckung stärken (aktuell sind skriptgetriebene Smoke-Checks vorhanden; kein vollständiges CI-Manifest am Root dokumentiert).
- Determinismus von Parser/Import/Codegen rund um AAPS v1 und kanonische IR weiter härten.

## 🤝 Mitwirken
Beiträge sind über Issues und Pull Requests willkommen.

Empfohlener Workflow:
1. Fork erstellen und Feature-Branch anlegen.
2. Änderungen fokussiert und reproduzierbar halten.
3. Wo möglich deterministische Skripte/Tests bevorzugen.
4. Doku aktualisieren, wenn Verhalten/Verträge sich ändern (`docs/*`, API-Verträge, Beispiele).
5. PR mit Kontext, Validierungsschritten und Laufzeitannahmen eröffnen.

Repository-Remotes enthalten derzeit:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Zusätzliche Remotes können in lokalen Klonen vorhanden sein (Beispiel in diesem Workspace: `novel`).

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

Im Snapshot dieses Repositories wurde keine `LICENSE`-Datei im Root gefunden.

Annahmehinweis:
- Bis eine Lizenzdatei ergänzt wird, gelten Nutzungs-/Weitergabebedingungen als nicht spezifiziert und sollten mit dem Maintainer geklärt werden.
