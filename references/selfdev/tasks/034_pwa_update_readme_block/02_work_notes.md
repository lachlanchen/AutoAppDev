# Work Notes: 034 pwa_update_readme_block

## Summary
- Added a new PWA palette block “Update README”.
- The block captures a workspace slug, renders the explicit target `auto-apps/<workspace>/README.md` on the canvas, and exports to AAPS/IR as `ACTION.kind="update_readme"` with required params.

## Changes Made
- `pwa/index.html`
  - Added toolbox entry: `data-block="update_readme"` (“Update README”).
- `pwa/app.js`
  - Added `update_readme` to `BLOCK_META`.
  - On drop: prompts for `workspace` slug, validates it, stores `{ type: "update_readme", workspace }`.
  - Canvas rendering shows: `Update README (auto-apps/<workspace>/README.md)`.
  - Export:
    - `programToIr()` and `programToAapsScript()` emit `STEP.block="summary"` plus `ACTION.kind="update_readme"` with `params.workspace` and `params.block_markdown` (includes `## Philosophy`).
    - `programToPlan()` maps `update_readme` blocks to plan step `block: "summary"` (compat with allowed step blocks).
  - Import (round-trip helper): `irToProgram()` detects `ACTION.kind="update_readme"` and reconstructs an `update_readme` block with `workspace`.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 5s node --check pwa/app.js && echo "node_check_ok"

timeout 10s rg -n 'data-block=\"update_readme\"|update_readme' pwa/index.html pwa/app.js
timeout 10s rg -n 'block_markdown' pwa/app.js
```

