# Work Notes: 020 logs_panel_incremental_view

## Summary
- Switched the PWA Logs panel from “tail + replace” to **incremental polling + append** using `GET /api/logs?source=...&since=...`.
- Added a **follow/pause toggle** that controls auto-scroll so users can pause, select, and copy text.
- Kept changes minimal (PWA-only) and bumped the service worker cache name to reduce stale shell assets during manual verification.

## Changes Made
- `pwa/index.html`
  - Added a Logs toolbar toggle button `#log-follow` (Pause/Follow) next to `#log-refresh`.
- `pwa/styles.css`
  - Updated `.logbar` to `grid-template-columns: 1fr auto auto` to fit the new toggle button.
  - Explicitly enabled selection: `.logview { user-select: text; }`.
- `pwa/app.js`
  - Added incremental log state:
    - `logSince` cursor per source (`pipeline`, `backend`)
    - `logInitialized` per source
    - `logFollow` boolean
  - Added helpers:
    - `scrollLogsToBottom()`, `appendLogText()`, `setLogFollow()`
  - Replaced `refreshLogs()` implementation:
    - Reset mode loads the last window via `/api/logs?source=...&since=0&limit=2000` and renders the last 400 lines.
    - Incremental mode appends new lines via `/api/logs?source=...&since=<cursor>&limit=400`.
    - Auto-scrolls only when follow is enabled.
  - Wiring:
    - `#log-follow` toggles follow/pause.
    - `#log-select` change triggers a reset reload.
    - `#log-refresh` triggers a reset reload.
    - Switching to the Logs tab triggers an immediate `refreshLogs()` call.
- `pwa/service-worker.js`
  - Bumped `CACHE_NAME` to `autoappdev-shell-v4`.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'id=\"log-follow\"' pwa/index.html
rg -n '/api/logs\\?source=|/api/logs\\b' pwa/app.js
rg -n 'logSince|logInitialized|setLogFollow\\(|scrollLogsToBottom\\(|insertAdjacentText\\(' pwa/app.js
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

