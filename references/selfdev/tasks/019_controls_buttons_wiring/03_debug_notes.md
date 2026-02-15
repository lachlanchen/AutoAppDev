# Debug Notes: 019 controls_buttons_wiring

## Goal
Smallest possible verification for the wiring changes:
- Ensure buttons still call `/api/pipeline/start|pause|resume|stop`
- Ensure state-based disabling logic exists
- Ensure inline 400 error display is wired
- Ensure default theme remains light

Note: This sandbox environment cannot bind/listen on ports, so manual UI verification (running backend + PWA HTTP server) must be performed outside this sandbox.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'id=\"ctrl-msg\"' pwa/index.html
rg -n '\\.btn:disabled|ctrl-msg' pwa/styles.css
rg -n 'updateActionButtons\\(|normalizePipelineState\\(|doPipelineAction\\(|ctrlMsg' pwa/app.js
rg -n '/api/pipeline/(start|pause|resume|stop)' pwa/app.js
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html
```
Result:
- Found `#ctrl-msg` in `pwa/index.html`.
- Found `.btn:disabled` + `.ctrl-msg` styles in `pwa/styles.css`.
- Found `normalizePipelineState()`, `updateActionButtons()`, `doPipelineAction()`, and `els.ctrlMsg` usage in `pwa/app.js`.
- Found `/api/pipeline/start|pause|resume|stop` references in `pwa/app.js`.
- Confirmed `<body data-theme="light">` remains in `pwa/index.html`.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```
Result: exit code 0 for both checks (no syntax errors).

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s python3 -m py_compile backend/app.py backend/storage.py
```
Result: exit code 0 (sanity check; backend unchanged by this task).

## Issues Found
- None in static verification.

## Follow-Up Manual Verification (Outside This Sandbox)
1. Run backend and serve `pwa/` over HTTP (ports are blocked in this sandbox).
2. Confirm button disabled states track `GET /api/pipeline/status`:
   - stopped/idle: Start enabled; Pause/Resume/Stop disabled
   - running: Pause/Stop enabled; Start/Resume disabled
   - paused: Resume/Stop enabled; Start/Pause disabled
3. Trigger an invalid transition and confirm HTTP 400 displays inline error text in the top bar (`#ctrl-msg`), not `alert()`.

