# Work Notes: 021 settings_model_agent_selection

## Summary
- Wired the existing Agent/Model selects in the PWA topbar to backend config (`GET/POST /api/config`).
- On boot, the PWA loads persisted `agent`/`model` config and applies it to the selects (when the option exists and is enabled).
- On selection changes, the PWA persists `{ agent, model }` back to the backend so it survives reload.
- Bumped the PWA shell service-worker cache name to reduce stale `app.js` during manual verification.

## Changes Made
- `pwa/app.js`
  - Added `els.agentSelect` and `els.modelSelect`.
  - Added `loadSettings()` and `saveSettings()` using `GET/POST /api/config`.
  - Added change listeners for both selects in `bindControls()`.
  - Called `loadSettings()` during `boot()`.
- `pwa/service-worker.js`
  - Bumped `CACHE_NAME` to `autoappdev-shell-v5`.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'id=\"agent-select\"|id=\"model-select\"' pwa/index.html
rg -n 'agentSelect|modelSelect|/api/config|loadSettings\\(|saveSettings\\(' pwa/app.js
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
timeout 5s python3 -m py_compile backend/app.py backend/storage.py
```

