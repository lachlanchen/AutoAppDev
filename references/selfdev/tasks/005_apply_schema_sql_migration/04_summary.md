# Summary: 005 apply_schema_sql_migration

## What Changed
- Added `backend/apply_schema.py`: a CLI command to apply `backend/schema.sql` to the configured Postgres DB (`DATABASE_URL`).
- Updated `backend/README.md` to document the command.

## Why
This makes schema setup an explicit operator action (not only an implicit server startup side effect) and keeps schema application repeatable and idempotent.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Missing env: should fail fast and be actionable
timeout 3s env DATABASE_URL= python -m backend.apply_schema; echo EXIT_CODE:$?

# Invalid/unreachable target: should fail fast (internal timeouts)
timeout 5s env DATABASE_URL='postgresql://invalid' python -m backend.apply_schema; echo EXIT_CODE:$?

# Real DB: with DATABASE_URL set in .env, should succeed and be idempotent
# cp .env.example .env
# edit .env, then:
timeout 10s python -m backend.apply_schema
timeout 10s python -m backend.apply_schema
```
