# Summary: 020 logs_panel_incremental_view

## What Changed
- Implemented an incremental Logs viewer in the PWA:
  - `pwa/app.js`: switched from `GET /api/logs/tail` (replace) to `GET /api/logs?source=...&since=...` (append) with per-source cursors.
- Added follow/pause behavior for auto-scroll:
  - `pwa/index.html`: added `#log-follow` toggle button.
  - `pwa/app.js`: `setLogFollow()` controls auto-scroll; pause prevents forced scrolling so users can select/copy.
- Minor UI adjustments:
  - `pwa/styles.css`: updated `.logbar` columns and ensured `.logview` is text-selectable.
- Bumped service worker cache name to reduce stale UI during manual verification:
  - `pwa/service-worker.js`: `CACHE_NAME` -> `autoappdev-shell-v4`.

## Why
To make the Logs panel usable as a live log viewer: incremental updates without clobbering selection, auto-follow by default, and a pause toggle to read/copy content.

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'id=\"log-follow\"' pwa/index.html
rg -n '/api/logs\\?source=' pwa/app.js
rg -n 'logSince|logInitialized|setLogFollow\\(|insertAdjacentText\\(' pwa/app.js
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Manual UI verification (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open the Logs tab:
   - Confirm new lines append while logs are being written.
   - With follow enabled (“Pause” button), view auto-scrolls to bottom.
   - Toggle follow off (“Follow” button), select/copy text without forced scrolling.
   - Toggle follow on again and confirm it snaps to bottom and continues following.

