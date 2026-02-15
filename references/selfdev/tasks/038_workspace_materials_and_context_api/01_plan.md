# Plan: 038 workspace_materials_and_context_api

## Goal
Add a minimal backend feature to **persist per-workspace configuration** (materials path(s), shared context text/file reference, default language) with strict **safe path rules under `auto-apps/`**, and expose simple **read/write HTTP endpoints**.

Acceptance:
- Backend stores workspace config in Postgres
- All configured paths are validated to resolve **within** `auto-apps/<workspace>/`
- Exposes read/write endpoints to get/upsert config

## Current State (References)
- DB schema is applied at backend startup from `backend/schema.sql` via `backend/app.py`/`Storage.ensure_schema()`.
- Storage patterns:
  - `backend/storage.py` has Postgres-first CRUD and a JSON fallback store.
- Workspace safety precedent:
  - `backend/update_readme_action.py` implements `validate_workspace_slug()` and safe resolution under `auto-apps/`.
  - `backend/app.py` exposes `POST /api/actions/update-readme` using those helpers.
- API docs live in `docs/api-contracts.md`.
- Workspace layout contract exists in `docs/workspace-layout.md` (workspace roots under `auto-apps/` and contain `materials/`, `docs/`, etc.).

## Data Model (DB)
Add a new table holding one JSON config per workspace:
- Table: `workspace_configs`
  - `workspace text primary key`
  - `config jsonb not null`
  - `updated_at timestamptz not null default now()`

Config shape stored in `config` (v0):
```json
{
  "materials_paths": ["materials"],
  "shared_context_text": "",
  "shared_context_path": "docs/shared_context.md",
  "default_language": "en"
}
```

Notes:
- Paths are stored as **workspace-relative** strings, but validated to resolve under `auto-apps/<workspace>/`.
- Defaults (recommended):
  - `materials_paths`: `["materials"]`
  - `default_language`: `"en"`
  - `shared_context_text`/`shared_context_path`: omitted or empty.

## Validation / Safety Rules (Backend)
Implement a small validator/normalizer module to keep `backend/app.py` thin.

Rules:
- `workspace`: validate with `backend/update_readme_action.py:validate_workspace_slug()` (single path segment; no control chars; max length).
- `materials_paths`:
  - Must be a list of 1..20 strings (or omitted -> default `["materials"]`).
  - Each entry must be a repo-safe, workspace-relative path:
    - not absolute
    - must resolve within `auto-apps/<workspace>/` (reject `..` traversal and symlink escapes)
  - Normalize stored value to a clean relative string (e.g. `"materials/screenshots"`).
- `shared_context_path` (optional):
  - If present, must be a string path that resolves within `auto-apps/<workspace>/`.
  - Stored as normalized workspace-relative string.
- `shared_context_text` (optional):
  - If present, must be a string; clamp size (e.g. <= 200k).
