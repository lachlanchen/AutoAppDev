# Plan: 004 postgres_connection_smoketest

## Goal
Add a deterministic Postgres smoke test that:
- Uses env configuration (at minimum `DATABASE_URL`).
- Connects to Postgres and runs `SELECT 1`.
- Fails fast with an actionable error message.

Acceptance:
- A CLI or startup check can connect to Postgres using env config and run `SELECT 1`.
- On failure, it exits non-zero quickly and prints a clear, actionable error.

## Current State (References)
- Backend requires `DATABASE_URL` to start (fast-fail) in `backend/app.py` via `_require_env()`.
- Postgres connectivity is currently implicit:
  - `backend/storage.py` calls `asyncpg.create_pool(dsn=DATABASE_URL)` inside `Storage.start()`.
  - If pool creation fails it silently sets `_pool = None` and falls back to file-based state.
- No explicit “connectivity check” exists that runs `SELECT 1` and reports why it failed.

## Approach (Minimal)
Add a dedicated CLI smoke test module so we can verify DB wiring without starting the Tornado server.

- Add: `backend/db_smoketest.py` (new)
  - Loads `.env` using the same convention as the backend (`dotenv.load_dotenv(REPO_ROOT / ".env")`).
  - Reads `DATABASE_URL` from env.
  - Uses `asyncpg.connect()` (or `create_pool()` with a single acquire) and runs `SELECT 1`.
  - Uses a short timeout (e.g. 2 seconds) to avoid hangs.
  - Prints `OK: postgres SELECT 1` on success.
  - On failure prints:
    - Which env key is missing (if missing).
    - The connection target (sanitized; do not print password).
    - The exception type + message.
    - A hint to check `.env` / `docs/env.md`.
  - Exits with a non-zero code on failure.

This keeps changes isolated and testable, and avoids changing the Storage fallback behavior yet.

## Files To Change (Implementation Phase)
- Add: `backend/db_smoketest.py`
- Optional docs touch (keep minimal): add one short line to `backend/README.md` showing the smoke test command.

## Implementation Steps (Next Phase)
1. Create `backend/db_smoketest.py`:
   - Compute `REPO_ROOT = Path(__file__).resolve().parents[1]`.
   - `load_dotenv(REPO_ROOT / ".env", override=False)`.
   - Validate `DATABASE_URL` is set and non-empty; if not, print an error and exit(2).
   - Connect with a timeout:
     - `await asyncio.wait_for(asyncpg.connect(dsn=url), timeout=2.0)`
   - Run `await conn.fetchval("SELECT 1")` (or `execute`), assert result is `1`.
   - Close connection in `finally`.
   - Sanitize DSN for logs (strip password if present).
2. (Optional) Update `backend/README.md` with:
   - `conda run -n autoappdev python -m backend.db_smoketest`

## Commands To Run (Verification)
Use timeouts for anything that could hang.

1) Missing env should fail fast with actionable output:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Ensure DATABASE_URL is not present
(timeout 3s env DATABASE_URL= python -m backend.db_smoketest) ; echo EXIT_CODE:$?
# Expect: non-zero exit, message mentions missing DATABASE_URL and points at docs/env.md
```

2) Invalid DSN should fail fast and include exception info:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
(timeout 3s env DATABASE_URL='postgresql://invalid' python -m backend.db_smoketest) ; echo EXIT_CODE:$?
# Expect: non-zero exit, message mentions connection failure
```

3) Real DB should succeed:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
# With a real DATABASE_URL in .env:
(timeout 5s python -m backend.db_smoketest)
# Expect: prints OK and exits 0
```

## Acceptance Criteria Checks
- `python -m backend.db_smoketest` runs `SELECT 1` against the Postgres target from env.
- On missing/invalid config it exits non-zero within a few seconds and prints a clear error + hint.
- No servers or background processes remain running after verification (all tests use `timeout`).
