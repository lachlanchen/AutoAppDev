# Plan: 015 pwa_api_client_and_status

## Goal
Add a small, centralized PWA API client module and upgrade the Status UI to show:
- Backend health
- DB status (from `/api/health.db`)
- Pipeline state badge

Acceptance:
- PWA has a small API client module.
- Status area shows health, DB status, and a pipeline state badge.
- Status updates at least every 2 seconds (polling is fine; push is optional).
- Default PWA theme remains light.

## Current State (References)
- PWA shell + layout already exist:
  - `pwa/index.html` has the Status rows: `#backend-health`, `#pipeline-status`, `#pipeline-pid`.
  - `pwa/styles.css` defines light theme tokens and Status row layout (`.kv`, `.k`, `.v`).
- API calls are currently inline inside `pwa/app.js`:
  - `async function api(path, opts = {})` and direct calls to `/api/health`, `/api/pipeline/status`, `/api/logs/tail`, etc.
  - Polling: `refreshStatus()` is every 2s; `refreshHealth()` is every 5s.
- Backend endpoints already exist:
  - `GET /api/health` returns `{ ok: true, db: { ok, time|error } }` (`backend/app.py` `HealthHandler`).
  - `GET /api/pipeline/status` returns `{ status: { state, running, pid, run_id } }` (`backend/app.py` `PipelineStatusHandler`).

## Approach (Minimal / Incremental)
1. Extract the existing fetch wrapper into a small standalone file (a “module” in the sense of a dedicated file):
   - Add `pwa/api-client.js` that exposes a single global (no bundler / no ES modules required).
2. Update Status UI to use badge styling and add a DB row.
3. Make health + pipeline polling cadence consistent with acceptance (<= 2s).
4. Keep the default theme light and avoid any layout redesign.
5. Preserve offline-shell behavior by updating the service worker precache list to include the new JS asset.

## Implementation Steps (Next Phase)
1. Add `pwa/api-client.js` (new file).
   - Read config from `window.__AUTOAPPDEV_CONFIG__` (already set in `pwa/index.html`).
   - Compute `API_BASE_URL` with the existing default (`http://127.0.0.1:8788`).
   - Provide a single request helper:
     - `requestJson(path, opts)` that:
       - Calls `fetch(`${API_BASE_URL}${path}`, ...)`.
       - Sets JSON content-type header.
       - Parses JSON response (best-effort).
       - Throws a normalized Error when `!res.ok` (use `{error|detail}` fields if present).
       - (Optional but small) include an AbortController timeout (ex: 4s) to avoid hanging UI.
   - Export it as `window.AutoAppDevApi = { requestJson }` (and optionally convenience methods like `getHealth`, `getPipelineStatus` if it keeps `pwa/app.js` cleaner).

2. Wire the new API client script into `pwa/index.html`.
   - Add `<script src="api-client.js" defer></script>` before `<script src="app.js" defer></script>`.
   - Update Status markup:
     - Change the existing backend + pipeline value nodes to badges by adding CSS classes (keep IDs unchanged):
       - `#backend-health` becomes `class="v badge badge--unknown"`.
       - `#pipeline-status` becomes `class="v badge badge--unknown"`.
     - Add a new Status row for DB:
       - Key label: `DB`
       - Value node: `id="db-health"` with `class="v badge badge--unknown"` and initial text `unknown`.
   - Keep `<body data-theme="light">` intact.

3. Add minimal badge styles in `pwa/styles.css`.
   - Add `.badge` as a pill:
     - `display: inline-flex; align-items: center; justify-content: center;`
     - `padding`, `border-radius`, `border`, `font-size`.
   - Add state variants using existing theme variables:
     - `.badge--ok` (blue-tinted or greenish using `--b-debug`).
     - `.badge--warn` (yellow using `--b-plan`).
     - `.badge--err` (red using `--red`).
     - `.badge--unknown` / `.badge--idle` (muted).
   - Ensure colors work in light theme (default) and degrade reasonably in dark theme without changing the default.

4. Refactor `pwa/app.js` to use the API client module.
   - Remove the inline `api()` function (or keep it only as an alias to `window.AutoAppDevApi.requestJson`).
   - Replace calls like `api("/api/health")` with the centralized request helper.
   - Upgrade `refreshHealth()`:
     - On success: set backend badge to ok.
     - Use the `/api/health` response to set DB badge:
       - If `data.db.ok`: badge ok, text `ok`, and set `title` to include `db.time`.
       - Else: badge err, text `error`, and set `title` to include `db.error`.
     - On failure: backend badge down/err, DB badge unknown.
   - Upgrade `refreshStatus()`:
     - Read `data.status.state` and map to badge variants:
       - `running` -> ok
       - `paused` -> warn
       - `failed` -> err
       - `completed|stopped|idle` -> idle/unknown
     - Keep updating `#pipeline-pid` as now.
   - Polling cadence:
     - Change health polling from 5s to 2s (or unify with status polling so all badges update at <= 2s).
     - Keep existing 2s status polling or reduce to a single `setInterval(refreshAll, 2000)` to avoid duplicate timers.

5. Update `pwa/service-worker.js` precache list.
   - Add `./api-client.js` to `PRECACHE_URLS` so offline reloads still have the full shell JS available.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -s pwa/api-client.js
rg -n 'api-client\\.js' pwa/index.html
rg -n 'id=\"db-health\"' pwa/index.html
rg -n 'AutoAppDevApi|requestJson' pwa/api-client.js pwa/app.js
rg -n '\\./api-client\\.js' pwa/service-worker.js

# Ensure default theme is still light.
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

# Syntax checks
node --check pwa/api-client.js
node --check pwa/app.js
```

Manual browser verification (required to validate real badge behavior):
1. Serve the PWA (`cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`).
2. Open `http://127.0.0.1:5173/`.
3. Confirm Status shows three badges: Backend, DB, Pipeline.
4. Confirm badges update within 2 seconds after backend/DB/pipeline state changes.
5. Optional: DevTools -> Application -> Service Workers -> ensure SW still installs after adding `api-client.js`.

## Acceptance Checklist
- [ ] `pwa/api-client.js` exists and `pwa/app.js` uses it (no duplicated fetch wrapper logic).
- [ ] Status UI shows:
  - [ ] Backend badge (ok/down)
  - [ ] DB badge (ok/error/unknown) populated from `/api/health.db`
  - [ ] Pipeline state badge from `/api/pipeline/status.status.state`
- [ ] Status refresh interval is <= 2 seconds for the badges (polling).
- [ ] Default light theme remains the default (`<body data-theme="light">`).

