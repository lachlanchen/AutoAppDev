# Work Notes: 006 storage_layer_pg_pool

## Summary of Changes
- Updated `backend/storage.py` to expose a single shared `asyncpg` pool and simple query helpers.
- Made Postgres pool creation deterministic: if `DATABASE_URL` is set but the pool cannot be created, `Storage.start()` now raises a clear error (no silent fallback).
- Added `Storage.get_server_time_iso()` to fetch server time from DB.
- Updated `backend/app.py` startup to fetch and log DB server time (`DB time: ...`) after applying schema.

## Files Changed
- Updated: `backend/storage.py`
- Updated: `backend/app.py`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Syntax check
python -m py_compile backend/storage.py backend/app.py
```

## Notes
- `asyncpg.create_pool(..., timeout=2.0)` is used to keep failures fast/deterministic.
- `ensure_schema()` remains a no-op if no pool exists (for non-DB scenarios), but the backend requires `DATABASE_URL` so it will use Postgres in normal runs.
