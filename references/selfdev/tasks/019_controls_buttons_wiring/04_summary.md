# Summary: 019 controls_buttons_wiring

## What Changed
- Added an inline control message area in the topbar to display pipeline control errors:
  - `pwa/index.html`: added `#ctrl-msg` next to Start/Pause/Resume/Stop.
  - `pwa/styles.css`: added `.ctrl-msg` styling (including `.ctrl-msg.is-error`).
- Disabled/enabled pipeline control buttons based on the polled pipeline state:
  - `pwa/app.js`: added `normalizePipelineState()` + `updateActionButtons()` and called it from `refreshStatus()`.
- Standardized control button behavior and error handling:
  - `pwa/app.js`: `doPipelineAction()` shows inline error text on HTTP 400 (prefers `e.data.detail`) and no longer uses `alert()` or ignores errors.
- Reduced stale shell assets during manual verification:
  - `pwa/service-worker.js`: bumped `CACHE_NAME` to `autoappdev-shell-v3`.

## Why
To make Start/Pause/Resume/Stop reflect valid pipeline transitions in the UI, and to surface backend HTTP 400 “invalid transition” errors directly in the PWA without disruptive alerts.

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'id=\"ctrl-msg\"' pwa/index.html
rg -n '\\.btn:disabled|ctrl-msg' pwa/styles.css
rg -n 'updateActionButtons\\(|normalizePipelineState\\(|doPipelineAction\\(|ctrlMsg' pwa/app.js
rg -n '/api/pipeline/(start|pause|resume|stop)' pwa/app.js
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Manual UI verification (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Confirm disabled states:
   - stopped/idle: Start enabled; Pause/Resume/Stop disabled
   - running: Pause/Stop enabled; Start/Resume disabled
   - paused: Resume/Stop enabled; Start/Pause disabled
3. Trigger an invalid transition and confirm the HTTP 400 error renders inline in `#ctrl-msg`.

