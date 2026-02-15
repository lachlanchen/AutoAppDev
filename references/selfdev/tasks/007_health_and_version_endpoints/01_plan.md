# Plan: 007 health_and_version_endpoints

## Goal
Extend backend API observability:
- `GET /api/health` returns `{ ok: true }` plus DB connectivity status.
- `GET /api/version` returns app name + a git-less build/version string.

Acceptance:
- `GET /api/health` returns ok with DB connectivity status.
- `GET /api/version` returns app name + git-less build/version string.

## Current State (References)
- `backend/app.py` has `HealthHandler` at `GET /api/health`, currently returns only `{ok, service}`.
- There is no `GET /api/version` route.
- Backend startup already validates env and DB connectivity (tasks 003 + 006):
  - Requires `DATABASE_URL`.
  - `Storage.start()` now raises if it cannot create a Postgres pool.
  - Startup fetches DB time once and prints `DB time: ...`.

## Approach (Minimal)
1. Make `HealthHandler` DB-aware by injecting `Storage`.
2. Add a `VersionHandler` that returns:
- `app`: fixed string (e.g. `"autoappdev"`).
- `service`: fixed string (e.g. `"autoappdev-backend"`).
- `version`: from env `AUTOAPPDEV_VERSION` (default `"dev"`).
- `build`: a git-less build id (use process-start timestamp), plus `started_at`.

## Files To Change (Implementation Phase)
- Update: `backend/app.py`
  - Modify `HealthHandler` to accept `storage: Storage` and report DB status.
  - Add `VersionHandler` and route `(r"/api/version", VersionHandler, {...})`.

## Step-by-Step Implementation Details

### Step 1: Add Process Build Metadata (git-less)
In `backend/app.py` (module-level near `REPO_ROOT`):
- Define a process-start timestamp, e.g.:
  - `STARTED_AT_ISO = datetime.datetime.now(datetime.timezone.utc).isoformat()`
  - `BUILD_ID = STARTED_AT_ISO` (simple, stable for the process, git-less)
- Read version string from env:
  - `AUTOAPPDEV_VERSION` (default `"dev"`).

### Step 2: `GET /api/version`
Add `VersionHandler(BaseHandler)`:
- Response shape:
  - `{ "ok": true, "app": "autoappdev", "service": "autoappdev-backend", "version": "...", "build": "...", "started_at": "..." }`
- No DB calls.

### Step 3: `GET /api/health` With DB Status
Update `HealthHandler`:
- `initialize(self, storage: Storage) -> None`.
- In `get()`:
  - Attempt `await self.storage.get_server_time_iso()`.
  - On success: `db: { ok: true, time: <iso> }`.
  - On failure: `db: { ok: false, error: "<Type>: <msg>" }`.
- Overall `ok` should remain `true` if the HTTP handler is running.

### Step 4: Wire Routes
In `make_app(...)` routes list in `backend/app.py`:
- Change health route to pass storage:
  - `(r"/api/health", HealthHandler, {"storage": storage})`
- Add version route:
  - `(r"/api/version", VersionHandler)`

## Commands To Run (Verification)
Use a single `timeout` wrapper so we do not leave background processes running.

1) Syntax check:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
python -m py_compile backend/app.py
```

2) Endpoint smoke (requires a working `.env` with Postgres):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Preflight
timeout 5s python -m backend.db_smoketest

timeout 10s python -m backend.apply_schema

# Run backend briefly, query endpoints, then shut it down.
# NOTE: This starts a short-lived background process, but the script kills it and is wrapped in timeout.
RT_DIR="$(mktemp -d)"
timeout 8s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  export AUTOAPPDEV_RUNTIME_DIR='"$RT_DIR"'
  python -m backend.app &
  pid=$!
  cleanup() { kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true; }
  trap cleanup EXIT
  # give tornado a moment
  for _ in 1 2 3 4 5; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done
  echo "--- /api/health ---"
  curl -fsS http://127.0.0.1:8788/api/health
  echo
  echo "--- /api/version ---"
  curl -fsS http://127.0.0.1:8788/api/version
  echo
'

# Acceptance-oriented grep checks
rg -n '"db"\s*:\s*\{' "$RT_DIR/logs/backend.log" || true
```

## Acceptance Criteria Checks
- `GET /api/health` returns JSON containing `ok: true` and a `db` object with `ok` and either `time` or `error`.
- `GET /api/version` returns JSON containing `app` and a git-less `version`/`build` string.
- Verification script leaves no backend process running (wrapped in `timeout` and uses `trap` cleanup).
