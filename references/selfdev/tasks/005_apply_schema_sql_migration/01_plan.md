# Plan: 005 apply_schema_sql_migration

## Goal
Provide a small, deterministic command to apply `backend/schema.sql` to the configured Postgres DB.

Acceptance:
- Add a small script/command to apply `backend/schema.sql` to the configured DB.
- Running it twice is idempotent or clearly warns without crashing.

## Current State (References)
- Schema file: `backend/schema.sql`.
  - Already uses `create table if not exists ...`, so it is idempotent by design.
- Backend server startup in `backend/app.py` currently applies schema implicitly:
  - Reads `backend/schema.sql` and calls `Storage.ensure_schema(sql)`.
  - This is not a standalone, explicit operator command.
- `DATABASE_URL` is required to start the backend (fast-fail) per task 003 changes in `backend/app.py`.
- There is already a CLI Postgres check: `backend/db_smoketest.py`.

## Approach (Minimal)
Add a dedicated CLI module for schema application.

- Add: `backend/apply_schema.py`
  - Loads `.env` (same convention as backend) and reads `DATABASE_URL`.
  - Connects to Postgres with a short timeout.
  - Reads `backend/schema.sql` from disk and executes it.
  - Prints a clear success message.
  - On failure, prints actionable error + sanitized DSN (do not print passwords).
  - Re-running is safe because `schema.sql` uses `IF NOT EXISTS`.

Optionally, document the command in `backend/README.md`.

## Files To Change (Implementation Phase)
- Add: `backend/apply_schema.py`
- Update: `backend/README.md` (add one short section: “Apply schema.sql”)

## Step-by-Step Implementation Details
1. Create `backend/apply_schema.py`.
   - Similar structure to `backend/db_smoketest.py` for consistency:
     - `REPO_ROOT = Path(__file__).resolve().parents[1]`
     - `load_dotenv(REPO_ROOT / ".env", override=False)`
     - Validate `DATABASE_URL` is non-empty; else error + exit(2).
     - Read SQL: `(Path(__file__).with_name("schema.sql")).read_text("utf-8")`.
     - Connect with `asyncpg.connect(dsn=dsn, timeout=2.0)`.
     - Execute SQL (single `conn.execute(sql)` is fine here).
     - Print `OK: schema applied`.
     - Close connection.
   - Use timeouts for connect/execute (2-5s) to avoid hangs.
   - Sanitize DSN in logs (reuse a small sanitizer function or copy the one from `backend/db_smoketest.py`).

2. Update `backend/README.md`.
   - Add:
     - `conda run -n autoappdev python -m backend.apply_schema`
   - Keep it minimal.

## Commands To Run (Verification)
Use `timeout` for anything that could hang.

1) Missing env should fail fast:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
(timeout 3s env DATABASE_URL= python -m backend.apply_schema) ; echo EXIT_CODE:$?
# Expect: non-zero exit, message mentions missing DATABASE_URL and points at docs/env.md.
```

2) Invalid/unreachable DSN should fail fast with actionable error:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
(timeout 5s env DATABASE_URL='postgresql://invalid' python -m backend.apply_schema) ; echo EXIT_CODE:$?
# Expect: non-zero exit, error includes exception type/message and sanitized DSN.
```

3) Real DB should apply schema successfully and be idempotent:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
# With a real DATABASE_URL in .env:
(timeout 10s python -m backend.apply_schema)
(timeout 10s python -m backend.apply_schema)
# Expect: both runs succeed (idempotent) and do not crash.
```

## Acceptance Criteria Checks
- Command exists and applies `backend/schema.sql` to the configured DB (`DATABASE_URL`).
- Second run succeeds (schema is idempotent because it uses `IF NOT EXISTS`).
- Failure modes exit non-zero quickly and print actionable diagnostics.
