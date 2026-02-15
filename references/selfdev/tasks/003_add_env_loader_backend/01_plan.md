# Plan: 003 add_env_loader_backend

## Goal
Make backend `.env` loading correct and predictable in dev, and ensure a clear startup error when DB env is missing.

Acceptance:
- Backend loads `.env` in dev (without committing secrets).
- Starting backend without DB prints a clear error listing missing vars.

## Current State (What Needs Fixing)
- `backend/app.py` calls `load_dotenv(REPO_ROOT / ".env")` inside `make_app()`.
- `RUNTIME_DIR` and `LOG_DIR` are computed at import time using `safe_env()` before `.env` is loaded:
  - `RUNTIME_DIR = Path(safe_env("AUTOAPPDEV_RUNTIME_DIR", ...))`
  - `LOG_DIR = RUNTIME_DIR / "logs"`
  - This means `AUTOAPPDEV_RUNTIME_DIR` in `.env` is currently ignored.
- If `DATABASE_URL` is missing/empty, backend currently starts and silently falls back to local JSON state via `backend/storage.py`.
  - This conflicts with the task acceptance which expects an explicit missing-DB error.

## Approach (Minimal, Incremental)
1. Load `.env` before any env-derived paths are computed.
2. Make runtime/log directories derived after `.env` is loaded.
3. Add a small startup env validation step:
   - If `DATABASE_URL` is missing/empty after loading `.env`, print a clear error listing missing vars (at minimum `DATABASE_URL`) and exit non-zero.
   - Keep other keys (like `SECRET_KEY`) as warnings for now (not required for backend to boot yet).

## Files To Change (Implementation Phase)
- Update: `backend/app.py`
  - Move dotenv loading to happen before computing runtime/log paths.
  - Refactor runtime/log dir computation to be post-env-load.
  - Add startup validation for `DATABASE_URL`.
  - Ensure the error is visible in the terminal (perform validation before redirecting stdout/stderr to `runtime/logs/backend.log`).
- Optional (only if needed to keep changes clean): `backend/storage.py`
  - No change required for acceptance if `backend/app.py` exits before instantiating `Storage` when DB missing.

## Step-by-Step Implementation Details

### Step 1: Refactor Env Loading + Runtime/Log Paths
In `backend/app.py`:
- Introduce a small helper like `load_env()` that calls:
  - `load_dotenv(dotenv_path=REPO_ROOT / ".env", override=False)`
- Replace import-time `RUNTIME_DIR`/`LOG_DIR` initialization with runtime initialization:
  - Compute `runtime_dir = Path(safe_env("AUTOAPPDEV_RUNTIME_DIR", str(REPO_ROOT / "runtime"))).resolve()` after `load_env()`.
  - Compute `log_dir = runtime_dir / "logs"` and `mkdir(parents=True, exist_ok=True)` after `load_env()`.
- Ensure all code that uses `LOG_DIR`/`RUNTIME_DIR` uses the computed values:
  - Prefer passing `runtime_dir`/`log_dir` into the objects/handlers that need them.
  - Minimal option: set module-level globals inside `main()` after `load_env()` (and type them as `Path | None`), then assert they are set in request handlers.
  - Cleaner option: pass `runtime_dir` to `ChatHandler` and `PipelineControl`; pass `log_dir` to `PipelineControl` and `LogsTailHandler`.

### Step 2: Validate DB Env on Startup
In `backend/app.py` (likely in `main()` before redirecting logs):
- After `load_env()`:
  - Read `DATABASE_URL = safe_env("DATABASE_URL", "").strip()`.
  - If empty:
    - Print an error like:
      - `ERROR: missing required env: DATABASE_URL`
      - `Hint: cp .env.example .env and set DATABASE_URL (see docs/env.md)`
    - Exit with non-zero status (`sys.exit(2)`).

### Step 3: Support PORT Alias Without Breaking Current Behavior
Still in `backend/app.py`:
- When choosing the listen port:
  - Use `AUTOAPPDEV_PORT` if set, otherwise fall back to `PORT`, otherwise default `8788`.
- Keep host default behavior (`AUTOAPPDEV_HOST` default `127.0.0.1`).

### Step 4: Keep Log Redirection Working
In `backend/app.py`:
- After env is loaded and paths are computed:
  - Create/open `runtime/logs/backend.log` and redirect stdout/stderr as it does today.
- Ensure validation failures happen before redirection so the user sees the error in the terminal.

## Commands To Run (Verification)
All commands should be linear and use timeouts where applicable.

1) Static sanity checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n "load_dotenv\(" backend/app.py
rg -n "AUTOAPPDEV_RUNTIME_DIR|RUNTIME_DIR|LOG_DIR|DATABASE_URL|AUTOAPPDEV_PORT|\bPORT\b" backend/app.py
```

2) Verify missing DB produces a clear error and non-zero exit:
- Run with a clean env (do not rely on a local `.env` existing).
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Ensure DATABASE_URL is not present in the process env.
# timeout prevents hanging if something goes wrong.
timeout 3s env -u DATABASE_URL -u AUTOAPPDEV_RUNTIME_DIR -u AUTOAPPDEV_PORT -u PORT python -m backend.app

# Expected: exits quickly (non-zero) and prints an error mentioning missing DATABASE_URL.
```

3) Verify `.env` is honored for runtime dir:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Create a temporary env file and point to it only if you add AUTOAPPDEV_ENV_FILE support;
# otherwise, do a manual local check by setting AUTOAPPDEV_RUNTIME_DIR in your real .env.
# Expected: backend uses the configured runtime dir for logs/inbox.
```

## Acceptance Criteria Checks
- Backend reads `.env` such that `AUTOAPPDEV_RUNTIME_DIR` (if set) affects where logs/inbox are written.
- Starting backend with no `DATABASE_URL` available prints a clear error listing missing vars (at least `DATABASE_URL`) and exits non-zero within 3 seconds.
- No background processes are left running after the verification commands (use `timeout` for the negative test).
