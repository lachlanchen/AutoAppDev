# Summary: 052 pwa_action_palette_dynamic_and_editable_blocks

## What Changed
- PWA toolbox now appends a dynamic **Actions palette** generated from `GET /api/actions` (built-ins + user actions) and makes each action draggable (`pwa/app.js`).
- Dragging an action onto the canvas creates a normal step block pre-bound via `action_ref: { id }`, using a builtin-id-to-step-type mapping where available (otherwise defaults to `work`) (`pwa/app.js`).
- Canvas blocks gained a minimal prompt-based `Edit` flow for block parameters:
  - `update_readme.workspace`
  - `metatasks_generator.n_round` + `metatasks_generator.task_list_path` (also syncs nested `for_n_round` and resizes its body)
  - `for_n_round.n_round` (resizes body; syncs parent meta generator when nested)
  - `if_else.condition` (v0 only: `on_debug_failure`)
  (`pwa/app.js`)
- Actions are fetched once on boot so the palette appears without opening the Actions tab (`pwa/app.js`).
- Added English i18n keys for the new Edit button and prompts (`pwa/i18n.js`).
- Documented the dynamic Actions palette behavior in `pwa/README.md`.

## Why
To make the PWA feel Scratch-like by turning the action registry into a dynamic draggable palette, while keeping the existing “step blocks + optional action_ref binding” architecture and adding minimal editability for block parameters.

## How To Verify
Static checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/i18n.js
```

Manual smoke (with backend + PWA running, e.g. via `scripts/run_autoappdev_tmux.sh`):
1. Open the PWA; confirm the toolbox shows an appended list of draggable Actions (built-ins marked readonly, disabled marked disabled).
2. Drag an action into the canvas; confirm a step block is created with `-> #<id> <title>` binding.
3. Click `Edit` on `update_readme`, `metatasks_generator`, `for_n_round`, or `if_else` blocks; confirm the label updates and the program persists.
4. In Actions tab, edit a builtin action and click Save; confirm clone-on-edit creates an editable copy and the palette refresh includes it.

