# Debug/Verify Notes: 003 add_env_loader_backend

## What I Verified
Smallest possible startup smoke tests with timeouts:
- Missing `DATABASE_URL` causes an immediate, clear error message and a non-zero exit.
- `AUTOAPPDEV_RUNTIME_DIR` affects where the backend creates `runtime/logs/backend.log` (paths are computed after `.env` load).

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# 1) Negative test: missing DB env should fail fast with clear error
timeout 3s env DATABASE_URL= python -m backend.app; echo EXIT_CODE:$?
# Output:
# ERROR: missing required env: DATABASE_URL
# Hint: cp .env.example .env and set required values (see docs/env.md).
# EXIT_CODE:2

# 2) Runtime dir respects env (short run killed by timeout)
RT_DIR="$(mktemp -d)" && echo "RT_DIR=$RT_DIR" \
  && timeout 2s env AUTOAPPDEV_RUNTIME_DIR="$RT_DIR" DATABASE_URL="postgresql://invalid" python -m backend.app \
  ; echo "EXIT_CODE:$?" \
  ; test -f "$RT_DIR/logs/backend.log" && echo "backend.log exists" \
  ; ls -la "$RT_DIR/logs"
# Result:
# - EXIT_CODE is 124 due to timeout.
# - "$RT_DIR/logs/backend.log" exists (may be empty because the process is killed quickly).
```

## Issues Found
- None requiring code changes.

## Notes
- The positive runtime-dir check used an invalid `DATABASE_URL` on purpose; the backend may fall back to file-based state if Postgres cannot be reached, but this task only requires a clear error when DB env is missing.
