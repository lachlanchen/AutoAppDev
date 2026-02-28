[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/figs/banner.png" alt="LazyingArt-Banner" />
</p>

# AutoAppDev

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Backend](https://img.shields.io/badge/Backend-Tornado-222222)
![Frontend](https://img.shields.io/badge/Frontend-PWA-0A7EA4)
![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Self--Dev-51%2F55%20tasks%20done-2E8B57)
![i18n](https://img.shields.io/badge/i18n-11%20languages-1f6feb)

Wiederverwendbare Skripte + Leitfäden, um Apps Schritt für Schritt aus Screenshots/Markdown zu erstellen, mit Codex als nicht-interaktivem Tool.

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev-Status (automatisch aktualisiert)

- Aktualisiert: 2026-02-16T00:27:20Z
- Phase-Commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Fortschritt: 51 / 55 Aufgaben erledigt
- Codex-Sitzung: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophie: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, fortsetzbar)

Dieser Abschnitt wird von `scripts/auto-autoappdev-development.sh` aktualisiert.
Den Inhalt zwischen den Markern nicht manuell bearbeiten.

<!-- AUTOAPPDEV:STATUS:END -->

## 🚀 Überblick
AutoAppDev ist ein Controller-Projekt für lang laufende, fortsetzbare App-Entwicklungspipelines. Es kombiniert:

1. Eine Tornado-Backend-API mit PostgreSQL-gestützter Persistenz (plus lokalem JSON-Fallback-Verhalten im Storage-Code).
2. Eine Scratch-ähnliche statische PWA-Controller-UI.
3. Skripte und Doku für Pipeline-Authoring, deterministische Code-Generierung, Self-Development-Loops und README-Automatisierung.

### Auf einen Blick

| Bereich | Details |
| --- | --- |
| Core Runtime | Tornado-Backend + statisches PWA-Frontend |
| Persistenz | PostgreSQL-first mit Kompatibilitätsverhalten in `backend/storage.py` |
| Pipeline-Modell | Kanonisches IR (`autoappdev_ir` v1) und AAPS-Skriptformat |
| Steuerfluss | Start / Pause / Resume / Stop-Lebenszyklus |
| Dev-Modus | Fortsetzbarer Self-Dev-Loop + deterministische Script/Codegen-Workflows |
| README/i18n | Automatisierte README-Pipeline mit `i18n/`-Scaffolding |

## 🧭 Philosophie
AutoAppDev behandelt Agenten als Werkzeuge und hält die Arbeit über einen strikten, fortsetzbaren Loop stabil:
1. Plan
2. Implement
3. Debug/Verify (mit Timeouts)
4. Fix
5. Zusammenfassen + protokollieren
6. Commit + push

Die Controller-App soll dieselben Konzepte als Scratch-ähnliche Blöcke/Aktionen abbilden (einschließlich einer gemeinsamen `update_readme`-Aktion), damit jeder Workspace aktuell und reproduzierbar bleibt.

## ✨ Funktionen
- Fortsetzbare Pipeline-Lebenszyklussteuerung: start, pause, resume, stop.
- Script-Library-APIs für AAPS-Pipeline-Skripte (`.aaps`) und kanonisches IR (`autoappdev_ir` v1).
- Deterministische Parser/Import-Pipeline:
  - Formatierte AAPS-Skripte parsen.
  - Annotierte Shell über `# AAPS:`-Kommentare importieren.
  - Optionaler Codex-gestützter Parse-Fallback (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Aktions-Registry mit Built-ins + editierbaren/benutzerdefinierten Aktionen (Clone/Edit-Flow für schreibgeschützte Built-ins).
- Scratch-ähnliche PWA-Blöcke und zur Laufzeit geladene Action-Palette (`GET /api/actions`).
- Runtime-Messaging-Kanäle:
  - Inbox (`/api/inbox`) für Operator -> Pipeline-Hinweise.
  - Outbox (`/api/outbox`) inklusive File-Queue-Ingestion aus `runtime/outbox`.
- Inkrementelles Log-Streaming aus Backend- und Pipeline-Logs (`/api/logs`, `/api/logs/tail`).
- Deterministische Runner-Codegen aus kanonischem IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-Dev-Treiber für iterative Repository-Weiterentwicklung (`scripts/auto-autoappdev-development.sh`).
- README-Automatisierungspipeline mit mehrsprachigem Generierungs-Scaffolding unter `i18n/`.

## 📚 Inhalt
- `docs/auto-development-guide.md`: Zweisprachige (EN/ZH) Philosophie und Anforderungen für einen lang laufenden, fortsetzbaren Auto-Development-Agenten.
- `docs/ORDERING_RATIONALE.md`: Beispielbegründung für die Reihenfolge screenshot-getriebener Schritte.
- `docs/controller-mvp-scope.md`: Controller-MVP-Umfang (Screens + minimale APIs).
- `docs/end-to-end-demo-checklist.md`: Deterministische manuelle End-to-End-Demo-Checkliste (Backend + PWA Happy Path).
- `docs/env.md`: Konventionen für Umgebungsvariablen (`.env`).
- `docs/api-contracts.md`: API-Request/Response-Verträge für den Controller.
- `docs/pipeline-formatted-script-spec.md`: Standard-Pipeline-Skriptformat (AAPS) und kanonisches IR-Schema (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Deterministischer Generator für ausführbare Bash-Pipeline-Runner aus kanonischem IR.
- `docs/common-actions.md`: Gemeinsame Action-Verträge/Spezifikationen (inkl. `update_readme`).
- `docs/workspace-layout.md`: Standard-Workspace-Ordner + Verträge (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: Startet die AutoAppDev-App (Backend + PWA) in tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Startet den AutoAppDev-Self-Dev-Treiber in tmux.
- `scripts/app-auto-development.sh`: Der lineare Pipeline-Treiber (plan -> backend -> PWA -> Android -> iOS -> review -> summary) mit Resume/State-Unterstützung.
- `scripts/generate_screenshot_docs.sh`: Generator für Screenshot -> Markdown-Beschreibung (Codex-gesteuert).
- `scripts/setup_backend_env.sh`: Bootstrap für die Backend-conda-Umgebung bei lokalen Läufen.
- `examples/ralph-wiggum-example.sh`: Beispielhafter Automatisierungshelfer für die Codex CLI.

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

## ✅ Voraussetzungen
- Betriebssystem mit `bash`.
- Python `3.11+`.
- Conda (`conda`) für die bereitgestellten Setup-Skripte.
- `tmux` für One-Command-Backend+PWA- oder Self-Dev-Sessions.
- PostgreSQL, erreichbar über `DATABASE_URL`.
- Optional: `codex` CLI für Codex-gestützte Flows (self-dev, parse-llm fallback, auto-readme pipeline).

## 🛠️ Installation
### 1) Repository klonen und betreten
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

## ⚙️ Konfiguration
Primäre Datei: `.env` (siehe `docs/env.md` und `.env.example`).

### Wichtige Variablen

| Variable | Zweck |
| --- | --- |
| `SECRET_KEY` | Konventionsgemäß erforderlich |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Backend-Bind-Einstellungen |
| `DATABASE_URL` | PostgreSQL-DSN (bevorzugt) |
| `AUTOAPPDEV_RUNTIME_DIR` | Runtime-Verzeichnis überschreiben (Standard `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Standardziel für Pipeline-Läufe |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Aktiviert `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Codex-Standards für Actions/Endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Für künftige Integrationen reserviert |

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
### Backend + PWA zusammen starten (empfohlen)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
Standardwerte:
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### Nur Backend starten
```bash
conda run -n autoappdev python -m backend.app
```

### Nur PWA-Static-Server starten
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### Self-Dev-Treiber in tmux starten
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### Skripte parsen und speichern
- AAPS via API parsen: `POST /api/scripts/parse`
- Annotierte Shell importieren: `POST /api/scripts/import-shell`
- Optionaler LLM-Parse: `POST /api/scripts/parse-llm` (erfordert `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

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

Siehe `docs/api-contracts.md` für Request/Response-Formate.

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
Nutze dann in der PWA die Start/Pause/Resume/Stop-Steuerung und prüfe `/api/logs`.

## 🧱 Hinweise zur Entwicklung
- Das Backend basiert auf Tornado und ist auf lokale Dev-Ergonomie ausgelegt (inklusive permissivem CORS für localhost Split-Ports).
- Storage ist PostgreSQL-first mit Kompatibilitätsverhalten in `backend/storage.py`.
- PWA-Block-Keys und Script-`STEP.block`-Werte sind absichtlich aufeinander abgestimmt (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in-Aktionen sind schreibgeschützt; vor der Bearbeitung klonen.
- Die `update_readme`-Aktion ist per Path-Safety auf Workspace-README-Ziele unter `auto-apps/<workspace>/README.md` beschränkt.
- In einigen Docs/Skripten gibt es historische Pfad-/Namensreferenzen (`HeyCyan`, `LightMind`), geerbt aus der Projektentwicklung. Der kanonische Pfad ist aktuell das Root dieses Repos.
- Das Root-Verzeichnis `i18n/` existiert. Mehrsprachige README-Dateien werden dort bei multilingualen Läufen erwartet.

## 🩺 Fehlerbehebung
- `tmux not found`:
  - `tmux` installieren oder Backend/PWA manuell starten.
- Backend startet wegen fehlender Env nicht:
  - `.env` gegen `.env.example` und `docs/env.md` prüfen.
- Datenbankfehler (Verbindung/Auth/Schema):
  - `DATABASE_URL` prüfen.
  - `conda run -n autoappdev python -m backend.apply_schema` erneut ausführen.
  - Optionaler Konnektivitätscheck: `conda run -n autoappdev python -m backend.db_smoketest`.
- PWA lädt, kann aber API nicht aufrufen:
  - Prüfen, ob Backend auf erwartetem Host/Port lauscht.
  - `pwa/config.local.js` neu generieren, indem `./scripts/run_autoappdev_tmux.sh` erneut ausgeführt wird.
- Pipeline-Start liefert invalid transition:
  - Erst den aktuellen Pipeline-Status prüfen; Start aus `stopped`.
- Keine Log-Updates in der UI:
  - Prüfen, ob `runtime/logs/pipeline.log` geschrieben wird.
  - `/api/logs` und `/api/logs/tail` direkt verwenden, um UI- vs. Backend-Probleme zu isolieren.
- LLM-Parse-Endpoint meldet disabled:
  - `AUTOAPPDEV_ENABLE_LLM_PARSE=1` setzen und Backend neu starten.

Für einen deterministischen manuellen Verifikationspfad: `docs/end-to-end-demo-checklist.md`.

## 🗺️ Roadmap
- Verbleibende Self-Dev-Aufgaben über den aktuellen Status `51 / 55` hinaus abschließen.
- Workspace/Materials/Context-Tooling erweitern und Safe-Path-Verträge stärken.
- UX der Action-Palette und editierbare Action-Workflows weiter verbessern.
- Mehrsprachige README-/UI-Unterstützung über `i18n/` und Runtime-Sprachumschaltung ausbauen.
- Smoke-/Integrationschecks und CI-Abdeckung stärken (aktuell sind skriptgetriebene Smoke-Checks vorhanden; kein vollständiges CI-Manifest im Root dokumentiert).

## 🤝 Mitwirken
Beiträge sind über Issues und Pull Requests willkommen.

Empfohlener Workflow:
1. Fork erstellen und einen Feature-Branch anlegen.
2. Änderungen fokussiert und reproduzierbar halten.
3. Wenn möglich deterministische Skripte/Tests bevorzugen.
4. Docs aktualisieren, wenn sich Verhalten/Verträge ändern (`docs/*`, API-Verträge, Beispiele).
5. PR mit Kontext, Validierungsschritten und eventuellen Runtime-Annahmen öffnen.

Repository-Remotes enthalten aktuell:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- In lokalen Klonen kann zusätzlich ein weiteres Remote für verwandte Repos vorhanden sein.

## 📄 Lizenz
Im aktuellen Repository-Snapshot wurde keine `LICENSE`-Datei im Root gefunden.

Hinweis zur Annahme:
- Bis eine Lizenzdatei hinzugefügt wird, Nutzungs-/Weitergabebedingungen als nicht spezifiziert behandeln und beim Maintainer bestätigen.

## ❤️ Sponsor & Spenden

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Spenden: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
