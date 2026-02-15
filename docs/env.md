# Environment Variables (.env)

AutoAppDev reads configuration from environment variables. In local development, create a `.env` file in the repo root.

## Quickstart
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
cp .env.example .env
```
Then edit `.env` with your local values.

## Required Conventions
These keys are required by convention for running the controller reliably (some are reserved for near-future features).

- `SECRET_KEY`
  - Required convention for future auth/signed state.
  - For dev: any non-empty value is fine.
- `AUTOAPPDEV_HOST`
  - Backend bind address (default `127.0.0.1`).
- `AUTOAPPDEV_PORT`
  - Backend port (default `8788`).
- `PORT`
  - Deployment-friendly alias. For now, set `PORT` to the same value as `AUTOAPPDEV_PORT`.
- Database
  - Preferred: `DATABASE_URL` (PostgreSQL connection string).
  - Alternate convention: set `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` and derive `DATABASE_URL` in your tooling.

## Optional
- `AUTOAPPDEV_RUNTIME_DIR`
  - Overrides the runtime directory (defaults to `./runtime`).
- `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT`
  - Defaults for pipeline runner.
- `AI_API_BASE_URL`, `AI_API_KEY`
  - Reserved for future AI integrations.

## Validate Your .env (Single Command)
Run this from the repo root. It fails non-zero if required keys are missing.

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
