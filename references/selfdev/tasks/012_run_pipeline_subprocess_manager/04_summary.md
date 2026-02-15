# Summary: 012 run_pipeline_subprocess_manager

## What Changed
- Hardened `PipelineControl` in `backend/app.py`:
  - Closes the parent-side pipeline log file handle after spawning.
  - `stop()` now waits after SIGKILL, updates DB state, and clears internal process references.
  - Added exit detection (`maybe_collect_exit()`) to mark runs `completed`/`failed` and set `pipeline_state` to `stopped`.
- Added a Tornado `PeriodicCallback` to poll for subprocess exit.

## Why
This makes pipeline subprocess management more reliable and prevents common failure modes (orphaned process groups, leaked file handles, stale running state when the process exits).

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Requires a real .env with DATABASE_URL
# timeout 5s python -m backend.db_smoketest
# timeout 10s python -m backend.apply_schema

RT_DIR="$(mktemp -d)"
export AUTOAPPDEV_RUNTIME_DIR="$RT_DIR"

timeout 20s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  python -m backend.app &
  bpid=$!
  trap "kill $bpid 2>/dev/null || true; wait $bpid 2>/dev/null || true" EXIT

  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done

  start_json=$(curl -fsS -X POST http://127.0.0.1:8788/api/pipeline/start -H "Content-Type: application/json" -d '{}')
  echo "$start_json"

  curl -fsS -X POST http://127.0.0.1:8788/api/pipeline/stop -H "Content-Type: application/json" -d '{}'
  sleep 1

  curl -fsS http://127.0.0.1:8788/api/pipeline
'
```
