# Work Notes: 027 pwa_script_import_visualize

## Summary
- Added a new **Script** tab in the PWA right panel for importing/pasting scripts.
- Script tab can call backend parse/import endpoints and render the resulting IR as blocks on the canvas (via existing `irToProgram()` mapping).
- Added minimal UI messaging and bumped the service worker cache name so changes refresh reliably.

## Changes Made
- `pwa/index.html`
  - Added `Script` tab button (`data-tab="script"`) and a new tab view `#tab-script` with:
    - file input (`#script-file`)
    - textarea (`#script-text`)
    - buttons (`#script-parse`, `#script-import-shell`, `#script-from-blocks`)
    - inline status (`#script-msg`)
- `pwa/styles.css`
  - Updated `.tabs` to 4 columns.
  - Extended form styling to include `textarea`.
  - Added Script tab layout styles: `.scriptbar`, `.script-text`, `.script-msg`.
- `pwa/app.js`
  - Added Script tab element bindings and updated `bindTabs()` to support `script`.
  - Implemented:
    - `parseAapsToBlocks()` -> `POST /api/scripts/parse` -> IR -> canvas blocks
    - `importShellToBlocks()` -> `POST /api/scripts/import-shell` -> IR -> canvas blocks
    - `fillScriptFromBlocks()` -> generate AAPS from current blocks
    - file import handler (auto-imports `.sh` via import-shell, otherwise parses as AAPS)
  - Errors are surfaced inline with `line N:` when provided by backend.
- `pwa/service-worker.js`
  - Bumped `CACHE_NAME` to `autoappdev-shell-v7`.
- `docs/end-to-end-demo-checklist.md`
  - Added an optional Script tab import step for manual verification.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'data-tab="script"|tab-script|script-text|/api/scripts/parse|/api/scripts/import-shell' pwa/index.html pwa/app.js docs/end-to-end-demo-checklist.md

node --check pwa/app.js
node --check pwa/service-worker.js
```

