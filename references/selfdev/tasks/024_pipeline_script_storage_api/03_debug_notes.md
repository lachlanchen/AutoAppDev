# Debug Notes: 024 pipeline_script_storage_api

## Goal
Smallest possible verification for script storage API + minimal PWA wiring:
- Confirm DB schema includes `pipeline_scripts`.
- Confirm backend routes/handlers and storage methods exist.
- Confirm API contracts doc updated.
- Confirm PWA has Save/Load Script buttons and calls `/api/scripts`.
- Run syntax checks (`py_compile`, `node --check`).

Note: This sandbox cannot bind/listen on ports, so end-to-end HTTP verification (creating a script and loading it back via the UI) must be performed outside this sandbox.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'create table if not exists pipeline_scripts' backend/schema.sql
rg -n '/api/scripts' backend/app.py
rg -n 'create_pipeline_script|get_pipeline_script|list_pipeline_scripts|update_pipeline_script|delete_pipeline_script' backend/storage.py
rg -n '## Scripts|/api/scripts' docs/api-contracts.md
rg -n 'btn-save-script|btn-load-script' pwa/index.html
rg -n '/api/scripts|saveScript\\(|loadScript\\(|programToAapsScript\\(|programToIr\\(' pwa/app.js

timeout 5s python3 -m py_compile backend/app.py backend/storage.py backend/apply_schema.py
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Result:
- `pipeline_scripts` table exists in `backend/schema.sql`.
- Backend routes for `/api/scripts` and `/api/scripts/<id>` exist in `backend/app.py`.
- Storage methods exist in `backend/storage.py`.
- `docs/api-contracts.md` contains a “Scripts” section documenting the endpoints.
- PWA UI includes `Save Script` / `Load Script` buttons and `pwa/app.js` calls `/api/scripts`.
- `py_compile` passes for backend modules; `node --check` passes for PWA JS.

## Issues Found
- None in static verification.

## Follow-Up Manual Verification (Outside This Sandbox)
1. Apply schema and start backend:
   - `conda run -n autoappdev python -m backend.apply_schema`
   - `conda run -n autoappdev python -m backend.app`
2. Serve PWA and open UI:
   - `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
3. Create a small program on canvas and click `Save Script`; confirm response includes `script.id`.
4. Reload the page and click `Load Script` with that id; confirm script returns and canvas restores from `script.ir` steps.

