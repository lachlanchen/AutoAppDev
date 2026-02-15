# Summary: 038 workspace_materials_and_context_api

## What Changed
- Added per-workspace config persistence and API with safe path rules under `auto-apps/<workspace>/`:
  - DB: `workspace_configs` table in `backend/schema.sql`
  - Storage: `get_workspace_config()` / `upsert_workspace_config()` in `backend/storage.py`
  - Validation/normalization: `backend/workspace_config.py`
  - API:
    - `GET /api/workspaces/<workspace>/config` (returns defaults if not stored)
    - `POST /api/workspaces/<workspace>/config` (partial upsert, normalized)
- Documented the endpoints in `docs/api-contracts.md`.

## Why
Pipelines need durable, workspace-scoped inputs and context (materials locations, shared context, default language) while enforcing safe path boundaries (no arbitrary filesystem writes outside `auto-apps/<workspace>/`).

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/workspace_config.py
timeout 10s rg -n \"WorkspaceConfigHandler|/api/workspaces/\\(\\[\\^/\\]\\+\\)/config\" backend/app.py
timeout 10s rg -n \"GET /api/workspaces/<workspace>/config|POST /api/workspaces/<workspace>/config\" docs/api-contracts.md
```

Manual API smoke (with backend running):
1. `POST /api/workspaces/my_workspace/config` with a valid config and confirm `ok:true`.
2. `GET /api/workspaces/my_workspace/config` returns the normalized config.
3. Try `materials_paths: [\"../secrets\"]` and confirm it is rejected.

