# Summary: 006 storage_layer_pg_pool

## What Changed
- Tightened `backend/storage.py` into a Postgres-first storage layer:
  - Deterministic pool creation (raises if `DATABASE_URL` is set but pool creation fails).
  - Exposed a single shared pool (`pool`/`require_pool()`) plus simple query helpers.
  - Added `get_server_time_iso()`.
- Updated backend startup in `backend/app.py` to:
  - Fetch and log DB server time (`DB time: ...`) during startup.
  - Fail fast on startup errors by running `make_app()` before entering the Tornado IOLoop.

## Why
This makes DB connectivity a first-class requirement (no silent fallback) and provides a simple, testable proof that the backend can talk to Postgres by fetching server time.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Unreachable/invalid DSN: backend should fail fast and exit non-zero
timeout 5s env DATABASE_URL='postgresql://invalid' python -m backend.app; echo EXIT_CODE:$?

# Real DB: with DATABASE_URL set in .env
# timeout 5s python -m backend.db_smoketest
# timeout 10s python -m backend.apply_schema
# RT_DIR="$(mktemp -d)"
# (timeout 3s env AUTOAPPDEV_RUNTIME_DIR="$RT_DIR" python -m backend.app) ; true
# rg -n "DB time:" "$RT_DIR/logs/backend.log"
```
