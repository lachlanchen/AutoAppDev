# Work Notes: 003 add_env_loader_backend

## Summary of Changes
- Fixed `.env` loading order in `backend/app.py` so env is loaded before computing runtime/log paths.
- Made the backend fail fast on startup when `DATABASE_URL` is missing, with a clear error message and non-zero exit.
- Added support for `PORT` as an alias for `AUTOAPPDEV_PORT` (without changing the existing default).

## Key Behavior Changes
- `AUTOAPPDEV_RUNTIME_DIR` set in `.env` now affects where runtime artifacts are written (logs/inbox) because runtime/log paths are computed after calling `load_dotenv()`.
- If `DATABASE_URL` is empty/missing, backend prints:
  - `ERROR: missing required env: DATABASE_URL`
  - A hint to create `.env` from `.env.example` and see `docs/env.md`
  - Then exits with status 2.

## Files Changed
- Updated: `backend/app.py`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Syntax/type sanity compile (does not require installed deps)
python -m py_compile backend/app.py backend/storage.py

# Quick scan of relevant symbols
rg -n "RUNTIME_DIR\\b|LOG_DIR\\b|load_dotenv\\(|_require_env\\(|DATABASE_URL\\b|AUTOAPPDEV_RUNTIME_DIR\\b|\\bPORT\\b" backend/app.py
```

## Notes
- This task intentionally enforces Postgres presence by requiring `DATABASE_URL` at startup, matching the acceptance criteria.
- No background processes were started in this phase.
