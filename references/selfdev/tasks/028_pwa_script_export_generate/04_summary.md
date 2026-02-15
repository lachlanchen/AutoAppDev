# Summary: 028 pwa_script_export_generate

## What Changed
- Added PWA Script tab export buttons:
  - `pwa/index.html`: `Download AAPS` and `Download Runner`
- Implemented client-side generation + downloads:
  - `pwa/app.js`:
    - generates AAPS v1 from current blocks and downloads it as `.aaps`
    - generates a safe runnable bash runner (`.sh`) that respects `runtime/PAUSE` and embeds the AAPS as `# AAPS:` lines for re-import
- Refreshed PWA shell cache:
  - `pwa/service-worker.js`: cache bumped to `autoappdev-shell-v8`
- Updated manual demo checklist:
  - `docs/end-to-end-demo-checklist.md`: optional export verification steps

## Why
To let users export their block-based pipeline as a standardized formatted script and a runnable driver directly from the PWA, without adding backend complexity.

## How To Verify
Static checks (in this repo):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n "script-download-aaps|script-download-runner|exportAapsFile\\(|exportRunnerFile\\(|generateRunnerScript\\(" pwa/index.html pwa/app.js
timeout 10s node --check pwa/app.js
```

Manual browser smoke (requires serving `pwa/` and opening the PWA):
1. Add a few blocks to the canvas.
2. Open **Script** tab.
3. Click `Download AAPS` and confirm a `.aaps` file downloads containing `AUTOAPPDEV_PIPELINE 1` and `TASK/STEP/ACTION` lines.
4. Click `Download Runner` and confirm a `.sh` file downloads with pause logic using `runtime/PAUSE` and embedded `# AAPS:` lines.

