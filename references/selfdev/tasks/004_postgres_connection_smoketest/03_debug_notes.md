# Debug/Verify Notes: 004 postgres_connection_smoketest

## What I Verified
- The CLI smoke test `python -m backend.db_smoketest`:
  - Fails fast and clearly when `DATABASE_URL` is missing.
  - Times out quickly and exits non-zero when the target is unreachable.
- A real-DB success test was skipped because no local `.env` exists in this workspace.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# 1) Missing env should fail fast and be actionable
timeout 3s env DATABASE_URL= python -m backend.db_smoketest; echo EXIT_CODE:$?
# ERROR: missing required env: DATABASE_URL
# Hint: cp .env.example .env and set DATABASE_URL (see docs/env.md).
# EXIT_CODE:2

# 2) Unreachable/invalid target should fail fast (internal 2s timeout)
timeout 3s env DATABASE_URL='postgresql://invalid' python -m backend.db_smoketest; echo EXIT_CODE:$?
# ERROR: postgres connection/query timed out (2s)
# DSN: postgresql://invalid
# EXIT_CODE:4

# 3) Real DB success test (skipped; requires .env)
if test -f .env; then
  timeout 5s python -m backend.db_smoketest; echo EXIT_CODE:$?
else
  echo 'HAVE_DOTENV=0 (skipping real DB test; no .env present)'
fi
# HAVE_DOTENV=0 (skipping real DB test; no .env present)
```

## Issues Found
- Initially, the invalid-host test could hang on exit due to lingering resolver threads, causing the outer `timeout` to kill the process.

## Fix Applied In This Phase
- Updated `backend/db_smoketest.py` to avoid `asyncio.run()` and instead run the loop manually, then hard-exit with `os._exit(rc)` after flushing output.
  - This makes failure cases deterministic and prevents hangs during asyncio shutdown.
