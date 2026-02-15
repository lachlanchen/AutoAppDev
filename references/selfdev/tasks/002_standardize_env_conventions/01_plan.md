# Plan: 002 standardize_env_conventions

## Goal
Standardize and document `.env` conventions for AutoAppDev.

Acceptance requires:
- Docs specify required env vars: `DATABASE_URL` or `PG*` vars, `PORT`, `SECRET_KEY`.
- Docs say how to copy from `.env.example`.
- Docs include one command to validate env.

This phase (PLAN) does not change code.

## Current State (References)
- Example env file: `.env.example` (currently has `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `DATABASE_URL`, pipeline vars; no `PORT`/`SECRET_KEY`/`PG*`).
- Backend loads `.env` in dev: `backend/app.py` uses `dotenv.load_dotenv(REPO_ROOT / ".env")` and reads env via `safe_env()`.
  - Uses `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `DATABASE_URL`.
- Dev tmux runner uses the same host/port vars: `scripts/run_autoappdev_tmux.sh`.

## Files To Change (Implementation Phase)
- Update: `.env.example`
  - Add `PORT` and `SECRET_KEY` (even if not yet used by backend, reserve it now as a required convention).
  - Add commented `PG*` vars as an alternative to writing `DATABASE_URL` directly.
  - Keep existing `AUTOAPPDEV_*` variables as the canonical app-prefixed keys.
- Add: `docs/env.md`
  - Single source of truth for env conventions.
  - Includes copy instructions from `.env.example`.
  - Includes a single validation command.
- Update: `README.md`
  - Add one bullet under Contents linking to `docs/env.md`.
- Optional (keep minimal): update `backend/README.md`
  - Add one short “Env” note linking to `docs/env.md`.

## Env Conventions To Document
Document these as “required to run the controller” even if some are not consumed yet:
- `SECRET_KEY`
  - Required convention for future auth/signed state; set a dev value locally.
- HTTP port
  - `AUTOAPPDEV_PORT` is what the backend reads today (`backend/app.py`).
  - `PORT` is a deployment-friendly alias; for now docs should instruct setting both to the same value.
- HTTP host
  - `AUTOAPPDEV_HOST` (defaults to `127.0.0.1`).
- Database
  - Recommended: set `DATABASE_URL` directly.
  - Alternative: set `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` and derive `DATABASE_URL`.
    - Note in docs: current backend reads `DATABASE_URL`; `PG*` is a documented convention for developers and future wiring.

Also document existing (optional) keys already in `.env.example`:
- `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT`
- `AI_API_BASE_URL`, `AI_API_KEY` (optional)

## Validation Command (Single Command In Docs)
Include exactly one copy-pastable command that:
- Loads `.env` into the shell environment.
- Verifies required keys are present and non-empty: `SECRET_KEY`, `DATABASE_URL`, plus one of `AUTOAPPDEV_PORT` or `PORT`.

Proposed command to put in `docs/env.md`:
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

## Implementation Steps (Next Phase)
1. Edit `.env.example`:
   - Add `SECRET_KEY=dev_change_me` (comment: generate a long random value).
   - Add `PORT=8788` (comment: keep in sync with `AUTOAPPDEV_PORT`).
   - Add commented `PG*` variables with sane defaults and a note on deriving `DATABASE_URL`.
2. Create `docs/env.md`:
   - Quickstart: `cp .env.example .env`.
   - Required keys section with short explanations.
   - Postgres section: recommended `DATABASE_URL` and optional `PG*`.
   - Include the single validation command.
3. Update `README.md` Contents with a link bullet to `docs/env.md`.
4. (Optional) Add a 2-3 line “Env” section in `backend/README.md` pointing to `docs/env.md`.

## Acceptance Checks (Commands)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Docs exist and mention the required env vars
test -s docs/env.md
rg -n "\\bDATABASE_URL\\b" docs/env.md
rg -n "\\bPGHOST\\b|\\bPGPORT\\b|\\bPGUSER\\b|\\bPGPASSWORD\\b|\\bPGDATABASE\\b" docs/env.md
rg -n "\\bPORT\\b" docs/env.md
rg -n "\\bSECRET_KEY\\b" docs/env.md

# Copy instructions from .env.example are present
rg -n "cp \\.env\\.example \\.env" docs/env.md

# .env.example contains the newly standardized keys
rg -n "^SECRET_KEY=" .env.example
rg -n "^PORT=" .env.example
rg -n "^AUTOAPPDEV_PORT=" .env.example
rg -n "^DATABASE_URL=" .env.example

# README links to the env doc
rg -n "docs/env\\.md" README.md

# Run the validation command from docs (manually copy/paste)
# (This will exit non-zero if required keys are missing.)
```
