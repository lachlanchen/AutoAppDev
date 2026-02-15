# Plan: 024 pipeline_script_storage_api

## Goal
Persist pipeline scripts (formatted script text) and their parsed IR in Postgres, and expose minimal CRUD endpoints so the PWA can save/reload by id.

Acceptance:
- Backend adds DB tables + minimal CRUD endpoints for pipeline scripts + IR.
- PWA can save and reload a script by id.

## Current State (References)
- Backend DB + schema:
  - `backend/schema.sql` contains core tables (`app_config`, `inbox_messages`, `pipeline_runs`, etc.).
  - `backend/app.py` calls `storage.ensure_schema(schema.sql)` on startup.
  - `backend/apply_schema.py` applies `backend/schema.sql` to the configured Postgres DB.
- Backend HTTP patterns:
  - `backend/app.py` uses Tornado handlers (see `ConfigHandler`, `PlanHandler`, etc.) and mounts routes in `make_app()`.
  - `backend/storage.py` is the Postgres-first persistence layer (JSON fallback exists but backend requires `DATABASE_URL`).
- Script + IR spec exists (docs only, no parser yet):
  - `docs/pipeline-formatted-script-spec.md` defines AAPS v1 (`AUTOAPPDEV_PIPELINE 1`) and canonical IR `autoappdev_ir` v1 (`TASK -> STEP -> ACTION`).
- PWA baseline:
  - `pwa/app.js` already uses `window.AutoAppDevApi.requestJson()` and renders results into `#export` for plan posting (`/api/plan`).

## Approach (Minimal / Incremental)
1. Add a single `pipeline_scripts` table that stores:
   - formatted script text (AAPS v1 string)
   - optional IR JSON (`jsonb`)
2. Add minimal CRUD endpoints under `/api/scripts` to create/list/get/update/delete scripts.
3. Add minimal PWA wiring to prove save/load by id works (no full “Script editor” yet):
   - A “Save Script” button that posts a deterministic script skeleton + IR derived from the current block program.
   - A “Load Script” button that fetches by id and (minimally) shows the stored object in `#export` (optionally also restores the block program from IR steps).

## Implementation Steps (Next Phase)
1. Add DB table(s) to `backend/schema.sql`.
   - Add:
     - `pipeline_scripts` with columns:
       - `id bigserial primary key`
       - `title text not null default ''`
       - `script_text text not null`
       - `script_version integer not null default 1` (AAPS version)
       - `script_format text not null default 'aaps'`
       - `ir jsonb` (nullable)
       - `created_at timestamptz not null default now()`
       - `updated_at timestamptz not null default now()`
     - Optional index: `create index if not exists pipeline_scripts_updated_at_idx on pipeline_scripts(updated_at);`
   - Keep schema idempotent (`create table if not exists`).

2. Add persistence helpers to `backend/storage.py`.
   - Add methods (Postgres-first; optional state.json fallback for consistency):
     - `create_pipeline_script(title, script_text, script_version, script_format, ir) -> dict`
     - `get_pipeline_script(script_id) -> dict|None`
     - `list_pipeline_scripts(limit) -> list[dict]`
     - `update_pipeline_script(script_id, fields...) -> dict|None`
     - `delete_pipeline_script(script_id) -> bool`
   - Serialize timestamps to ISO strings (match existing patterns in `list_*` functions).
   - Validate sizes defensively in handler layer (script_text length cap, etc.).

3. Add Tornado handlers + routes in `backend/app.py`.
   - Add:
     - `ScriptsHandler` mounted at `GET/POST /api/scripts`:
       - `GET`: list recent scripts (query: `limit`, default 50, clamp 1..200).
       - `POST`: create a script.
     - `ScriptHandler` mounted at `GET/PUT/DELETE /api/scripts/<id>`:
       - `GET`: fetch one script by id (404 if missing).
       - `PUT` (or `POST` if keeping API style consistent): update fields; set `updated_at=now()`.
       - `DELETE`: remove script (optional but completes “CRUD”).
   - Request/response shape (keep minimal and explicit):
     - Create request:
       - `{ "title": "...", "script_text": "...", "script_version": 1, "script_format": "aaps", "ir": { ... } }`
     - Create response:
       - `{ "ok": true, "script": { ... } }`
     - Errors:
       - 400 for invalid JSON/body/types
       - 404 for unknown id

