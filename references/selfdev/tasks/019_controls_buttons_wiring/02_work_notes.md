# Work Notes: 019 controls_buttons_wiring

## Summary
- Added an inline control message area in the top bar to display pipeline control errors (notably HTTP 400 invalid transitions).
- Disabled/enabled Start/Pause/Resume/Stop buttons based on the polled pipeline state from `GET /api/pipeline/status`.
- Standardized pipeline control button handlers so errors are no longer ignored (Pause/Resume/Stop) and Start no longer uses `alert()`.
- Bumped the PWA shell service-worker cache name to avoid stale `index.html`/`app.js`/`styles.css` during manual verification.

## Changes Made
- `pwa/index.html`
  - Added `<span class="ctrl-msg" id="ctrl-msg" aria-live="polite"></span>` inside the `.controls` topbar area.
- `pwa/styles.css`
  - Added disabled button styling (`.btn:disabled`, `.btn:disabled:active`).
  - Added `.ctrl-msg` styling, including `.ctrl-msg:empty { display: none; }` to avoid extra layout gap when no message is present.
- `pwa/app.js`
  - Added `els.ctrlMsg`.
  - Added helpers: `normalizePipelineState()`, `updateActionButtons()`, `setCtrlMsg()`, `doPipelineAction()`.
  - Updated `refreshStatus()` to call `updateActionButtons()` (and default to "stopped" on fetch failure).
  - Rewired Start/Pause/Resume/Stop click handlers to use `doPipelineAction()` and show inline error text (prefers `e.data.detail` on HTTP 400).
  - Set initial control state to "stopped" on boot (until the first status poll).
- `pwa/service-worker.js`
  - Bumped `CACHE_NAME` from `autoappdev-shell-v2` to `autoappdev-shell-v3`.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
ls

sed -n '1,200p' references/selfdev/tasks/019_controls_buttons_wiring/01_plan.md
sed -n '1,200p' references/selfdev/tasks/019_controls_buttons_wiring/context.md

sed -n '1,220p' pwa/index.html
sed -n '1,260p' pwa/styles.css
sed -n '260,520p' pwa/styles.css
sed -n '1,260p' pwa/app.js
sed -n '260,520p' pwa/app.js
sed -n '1,220p' pwa/service-worker.js

rg -n "class Pipeline" backend/app.py | head
sed -n '250,520p' backend/app.py
rg -n "def get_latest_status" -S backend | head
sed -n '200,300p' backend/storage.py

ls references/selfdev/tasks/019_controls_buttons_wiring
```

