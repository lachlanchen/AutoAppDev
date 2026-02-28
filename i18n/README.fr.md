[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/figs/banner.png" alt="Bannière LazyingArt" />
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

Scripts réutilisables + guides pour créer des applications étape par étape à partir de captures d’écran/markdown, avec Codex utilisé comme outil non interactif.

> 🎯 **Mission :** rendre les pipelines de développement d’applications déterministes, reprenables et pilotés par artefacts.
>
> 🧩 **Principe de conception :** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🔗 Navigation rapide

| Besoin | Aller à |
| --- | --- |
| Premier lancement local | [⚡ Démarrage rapide](#-démarrage-rapide) |
| Environnement et variables requises | [⚙️ Configuration](#-configuration) |
| Surface API | [📡 Aperçu API](#-aperçu-api) |
| Runbooks runtime/debug | [🧭 Runbooks opérationnels](#-runbooks-opérationnels) |
| Règles de génération README/i18n | [🌐 Workflow README & i18n](#-workflow-readme--i18n) |
| Matrice de dépannage | [🔧 Dépannage](#-dépannage) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Statut Self-Dev (Mise à jour automatique)

- Mis à jour : 2026-02-16T00:27:20Z
- Commit de phase : `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progression : 51 / 55 tâches terminées
- Session Codex : `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophie : Plan -> Work -> Verify -> Summary -> Commit/Push (linéaire, reprenable)

Cette section est mise à jour par `scripts/auto-autoappdev-development.sh`.
Ne modifiez pas le contenu entre les marqueurs.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Table des matières
- [🚀 Vue d’ensemble](#-vue-densemble)
- [🧭 Philosophie](#-philosophie)
- [✨ Fonctionnalités](#-fonctionnalités)
- [📌 En bref](#-en-bref)
- [🏗️ Architecture](#-architecture)
- [📚 Contenu](#-contenu)
- [🗂️ Structure du projet](#-structure-du-projet)
- [✅ Prérequis](#-prérequis)
- [🧩 Compatibilité et hypothèses](#-compatibilité-et-hypothèses)
- [🛠️ Installation](#-installation)
- [⚡ Démarrage rapide](#-démarrage-rapide)
- [⚙️ Configuration](#-configuration)
- [▶️ Utilisation](#-utilisation)
- [🧭 Runbooks opérationnels](#-runbooks-opérationnels)
- [📡 Aperçu API](#-aperçu-api)
- [🧪 Exemples](#-exemples)
- [🧱 Notes de développement](#-notes-de-développement)
- [🔐 Notes de sécurité](#-notes-de-sécurité)
- [🔧 Dépannage](#-dépannage)
- [🌐 Workflow README & i18n](#-workflow-readme--i18n)
- [❓ FAQ](#-faq)
- [🗺️ Feuille de route](#-feuille-de-route)
- [🤝 Contribuer](#-contribuer)
- [🙌 Support](#-support)
- [📄 Licence](#-licence)
- [❤️ Sponsor et dons](#-sponsor-et-dons)

## 🚀 Vue d’ensemble
AutoAppDev est un projet contrôleur pour des pipelines de développement d’applications longue durée et reprenables. Il combine :

1. Une API backend Tornado avec persistance adossée à PostgreSQL (avec aussi un comportement de repli JSON local dans le code de stockage).
2. Une interface contrôleur PWA statique de type Scratch.
3. Des scripts et de la documentation pour l’écriture de pipelines, la génération de code déterministe, les boucles d’auto-développement et l’automatisation du README.

Le projet est optimisé pour une exécution d’agent prévisible, avec un séquencement strict et un historique de workflow orienté artefacts.

### 🎨 Pourquoi ce dépôt existe

| Thème | Signification en pratique |
| --- | --- |
| Déterminisme | IR canonique du pipeline + workflows parser/import/codegen conçus pour la répétabilité |
| Reprise | Machine à états explicite du cycle de vie (`start/pause/resume/stop`) pour les exécutions longues |
| Exploitabilité | Logs runtime, canaux inbox/outbox et boucles de vérification pilotées par scripts |
| Documentation d’abord | Contrats/spécifications/exemples dans `docs/`, avec flux README multilingue automatisé |

## 🧭 Philosophie
AutoAppDev traite les agents comme des outils et maintient la stabilité du travail via une boucle stricte et reprenable :

1. Plan
2. Implement
3. Debug/verify (avec timeouts)
4. Fix
5. Summarize + log
6. Commit + push

L’application contrôleur vise à incarner les mêmes concepts que les blocs/actions de type Scratch (dont l’action commune `update_readme`) afin que chaque espace de travail reste à jour et reproductible.

### 🔁 Intention des états du cycle de vie

| Transition d’état | Intention opérationnelle |
| --- | --- |
| `start` | Démarrer un pipeline depuis l’état arrêté/prêt |
| `pause` | Mettre en pause en sécurité une exécution longue sans perdre le contexte |
| `resume` | Reprendre depuis l’état/les artefacts runtime sauvegardés |
| `stop` | Terminer l’exécution et revenir à un état non actif |

## ✨ Fonctionnalités
- Contrôle reprenable du cycle de vie des pipelines : start, pause, resume, stop.
- APIs de bibliothèque de scripts pour les scripts pipeline AAPS (`.aaps`) et l’IR canonique (`autoappdev_ir` v1).
- Pipeline parser/import déterministe :
  - Analyse de scripts AAPS formatés.
  - Import de shell annoté via les commentaires `# AAPS:`.
  - Repli d’analyse assistée par Codex en option (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Registre d’actions avec actions intégrées + actions modifiables/personnalisées (flux clone/edit pour les actions intégrées en lecture seule).
- Blocs PWA de type Scratch et palette d’actions chargée à l’exécution (`GET /api/actions`).
- Canaux de messagerie runtime :
  - Inbox (`/api/inbox`) pour les indications opérateur -> pipeline.
  - Outbox (`/api/outbox`) incluant l’ingestion de file de fichiers depuis `runtime/outbox`.
- Streaming incrémental des logs backend et pipeline (`/api/logs`, `/api/logs/tail`).
- Génération déterministe du runner à partir de l’IR canonique (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev pour l’évolution itérative du dépôt (`scripts/auto-autoappdev-development.sh`).
- Pipeline d’automatisation du README avec ossature de génération multilingue sous `i18n/`.

## 📌 En bref

| Zone | Détails |
| --- | --- |
| Runtime cœur | Backend Tornado + frontend PWA statique |
| Persistance | PostgreSQL prioritaire avec comportement de compatibilité dans `backend/storage.py` |
| Modèle pipeline | IR canonique (`autoappdev_ir` v1) et format de script AAPS |
| Flux de contrôle | Cycle Start / Pause / Resume / Stop |
| Mode dev | Boucle self-dev reprenable + workflows déterministes script/codegen |
| README/i18n | Pipeline README automatisé avec structure `i18n/` |

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

### Responsabilités du backend
- Exposer les APIs contrôleur pour les scripts, actions, plan, cycle de vie pipeline, logs, inbox/outbox, config workspace.
- Valider et persister les artefacts de script pipeline.
- Coordonner l’état d’exécution du pipeline et les transitions de statut.
- Fournir un comportement de repli déterministe quand le pool DB est indisponible.

### Responsabilités du frontend
- Rendre l’UI de blocs de type Scratch et le flux d’édition de pipeline.
- Charger dynamiquement la palette d’actions depuis le registre backend.
- Piloter les contrôles de cycle de vie et surveiller statut/logs/messages.

## 📚 Contenu
Carte de référence des docs, scripts et exemples les plus utilisés :

- `docs/auto-development-guide.md` : Philosophie et exigences bilingues (EN/ZH) pour un agent d’auto-développement longue durée et reprenable.
- `docs/ORDERING_RATIONALE.md` : Exemple de justification pour l’ordonnancement d’étapes pilotées par captures d’écran.
- `docs/controller-mvp-scope.md` : Périmètre MVP du contrôleur (écrans + APIs minimales).
- `docs/end-to-end-demo-checklist.md` : Checklist manuelle déterministe de démonstration end-to-end (backend + happy path PWA).
- `docs/env.md` : Conventions des variables d’environnement (`.env`).
- `docs/api-contracts.md` : Contrats request/response API du contrôleur.
- `docs/pipeline-formatted-script-spec.md` : Format standard de script pipeline (AAPS) et schéma IR canonique (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md` : Générateur déterministe de runners bash exécutables à partir de l’IR canonique.
- `docs/common-actions.md` : Contrats/spécifications des actions communes (inclut `update_readme`).
- `docs/workspace-layout.md` : Dossiers workspace standard + contrats (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh` : Démarre l’application AutoAppDev (backend + PWA) dans tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh` : Démarre le driver self-dev AutoAppDev dans tmux.
- `scripts/app-auto-development.sh` : Driver de pipeline linéaire (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) avec support reprise/état.
- `scripts/generate_screenshot_docs.sh` : Générateur de descriptions markdown à partir de captures d’écran (piloté par Codex).
- `scripts/setup_autoappdev_env.sh` : Script principal d’amorçage d’environnement conda pour exécutions locales.
- `scripts/setup_backend_env.sh` : Script utilitaire d’environnement backend.
- `examples/ralph-wiggum-example.sh` : Exemple d’utilitaire d’automatisation Codex CLI.

## 🗂️ Structure du projet
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

## ✅ Prérequis
- OS avec `bash`.
- Python `3.11+`.
- Conda (`conda`) pour les scripts de configuration fournis.
- `tmux` pour des sessions backend+PWA ou self-dev en une commande.
- PostgreSQL joignable via `DATABASE_URL`.
- Optionnel : CLI `codex` pour les flux pilotés par Codex (self-dev, repli parse-llm, pipeline auto-readme).

Matrice rapide des exigences :

| Composant | Requis | But |
| --- | --- | --- |
| `bash` | Oui | Exécution de scripts |
| Python `3.11+` | Oui | Backend + outillage codegen |
| Conda | Oui (flux recommandé) | Scripts d’amorçage d’environnement |
| PostgreSQL | Oui (mode préféré) | Persistance primaire via `DATABASE_URL` |
| `tmux` | Recommandé | Sessions backend/PWA et self-dev gérées |
| `codex` CLI | Optionnel | Analyse assistée LLM et automatisation README/self-dev |

## 🧩 Compatibilité et hypothèses

| Sujet | Attente actuelle |
| --- | --- |
| OS local | Les shells Linux/macOS sont la cible principale (scripts `bash`) |
| Runtime Python | `3.11` (géré par `scripts/setup_autoappdev_env.sh`) |
| Mode de persistance | PostgreSQL est préféré et considéré comme canonique |
| Comportement de repli | `backend/storage.py` inclut un repli de compatibilité JSON pour les scénarios dégradés |
| Modèle réseau | Développement localhost à ports séparés (backend + PWA statique) |
| Outils agent | Le CLI `codex` est optionnel sauf pour l’analyse assistée LLM ou l’automatisation self-dev |

Hypothèses utilisées dans ce README :
- Vous exécutez les commandes depuis la racine du dépôt, sauf indication contraire.
- `.env` est configuré avant le démarrage des services backend.
- `conda` et `tmux` sont disponibles pour les workflows recommandés en une commande.

## 🛠️ Installation
### 1) Cloner et entrer dans le dépôt
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Configurer l’environnement
```bash
cp .env.example .env
```
Éditez `.env` et définissez au minimum :
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` et `AUTOAPPDEV_PORT` (ou `PORT`)

### 3) Créer/mettre à jour l’environnement backend
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Appliquer le schéma de base de données
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Optionnel : smoke test base de données
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Démarrage rapide
```bash
# from repo root
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Ensuite, ouvrez :
- PWA : `http://127.0.0.1:5173/`
- Base API backend : `http://127.0.0.1:8788`
- Vérification santé : `http://127.0.0.1:8788/api/health`

Vérification rapide avec une commande :
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Carte rapide des endpoints :

| Surface | URL |
| --- | --- |
| UI PWA | `http://127.0.0.1:5173/` |
| API backend | `http://127.0.0.1:8788` |
| Endpoint de santé | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
Fichier principal : `.env` (voir `docs/env.md` et `.env.example`).

### Variables importantes

| Variable | But |
| --- | --- |
| `SECRET_KEY` | Requise par convention |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Paramètres de bind backend |
| `DATABASE_URL` | DSN PostgreSQL (préféré) |
| `AUTOAPPDEV_RUNTIME_DIR` | Surcharge du dossier runtime (par défaut `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Cible d’exécution pipeline par défaut |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Active `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Valeurs par défaut Codex pour actions/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Réservées aux intégrations futures |

Validez rapidement `.env` :
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

## ▶️ Utilisation

| Mode | Commande | Notes |
| --- | --- | --- |
| Démarrer backend + PWA (recommandé) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Démarrer uniquement le backend | `conda run -n autoappdev python -m backend.app` | Utilise les paramètres bind + DB de `.env` |
| Démarrer uniquement le serveur statique PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Utile pour les vérifications frontend seules |
| Exécuter le driver self-dev dans tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Boucle d’auto-développement reprenable |

### Options de script courantes
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Analyser et stocker des scripts
- Analyse AAPS via API : `POST /api/scripts/parse`
- Import de shell annoté : `POST /api/scripts/import-shell`
- Analyse LLM optionnelle : `POST /api/scripts/parse-llm` (nécessite `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### APIs de contrôle du pipeline
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Autres APIs fréquemment utilisées
- Santé/version/config : `/api/health`, `/api/version`, `/api/config`
- Plan/scripts : `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions : `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messagerie : `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs : `/api/logs`, `/api/logs/tail`

Voir `docs/api-contracts.md` pour les formats request/response.

## 🧭 Runbooks opérationnels

### Runbook : démarrer la stack locale complète
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Points de validation :
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Ouvrir `http://127.0.0.1:5173/` et confirmer que l’UI peut charger `/api/config`.
- Optionnel : ouvrir `/api/version` et vérifier que les métadonnées backend attendues sont renvoyées.

### Runbook : debug backend uniquement
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook : smoke codegen déterministe
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

## 📡 Aperçu API

Principaux groupes d’API en un coup d’œil :

| Catégorie | Endpoints |
| --- | --- |
| Santé + infos runtime | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Modèle plan | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Registre d’actions | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Runtime pipeline | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messagerie + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
| Paramètres workspace | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Exemples
### Exemple AAPS
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

Exemples complets :
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### Génération déterministe de runner
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Pipeline démo déterministe
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Ensuite utilisez les contrôles Start/Pause/Resume/Stop de la PWA et inspectez `/api/logs`.

### Import depuis un shell annoté
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 Notes de développement
- Le backend est basé sur Tornado et conçu pour l’ergonomie de développement local (y compris un CORS permissif pour localhost à ports séparés).
- Le stockage est PostgreSQL-first avec comportement de compatibilité dans `backend/storage.py`.
- Les clés de blocs PWA et les valeurs `STEP.block` des scripts sont volontairement alignées (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Les actions intégrées sont en lecture seule ; clonez avant de modifier.
- L’action `update_readme` est contrainte en sécurité de chemin aux cibles README de workspace sous `auto-apps/<workspace>/README.md`.
- Certains docs/scripts contiennent des références historiques de chemin/nom (`HeyCyan`, `LightMind`) héritées de l’évolution du projet. Le chemin canonique actuel est la racine de ce dépôt.
- Le répertoire racine `i18n/` existe. Les fichiers README de langue sont attendus à cet emplacement lors des exécutions multilingues.

### Modèle de travail et fichiers d’état
- Le runtime utilise `./runtime` par défaut, sauf surcharge par `AUTOAPPDEV_RUNTIME_DIR`.
- L’état/historique de l’automatisation self-dev est suivi sous `references/selfdev/`.
- Les artefacts du pipeline README sont enregistrés sous `.auto-readme-work/<timestamp>/`.

### Posture de test (actuelle)
- Le dépôt inclut des vérifications smoke et des scripts de démonstration déterministes.
- Une suite de tests automatisés/manifest CI complète au niveau racine n’est pas définie actuellement dans les métadonnées racine.
- Hypothèse : la validation est principalement pilotée par scripts pour l’instant (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, checklist end-to-end).

## 🔐 Notes de sécurité
- L’action `update_readme` est volontairement contrainte aux cibles README de workspace (`auto-apps/<workspace>/README.md`) avec protections contre la traversal de chemin.
- La validation du registre d’actions applique des champs de spécification normalisés et des valeurs bornées pour les niveaux de raisonnement supportés.
- Les scripts du dépôt supposent une exécution locale de confiance ; examinez les scripts avant exécution dans des environnements partagés ou proches production.
- `.env` peut contenir des valeurs sensibles (`DATABASE_URL`, clés API). Gardez `.env` non commité et utilisez une gestion de secrets adaptée en dehors du dev local.

## 🔧 Dépannage

| Symptôme | Vérifications |
| --- | --- |
| `tmux not found` | Installez `tmux` ou exécutez backend/PWA manuellement. |
| Échec du backend au démarrage à cause d’env manquantes | Revalidez `.env` contre `.env.example` et `docs/env.md`. |
| Erreurs base de données (connexion/auth/schema) | Vérifiez `DATABASE_URL` ; relancez `conda run -n autoappdev python -m backend.apply_schema` ; vérification connectivité optionnelle : `conda run -n autoappdev python -m backend.db_smoketest`. |
| La PWA se charge mais ne peut pas appeler l’API | Vérifiez que le backend écoute sur l’hôte/port attendu ; régénérez `pwa/config.local.js` en relançant `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start renvoie une transition invalide | Vérifiez d’abord le statut actuel du pipeline ; démarrez depuis l’état `stopped`. |
| Pas de mise à jour de logs dans l’UI | Confirmez que `runtime/logs/pipeline.log` est bien écrit ; utilisez `/api/logs` et `/api/logs/tail` directement pour isoler UI vs backend. |
| L’endpoint d’analyse LLM renvoie disabled | Définissez `AUTOAPPDEV_ENABLE_LLM_PARSE=1` puis redémarrez le backend. |
| `conda run -n autoappdev ...` échoue | Relancez `./scripts/setup_autoappdev_env.sh` ; confirmez que l’environnement conda `autoappdev` existe (`conda env list`). |
| Mauvaise cible API côté frontend | Confirmez que `pwa/config.local.js` existe et pointe vers l’hôte/port backend actif. |

Pour une vérification manuelle déterministe, utilisez `docs/end-to-end-demo-checklist.md`.

## 🌐 Workflow README & i18n
- Le README racine est la source canonique utilisée par le pipeline d’automatisation README.
- Les variantes multilingues sont attendues sous `i18n/`.
- Statut du répertoire i18n : ✅ présent dans ce dépôt.
- Jeu de langues actuel dans ce dépôt :
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
- La navigation des langues doit rester sur une seule ligne en haut de chaque variante README (pas de barres de langue dupliquées).
- Point d’entrée du pipeline README : `prompt_tools/auto-readme-pipeline.sh`.

### Contraintes de génération i18n (strictes)
- Traitez toujours la génération multilingue lors de la mise à jour du README canonique.
- Générez/mettez à jour les fichiers de langue un par un (séquentiellement), pas en lots ambigus.
- Gardez exactement une ligne de navigation des options de langue en haut de chaque variante.
- Ne dupliquez pas les barres de langue dans un même fichier.
- Préservez les extraits de commandes canoniques, les liens, les chemins API et l’intention des badges dans les traductions.

Ordre suggéré de génération un par un :
1. `README.md` (source canonique anglaise)
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

Table de couverture des langues :

| Langue | Fichier |
| --- | --- |

## ❓ FAQ

### PostgreSQL est-il obligatoire ?
Préféré et attendu pour un fonctionnement normal. La couche de stockage contient un comportement de compatibilité de repli, mais un usage de type production doit supposer que PostgreSQL est disponible via `DATABASE_URL`.

### Pourquoi `AUTOAPPDEV_PORT` et `PORT` ?
`AUTOAPPDEV_PORT` est spécifique au projet. `PORT` existe comme alias compatible déploiement. Gardez-les alignés sauf si vous voulez volontairement surcharger ce comportement dans votre chemin de lancement.

### Par où commencer si je veux seulement inspecter les APIs ?
Lancez uniquement le backend (`conda run -n autoappdev python -m backend.app`) puis utilisez `/api/health`, `/api/version`, `/api/config`, ensuite les endpoints scripts/actions listés dans `docs/api-contracts.md`.

### Les README multilingues sont-ils générés automatiquement ?
Oui. Le dépôt inclut `prompt_tools/auto-readme-pipeline.sh`, et les variantes de langue sont maintenues sous `i18n/` avec une ligne unique de navigation de langue en haut de chaque variante.

## 🗺️ Feuille de route
- Finaliser les tâches self-dev restantes au-delà du statut actuel `51 / 55`.
- Étendre l’outillage workspace/materials/context et renforcer les contrats de chemin sécurisé.
- Continuer à améliorer l’UX de la palette d’actions et les workflows d’actions modifiables.
- Approfondir le support multilingue README/UI dans `i18n/` et le changement de langue à l’exécution.
- Renforcer les vérifications smoke/intégration et la couverture CI (actuellement des smoke checks pilotés par script sont présents ; aucun manifeste CI complet n’est documenté à la racine).
- Continuer à durcir le déterminisme parser/import/codegen autour de AAPS v1 et de l’IR canonique.

## 🤝 Contribuer
Les contributions sont bienvenues via issues et pull requests.

Workflow suggéré :
1. Forkez puis créez une branche de fonctionnalité.
2. Gardez des changements ciblés et reproductibles.
3. Préférez des scripts/tests déterministes lorsque possible.
4. Mettez à jour la documentation quand les comportements/contrats changent (`docs/*`, contrats API, exemples).
5. Ouvrez une PR avec le contexte, les étapes de validation et les hypothèses runtime.

Les remotes du dépôt incluent actuellement :
- `origin` : `git@github.com:lachlanchen/AutoAppDev.git`
- D’autres remotes peuvent être présents dans les clones locaux pour des dépôts liés (exemple trouvé dans cet espace de travail : `novel`).

## 🙌 Support
- Issues et pull requests GitHub pour les rapports de bugs et propositions de fonctionnalités.
- Les liens sponsor/don sont listés ci-dessous.

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 Licence
Aucun fichier `LICENSE` à la racine n’a été détecté dans cet instantané du dépôt.

Note d’hypothèse :
- Tant qu’un fichier de licence n’est pas ajouté, considérez les conditions d’utilisation/de redistribution comme non spécifiées et confirmez avec le mainteneur.

## ❤️ Sponsor et dons
- GitHub Sponsors : https://github.com/sponsors/lachlanchen
- Donate : https://chat.lazying.art/donate
- PayPal : https://paypal.me/RongzhouChen
- Stripe : https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400

Si ce projet aide votre workflow, le sponsoring soutient directement la poursuite des tâches self-dev, la qualité de la documentation et le durcissement des outils.
