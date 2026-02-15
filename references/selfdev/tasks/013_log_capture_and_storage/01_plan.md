# Plan: 013 log_capture_and_storage

## Goal
Improve log observability beyond file tailing by adding an incremental log API.

Acceptance:
- Backend captures subprocess stdout/stderr into a rolling buffer and optionally persists last N lines in DB.
- `GET /api/logs?since=<id>` returns incremental lines.

## Current State (References)
- Logs are currently file-based:
  - Pipeline subprocess writes to `runtime/logs/pipeline.log` via `PipelineControl._spawn()` in `backend/app.py`.
  - Backend stdout/stderr are redirected to `runtime/logs/backend.log` in `backend/app.py`.
  - `GET /api/logs/tail` in `backend/app.py` reads last N lines from these files.
  - PWA calls `/api/logs/tail` in `pwa/app.js`.
- There is no rolling in-memory buffer and no incremental “since id” API.
- DB schema has no log table.

## Approach (Minimal)
Implement an in-memory rolling buffer first, with an optional DB persistence path.

1) Add a `LogBuffer` class in `backend/app.py` (or a small new module `backend/logs.py`).
- Stores log entries with monotonically increasing integer `id`.
- Keeps a fixed maximum number of entries in memory (e.g. 2000).
- Each entry: `{ id, ts, source, line }`.

2) Capture sources:
- Pipeline subprocess output:
  - Change `PipelineControl._spawn()` to pipe stdout/stderr to the parent (use `stdout=PIPE, stderr=STDOUT`).
  - Start an async reader task that reads lines and appends to `LogBuffer` and still writes to `pipeline.log` for persistence.
  - Keep the file log as the durable source of truth.
- Backend logs:
  - Keep current file redirection for now.
  - Optionally also tee lines into `LogBuffer` (this is harder because stdout/stderr are redirected). To keep the step small, start with pipeline logs only.

3) Add DB persistence (optional in this step):
- Add `pipeline_log_lines` table to `backend/schema.sql`:
  - `id bigserial primary key`
  - `run_id bigint`
  - `source text not null` (e.g. `pipeline`)
  - `line text not null`
  - `created_at timestamptz not null default now()`
- Add `Storage.add_log_line(run_id, source, line)` that inserts.
- In the pipeline reader task, optionally insert last N lines (or insert all; retention later).

4) Add incremental log endpoint:
- `GET /api/logs?since=<id>&limit=<n>&source=pipeline`
  - Returns entries with `id > since`, up to `limit`.
  - Response shape:
    - `{ "since": <since>, "next": <last_id>, "lines": [ {"id":...,"ts":...,"source":"pipeline","line":"..."}, ... ] }`

5) Keep existing `/api/logs/tail` intact for now.

## Files To Change (Implementation Phase)
- Update: `backend/app.py`
  - Add `LogBuffer`.
  - Modify `PipelineControl` to capture output lines into the buffer (and file).
  - Add `LogsSinceHandler` for `GET /api/logs`.
- Optional (if implementing DB persistence in this step):
  - Update: `backend/schema.sql`
  - Update: `backend/storage.py`

## Commands To Run (Verification)
Requires a working `.env` with Postgres (backend requires DB).

1) Start backend briefly, start pipeline, fetch incremental logs:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

RT_DIR="$(mktemp -d)"
export AUTOAPPDEV_RUNTIME_DIR="$RT_DIR"

timeout 25s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  python -m backend.app &
  bpid=$!
  trap "kill $bpid 2>/dev/null || true; wait $bpid 2>/dev/null || true" EXIT

  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done

  curl -fsS -X POST http://127.0.0.1:8788/api/pipeline/start -H "Content-Type: application/json" -d '{}'
  sleep 1

  echo "--- logs since 0 ---"
  curl -fsS "http://127.0.0.1:8788/api/logs?source=pipeline&since=0&limit=50"
  echo

  curl -fsS -X POST http://127.0.0.1:8788/api/pipeline/stop -H "Content-Type: application/json" -d '{}'
'
```

## Acceptance Criteria Checks
- `GET /api/logs?since=...` returns incremental entries with stable ids.
- Buffer does not grow unbounded (fixed max).
- Pipeline output is captured (at least when pipeline is running).
- No background processes remain after verification (all wrapped in `timeout` + traps).
