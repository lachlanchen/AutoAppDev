# Plan: 006 storage_layer_pg_pool

## Goal
Tighten `backend/storage.py` into a Postgres-first storage layer with:
- A single shared `asyncpg` pool.
- Simple query helpers.
- A way to fetch DB server time.
- Backend startup verifies it can fetch server time from DB.

Acceptance:
- Storage exposes a single shared connection/pool and simple query helpers.
- Backend starts and can fetch server time from DB.

## Current State (References)
- `backend/storage.py` already has `_pool: Optional[asyncpg.Pool]` and uses `asyncpg.create_pool()`.
  - But `Storage.start()` silently swallows pool creation errors and sets `_pool = None`.
  - Many methods fall back to file-based JSON state when `_pool` is missing.
- `backend/app.py` now requires `DATABASE_URL` (task 003) but does not verify DB connectivity.
  - It calls `await storage.start()` then `await storage.ensure_schema(...)`, but `ensure_schema()` is a no-op if `_pool` is None.

## Approach (Minimal, Incremental)
Because the controller is Postgres-based, treat DB connectivity as required once `DATABASE_URL` is set.

1. Make `Storage.start()` deterministic:
- If `DATABASE_URL` is set but the pool cannot be created, raise an exception with an actionable message.
- Do not silently fall back to local JSON state in this case.

2. Expose a single pool and helper methods:
- Add a `pool` property (read-only) or `require_pool()` method to ensure `_pool` is available.
- Add query helpers that encapsulate pool acquisition:
  - `execute(sql, *args)`
  - `fetch(sql, *args)`
  - `fetchrow(sql, *args)`
  - `fetchval(sql, *args)`

3. Add a “server time” helper:
- Add `async def get_server_time_iso(self) -> str`:
  - `SELECT now()` (or `SELECT now() AT TIME ZONE 'UTC'` if you want stable semantics).
  - Return ISO-8601 string.

4. Verify on backend startup:
- In `backend/app.py` after `await storage.start()` and after schema apply:
  - Call `await storage.get_server_time_iso()`.
  - Log one line like `DB time: <iso>` (goes to `runtime/logs/backend.log`).
  - If it fails, raise and crash startup (fast-fail).

## Files To Change (Implementation Phase)
- Update: `backend/storage.py`
  - Make pool creation failures raise.
  - Add `require_pool()` / `.pool`.
  - Add query helpers and `get_server_time_iso()`.
- Update: `backend/app.py`
  - After creating/starting storage and applying schema, call the new server-time helper.
  - Ensure failures surface clearly (exception message should mention connection failure and hint at `docs/env.md`).

## Commands To Run (Verification)
Use `timeout` for anything that could hang.

1) Storage module sanity (no external deps beyond syntax):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
python -m py_compile backend/storage.py backend/app.py
```

2) Backend fails fast if DB is unreachable (connect failure is now fatal):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
# With an obviously invalid/unreachable DSN
(timeout 5s env DATABASE_URL='postgresql://invalid' python -m backend.app) ; echo EXIT_CODE:$?
# Expect: non-zero exit quickly, error mentions DB connection/pool failure and hints at docs/env.md.
```

3) Backend can fetch server time from DB (requires a real `.env` with working Postgres):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
# Pre-check (already exists):
timeout 5s python -m backend.db_smoketest

# Apply schema (already exists):
timeout 10s python -m backend.apply_schema

# Start backend briefly; it should log DB time during startup.
RT_DIR="$(mktemp -d)"
(timeout 3s env AUTOAPPDEV_RUNTIME_DIR="$RT_DIR" python -m backend.app) ; true
rg -n "DB time:" "$RT_DIR/logs/backend.log"
# Expect: at least one line containing "DB time:".
```

## Acceptance Criteria Checks
- `backend/storage.py` exposes a single pool (read-only) and has simple query helpers used by the backend.
- If `DATABASE_URL` is set but Postgres is unreachable, backend startup fails fast with an actionable error.
- With a working Postgres, backend startup fetches DB server time successfully (observable via a log line).
