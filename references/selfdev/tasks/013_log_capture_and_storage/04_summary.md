# Summary: 013 log_capture_and_storage

## What Changed
- Added an in-memory rolling log buffer in `backend/app.py`.
- Added `GET /api/logs?source=...&since=<id>&limit=N` returning incremental log entries.
- Added file tail pollers that capture lines from `runtime/logs/pipeline.log` and `runtime/logs/backend.log` into the rolling buffer.
- Updated `docs/api-contracts.md` to document the new incremental logs endpoint.

## Why
This enables incremental log viewing for the controller UI (poll-by-id), without relying only on whole-file tailing.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Requires a real .env with DATABASE_URL
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

  curl -fsS "http://127.0.0.1:8788/api/logs?source=pipeline&since=0&limit=20"
  curl -fsS "http://127.0.0.1:8788/api/logs?source=backend&since=0&limit=20"
'
```
