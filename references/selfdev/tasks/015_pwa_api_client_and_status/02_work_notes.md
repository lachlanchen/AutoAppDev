# Work Notes: 015 pwa_api_client_and_status

## Summary of Changes
- Added a small standalone API client module:
  - `pwa/api-client.js` exposes `window.AutoAppDevApi.requestJson()` (JSON fetch wrapper with timeout + normalized errors).
- Upgraded Status UI to show badges for Backend, DB, and Pipeline:
  - `pwa/index.html` adds a `DB` row (`#db-health`) and turns `#backend-health` + `#pipeline-status` into badge elements.
  - `pwa/styles.css` adds `.badge` + state variants (`--ok/--warn/--err/--idle/--unknown`).
- Refactored PWA status polling to use the shared client and meet the 2s update acceptance:
  - `pwa/app.js` now delegates all API calls through `window.AutoAppDevApi.requestJson()`.
  - `refreshHealth()` consumes `/api/health` and sets backend + DB badges.
  - `refreshStatus()` consumes `/api/pipeline/status` and sets the pipeline badge variant from `status.state`.
  - Health polling interval changed from 5s to 2s (pipeline was already 2s).
- Updated offline shell precache list:
  - `pwa/service-worker.js` now includes `./api-client.js` in `PRECACHE_URLS`.

## Files Changed
- Added: `pwa/api-client.js`
- Updated: `pwa/index.html`
- Updated: `pwa/styles.css`
- Updated: `pwa/app.js`
- Updated: `pwa/service-worker.js`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -s pwa/api-client.js && echo api_client_ok
rg -n "api-client\\.js" pwa/index.html
rg -n "id=\\\"db-health\\\"" pwa/index.html
rg -n "AutoAppDevApi|requestJson" pwa/api-client.js pwa/app.js
rg -n "\\./api-client\\.js" pwa/service-worker.js
rg -n "<body[^>]*data-theme=\\\"light\\\"" pwa/index.html

timeout 5s node --check pwa/api-client.js
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

