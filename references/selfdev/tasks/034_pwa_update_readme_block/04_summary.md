# Summary: 034 pwa_update_readme_block

## What Changed
- Added an “Update README” block to the PWA palette:
  - `pwa/index.html`: new toolbox block `data-block="update_readme"`.
  - `pwa/app.js`: block captures a workspace slug on drop, renders the explicit target `auto-apps/<workspace>/README.md` on the canvas, and round-trips from imported IR when an `update_readme` action is present.
- Updated exports so the block becomes a real action in scripts:
  - `programToIr()` / `programToAapsScript()` emit `STEP.block="summary"` (backend-parseable) plus `ACTION.kind="update_readme"` with required `params.workspace` and `params.block_markdown` (includes `## Philosophy`).

## Why
To let users author the common `update_readme` action from the UI while keeping AAPS `STEP.block` values within the backend’s allowed set and making the target README path explicit.

## How To Verify (Smallest Smoke)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 5s node --check pwa/app.js
timeout 10s rg -n 'data-block=\"update_readme\"' pwa/index.html
timeout 10s rg -n 'update_readme|block_markdown|Workspace slug' pwa/app.js
```

Manual UI check (outside sandbox):
1. Serve PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`, drag “Update README” onto the canvas, enter a workspace slug.
3. Confirm the block label shows `auto-apps/<workspace>/README.md`.
4. Script tab: click “From Blocks”; confirm the generated AAPS contains `ACTION {"kind":"update_readme", ... "block_markdown":"...## Philosophy..."}`.

