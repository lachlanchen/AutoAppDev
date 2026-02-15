# Summary: 007 health_and_version_endpoints

## What Changed
- Updated `GET /api/health` to include DB connectivity status (`db.ok` plus `db.time` or `db.error`).
- Added `GET /api/version` returning app/service name plus a git-less build id and version string.
  - `version` comes from `AUTOAPPDEV_VERSION` (default `dev`).
  - `build`/`started_at` are derived from process start time.

## Why
This makes the controller backend observable from the PWA: clients can distinguish “backend up” from “DB reachable”, and can display a stable build/version identifier without relying on git.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Requires a real .env with DATABASE_URL
# timeout 5s python -m backend.db_smoketest
# timeout 10s python -m backend.apply_schema

RT_DIR="$(mktemp -d)"
timeout 8s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  export AUTOAPPDEV_RUNTIME_DIR='"$RT_DIR"'
  python -m backend.app &
  pid=$!
  trap "kill $pid 2>/dev/null || true; wait $pid 2>/dev/null || true" EXIT
  for _ in 1 2 3 4 5; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done
  curl -fsS http://127.0.0.1:8788/api/health
  curl -fsS http://127.0.0.1:8788/api/version
'
```
