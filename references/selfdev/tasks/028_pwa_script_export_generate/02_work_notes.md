# Work Notes: 028 pwa_script_export_generate

## Summary
- Added Script tab export actions to download:
  - a generated AAPS v1 formatted script (`.aaps`)
  - a generated runnable shell runner (`.sh`) that respects `runtime/PAUSE` and embeds `# AAPS:` lines for re-import.
- Bumped PWA service worker cache so the new UI/JS updates reliably.
- Updated the end-to-end demo checklist with optional export verification steps.

## Changes Made
- `pwa/index.html`
  - Added `Download AAPS` (`#script-download-aaps`) and `Download Runner` (`#script-download-runner`) buttons in the Script tab.
- `pwa/app.js`
  - Added client-side download helpers (`downloadTextFile`, `sanitizeFileBase`).
  - Implemented `generateRunnerScript()` (safe bash runner with pause flag + embedded AAPS as `# AAPS:` lines).
  - Implemented `exportAapsFile()` and `exportRunnerFile()` and wired them in `bindControls()`.
- `pwa/service-worker.js`
  - Bumped `CACHE_NAME` to `autoappdev-shell-v8`.
- `docs/end-to-end-demo-checklist.md`
  - Added optional Script tab export steps (Download AAPS/Runner).

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n "script-download-aaps|script-download-runner|exportAapsFile\\(|exportRunnerFile\\(|generateRunnerScript\\(" pwa/index.html pwa/app.js

timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/service-worker.js
```

