# Summary: 011 pipeline_control_endpoints

## What Changed
- Enforced a simple pipeline state machine for control endpoints in `backend/app.py`.
  - Invalid transitions now return HTTP 400 with `{ ok:false, error:"invalid_transition", from, action, detail }`.
- Updated `docs/api-contracts.md` with an example `invalid_transition` response.

## Why
This prevents nonsensical control actions (e.g. pausing when stopped) and makes client behavior deterministic.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Requires a real .env with DATABASE_URL
# timeout 5s python -m backend.db_smoketest
# timeout 10s python -m backend.apply_schema

RT_DIR="$(mktemp -d)"
export AUTOAPPDEV_RUNTIME_DIR="$RT_DIR"

timeout 12s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  python -m backend.app &
  pid=$!
  trap "kill $pid 2>/dev/null || true; wait $pid 2>/dev/null || true" EXIT
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done

  # invalid transitions => 400
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/pause -H "Content-Type: application/json" -d '{}'
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/resume -H "Content-Type: application/json" -d '{}'
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/stop -H "Content-Type: application/json" -d '{}'
'
```