- `default_language`:
  - Must be one of: `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `vi`, `ar`, `fr`, `es`.
  - Default `"en"` if omitted.

Implementation detail:
- Use the same symlink guard pattern as `backend/update_readme_action.py:resolve_workspace_readme_path()` to ensure `auto-apps/` itself cannot resolve outside the repo.

## API Design (Minimal)
Add one handler with GET (read) and POST (upsert) under a workspace-scoped URL:
- `GET /api/workspaces/<workspace>/config`
  - Response:
    ```json
    { "ok": true, "workspace": "my_workspace", "exists": true, "config": { ... }, "updated_at": "..." }
    ```
  - If not found, return defaults with `exists:false` (still `ok:true`) so the UI can render without a pre-create step.
- `POST /api/workspaces/<workspace>/config`
  - Request (partial allowed; backend applies defaults and normalizes):
    ```json
    {
      "materials_paths": ["materials", "materials/screenshots"],
      "shared_context_text": "...\n",
      "shared_context_path": "docs/shared_context.md",
      "default_language": "en"
    }
    ```
  - Response:
    ```json
    { "ok": true, "workspace": "my_workspace", "config": { ...normalized... }, "updated_at": "..." }
    ```

Error codes (examples):
- `invalid_workspace`
- `invalid_body`, `invalid_json`
- `invalid_materials_paths`, `invalid_materials_path`
- `path_outside_auto_apps`, `path_outside_workspace`
- `invalid_shared_context_text`, `invalid_shared_context_path`
- `invalid_default_language`

## Implementation Steps (Next Phase: WORK)
1. Schema: add table
   - Edit `backend/schema.sql`:
     - Add `create table if not exists workspace_configs (...)`
     - Optional: add index on `updated_at` if needed later.

2. Storage: add CRUD helpers
   - Edit `backend/storage.py`:
     - `get_workspace_config(workspace: str) -> dict | None`
     - `upsert_workspace_config(workspace: str, config: dict) -> dict`
     - Mirror patterns used for action/scripts CRUD (return ISO timestamps).
     - Add JSON fallback storage under a new key like `state["workspace_configs"]`.

3. Validation/normalization module
   - Add `backend/workspace_config.py`:
     - `WorkspaceConfigError(code, detail).to_dict()`
     - `ALLOWED_LANGUAGES` constant
     - `resolve_workspace_root(repo_root: Path, workspace: str) -> Path` (safe under `auto-apps/`)
     - `normalize_workspace_relative_path(workspace_root: Path, raw: str) -> str`
     - `normalize_workspace_config(body: dict, *, repo_root: Path, workspace: str, base: dict | None) -> dict`
       - Supports partial updates by merging `body` onto `base` then applying defaults + normalization.

4. HTTP handlers + routes
   - Edit `backend/app.py`:
     - Add `WorkspaceConfigHandler(BaseHandler)`:
       - `initialize(storage: Storage)`
       - `get(workspace: str)`:
         - validate workspace
         - fetch from storage
         - return normalized config + `exists` and `updated_at`
       - `post(workspace: str)`:
         - parse JSON
         - fetch existing base config (if any)
         - validate/normalize partial update
         - upsert via storage
     - Add route in `make_app(...)`:
       - `(r\"/api/workspaces/([^/]+)/config\", WorkspaceConfigHandler, {\"storage\": storage})`

5. Docs
   - Edit `docs/api-contracts.md`:
     - Add a `## Workspaces` section documenting:
       - `GET /api/workspaces/<workspace>/config`
       - `POST /api/workspaces/<workspace>/config`
     - Document path safety rules (workspace-relative but validated under `auto-apps/<workspace>/`) and allowed languages list.

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Static compile
timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/workspace_config.py

# Grep: ensure routes + docs exist
timeout 10s rg -n \"/api/workspaces/\\(\\[\\^/\\]\\+\\)/config|WorkspaceConfigHandler\" backend/app.py
timeout 10s rg -n \"GET /api/workspaces/<workspace>/config|POST /api/workspaces/<workspace>/config\" docs/api-contracts.md
```

Optional manual API smoke (requires Postgres + backend running):
```bash
# start backend (in a separate terminal)
python3 -m backend.app

# upsert config
curl -sS -X POST http://127.0.0.1:8788/api/workspaces/my_workspace/config \\
  -H 'content-type: application/json' \\
  -d '{\"materials_paths\":[\"materials\"],\"shared_context_path\":\"docs/shared_context.md\",\"default_language\":\"en\"}'

# read back
curl -sS http://127.0.0.1:8788/api/workspaces/my_workspace/config

# path traversal should fail
curl -sS -X POST http://127.0.0.1:8788/api/workspaces/my_workspace/config \\
  -H 'content-type: application/json' \\
  -d '{\"materials_paths\":[\"../secrets\"]}'
```

## Acceptance Checklist
- [ ] `backend/schema.sql` creates `workspace_configs`.
- [ ] `backend/storage.py` can get/upsert workspace configs.
- [ ] Backend validates workspace slug and rejects paths resolving outside `auto-apps/<workspace>/`.
- [ ] `GET` returns defaults with `exists:false` when no config stored.
- [ ] `POST` upserts normalized config and returns it.
- [ ] `docs/api-contracts.md` documents the endpoints and safety rules.

