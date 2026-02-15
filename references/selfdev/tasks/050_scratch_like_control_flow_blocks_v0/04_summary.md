# Summary: 050 scratch_like_control_flow_blocks_v0

## What Changed
- Added 4 Scratch-like control-flow blocks to the PWA toolbox/canvas:
  - `metatasks_generator`, `for_n_round`, `for_each_task`, `if_else`.
- Added a default nested “meta-round” template that appears on first load (when no stored program exists).
- Updated the canvas renderer to display nested container blocks with indentation and allow removing nested nodes; `Bind` remains available only on leaf step blocks.
- Updated export/import so the nested template round-trips via deterministic formats:
  - Export encodes control flow into canonical IR + AAPS v1 using `TASK.meta.meta_round_v0`, `TASK.meta.task_template_v0`, and `STEP.meta.conditional="on_debug_failure"`.
  - Import detects that meta-round IR shape and reconstructs the nested blocks.

## Why
To make the PWA’s block editor feel closer to Scratch by introducing minimal control-flow structure, while keeping AAPS v1 deterministic (no new grammar) and using existing `meta` conventions for loops/templates.

## How To Verify
Static checks (from repo root):
```bash
timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/i18n.js
timeout 10s python3 -m py_compile backend/pipeline_parser.py
```

Manual UI smoke:
1. Open the PWA with a fresh localStorage (or clear `autoappdev_program`).
2. Confirm the Program canvas shows the nested default template.
3. Script tab:
   - Click `From Blocks`, confirm the generated AAPS contains two tasks with `meta_round_v0` and `task_template_v0`.
   - Click `Parse AAPS -> Blocks`, confirm the nested structure is reconstructed.

