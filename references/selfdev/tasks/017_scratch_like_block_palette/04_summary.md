# Summary: 017 scratch_like_block_palette

## What Changed
- Trimmed the visible block palette down to 6 blocks to meet the “3-6 blocks” acceptance:
  - `pwa/index.html`: removed `While` (`while_loop`), `Wait Input` (`wait_input`), and the divider from `#toolbox`.

## Why
Task 17 requires a minimal palette (3-6 blocks) while preserving the existing drag/drop workspace and JSON serialization.

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'data-block=\"' pwa/index.html | wc -l   # expect 6
rg -n 'function bindDnD\\(|dragstart|addEventListener\\(\"drop\"' pwa/app.js
rg -n 'persistProgram\\(|loadProgram\\(|btn-export|Export JSON' pwa/app.js pwa/index.html
node --check pwa/app.js
```

Manual UI check (outside this sandbox, which cannot bind ports):
1. `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`.
3. Confirm palette shows 6 blocks, dragging into the canvas adds blocks, and “Export JSON” shows the serialized program.

