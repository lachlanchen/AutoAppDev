# Work Notes: 024 pipeline_script_storage_api

## Summary
- Added `pipeline_scripts` persistence (DB table + storage helpers) and exposed CRUD endpoints under `/api/scripts`.
- Added minimal PWA wiring to save the current block program as a stored script+IR and reload it by id.
- Updated API contracts doc to document the new endpoints.

## Changes Made
- `backend/schema.sql`
  - Added `pipeline_scripts` table:
    - `title`, `script_text`, `script_version`, `script_format`, `ir (jsonb)`, timestamps.
  - Added index on `updated_at`.
- `backend/storage.py`
  - Added storage methods:
    - `create_pipeline_script()`
    - `get_pipeline_script()`
    - `list_pipeline_scripts()`
    - `update_pipeline_script()`
    - `delete_pipeline_script()`
  - (Also supports the JSON `runtime/state.json` fallback for consistency.)
- `backend/app.py`
  - Added Tornado handlers:
    - `ScriptsHandler`: `GET/POST /api/scripts`
    - `ScriptHandler`: `GET/PUT/DELETE /api/scripts/<id>`
  - Registered routes in `make_app()`.
- `docs/api-contracts.md`
  - Added “Scripts” section documenting `/api/scripts` endpoints.
- `pwa/index.html`
  - Added Program panel buttons:
    - `#btn-save-script`, `#btn-load-script`
- `pwa/app.js`
  - Added script/IR generation + API calls:
    - `programToAapsScript()`, `programToIr()`
    - `saveScript()` -> `POST /api/scripts`
    - `loadScript()` -> `GET /api/scripts/<id>` (and restores canvas from `script.ir` steps when present)
  - Wired button click handlers.
- `pwa/service-worker.js`
  - Bumped `CACHE_NAME` to `autoappdev-shell-v6` to avoid stale `index.html/app.js` during manual verification.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'pipeline_scripts|/api/scripts' backend/schema.sql backend/app.py backend/storage.py docs/api-contracts.md pwa/index.html pwa/app.js

timeout 5s python3 -m py_compile backend/app.py backend/storage.py backend/apply_schema.py
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

