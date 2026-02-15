# Work Notes: 038 workspace_materials_and_context_api

## What Changed
- Added persistent per-workspace configuration storage + API:
  - DB table `workspace_configs` in `backend/schema.sql`
  - Storage helpers in `backend/storage.py`:
    - `get_workspace_config(workspace)`
    - `upsert_workspace_config(workspace, config)`
  - Validation/normalization module `backend/workspace_config.py` enforcing safe path rules under `auto-apps/<workspace>/` and allowed languages.
  - New backend endpoint:
    - `GET /api/workspaces/<workspace>/config` (returns defaults if none exists)
    - `POST /api/workspaces/<workspace>/config` (partial upsert; normalized + safe)
- Updated docs:
  - `docs/api-contracts.md` now documents the workspace config endpoints and safety constraints.

## Files Touched
- `backend/schema.sql`
- `backend/storage.py`
- `backend/workspace_config.py`
- `backend/app.py`
- `docs/api-contracts.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/workspace_config.py

timeout 10s rg -n '/api/workspaces/([^/]+)/config|WorkspaceConfigHandler' backend/app.py
timeout 10s rg -n 'GET /api/workspaces/<workspace>/config|POST /api/workspaces/<workspace>/config' docs/api-contracts.md
```

Results:
- `py_compile` exited `0` (syntax OK).
- `rg` confirms handler + route are present and docs updated.

