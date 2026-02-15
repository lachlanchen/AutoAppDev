# Summary: 015 pwa_api_client_and_status

## What Changed
- Added `pwa/api-client.js`: a small API client wrapper exposed as `window.AutoAppDevApi.requestJson()` (JSON fetch + timeout + normalized errors).
- Updated Status UI to show badge-style values for Backend, DB, and Pipeline:
  - `pwa/index.html` adds a DB row (`#db-health`) and applies badge classes to status values.
  - `pwa/styles.css` adds `.badge` styling and variants (`--ok/--warn/--err/--idle/--unknown`).
- Refactored `pwa/app.js` to use the shared API client and set badge variants based on `/api/health` and `/api/pipeline/status`.
- Increased health polling to 2s to meet the “updates at least every 2 seconds” acceptance (pipeline polling was already 2s).
- Updated `pwa/service-worker.js` precache list to include `./api-client.js` for offline shell reloads.

## Why
To centralize API calls and make controller status clearer (including DB connectivity) while keeping the default PWA theme light.

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
test -s pwa/api-client.js
rg -n 'api-client\\.js' pwa/index.html
rg -n 'id=\"db-health\"' pwa/index.html
rg -n 'AutoAppDevApi|requestJson' pwa/api-client.js pwa/app.js
rg -n 'setInterval\\(refreshHealth, 2000\\)|setInterval\\(refreshStatus, 2000\\)' pwa/app.js
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html
node --check pwa/api-client.js
node --check pwa/app.js
```

Manual UI check (outside this sandbox, which cannot bind ports):
1. `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`
3. Confirm Backend/DB/Pipeline badges update within ~2 seconds (DB badge reflects `/api/health` -> `db.ok` / `db.time` / `db.error`).

