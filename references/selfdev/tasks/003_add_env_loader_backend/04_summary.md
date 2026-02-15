# Summary: 003 add_env_loader_backend

## What Changed
- Refactored `backend/app.py` so `.env` is loaded before computing runtime/log directories.
- `AUTOAPPDEV_RUNTIME_DIR` now correctly controls where runtime artifacts are written.
- Backend now fails fast if `DATABASE_URL` is missing, printing a clear error listing missing vars and exiting non-zero.
- Added `PORT` as an alias for `AUTOAPPDEV_PORT` when selecting the listen port.

## Why
- Previously, `AUTOAPPDEV_RUNTIME_DIR` in `.env` was ignored because paths were computed at import time.
- The controller is Postgres-first; missing DB configuration should be an explicit startup error (not a silent fallback).

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Missing DB env should fail fast with clear message
timeout 3s env DATABASE_URL= python -m backend.app; echo EXIT_CODE:$?

# Runtime dir respects env (process will be killed by timeout)
RT_DIR="$(mktemp -d)" && timeout 2s env AUTOAPPDEV_RUNTIME_DIR="$RT_DIR" DATABASE_URL="postgresql://invalid" python -m backend.app \
  ; test -f "$RT_DIR/logs/backend.log" && echo "OK: backend.log created under AUTOAPPDEV_RUNTIME_DIR"
```
