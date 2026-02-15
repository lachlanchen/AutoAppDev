# Summary: 024 pipeline_script_storage_api

## What Changed
- Added Postgres persistence for pipeline scripts + optional IR:
  - `backend/schema.sql`: new `pipeline_scripts` table.
  - `backend/storage.py`: CRUD helpers for scripts (`create/get/list/update/delete`).
- Added backend CRUD API:
  - `backend/app.py`: new handlers and routes:
    - `GET/POST /api/scripts`
    - `GET/PUT/DELETE /api/scripts/<id>`
- Added minimal PWA save/load wiring:
  - `pwa/index.html`: `Save Script` / `Load Script` buttons.
  - `pwa/app.js`: generates deterministic AAPS + `autoappdev_ir` skeletons from the current canvas and saves/loads via `/api/scripts` (restores canvas from `script.ir` steps when present).
- Documented the endpoints:
  - `docs/api-contracts.md`: new “Scripts” section.
- Bumped service worker cache name to reduce stale PWA assets:
  - `pwa/service-worker.js`: `CACHE_NAME` -> `autoappdev-shell-v6`.

## Why
To support storing and reloading pipeline scripts and their IR by id, enabling the controller to move beyond transient in-browser programs toward persisted, shareable pipelines.

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'create table if not exists pipeline_scripts' backend/schema.sql
rg -n '/api/scripts' backend/app.py
timeout 5s python3 -m py_compile backend/app.py backend/storage.py
timeout 5s node --check pwa/app.js
```

Manual end-to-end verification (outside this sandbox, which cannot bind ports):
1. Apply schema + start backend:
   - `conda run -n autoappdev python -m backend.apply_schema`
   - `conda run -n autoappdev python -m backend.app`
2. Serve PWA and open UI:
   - `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
3. Drag blocks onto canvas, click `Save Script`, confirm response includes `script.id`.
4. Reload the page, click `Load Script`, enter that id, confirm it loads and restores the canvas from `script.ir`.

