# Debug/Verify Notes: 012 run_pipeline_subprocess_manager

## What I Verified
- Static verification:
  - Backend compiles after subprocess manager hardening changes.
- Live start/stop + orphan checks were skipped because no `.env` exists in this workspace (backend requires `DATABASE_URL` to start).

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

python -m py_compile backend/app.py

# Live verify (skipped; requires .env)
if test -f .env; then
  timeout 5s python -m backend.db_smoketest
  timeout 10s python -m backend.apply_schema
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

    if command -v jq >/dev/null 2>&1; then
      spid=$(echo "$start_json" | jq -r .pid)
      sleep 0.5
      kill -0 "$spid" 2>/dev/null && exit 1 || true
    fi

    curl -fsS http://127.0.0.1:8788/api/pipeline
  '
else
  echo 'HAVE_DOTENV=0 (skipping live verify; no .env present)'
fi
# HAVE_DOTENV=0 (skipping live verify; no .env present)
```

## Issues Found
- None requiring code changes.
