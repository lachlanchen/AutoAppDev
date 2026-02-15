# Plan: 010 pipeline_state_table_and_api

## Goal
Add a simple, explicit pipeline state table and an API endpoint:
- Create a DB table for pipeline state.
- Implement `GET /api/pipeline` returning state (`stopped|running|paused`) plus timestamps.

Acceptance:
- DB table exists for pipeline state.
- `GET /api/pipeline` returns state and timestamps.

## Current State (References)
- Existing run tracking table: `pipeline_runs` in `backend/schema.sql`.
- Existing status API: `GET /api/pipeline/status` in `backend/app.py` uses `Storage.get_latest_status()`.
  - Returns `{ running, pid, run_id, state }` but no timestamps.
- Control endpoints update `pipeline_runs.status` and `stopped_at` in `backend/storage.py`.

## Design Choice (Minimal, Non-Breaking)
Introduce the requested new table + endpoint without removing or changing existing `/api/pipeline/status`.

- Keep `/api/pipeline/status` as-is for current PWA compatibility.
- Add `pipeline_state` table as a cached “current state” record.
- Add `GET /api/pipeline` endpoint that reads from `pipeline_state` (authoritative current state) and returns timestamps.

Update pipeline control paths (start/stop/pause/resume) to maintain `pipeline_state` in addition to `pipeline_runs`.

## Files To Change (Implementation Phase)
- Update: `backend/schema.sql`
  - Add `pipeline_state` table.
- Update: `backend/storage.py`
  - Add methods to set/get pipeline state with timestamps.
- Update: `backend/app.py`
  - Add `PipelineStateHandler` for `GET /api/pipeline`.
  - Ensure pipeline control updates state table.
- Update docs (optional but recommended): `docs/api-contracts.md`
  - Add `/api/pipeline` response shape.

## Schema Details
Add to `backend/schema.sql`:
- `pipeline_state` table with a single row keyed by `id = 1`:
  - `id integer primary key`
  - `state text not null` (values: `stopped|running|paused`)
  - `pid integer`
  - `run_id bigint`
  - `started_at timestamptz`
  - `paused_at timestamptz`
  - `resumed_at timestamptz`
  - `stopped_at timestamptz`
  - `updated_at timestamptz not null default now()`

Initialize default row (idempotent):
- Insert `id=1, state='stopped'` if missing.

## Storage API
In `backend/storage.py`, add:
- `async def get_pipeline_state(self) -> dict[str, Any]`
  - Returns state record; if missing, returns defaults.
- `async def set_pipeline_state(self, *, state: str, pid: int|None, run_id: int|None, ts_kind: str) -> None`
  - Updates the singleton row and sets the relevant timestamp column:
    - start: set `started_at=now()`, clear `stopped_at`, set `state='running'`
    - pause: set `paused_at=now()`, `state='paused'`
    - resume: set `resumed_at=now()`, `state='running'`
    - stop: set `stopped_at=now()`, `state='stopped'`
  - Always update `pid`, `run_id`, `updated_at=now()`.

Implementation should use the shared pool (`require_pool()` + acquire) and `INSERT ... ON CONFLICT (id) DO UPDATE`.

## API Handler
In `backend/app.py`, add:
- `PipelineStateHandler(BaseHandler)`
  - `initialize(storage: Storage)`
  - `GET /api/pipeline` -> `{ "pipeline": { state, pid, run_id, started_at, paused_at, resumed_at, stopped_at, updated_at } }`

## Update Control Flow
In `backend/app.py` pipeline control handlers, after each action succeeds:
- `start`: after `controller.start(...)` returns ok, call `storage.set_pipeline_state(state='running', pid=<pid>, run_id=<run_id>, ts_kind='start')`.
- `pause`: call `storage.set_pipeline_state(state='paused', pid=<pid>, run_id=<run_id>, ts_kind='pause')`.
- `resume`: call `storage.set_pipeline_state(state='running', pid=<pid>, run_id=<run_id>, ts_kind='resume')`.
- `stop`: call `storage.set_pipeline_state(state='stopped', pid=<pid>, run_id=<run_id>, ts_kind='stop')`.

Use the controller's `run_id` (and pid if available) for these updates.

## Commands To Run (Verification)
Requires a working `.env` with `DATABASE_URL`.

1) Apply schema:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 5s python -m backend.db_smoketest

timeout 10s python -m backend.apply_schema
```

2) Endpoint smoke:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

RT_DIR="$(mktemp -d)"
export AUTOAPPDEV_RUNTIME_DIR="$RT_DIR"

timeout 10s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  python -m backend.app &
  pid=$!
  trap "kill $pid 2>/dev/null || true; wait $pid 2>/dev/null || true" EXIT

  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done

  echo "--- GET /api/pipeline (initial) ---"
  curl -fsS http://127.0.0.1:8788/api/pipeline
  echo
'
```

3) State transition smoke (optional):
```bash
# Start -> pause -> resume -> stop, then GET /api/pipeline and confirm timestamps filled.
```

## Acceptance Criteria Checks
- Schema includes `pipeline_state` and it can be applied idempotently.
- `GET /api/pipeline` returns a JSON object containing state and timestamps.
- Pipeline control endpoints keep `pipeline_state` up-to-date.
