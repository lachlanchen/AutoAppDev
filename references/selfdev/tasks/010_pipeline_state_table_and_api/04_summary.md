# Summary: 010 pipeline_state_table_and_api

## What Changed
- Added `pipeline_state` table to `backend/schema.sql` (singleton row `id=1`) to track current pipeline state and timestamps.
- Added storage methods in `backend/storage.py` to read/update pipeline state.
- Added `GET /api/pipeline` in `backend/app.py` returning `{ pipeline: { state, pid, run_id, started_at, paused_at, resumed_at, stopped_at, updated_at } }`.
- Updated pipeline control endpoints to update `pipeline_state` on start/pause/resume/stop.
- Updated `docs/api-contracts.md` to document `GET /api/pipeline`.

## Why
This makes the current pipeline state explicit and timestamped (stopped/running/paused), independent from the historical `pipeline_runs` log.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Requires a real .env with DATABASE_URL
# timeout 5s python -m backend.db_smoketest
# timeout 10s python -m backend.apply_schema

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
  curl -fsS http://127.0.0.1:8788/api/pipeline
'
```
