# Debug Notes: 021 settings_model_agent_selection

## Goal
Smallest possible verification for agent/model settings persistence wiring:
- Confirm PWA references `GET/POST /api/config`
- Confirm selects are wired and theme remains light
- Run quick syntax checks (`node --check`)

Note: This sandbox cannot bind/listen on ports, so manual end-to-end verification (confirming values persist across reload against a running backend) must be done outside this sandbox.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'id=\"agent-select\"|id=\"model-select\"' pwa/index.html
rg -n '/api/config' pwa/app.js
rg -n 'loadSettings\\(|saveSettings\\(|agentSelect|modelSelect' pwa/app.js
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
timeout 5s python3 -m py_compile backend/app.py backend/storage.py
```

Result:
- `#agent-select` and `#model-select` exist in `pwa/index.html`.
- `pwa/app.js` calls `GET /api/config` in `loadSettings()` and `POST /api/config` in `saveSettings()`.
- `bindControls()` wires change handlers for both selects.
- Default theme remains light (`<body data-theme="light">`).
- `node --check` passes for `pwa/app.js` and `pwa/service-worker.js`.
- `py_compile` passes for `backend/app.py` and `backend/storage.py` (backend unchanged, sanity check only).

## Issues Found
- None in static verification.

## Follow-Up Manual Verification (Outside This Sandbox)
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`, change Agent/Model selects.
3. Confirm persistence:
   - `curl -s http://127.0.0.1:8788/api/config | jq`
4. Reload the PWA and confirm selections restore from backend config.

