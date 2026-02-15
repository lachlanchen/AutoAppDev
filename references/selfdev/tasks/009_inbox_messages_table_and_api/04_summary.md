# Summary: 009 inbox_messages_table_and_api

## What Changed
- Added `inbox_messages` table to `backend/schema.sql`.
- Added inbox persistence methods in `backend/storage.py`.
- Added `/api/inbox` endpoints in `backend/app.py`:
  - `GET /api/inbox?limit=N`
  - `POST /api/inbox { content }` with basic validation
  - Side effect: writes `runtime/inbox/*_user.md`
- Updated `docs/api-contracts.md` to document `/api/inbox`.

## Why
This introduces a first-class inbox API and DB table for user guidance messages, while preserving the existing `/api/chat` behavior used by the current PWA.

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

  curl -fsS -X POST http://127.0.0.1:8788/api/inbox \
    -H "Content-Type: application/json" \
    -d '{"content":"hello inbox"}'

  curl -fsS "http://127.0.0.1:8788/api/inbox?limit=5"
'

ls -la "$RT_DIR/inbox" | head -n 5
```
