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

Scripts réutilisables et guides pour construire des applications étape par étape à partir de captures d'écran/markdown, avec Codex en tant qu'outil non interactif.

> 🎯 **Mission :** Rendre les pipelines de développement d'applications déterministes, reprenables et pilotés par des artefacts.
>
> 🧩 **Principe de conception :** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Signaux Du Projet

| Signal | Direction actuelle |
| --- | --- |
| Modèle d'exécution | Backend Tornado + contrôleur PWA statique |
| Exécution du pipeline | Déterministe et reprenable (`start/pause/resume/stop`) |
| Stratégie de persistance | PostgreSQL en priorité avec comportement de repli compatible |
| Flux documentaire | README racine canonique + variantes `i18n/` automatisées |

### 🔗 Navigation Rapide

| Besoin | Aller à |
| --- | --- |
| Premier lancement local | [⚡ Démarrage Rapide](#-démarrage-rapide) |
| Environnement et variables requises | [⚙️ Configuration](#️-configuration) |
| Surface API | [📡 Aperçu API](#-aperçu-api) |
| Runbooks d'exécution/débogage | [🧭 Runbooks Opérationnels](#-runbooks-opérationnels) |
| Règles de génération README/i18n | [🌐 Workflow README & i18n](#-workflow-readme--i18n) |
| Matrice de dépannage | [🔧 Dépannage](#-dépannage) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Statut Self-Dev (Mise à jour automatique)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophie : Plan -> Work -> Verify -> Summary -> Commit/Push (linéaire, reprenable)

Cette section est mise à jour par `scripts/auto-autoappdev-development.sh`.
Ne modifiez pas le contenu entre les marqueurs.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Table Des Matières
- [🚀 Vue d'ensemble](#-vue-densemble)
- [🧭 Instantané Du Dépôt](#-instantané-du-dépôt)
- [🧭 Philosophie](#-philosophie)
- [✨ Fonctionnalités](#-fonctionnalités)
- [📌 En Un Coup D'œil](#-en-un-coup-dœil)
- [🏗️ Architecture](#-architecture)
- [📚 Contenu](#-contenu)
- [🗂️ Structure Du Projet](#-structure-du-projet)
- [✅ Prérequis](#-prérequis)
- [🧩 Compatibilité & Hypothèses](#-compatibilité--hypothèses)
- [🛠️ Installation](#️-installation)
- [⚡ Démarrage Rapide](#-démarrage-rapide)
- [⚙️ Configuration](#️-configuration)
- [▶️ Utilisation](#️-utilisation)
- [🧭 Runbooks Opérationnels](#-runbooks-opérationnels)
- [📡 Aperçu API](#-aperçu-api)
- [🧪 Exemples](#-exemples)
- [🧱 Notes De Développement](#-notes-de-développement)
- [🔐 Notes De Sécurité](#-notes-de-sécurité)
- [🔧 Dépannage](#-dépannage)
- [🌐 Workflow README & i18n](#-workflow-readme--i18n)
- [📘 Contexte De Génération Du README](#-contexte-de-génération-du-readme)
- [❓ FAQ](#-faq)
- [🗺️ Feuille De Route](#️-feuille-de-route)
- [🤝 Contribuer](#-contribuer)
- [❤️ Support](#-support)
- [📄 Licence](#-licence)

## 🧭 Instantané Du Dépôt

| Focus | Configuration actuelle |
| --- | --- |
| Boucle principale | Plan → Work → Debug → Fix → Summary → Commit/Push |
| Modèle d'exécution | Backend Tornado + contrôleur PWA statique |
| Machine d'état | `start` / `pause` / `resume` / `stop` |
| Persistance | PostgreSQL en priorité avec compatibilité de repli JSON |
| Documentation | `README.md` canonique + sorties multilingues `i18n/` |

## 🚀 Vue d'ensemble
AutoAppDev est un projet de contrôleur pour des pipelines de développement applicatif longs et reprenables. Il combine :

1. Une API backend Tornado avec persistance PostgreSQL (plus un comportement de repli JSON local dans le code de stockage).
2. Une interface PWA statique de type Scratch.
3. Des scripts et de la documentation pour l'écriture de pipelines, la génération de code déterministe, les boucles d'auto-développement et l'automatisation du README.

Le projet est optimisé pour une exécution agentique prévisible avec un séquencement strict et un historique de workflow orienté artefacts.

### 🎨 Pourquoi ce dépôt existe

| Thème | Ce que cela signifie concrètement |
| --- | --- |
| Déterminisme | Workflows IR canoniques + parsing/import/codegen conçus pour la répétabilité |
| Reprise | Machine d'état explicite (`start/pause/resume/stop`) pour les exécutions longues |
| Opérabilité | Logs d'exécution, canaux inbox/outbox, et boucles de vérification pilotées par scripts |
| Documentation-first | Contrats/spécifications/exemples dans `docs/`, avec flux README multilingue automatisé |

## 🧭 Philosophie
AutoAppDev traite les agents comme des outils et stabilise le travail via une boucle stricte et reprenable :

1. Plan
2. Implémentation
3. Débogage/vérification (avec timeouts)
4. Correction
5. Synthèse + journalisation
6. Commit + push

L'application contrôleur vise à incarner les mêmes concepts sous forme de blocs/actions type Scratch (dont une action commune `update_readme`) afin que chaque workspace reste à jour et reproductible.

### 🔁 Intention des états du cycle de vie

| Transition d'état | Intention opérationnelle |
| --- | --- |
| `start` | Démarrer un pipeline depuis un état arrêté/prêt |
| `pause` | Suspendre une exécution longue en sécurité sans perdre le contexte |
| `resume` | Reprendre depuis l'état/les artefacts d'exécution sauvegardés |
| `stop` | Terminer l'exécution et revenir à un état non actif |

## ✨ Fonctionnalités
- Contrôle reprenable du cycle de vie des pipelines : start, pause, resume, stop.
- API de bibliothèque de scripts pour les scripts pipeline AAPS (`.aaps`) et l'IR canonique (`autoappdev_ir` v1).
- Pipeline déterministe de parsing/import :
  - Parser les scripts AAPS formatés.
  - Importer du shell annoté via commentaires `# AAPS:`.
  - Repli d'analyse assistée Codex en option (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Registre d'actions avec actions intégrées + actions personnalisées/modifiables (flux clone/édition pour les intégrées en lecture seule).
- Blocs PWA de type Scratch et palette d'actions chargée dynamiquement à l'exécution (`GET /api/actions`).
- Canaux de messagerie runtime :
  - Inbox (`/api/inbox`) pour les consignes opérateur -> pipeline.
  - Outbox (`/api/outbox`) incluant l'ingestion de file de fichiers depuis `runtime/outbox`.
- Streaming incrémental des logs backend et pipeline (`/api/logs`, `/api/logs/tail`).
- Génération déterministe du runner depuis l'IR canonique (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev pour l'évolution itérative du dépôt (`scripts/auto-autoappdev-development.sh`).
- Pipeline d'automatisation README avec structure de génération multilingue sous `i18n/`.

## 📌 En Un Coup D'œil

| Domaine | Détails |
| --- | --- |
| Runtime principal | Backend Tornado + frontend PWA statique |
| Persistance | PostgreSQL en priorité avec comportement de compatibilité dans `backend/storage.py` |
| Modèle de pipeline | IR canonique (`autoappdev_ir` v1) et format de script AAPS |
| Flux de contrôle | Cycle Start / Pause / Resume / Stop |
| Mode dev | Boucle self-dev reprenable + workflows script/codegen déterministes |
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
- Exposer les API du contrôleur pour scripts, actions, plan, cycle de vie pipeline, logs, inbox/outbox, config workspace.
- Valider et persister les artefacts de scripts pipeline.
- Coordonner l'état d'exécution pipeline et les transitions de statut.
- Fournir un comportement de repli déterministe si le pool DB est indisponible.

### Responsabilités du frontend
- Rendre l'UI en blocs type Scratch et le flux d'édition de pipeline.
- Charger dynamiquement la palette d'actions depuis le registre backend.
- Piloter les contrôles de cycle de vie et surveiller statut/logs/messages.

## 📚 Contenu
Carte de référence des documents, scripts et exemples les plus utilisés :

- `docs/auto-development-guide.md`: Philosophie et exigences bilingues (EN/ZH) pour un agent d'auto-développement long et reprenable.
- `docs/ORDERING_RATIONALE.md`: Exemple de justification pour le séquencement des étapes pilotées par captures d'écran.
- `docs/controller-mvp-scope.md`: Périmètre MVP du contrôleur (écrans + APIs minimales).
- `docs/end-to-end-demo-checklist.md`: Checklist de démonstration manuelle end-to-end déterministe (happy path backend + PWA).
- `docs/env.md`: Conventions des variables d'environnement (`.env`).
- `docs/api-contracts.md`: Contrats requête/réponse des APIs du contrôleur.
- `docs/pipeline-formatted-script-spec.md`: Format standard de script pipeline (AAPS) et schéma IR canonique (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Générateur déterministe de runners bash exécutables depuis l'IR canonique.
- `docs/common-actions.md`: Contrats/spécifications des actions communes (inclut `update_readme`).
- `docs/workspace-layout.md`: Dossiers workspace standard + contrats (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Démarre l'application AutoAppDev (backend + PWA) dans tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Démarre le driver self-dev AutoAppDev dans tmux.
- `scripts/app-auto-development.sh`: Driver pipeline linéaire (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) avec support reprise/état.
- `scripts/generate_screenshot_docs.sh`: Générateur de description markdown à partir de captures (piloté par Codex).
- `scripts/setup_autoappdev_env.sh`: Script principal de bootstrap conda pour les exécutions locales.
- `scripts/setup_backend_env.sh`: Script utilitaire d'environnement backend.
- `examples/ralph-wiggum-example.sh`: Exemple d'utilitaire d'automatisation Codex CLI.

## 🗂️ Structure Du Projet
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
- Conda (`conda`) pour les scripts d'installation fournis.
- `tmux` pour les sessions backend+PWA ou self-dev en une commande.
- PostgreSQL accessible via `DATABASE_URL`.
- Optionnel : CLI `codex` pour les flux pilotés par Codex (self-dev, repli parse-llm, pipeline auto-readme).

Matrice rapide des exigences :

| Composant | Requis | Rôle |
| --- | --- | --- |
| `bash` | Oui | Exécution de scripts |
| Python `3.11+` | Oui | Backend + outillage codegen |
| Conda | Oui (flux recommandé) | Scripts de bootstrap d'environnement |
| PostgreSQL | Oui (mode privilégié) | Persistance principale via `DATABASE_URL` |
| `tmux` | Recommandé | Sessions backend/PWA et self-dev |
| `codex` CLI | Optionnel | Parsing assisté LLM et automatisation README/self-dev |

## 🧩 Compatibilité & Hypothèses

| Sujet | Attente actuelle |
| --- | --- |
| OS local | Les shells Linux/macOS sont la cible principale (scripts `bash`) |
| Runtime Python | `3.11` (géré par `scripts/setup_autoappdev_env.sh`) |
| Mode de persistance | PostgreSQL est privilégié et traité comme canonique |
| Comportement de repli | `backend/storage.py` inclut un repli JSON compatible pour les scénarios dégradés |
| Modèle réseau | Développement localhost à ports séparés (backend + PWA statique) |
| Outillage agent | CLI `codex` optionnelle sauf si vous utilisez le parsing assisté LLM ou l'automatisation self-dev |

Hypothèses utilisées dans ce README :
- Vous exécutez les commandes depuis la racine du dépôt sauf indication contraire dans une section.
- `.env` est configuré avant de démarrer les services backend.
- `conda` et `tmux` sont disponibles pour les workflows recommandés en une commande.

## 🛠️ Installation
### 1) Cloner et entrer dans le dépôt
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Configurer l'environnement
```bash
cp .env.example .env
```
Éditez `.env` et renseignez au minimum :
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` et `AUTOAPPDEV_PORT` (ou `PORT`)

### 3) Créer/mettre à jour l'environnement backend
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Appliquer le schéma de base de données
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Optionnel : smoke test de la base de données
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Démarrage Rapide
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
- Endpoint health : `http://127.0.0.1:8788/api/health`

Smoke-check en une commande :
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Carte rapide des endpoints :

| Surface | URL |
| --- | --- |
| UI PWA | `http://127.0.0.1:5173/` |
| API backend | `http://127.0.0.1:8788` |
| Endpoint health | `http://127.0.0.1:8788/api/health` |

## ⚙️ Configuration
Fichier principal : `.env` (voir `docs/env.md` et `.env.example`).

### Variables importantes

| Variable | Rôle |
| --- | --- |
| `SECRET_KEY` | Requise par convention |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Paramètres de bind backend |
| `DATABASE_URL` | DSN PostgreSQL (préféré) |
| `AUTOAPPDEV_RUNTIME_DIR` | Redéfinir le dossier runtime (par défaut `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Cible de run pipeline par défaut |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Activer `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Valeurs Codex par défaut pour actions/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Réservé aux futures intégrations |

Valider rapidement `.env` :
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
| Démarrer backend uniquement | `conda run -n autoappdev python -m backend.app` | Utilise les paramètres `.env` de bind + DB |
| Démarrer uniquement le serveur statique PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Utile pour les vérifications frontend-only |
| Exécuter le driver self-dev dans tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Boucle d'auto-développement reprenable |

### Options de scripts fréquentes
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parser et stocker des scripts
- Parser AAPS via API : `POST /api/scripts/parse`
- Importer un shell annoté : `POST /api/scripts/import-shell`
- Parsing LLM optionnel : `POST /api/scripts/parse-llm` (nécessite `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### APIs de contrôle pipeline
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Autres APIs fréquemment utilisées
- Health/version/config : `/api/health`, `/api/version`, `/api/config`
- Plan/scripts : `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions : `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messagerie : `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs : `/api/logs`, `/api/logs/tail`

Voir `docs/api-contracts.md` pour les formats requête/réponse.

## 🧭 Runbooks Opérationnels

### Runbook : démarrer la stack locale complète
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Points de validation :
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Ouvrez `http://127.0.0.1:5173/` et confirmez que l'UI charge `/api/config`.
- Optionnel : ouvrez `/api/version` et vérifiez que les métadonnées backend attendues sont renvoyées.

### Runbook : débogage backend uniquement
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook : smoke test de codegen déterministe
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

Groupes d'API principaux en un coup d'œil :

| Catégorie | Endpoints |
| --- | --- |
| Health + infos runtime | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Modèle de plan | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Registre d'actions | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Runtime pipeline | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messagerie + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET /api/logs/tail` |
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

### Génération déterministe du runner
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Pipeline de démo déterministe
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Puis utilisez les contrôles Start/Pause/Resume/Stop de la PWA et inspectez `/api/logs`.

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

## 🧱 Notes De Développement
- Le backend est basé sur Tornado et conçu pour l'ergonomie du développement local (y compris CORS permissif pour des ports localhost séparés).
- Le stockage est PostgreSQL-first avec comportement de compatibilité dans `backend/storage.py`.
- Les clés de blocs PWA et les valeurs `STEP.block` des scripts sont volontairement alignées (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Les actions intégrées sont en lecture seule ; clonez-les avant modification.
- L'action `update_readme` est limitée pour la sécurité des chemins aux cibles README workspace sous `auto-apps/<workspace>/README.md`.
- Des références historiques de chemin/nom existent dans certains docs/scripts (`HeyCyan`, `LightMind`), héritées de l'évolution du projet. Le chemin canonique actuel est la racine de ce dépôt.
- Le dossier racine `i18n/` existe. Les fichiers README de langue y sont attendus lors des exécutions multilingues.

### Modèle de travail et fichiers d'état
- Le runtime pointe par défaut vers `./runtime`, sauf redéfinition via `AUTOAPPDEV_RUNTIME_DIR`.
- L'état/l'historique de l'automatisation self-dev est suivi sous `references/selfdev/`.
- Les artefacts du pipeline README sont enregistrés sous `.auto-readme-work/<timestamp>/`.

### Posture de test (actuelle)
- Le dépôt inclut des smoke checks et des scripts de démo déterministes.
- Une suite de tests automatisés complète / un manifeste CI au niveau racine n'est pas encore défini dans les métadonnées racine.
- Hypothèse : la validation est principalement pilotée par scripts pour l'instant (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, checklist end-to-end).

## 🔐 Notes De Sécurité
- L'action `update_readme` est volontairement limitée aux cibles README workspace (`auto-apps/<workspace>/README.md`) avec protections contre la traversée de chemin.
- La validation du registre d'actions impose des champs de spécification normalisés et des valeurs bornées pour les niveaux de raisonnement pris en charge.
- Les scripts du dépôt supposent une exécution locale de confiance ; examinez les scripts avant exécution en environnement partagé ou proche production.
- `.env` peut contenir des valeurs sensibles (`DATABASE_URL`, clés API). Gardez `.env` non versionné et utilisez une gestion de secrets adaptée hors dev local.

## 🔧 Dépannage

| Symptôme | Vérification |
| --- | --- |
| `tmux not found` | Installez `tmux` ou lancez backend/PWA manuellement. |
| Le backend échoue au démarrage à cause d'une variable d'env manquante | Revérifiez `.env` par rapport à `.env.example` et `docs/env.md`. |
| Erreurs base de données (connexion/auth/schema) | Vérifiez `DATABASE_URL` ; relancez `conda run -n autoappdev python -m backend.apply_schema` ; test de connectivité optionnel : `conda run -n autoappdev python -m backend.db_smoketest`. |
| La PWA charge mais n'appelle pas l'API | Vérifiez que le backend écoute sur l'hôte/port attendu ; régénérez `pwa/config.local.js` en relançant `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start renvoie une transition invalide | Vérifiez d'abord le statut pipeline actuel ; démarrez depuis l'état `stopped`. |
| Pas de mises à jour de logs dans l'UI | Confirmez que `runtime/logs/pipeline.log` est alimenté ; utilisez `/api/logs` et `/api/logs/tail` directement pour isoler UI vs backend. |
| L'endpoint parse LLM renvoie disabled | Définissez `AUTOAPPDEV_ENABLE_LLM_PARSE=1` puis redémarrez le backend. |
| `conda run -n autoappdev ...` échoue | Relancez `./scripts/setup_autoappdev_env.sh` ; confirmez que l'env conda `autoappdev` existe (`conda env list`). |
| Mauvaise cible API dans le frontend | Confirmez que `pwa/config.local.js` existe et pointe vers l'hôte/port backend actif. |

Pour un chemin de validation manuelle déterministe, utilisez `docs/end-to-end-demo-checklist.md`.

## 🌐 Workflow README & i18n
- Le README racine est la source canonique utilisée par le pipeline d'automatisation README.
- Les variantes multilingues sont attendues sous `i18n/`.
- Statut du dossier i18n : ✅ présent dans ce dépôt.
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
- La navigation de langues doit rester sur une seule ligne en haut de chaque variante README (pas de barres de langues dupliquées).
- Point d'entrée du pipeline README : `prompt_tools/auto-readme-pipeline.sh`.

### Contraintes de génération i18n (strictes)
- Toujours traiter la génération multilingue lors de la mise à jour du README canonique.
- Générer/mettre à jour les fichiers de langue un par un (séquentiellement), pas en batch ambigu.
- Conserver exactement une ligne de navigation linguistique en haut de chaque variante.
- Ne pas dupliquer les barres de langues dans un même fichier.
- Préserver les snippets de commande canoniques, liens, chemins API et intention des badges dans les traductions.

Ordre suggéré de génération unitaire :
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

Table de couverture des langues :

| Langue | Fichier |
| --- | --- |
| Arabic | `i18n/README.ar.md` |

Note observée dans cet espace :
- `i18n/README.zh-Hant.md.tmp` peut apparaître comme artefact temporaire de traduction ; conservez les fichiers canoniques finaux au format `README.<lang>.md`.

## 📘 Contexte De Génération Du README

- Horodatage du run pipeline : `20260301_095119`
- Déclencheur : génération du premier brouillon complet de `./README.md` (mise à jour incrémentale sur base canonique)
- Prompt utilisateur d'entrée : `Use current README as canonical base. No reduction: only increment and improve. Preserve existing content, links, badges, commands, and details. Always process multilingual generation (do not skip): ensure i18n exists and generate/update language files one-by-one with a single language-options line at the top and no duplicates.`
- Objectif : générer un brouillon README complet, soigné, avec sections requises et informations de support
- Snapshot source utilisé :
  - `./.auto-readme-work/20260301_095119/pipeline-context.md`
  - `./.auto-readme-work/20260301_095119/repo-structure-analysis.md`
- Ce fichier a été généré depuis le contenu du dépôt et conservé comme point d'entrée de brouillon canonique.

## ❓ FAQ

### PostgreSQL est-il obligatoire ?
Il est privilégié et attendu pour un fonctionnement normal. La couche de stockage contient un comportement de compatibilité de repli, mais l'usage de type production doit supposer PostgreSQL disponible via `DATABASE_URL`.

### Pourquoi à la fois `AUTOAPPDEV_PORT` et `PORT` ?
`AUTOAPPDEV_PORT` est spécifique au projet. `PORT` existe comme alias orienté déploiement. Gardez-les alignés sauf si vous voulez volontairement surcharger le comportement dans votre chemin de lancement.

### Par où commencer si je veux seulement inspecter les APIs ?
Lancez le backend seul (`conda run -n autoappdev python -m backend.app`) et utilisez `/api/health`, `/api/version`, `/api/config`, puis les endpoints scripts/actions listés dans `docs/api-contracts.md`.

### Les README multilingues sont-ils générés automatiquement ?
Oui. Le dépôt inclut `prompt_tools/auto-readme-pipeline.sh`, et les variantes de langues sont maintenues sous `i18n/` avec une seule ligne de navigation des langues en haut de chaque variante.

## 🗺️ Feuille De Route
- Finaliser les tâches self-dev restantes au-delà du statut actuel `51 / 55`.
- Étendre l'outillage workspace/materials/context et renforcer les contrats de chemins sûrs.
- Continuer d'améliorer l'UX de la palette d'actions et les workflows d'actions modifiables.
- Approfondir la prise en charge multilingue README/UI dans `i18n/` et le changement de langue au runtime.
- Renforcer les smoke checks/intégration et la couverture CI (des smoke checks pilotés par scripts existent déjà ; aucun manifeste CI complet n'est documenté à la racine).
- Continuer à durcir le déterminisme parse/import/codegen autour d'AAPS v1 et de l'IR canonique.

## 🤝 Contribuer
Les contributions sont bienvenues via issues et pull requests.

Workflow suggéré :
1. Forkez puis créez une branche de fonctionnalité.
2. Gardez des changements ciblés et reproductibles.
3. Préférez des scripts/tests déterministes lorsque possible.
4. Mettez à jour la documentation lorsque le comportement/les contrats changent (`docs/*`, contrats API, exemples).
5. Ouvrez une PR avec contexte, étapes de validation et hypothèses runtime.

Les remotes du dépôt incluent actuellement :
- `origin` : `git@github.com:lachlanchen/AutoAppDev.git`
- D'autres remotes peuvent exister dans des clones locaux pour des dépôts liés (exemple trouvé dans cet espace : `novel`).

---

## 📄 Licence
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

Aucun fichier `LICENSE` à la racine n'a été détecté dans cet instantané du dépôt.

Note d'hypothèse :
- Tant qu'un fichier de licence n'est pas ajouté, considérez que les conditions d'usage/de redistribution sont non spécifiées et confirmez auprès du mainteneur.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
