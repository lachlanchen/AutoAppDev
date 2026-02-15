# Debug/Verify Notes: 005 apply_schema_sql_migration

## What I Verified
- The CLI schema apply command `python -m backend.apply_schema`:
  - Fails fast and clearly when `DATABASE_URL` is missing.
  - Fails fast (with timeouts) when the target is unreachable.
- Real-DB idempotency (apply twice) was skipped because no local `.env` exists in this workspace.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# 1) Missing env should fail fast and be actionable
timeout 3s env DATABASE_URL= python -m backend.apply_schema; echo EXIT_CODE:$?
# ERROR: missing required env: DATABASE_URL
# Hint: cp .env.example .env and set DATABASE_URL (see docs/env.md).
# EXIT_CODE:2

# 2) Unreachable/invalid target should fail fast (internal timeouts)
timeout 5s env DATABASE_URL='postgresql://invalid' python -m backend.apply_schema; echo EXIT_CODE:$?
# ERROR: schema apply timed out
# DSN: postgresql://invalid
# EXIT_CODE:4

# 3) Real DB (skipped; requires .env)
if test -f .env; then
  timeout 10s python -m backend.apply_schema; echo EXIT_CODE:$?
  timeout 10s python -m backend.apply_schema; echo EXIT_CODE_2:$?
else
  echo 'HAVE_DOTENV=0 (skipping real DB schema apply; no .env present)'
fi
# HAVE_DOTENV=0 (skipping real DB schema apply; no .env present)
```

## Issues Found
- None requiring code changes.
