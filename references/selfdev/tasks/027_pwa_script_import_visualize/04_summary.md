# Summary: 027 pwa_script_import_visualize

## What Changed
- Added a new **Script** tab in the PWA right panel:
  - `pwa/index.html` includes the tab UI, textarea, file picker, and actions.
- Wired script parsing/import to block visualization:
  - `pwa/app.js` calls backend `POST /api/scripts/parse` (AAPS) and `POST /api/scripts/import-shell` (annotated `.sh`) and renders returned IR as canvas blocks (via existing `irToProgram()` mapping).
  - Supports generating an AAPS script from current blocks (“From Blocks”).
- Styled the Script tab and adjusted tabs layout:
  - `pwa/styles.css` adds Script tab styles and updates `.tabs` to 4 columns.
- Refreshed service worker cache:
  - `pwa/service-worker.js` cache name bumped to `autoappdev-shell-v7`.
- Added optional manual demo step:
  - `docs/end-to-end-demo-checklist.md` includes Script tab import steps.

## Why
To let users paste/import a pipeline script, validate/parse it via backend, and visualize it as Scratch-like blocks on the canvas, with a simple raw-script vs blocks workflow.

## How To Verify
Static checks (in this repo):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'data-tab="script"|tab-script|script-text|/api/scripts/parse|/api/scripts/import-shell' pwa/index.html pwa/app.js
timeout 10s node --check pwa/app.js
```

Manual browser smoke (requires running backend + serving `pwa/`):
1. Start backend (see `docs/end-to-end-demo-checklist.md`).
2. Serve PWA (`cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`).
3. In PWA open **Script** tab:
   - Paste `examples/pipeline_formatted_script_v1.aaps`, click `Parse AAPS -> Blocks`.
   - Paste `examples/pipeline_shell_annotated_v0.sh`, click `Import Shell -> Blocks`.
Expected: blocks appear on canvas and inline status shows success (or `line N:` on errors).

