# Work Notes: 004 postgres_connection_smoketest

## Summary of Changes
- Added a dedicated Postgres CLI smoke test: `python -m backend.db_smoketest`.
  - Loads `.env` from repo root.
  - Uses `DATABASE_URL`.
  - Connects and runs `SELECT 1` with short (2s) timeouts.
  - Prints clear actionable errors and exits non-zero on failure.
- Updated `backend/README.md` to document the smoke test command.

## Files Changed
- Added: `backend/db_smoketest.py`
- Updated: `backend/README.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Syntax check
python -m py_compile backend/db_smoketest.py
```

## Notes
- The smoke test sanitizes the DSN for logs (best-effort) so passwords are not printed.
- Runtime verification (missing/invalid/real DB) is deferred to the DEBUG/VERIFY phase per the task workflow.