4. Document the new endpoints.
   - Update `docs/api-contracts.md`:
     - Add a “Scripts” section documenting:
       - `POST /api/scripts`
       - `GET /api/scripts?limit=N`
       - `GET /api/scripts/<id>`
       - `PUT /api/scripts/<id>` (or `POST` if that’s what we implement)
       - `DELETE /api/scripts/<id>` (if implemented)
     - Include one example storing AAPS v1 script + `autoappdev_ir` JSON.

5. Minimal PWA save/load wiring.
   - `pwa/index.html`:
     - In Program panel actions (`.panel-actions`), add:
       - `#btn-save-script` and `#btn-load-script` (keep layout minimal; avoid new panels).
       - Use `prompt()` for title/id to avoid adding new inputs/CSS (small step).
   - `pwa/app.js`:
     - Add `els.saveScriptBtn` / `els.loadScriptBtn`.
     - Add helpers:
       - `programToAapsScript(program)`:
         - Generate deterministic AAPS v1 skeleton from blocks:
           - Header + single `TASK`
           - One `STEP` per block with `block` key = palette key
           - Optional: one `ACTION` per step with `kind:"noop"` (keeps the script valid per spec)
       - `programToIr(program)`:
         - Generate `autoappdev_ir` v1 skeleton that matches the script (TASK->STEP->ACTION).
     - Implement:
       - `saveScript()` -> `POST /api/scripts`, show `{ok, script}` in `#export`.
       - `loadScript()` -> prompt id, `GET /api/scripts/<id>`, show result in `#export`.
       - Optional small win (if IR present): restore `program` by flattening tasks/steps -> `{type: step.block}` and call `renderProgram()`.
   - `pwa/service-worker.js`:
     - Bump `CACHE_NAME` to avoid stale cached `index.html/app.js` during manual verification.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Schema/table + backend handlers exist
rg -n 'create table if not exists pipeline_scripts' backend/schema.sql
rg -n '/api/scripts' backend/app.py
rg -n 'create_pipeline_script|get_pipeline_script|list_pipeline_scripts|update_pipeline_script|delete_pipeline_script' backend/storage.py

# PWA wiring exists
rg -n 'btn-save-script|btn-load-script' pwa/index.html
rg -n '/api/scripts|programToAapsScript\\(|programToIr\\(|saveScript\\(|loadScript\\(' pwa/app.js

timeout 5s node --check pwa/app.js
timeout 5s python3 -m py_compile backend/app.py backend/storage.py backend/apply_schema.py
```

DB-backed smoke (if Postgres + `.env` available in this environment):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 20s conda run -n autoappdev python -m backend.apply_schema

# (Optional) small python snippet to create + fetch a script using Storage with DATABASE_URL
```

Manual end-to-end verification (outside this sandbox, which cannot bind ports):
1. Start backend + PWA and open the UI.
2. Click “Save Script” (with a non-empty program) and confirm the response includes a numeric `id`.
3. Reload the page and use “Load Script” with that id; confirm the stored script/IR returns and (if implemented) the canvas restores from IR.

## Acceptance Checklist
- [ ] `pipeline_scripts` table exists in `backend/schema.sql` and is applied idempotently.
- [ ] Backend exposes CRUD endpoints under `/api/scripts` and stores/retrieves `script_text` + `ir` from Postgres.
- [ ] PWA can save and reload by id using the new endpoints (at minimum via `#export` output).
- [ ] Default PWA theme remains light.

