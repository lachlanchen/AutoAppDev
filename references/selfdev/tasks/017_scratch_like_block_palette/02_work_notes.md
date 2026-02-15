# Work Notes: 017 scratch_like_block_palette

## Summary of Changes
- Trimmed the visible block palette to meet the “3-6 blocks” acceptance:
  - `pwa/index.html`: removed `While` (`while_loop`) and `Wait Input` (`wait_input`) blocks and the divider.

Drag/drop behavior and JSON serialization were already implemented (`pwa/app.js`) and were left unchanged.

## Files Changed
- Updated: `pwa/index.html`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Palette block count (should be 3-6; now 6)
rg -n 'data-block=\"' pwa/index.html | wc -l

# Confirm DnD + serialization hooks still exist
rg -n 'function bindDnD\\(|dragstart|addEventListener\\(\"drop\"' pwa/app.js
rg -n 'persistProgram\\(|loadProgram\\(|btn-export|Export JSON' pwa/app.js pwa/index.html

# Ensure default theme is still light
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

# JS syntax
timeout 5s node --check pwa/app.js
```

