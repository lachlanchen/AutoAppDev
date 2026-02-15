# Summary: 021 settings_model_agent_selection

## What Changed
- Persisted agent/model selection via backend config:
  - `pwa/app.js`: added `loadSettings()` (GET `/api/config`) and `saveSettings()` (POST `/api/config`) and wired them to the existing topbar selects `#agent-select` and `#model-select`.
- Reduced stale shell assets during manual verification:
  - `pwa/service-worker.js`: bumped `CACHE_NAME` to `autoappdev-shell-v5`.

## Why
So the user’s agent/model selection survives page reloads and is shared across sessions by storing it in the backend config store (`app_config` / `runtime/state.json` fallback).

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n '/api/config|loadSettings\\(|saveSettings\\(|agentSelect|modelSelect' pwa/app.js
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Manual end-to-end verification (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`, change Agent/Model in the topbar.
3. Confirm backend persisted:
   - `curl -s http://127.0.0.1:8788/api/config | jq`
4. Reload the PWA and confirm the selects restore from `GET /api/config`.

