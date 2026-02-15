# Summary: 004 postgres_connection_smoketest

## What Changed
- Added `backend/db_smoketest.py`: a CLI Postgres smoke test that loads `.env`, connects using `DATABASE_URL`, and runs `SELECT 1` with short timeouts.
- Updated `backend/README.md` to document the smoke test command.

## Why
This provides a deterministic, server-free way to validate Postgres wiring and quickly localize config/connectivity failures with actionable messages.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Missing env: should fail fast and be actionable
timeout 3s env DATABASE_URL= python -m backend.db_smoketest; echo EXIT_CODE:$?

# Invalid/unreachable target: should fail fast (internal 2s timeout)
timeout 3s env DATABASE_URL='postgresql://invalid' python -m backend.db_smoketest; echo EXIT_CODE:$?

# Real DB: with DATABASE_URL set in .env, should succeed
# cp .env.example .env
# edit .env, then:
timeout 5s python -m backend.db_smoketest
```
