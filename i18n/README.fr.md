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

Scripts réutilisables + guides pour créer des applications pas à pas à partir de captures d’écran/markdown, avec Codex utilisé comme outil non interactif.

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

## 🚀 Vue d’ensemble
AutoAppDev est un projet contrôleur pour des pipelines de développement d’applications de longue durée et reprenables. Il combine :

1. Une API backend Tornado avec persistance adossée à PostgreSQL (plus un comportement de repli JSON local dans le code de stockage).
2. Une interface contrôleur PWA statique de type Scratch.
3. Des scripts et de la documentation pour l’écriture de pipelines, la génération de code déterministe, les boucles d’auto-développement et l’automatisation du README.

### En un coup d’œil

| Domaine | Détails |
| --- | --- |
| Runtime principal | Backend Tornado + frontend PWA statique |
| Persistance | PostgreSQL en priorité avec comportement de compatibilité dans `backend/storage.py` |
| Modèle de pipeline | IR canonique (`autoappdev_ir` v1) et format de script AAPS |
| Flux de contrôle | Cycle de vie Start / Pause / Resume / Stop |
| Mode dev | Boucle self-dev reprenable + workflows déterministes script/codegen |
| README/i18n | Pipeline README automatisé avec échafaudage `i18n/` |

## 🧭 Philosophie
AutoAppDev traite les agents comme des outils et maintient la stabilité du travail via une boucle stricte et reprenable :
1. Plan
2. Implement
3. Debug/verify (avec timeouts)
4. Fix
5. Summarize + log
6. Commit + push

L’application contrôleur vise à incarner ces mêmes concepts sous forme de blocs/actions type Scratch (y compris une action commune `update_readme`) afin que chaque espace de travail reste à jour et reproductible.

