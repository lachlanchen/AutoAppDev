# Debug/Verify Notes: 006 storage_layer_pg_pool

## What I Verified
- Backend now fails fast (non-zero) when `DATABASE_URL` is set but Postgres is unreachable.
- Pool-creation failures are surfaced as a clear startup error (not a silent fallback).
- Real DB startup + "DB time:" log verification was skipped because no `.env` exists in this workspace.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Unreachable/invalid DSN should fail fast and be actionable
timeout 5s env DATABASE_URL='postgresql://invalid' python -m backend.app; echo EXIT_CODE:$?
# ERROR: backend startup failed: RuntimeError: failed to create Postgres pool (DATABASE_URL is set): TimeoutError:
# Hint: verify Postgres is running and DATABASE_URL is correct (see docs/env.md).
# EXIT_CODE:1

# Real DB server-time check (skipped; requires .env)
if test -f .env; then
  RT_DIR="$(mktemp -d)"
  timeout 3s env AUTOAPPDEV_RUNTIME_DIR="$RT_DIR" python -m backend.app; echo EXIT_CODE:$?
  rg -n "DB time:" "$RT_DIR/logs/backend.log"
else
  echo 'HAVE_DOTENV=0 (skipping real DB time check; no .env present)'
fi
# HAVE_DOTENV=0 (skipping real DB time check; no .env present)
```

## Issues Found
- Initially, DB connection failure did not terminate the backend because `make_app()` ran as a background task; the IOLoop stayed running.

## Fix Applied In This Phase
- Updated `backend/app.py` to run `make_app()` via `loop.run_until_complete(...)` before starting the IOLoop so startup failures propagate and exit immediately.
