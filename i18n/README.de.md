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

Wiederverwendbare Skripte + Leitfäden, um Apps Schritt für Schritt aus Screenshots/Markdown mit Codex als nicht-interaktivem Tool zu erstellen.

> 🎯 **Mission:** App-Entwicklungs-Pipelines deterministisch, fortsetzbar und artefaktgetrieben machen.
>
> 🧩 **Designprinzip:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🔗 Schnelle Navigation

| Bedarf | Gehe zu |
| --- | --- |
| Erster lokaler Start | [⚡ Quick Start](#-quick-start) |
| Umgebung und erforderliche Variablen | [⚙️ Konfiguration](#-konfiguration) |
| API-Überblick | [📡 API-Snapshot](#-api-snapshot) |
| Laufzeit-/Debug-Playbooks | [🧭 Operative Runbooks](#-operative-runbooks) |
| README-/i18n-Generierungsregeln | [🌐 README-&-i18n-workflow](#-readme--i18n-workflow) |
| Troubleshooting-Matrix | [🔧 Fehlerbehebung](#-fehlerbehebung) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev-Status (automatisch aktualisiert)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Dieser Abschnitt wird von `scripts/auto-autoappdev-development.sh` aktualisiert.
Inhalte zwischen den Markern nicht bearbeiten.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Inhaltsverzeichnis
- [🚀 Überblick](#-überblick)
- [🧭 Philosophie](#-philosophie)
- [✨ Features](#-features)
- [📌 Auf einen Blick](#-auf-einen-blick)
- [🏗️ Architektur](#-architektur)
- [📚 Inhalte](#-inhalte)
- [🗂️ Projektstruktur](#-projektstruktur)
- [✅ Voraussetzungen](#-voraussetzungen)
- [🧩 Kompatibilität & Annahmen](#-kompatibilität--annahmen)
- [🛠️ Installation](#-installation)
- [⚡ Quick Start](#-quick-start)
- [⚙️ Konfiguration](#-konfiguration)
- [▶️ Nutzung](#-nutzung)
- [🧭 Operative Runbooks](#-operative-runbooks)
- [📡 API-Snapshot](#-api-snapshot)
- [🧪 Beispiele](#-beispiele)
- [🧱 Entwicklungshinweise](#-entwicklungshinweise)
- [🔐 Sicherheitshinweise](#-sicherheitshinweise)
- [🔧 Fehlerbehebung](#-fehlerbehebung)
- [🌐 README & i18n Workflow](#-readme--i18n-workflow)
- [❓ FAQ](#-faq)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Mitwirken](#-mitwirken)
- [🙌 Support](#-support)
- [📄 Lizenz](#-lizenz)
- [❤️ Sponsor & Spenden](#️-sponsor--spenden)

## 🚀 Überblick
AutoAppDev ist ein Controller-Projekt für langlaufende, fortsetzbare App-Entwicklungs-Pipelines. Es kombiniert:

1. Eine Tornado-Backend-API mit PostgreSQL-gestützter Persistenz (plus lokalem JSON-Fallback-Verhalten im Storage-Code).
2. Eine Scratch-ähnliche statische PWA-Controller-UI.
3. Skripte und Dokumentation für Pipeline-Authoring, deterministische Code-Generierung, Self-Development-Loops und README-Automatisierung.

Das Projekt ist auf vorhersagbare Agent-Ausführung mit strikter Sequenzierung und artefaktorientierter Workflow-Historie optimiert.

### 🎨 Warum dieses Repo existiert

| Thema | Bedeutung in der Praxis |
| --- | --- |
| Determinismus | Kanonische Pipeline-IR + Parser/Import/Codegen-Workflows sind auf Wiederholbarkeit ausgelegt |
| Fortsetzbarkeit | Explizite Lifecycle-State-Machine (`start/pause/resume/stop`) für langlaufende Ausführungen |
| Betreibbarkeit | Laufzeit-Logs, Inbox/Outbox-Kanäle und skriptgetriebene Verifikationsschleifen |
| Documentation-first | Verträge/Spezifikationen/Beispiele liegen in `docs/`, mit automatisiertem mehrsprachigem README-Flow |

## 🧭 Philosophie
AutoAppDev behandelt Agents als Werkzeuge und hält Arbeit über einen strikten, fortsetzbaren Loop stabil:

1. Plan
2. Implement
3. Debug/verify (mit Timeouts)
4. Fix
5. Summarize + log
6. Commit + push

Die Controller-App soll dieselben Konzepte wie Scratch-ähnliche Blöcke/Aktionen abbilden (inklusive einer gemeinsamen `update_readme`-Aktion), damit jeder Workspace aktuell und reproduzierbar bleibt.

### 🔁 Ziel der Lifecycle-States

| Zustandsübergang | Operative Absicht |
| --- | --- |
| `start` | Eine Pipeline aus gestopptem/bereitem Zustand starten |
| `pause` | Langlaufende Ausführung sicher anhalten, ohne Kontext zu verlieren |
| `resume` | Von gespeichertem Laufzeitstatus/Artefakten fortsetzen |
| `stop` | Ausführung beenden und in einen nicht laufenden Zustand zurückkehren |

## ✨ Features
- Fortsetzbare Pipeline-Lifecycle-Steuerung: start, pause, resume, stop.
- Skriptbibliotheks-APIs für AAPS-Pipeline-Skripte (`.aaps`) und kanonische IR (`autoappdev_ir` v1).
- Deterministische Parser/Import-Pipeline:
  - Formatierte AAPS-Skripte parsen.
  - Annotierte Shell über `# AAPS:`-Kommentare importieren.
  - Optionaler Codex-unterstützter Parse-Fallback (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Action-Registry mit Built-ins + editierbaren/benutzerdefinierten Aktionen (clone/edit-Flow für schreibgeschützte Built-ins).
- Scratch-ähnliche PWA-Blöcke und zur Laufzeit geladene Action-Palette (`GET /api/actions`).
- Laufzeit-Nachrichtenkanäle:
  - Inbox (`/api/inbox`) für Operator -> Pipeline-Hinweise.
  - Outbox (`/api/outbox`) inklusive File-Queue-Ingestion aus `runtime/outbox`.
- Inkrementelles Log-Streaming aus Backend- und Pipeline-Logs (`/api/logs`, `/api/logs/tail`).
- Deterministischer Runner-Codegen aus kanonischer IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-Dev-Treiber für iterative Repository-Weiterentwicklung (`scripts/auto-autoappdev-development.sh`).
- README-Automatisierungs-Pipeline mit mehrsprachigem Generation-Scaffolding unter `i18n/`.

## 📌 Auf einen Blick

| Bereich | Details |
| --- | --- |
| Core Runtime | Tornado-Backend + statisches PWA-Frontend |
| Persistenz | PostgreSQL-first mit Kompatibilitätsverhalten in `backend/storage.py` |
| Pipeline-Modell | Kanonische IR (`autoappdev_ir` v1) und AAPS-Skriptformat |
| Kontrollfluss | Start / Pause / Resume / Stop Lifecycle |
| Dev-Modus | Fortsetzbarer Self-Dev-Loop + deterministische Skript/Codegen-Workflows |
| README/i18n | Automatisierte README-Pipeline mit `i18n/`-Scaffolding |

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
- Controller-APIs für Skripte, Aktionen, Plan, Pipeline-Lifecycle, Logs, Inbox/Outbox, Workspace-Konfiguration bereitstellen.
- Pipeline-Skript-Assets validieren und persistieren.
- Ausführungsstatus und Statusübergänge der Pipeline koordinieren.
- Deterministisches Fallback-Verhalten bereitstellen, wenn der DB-Pool nicht verfügbar ist.

### Frontend-Verantwortlichkeiten
- Scratch-ähnliche Block-UI und Pipeline-Editing-Flow rendern.
- Action-Palette dynamisch aus der Backend-Registry laden.
- Lifecycle-Steuerung ausführen sowie Status/Logs/Nachrichten überwachen.

## 📚 Inhalte
Referenzkarte für die am häufigsten genutzten Dokus, Skripte und Beispiele:

- `docs/auto-development-guide.md`: Zweisprachige (EN/ZH) Philosophie und Anforderungen für einen langlaufenden, fortsetzbaren Auto-Development-Agent.
- `docs/ORDERING_RATIONALE.md`: Beispielbegründung für die Reihenfolge screenshot-getriebener Schritte.
- `docs/controller-mvp-scope.md`: Controller-MVP-Umfang (Screens + minimale APIs).
- `docs/end-to-end-demo-checklist.md`: Deterministische manuelle End-to-End-Demo-Checkliste (Backend + PWA Happy Path).
- `docs/env.md`: Konventionen für Umgebungsvariablen (`.env`).
- `docs/api-contracts.md`: API-Request/Response-Verträge für den Controller.
- `docs/pipeline-formatted-script-spec.md`: Standard-Pipeline-Skriptformat (AAPS) und kanonisches IR-Schema (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Deterministischer Generator für ausführbare Bash-Pipeline-Runner aus kanonischer IR.
- `docs/common-actions.md`: Verträge/Spezifikationen gemeinsamer Aktionen (inklusive `update_readme`).
- `docs/workspace-layout.md`: Standard-Workspace-Ordner + Verträge (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Startet die AutoAppDev-App (Backend + PWA) in tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Startet den AutoAppDev-Self-Dev-Treiber in tmux.
- `scripts/app-auto-development.sh`: Linearer Pipeline-Treiber (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) mit Resume/State-Unterstützung.
- `scripts/generate_screenshot_docs.sh`: Screenshot -> Markdown-Beschreibungsgenerator (Codex-getrieben).
- `scripts/setup_autoappdev_env.sh`: Hauptskript zum Bootstrap der Conda-Umgebung für lokale Läufe.
- `scripts/setup_backend_env.sh`: Helper-Skript für die Backend-Umgebung.
- `examples/ralph-wiggum-example.sh`: Beispielhafter Codex-CLI-Automatisierungshelfer.

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
- OS mit `bash`.
- Python `3.11+`.
- Conda (`conda`) für die bereitgestellten Setup-Skripte.
- `tmux` für One-Command-Backend+PWA- oder Self-Dev-Sessions.
- PostgreSQL erreichbar über `DATABASE_URL`.
- Optional: `codex` CLI für Codex-gestützte Flows (self-dev, parse-llm fallback, auto-readme pipeline).

Kurze Anforderungsmatrix:

| Komponente | Erforderlich | Zweck |
| --- | --- | --- |
| `bash` | Ja | Skriptausführung |
| Python `3.11+` | Ja | Backend + Codegen-Tooling |
| Conda | Ja (empfohlener Flow) | Umgebungs-Bootstrap-Skripte |
| PostgreSQL | Ja (bevorzugter Modus) | Primäre Persistenz über `DATABASE_URL` |
| `tmux` | Empfohlen | Verwaltete Backend/PWA- und Self-Dev-Sessions |
| `codex` CLI | Optional | LLM-unterstütztes Parsing und README/Self-Dev-Automatisierung |

## 🧩 Kompatibilität & Annahmen

| Thema | Aktuelle Erwartung |
| --- | --- |
| Lokales OS | Linux/macOS-Shells sind das primäre Ziel (`bash`-Skripte) |
| Python-Runtime | `3.11` (verwaltet durch `scripts/setup_autoappdev_env.sh`) |
| Persistenzmodus | PostgreSQL ist bevorzugt und gilt als kanonisch |
| Fallback-Verhalten | `backend/storage.py` enthält JSON-Kompatibilitätsfallback für degradierte Szenarien |
| Netzwerkmodell | Lokale Split-Port-Entwicklung (Backend + statische PWA) |
| Agent-Tooling | `codex` CLI ist optional, außer bei LLM-unterstütztem Parsing oder Self-Dev-Automatisierung |

In diesem README verwendete Annahmen:
- Du führst Befehle aus dem Repository-Root aus, sofern nicht anders angegeben.
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

### 5) Optional: Datenbank-Smoketest
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
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

Smoketest mit einem Befehl:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Quick Endpoint Map:

| Oberfläche | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health Endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Konfiguration
Primäre Datei: `.env` (siehe `docs/env.md` und `.env.example`).

### Wichtige Variablen

| Variable | Zweck |
| --- | --- |
| `SECRET_KEY` | Konventionsgemäß erforderlich |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Backend-Bind-Settings |
| `DATABASE_URL` | PostgreSQL-DSN (bevorzugt) |
| `AUTOAPPDEV_RUNTIME_DIR` | Runtime-Verzeichnis überschreiben (Standard `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Standardziel für Pipeline-Lauf |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Aktiviert `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Codex-Standards für Aktionen/Endpoints |
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
| Nur Backend starten | `conda run -n autoappdev python -m backend.app` | Verwendet `.env`-Bind + DB-Settings |
| Nur statischen PWA-Server starten | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Nützlich für reine Frontend-Checks |
| Self-Dev-Treiber in tmux starten | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Fortsetzbarer Self-Development-Loop |

### Häufige Skriptoptionen
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Skripte parsen und speichern
- AAPS per API parsen: `POST /api/scripts/parse`
- Annotierte Shell importieren: `POST /api/scripts/import-shell`
- Optionales LLM-Parsing: `POST /api/scripts/parse-llm` (erfordert `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

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

Siehe `docs/api-contracts.md` für Request/Response-Formen.

## 🧭 Operative Runbooks

### Runbook: vollständigen lokalen Stack starten
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Validierungs-Checkpoints:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- `http://127.0.0.1:5173/` öffnen und bestätigen, dass die UI `/api/config` laden kann.
- Optional: `/api/version` öffnen und prüfen, ob erwartete Backend-Metadaten zurückgegeben werden.

### Runbook: nur-Backend-Debugging
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: deterministischer Codegen-Smoketest
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

## 📡 API-Snapshot

Wichtige API-Gruppen auf einen Blick:

| Kategorie | Endpoints |
| --- | --- |
| Health + Laufzeitinfos | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan-Modell | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action-Registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline-Runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + Logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
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
Dann die PWA-Controls Start/Pause/Resume/Stop verwenden und `/api/logs` prüfen.

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
- Storage ist PostgreSQL-first mit Kompatibilitätsverhalten in `backend/storage.py`.
- PWA-Block-Keys und Skript-`STEP.block`-Werte sind absichtlich ausgerichtet (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in-Aktionen sind schreibgeschützt; vor dem Bearbeiten klonen.
- `update_readme`-Aktion ist aus Pfadsicherheitsgründen auf Workspace-README-Ziele unter `auto-apps/<workspace>/README.md` beschränkt.
- Es gibt historische Pfad-/Namensreferenzen in einigen Dokus/Skripten (`HeyCyan`, `LightMind`), geerbt aus der Projektevolution. Der aktuell kanonische Repo-Pfad ist der Root dieses Repositories.
- Das Root-`i18n/`-Verzeichnis existiert. Mehrsprachige README-Dateien werden dort bei multilingualen Läufen erwartet.

### Arbeitsmodell und Statusdateien
- Runtime ist standardmäßig `./runtime`, sofern nicht durch `AUTOAPPDEV_RUNTIME_DIR` überschrieben.
- Self-Dev-Automatisierungsstatus/-Historie wird unter `references/selfdev/` verfolgt.
- README-Pipeline-Artefakte werden unter `.auto-readme-work/<timestamp>/` gespeichert.

### Teststatus (aktuell)
- Das Repository enthält Smoketests und deterministische Demo-Skripte.
- Eine vollständige top-level automatisierte Test-Suite/CI-Manifest ist aktuell nicht in den Root-Metadaten definiert.
- Annahme: Validierung ist vorerst primär skriptgetrieben (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, End-to-End-Checkliste).

## 🔐 Sicherheitshinweise
- Die `update_readme`-Aktion ist absichtlich auf Workspace-README-Ziele (`auto-apps/<workspace>/README.md`) begrenzt und durch Path-Traversal-Schutz abgesichert.
- Die Action-Registry-Validierung erzwingt normalisierte Action-Spec-Felder und begrenzte Werte für unterstützte Reasoning-Levels.
- Repository-Skripte gehen von vertrauenswürdiger lokaler Ausführung aus; Skriptinhalte vor Ausführung in geteilten oder produktionsnahen Umgebungen prüfen.
- `.env` kann sensible Werte enthalten (`DATABASE_URL`, API keys). `.env` nicht committen und außerhalb der lokalen Entwicklung umgebungsspezifisches Secret-Management verwenden.

## 🔧 Fehlerbehebung

| Symptom | Zu prüfen |
| --- | --- |
| `tmux not found` | `tmux` installieren oder Backend/PWA manuell starten. |
| Backend-Start schlägt wegen fehlender Env fehl | `.env` gegen `.env.example` und `docs/env.md` prüfen. |
| Datenbankfehler (Verbindung/Auth/Schema) | `DATABASE_URL` prüfen; `conda run -n autoappdev python -m backend.apply_schema` erneut ausführen; optionaler Connectivity-Check: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA lädt, kann aber API nicht aufrufen | Sicherstellen, dass Backend auf erwartetem Host/Port lauscht; `pwa/config.local.js` neu erzeugen durch erneutes Ausführen von `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start gibt invalid transition zurück | Zuerst aktuellen Pipeline-Status prüfen; aus `stopped` starten. |
| Keine Log-Updates in der UI | Prüfen, ob `runtime/logs/pipeline.log` geschrieben wird; `/api/logs` und `/api/logs/tail` direkt nutzen, um UI- vs Backend-Probleme zu isolieren. |
| LLM-Parse-Endpoint ist deaktiviert | `AUTOAPPDEV_ENABLE_LLM_PARSE=1` setzen und Backend neu starten. |
| `conda run -n autoappdev ...` schlägt fehl | `./scripts/setup_autoappdev_env.sh` erneut ausführen; prüfen, ob die conda-Umgebung `autoappdev` existiert (`conda env list`). |
| Falsches API-Ziel im Frontend | Prüfen, ob `pwa/config.local.js` existiert und auf den aktiven Backend-Host/Port zeigt. |

Für einen deterministischen manuellen Verifikationspfad siehe `docs/end-to-end-demo-checklist.md`.

## 🌐 README & i18n Workflow
- Root-README ist die kanonische Quelle für die README-Automatisierungs-Pipeline.
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
- Sprach-Navigation sollte als einzelne Zeile am Anfang jeder README-Variante bleiben (keine doppelten Sprachleisten).
- README-Pipeline-Entrypoint: `prompt_tools/auto-readme-pipeline.sh`.

### i18n-Generierungsregeln (strict)
- Beim Aktualisieren kanonischer README-Inhalte immer die mehrsprachige Generierung verarbeiten.
- Sprachdateien nacheinander (sequenziell) erzeugen/aktualisieren, nicht in uneindeutigen Batch-Läufen.
- Genau eine Language-Options-Navigationzeile am Anfang jeder Variante behalten.
- Keine Duplikate der Sprachleiste innerhalb derselben Datei.
- Kanonische Command-Snippets, Links, API-Pfade und Badge-Absicht in Übersetzungen beibehalten.

Empfohlene Reihenfolge für die schrittweise Generierung:
1. `README.md` (kanonische englische Quelle)
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

Sprachabdeckungstabelle:

| Sprache | Datei |
| --- | --- |

## ❓ FAQ

### Ist PostgreSQL verpflichtend?
Bevorzugt und für den Normalbetrieb erwartet. Die Storage-Schicht enthält Fallback-Kompatibilitätsverhalten, aber produktionsnahe Nutzung sollte davon ausgehen, dass PostgreSQL über `DATABASE_URL` verfügbar ist.

### Warum sowohl `AUTOAPPDEV_PORT` als auch `PORT`?
`AUTOAPPDEV_PORT` ist projektspezifisch. `PORT` existiert als deployment-freundlicher Alias. Beide synchron halten, außer du überschreibst das Verhalten bewusst im Launch-Pfad.

### Wo anfangen, wenn ich nur die APIs prüfen will?
Nur Backend ausführen (`conda run -n autoappdev python -m backend.app`) und `/api/health`, `/api/version`, `/api/config`, dann die in `docs/api-contracts.md` gelisteten Script-/Action-Endpoints nutzen.

### Werden mehrsprachige READMEs automatisch generiert?
Ja. Das Repository enthält `prompt_tools/auto-readme-pipeline.sh`, und Sprachvarianten werden unter `i18n/` mit einer Sprach-Navigationzeile am Anfang jeder Variante gepflegt.

## 🗺️ Roadmap
- Verbleibende Self-Dev-Tasks über den aktuellen Status `51 / 55` hinaus abschließen.
- Workspace/Materials/Context-Tooling und stärkere Safe-Path-Verträge ausbauen.
- UX der Action-Palette und editierbare Action-Workflows weiter verbessern.
- Mehrsprachige README/UI-Unterstützung in `i18n/` und Runtime-Sprachumschaltung vertiefen.
- Smoke/Integrations-Checks und CI-Abdeckung stärken (aktuell sind skriptgetriebene Smoketests vorhanden; kein vollständiges CI-Manifest im Root dokumentiert).
- Parser/Import/Codegen-Determinismus rund um AAPS v1 und kanonische IR weiter härten.

## 🤝 Mitwirken
Beiträge sind über Issues und Pull Requests willkommen.

Empfohlener Workflow:
1. Fork erstellen und einen Feature-Branch anlegen.
2. Änderungen fokussiert und reproduzierbar halten.
3. Nach Möglichkeit deterministische Skripte/Tests bevorzugen.
4. Doku aktualisieren, wenn sich Verhalten/Verträge ändern (`docs/*`, API-Verträge, Beispiele).
5. PR mit Kontext, Validierungsschritten und Laufzeitannahmen eröffnen.

Repository-Remotes enthalten aktuell:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Zusätzliche Remotes können in lokalen Klonen vorhanden sein (Beispiel in diesem Workspace gefunden: `novel`).

## 🙌 Support
- GitHub-Issues und Pull Requests für Bugreports und Feature-Vorschläge.
- Sponsor-/Spendenlinks sind unten aufgeführt.

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 Lizenz
In diesem Repository-Snapshot wurde keine `LICENSE`-Datei im Root erkannt.

Hinweis zur Annahme:
- Bis eine Lizenzdatei hinzugefügt ist, Nutzungs-/Weitergabebedingungen als nicht spezifiziert behandeln und beim Maintainer bestätigen.

## ❤️ Sponsor & Spenden
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400

Wenn dieses Projekt deinen Workflow unterstützt, fördert Sponsoring direkt die Weiterführung von Self-Dev-Tasks, Doku-Qualität und Tooling-Härtung.