## ✨ Fonctionnalités
- Contrôle du cycle de vie de pipeline reprenable : start, pause, resume, stop.
- API de bibliothèque de scripts pour les scripts pipeline AAPS (`.aaps`) et l’IR canonique (`autoappdev_ir` v1).
- Pipeline de parsing/import déterministe :
  - Parser des scripts AAPS formatés.
  - Importer des scripts shell annotés via des commentaires `# AAPS:`.
  - Repli de parsing assisté par Codex en option (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Registre d’actions avec actions intégrées + actions personnalisées/modifiables (flux clone/edit pour les actions intégrées en lecture seule).
- Blocs PWA type Scratch et palette d’actions chargée à l’exécution (`GET /api/actions`).
- Canaux de messagerie runtime :
  - Inbox (`/api/inbox`) pour les directives opérateur -> pipeline.
  - Outbox (`/api/outbox`) incluant l’ingestion d’une file de fichiers depuis `runtime/outbox`.
- Streaming incrémental des logs backend et pipeline (`/api/logs`, `/api/logs/tail`).
- Génération de runner déterministe depuis l’IR canonique (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev pour l’évolution itérative du dépôt (`scripts/auto-autoappdev-development.sh`).
- Pipeline d’automatisation README avec échafaudage de génération multilingue sous `i18n/`.

## 📚 Contenu
- `docs/auto-development-guide.md` : philosophie et exigences bilingues (EN/ZH) pour un agent d’auto-développement de longue durée et reprenable.
- `docs/ORDERING_RATIONALE.md` : exemple de justification pour l’ordonnancement des étapes pilotées par captures d’écran.
- `docs/controller-mvp-scope.md` : périmètre MVP du contrôleur (écrans + APIs minimales).
- `docs/end-to-end-demo-checklist.md` : checklist manuelle de démonstration end-to-end déterministe (happy path backend + PWA).
- `docs/env.md` : conventions des variables d’environnement (`.env`).
- `docs/api-contracts.md` : contrats requête/réponse API du contrôleur.
- `docs/pipeline-formatted-script-spec.md` : format standard de script pipeline (AAPS) et schéma IR canonique (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md` : générateur déterministe de runners bash exécutables à partir de l’IR canonique.
- `docs/common-actions.md` : contrats/spécifications des actions communes (inclut `update_readme`).
- `docs/workspace-layout.md` : dossiers standard de workspace + contrats (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh` : démarre l’application AutoAppDev (backend + PWA) dans tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh` : démarre le driver self-dev AutoAppDev dans tmux.
- `scripts/app-auto-development.sh` : driver pipeline linéaire (plan -> backend -> PWA -> Android -> iOS -> review -> summary), avec prise en charge resume/state.
- `scripts/generate_screenshot_docs.sh` : générateur description markdown depuis captures d’écran (piloté par Codex).
- `scripts/setup_backend_env.sh` : bootstrap de l’environnement conda backend pour exécutions locales.
- `examples/ralph-wiggum-example.sh` : exemple d’assistant d’automatisation Codex CLI.

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

## ✅ Prérequis
- OS avec `bash`.
- Python `3.11+`.
- Conda (`conda`) pour les scripts d’installation fournis.
- `tmux` pour les sessions backend+PWA ou self-dev en une commande.
- PostgreSQL accessible via `DATABASE_URL`.
- Optionnel : CLI `codex` pour les flux propulsés par Codex (self-dev, repli parse-llm, pipeline auto-readme).

## 🛠️ Installation
### 1) Cloner puis entrer dans le dépôt
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Configurer l’environnement
```bash
cp .env.example .env
```
Modifiez `.env` et définissez au minimum :
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

## ⚙️ Configuration
Fichier principal : `.env` (voir `docs/env.md` et `.env.example`).

### Variables importantes

| Variable | Rôle |
| --- | --- |
| `SECRET_KEY` | Requise par convention |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Paramètres de binding backend |
| `DATABASE_URL` | DSN PostgreSQL (préféré) |
| `AUTOAPPDEV_RUNTIME_DIR` | Remplacer le répertoire runtime (par défaut `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Cible d’exécution pipeline par défaut |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Active `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Valeurs Codex par défaut pour actions/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Réservées aux intégrations futures |

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
### Démarrer backend + PWA ensemble (recommandé)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
Valeurs par défaut :
- Backend : `http://127.0.0.1:8788`
- PWA : `http://127.0.0.1:5173/`

### Démarrer uniquement le backend
```bash
conda run -n autoappdev python -m backend.app
```

### Démarrer uniquement le serveur statique PWA
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### Exécuter le driver self-dev dans tmux
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### Parser et stocker des scripts
- Parser AAPS via API : `POST /api/scripts/parse`
- Importer du shell annoté : `POST /api/scripts/import-shell`
- Parsing LLM optionnel : `POST /api/scripts/parse-llm` (nécessite `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### API de contrôle du pipeline
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

Voir `docs/api-contracts.md` pour les formats de requête/réponse.

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

### Pipeline de démonstration déterministe
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Ensuite, utilisez les contrôles Start/Pause/Resume/Stop de la PWA et inspectez `/api/logs`.

## 🧱 Notes de développement
- Le backend est basé sur Tornado et conçu pour une bonne ergonomie en développement local (y compris un CORS permissif pour les ports localhost séparés).
- Le stockage est PostgreSQL-first avec un comportement de compatibilité dans `backend/storage.py`.
- Les clés de blocs PWA et les valeurs `STEP.block` des scripts sont volontairement alignées (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Les actions intégrées sont en lecture seule ; clonez-les avant modification.
- L’action `update_readme` est contrainte par la sécurité des chemins vers les cibles README de workspace sous `auto-apps/<workspace>/README.md`.
- Certaines docs/scripts contiennent des références historiques de chemin/nom (`HeyCyan`, `LightMind`) héritées de l’évolution du projet. Le chemin canonique actuel est la racine de ce dépôt.
- Le répertoire racine `i18n/` existe. Les fichiers README par langue sont attendus à cet emplacement lors des exécutions multilingues.

## 🩺 Dépannage
- `tmux not found` :
  - Installez `tmux` ou lancez backend/PWA manuellement.
- Le backend échoue au démarrage à cause d’un environnement manquant :
  - Revérifiez `.env` par rapport à `.env.example` et `docs/env.md`.
- Erreurs de base de données (connexion/authentification/schéma) :
  - Vérifiez `DATABASE_URL`.
  - Relancez `conda run -n autoappdev python -m backend.apply_schema`.
  - Vérification de connectivité optionnelle : `conda run -n autoappdev python -m backend.db_smoketest`.
- La PWA se charge mais ne peut pas appeler l’API :
  - Assurez-vous que le backend écoute sur l’hôte/port attendu.
  - Régénérez `pwa/config.local.js` en relançant `./scripts/run_autoappdev_tmux.sh`.
- Pipeline Start renvoie une transition invalide :
  - Vérifiez d’abord l’état actuel du pipeline ; lancez depuis l’état `stopped`.
- Pas de mise à jour de logs dans l’UI :
  - Confirmez que `runtime/logs/pipeline.log` est bien écrit.
  - Utilisez directement `/api/logs` et `/api/logs/tail` pour isoler les problèmes UI vs backend.
- L’endpoint de parsing LLM renvoie disabled :
  - Définissez `AUTOAPPDEV_ENABLE_LLM_PARSE=1` puis redémarrez le backend.

Pour un parcours de vérification manuelle déterministe, utilisez `docs/end-to-end-demo-checklist.md`.

## 🗺️ Feuille de route
- Terminer les tâches self-dev restantes au-delà du statut actuel `51 / 55`.
- Étendre l’outillage workspace/materials/context et renforcer les contrats de chemins sûrs.
- Continuer à améliorer l’UX de la palette d’actions et les workflows d’actions modifiables.
- Approfondir le support multilingue README/UI dans `i18n/` et le changement de langue à l’exécution.
- Renforcer les vérifications smoke/intégration et la couverture CI (des vérifications smoke pilotées par scripts existent actuellement ; aucun manifeste CI complet n’est documenté à la racine).

## 🤝 Contribution
Les contributions sont bienvenues via les issues et les pull requests.

Workflow suggéré :
1. Forkez et créez une branche de fonctionnalité.
2. Gardez des changements ciblés et reproductibles.
3. Privilégiez des scripts/tests déterministes lorsque possible.
4. Mettez à jour la documentation quand le comportement/les contrats changent (`docs/*`, contrats API, exemples).
5. Ouvrez une PR avec le contexte, les étapes de validation et toute hypothèse runtime.

Les remotes du dépôt incluent actuellement :
- `origin` : `git@github.com:lachlanchen/AutoAppDev.git`
- un remote additionnel peut être présent dans les clones locaux pour des dépôts liés.

## 📄 Licence
Aucun fichier `LICENSE` à la racine n’a été détecté dans cet instantané du dépôt.

Note d’hypothèse :
- Tant qu’un fichier de licence n’est pas ajouté, considérez que les conditions d’utilisation/redistribution ne sont pas spécifiées et confirmez avec le mainteneur.

## ❤️ Sponsor & Donations

- GitHub Sponsors : https://github.com/sponsors/lachlanchen
- Donation : https://chat.lazying.art/donate
- PayPal : https://paypal.me/RongzhouChen
- Stripe : https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
