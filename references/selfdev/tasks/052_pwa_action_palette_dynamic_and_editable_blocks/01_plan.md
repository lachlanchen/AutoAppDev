# Plan: 052 pwa_action_palette_dynamic_and_editable_blocks

## Goal
Make the PWA feel “Scratch-like” by turning the **action registry** into a **dynamic draggable palette**, while keeping the existing step-block architecture:
- Toolbox includes **built-in actions + user-created actions** (from `GET /api/actions`) as draggable blocks.
- Dropping an action creates a canvas step block **pre-bound** to that action (`block.action_ref`).
- Canvas blocks are editable:
  - action binding (rebind/clear) for leaf step blocks
  - parameters for blocks that have them (ex: `update_readme.workspace`, meta-round loop params).
- Built-in actions are readonly; editing them in the PWA follows clone-on-edit behavior already implemented (Task 051), and the palette reflects updated actions after refresh.

Acceptance:
- PWA toolbox is generated from Action library + built-ins.
- User-created actions appear as draggable blocks.
- Blocks are editable (binding + parameters).
- Editing a built-in action clones then edits the clone.

## Current State (Relevant Files)
- Toolbox is static HTML:
  - `pwa/index.html` `#toolbox` contains fixed blocks (plan/work/debug/...) plus control-flow blocks (Task 050).
- Drag/drop and program rendering:
  - `pwa/app.js`: `bindDnD()` reads `data-block` and pushes `{ type }` (or `update_readme` prompt).
  - `pwa/app.js`: `renderProgram()` shows blocks and supports `Bind` via a prompt for leaf step blocks.
  - `pwa/app.js`: nested container blocks exist (Task 050), but their parameters are not editable in the UI.
- Actions library editor:
  - `pwa/app.js`: `refreshActionsList()`, `loadActionDefinition()`, `saveActionFromForm()`.
  - Backend built-ins + clone endpoint (Task 051):
    - `GET /api/actions` returns builtins + DB actions, with `readonly` field.
    - `POST /api/actions/<id>/clone` clones readonly builtin into DB.
    - `PUT`/`DELETE` builtin returns `403 { error: "readonly" }`.

## Design (Minimal + Incremental)
Keep the “program = step blocks” model:
- Action palette blocks are *shortcuts* that create a normal leaf step block (ex: default `type: "work"`) and set `action_ref: { id }`.
- Built-in action blocks can map to a more appropriate default step type by ID convention (Plan -> `plan`, Work -> `work`, etc). User-created actions default to `work` initially.
- Editing “parameters” is prompt-based (consistent with existing `Bind`/`update_readme` flows) to keep UI changes small.

## Implementation Steps (Next Phase: WORK)

### 1) Add a Dynamic “Actions Palette” Render Pass
Edit `pwa/app.js`:
- Add `renderActionPalette()` that:
  - uses `actionsIndex` (populated from `/api/actions?limit=200`) to build draggable `.block` DOM nodes for each action
  - includes both builtins (`readonly:true`) and DB actions (`readonly:false`)
  - adds a visual divider before the dynamic action blocks (reuse `.divider` from `pwa/styles.css`)
  - sets data attributes to differentiate action blocks, e.g.:
    - `data-palette-kind="action"`
    - `data-action-id="<id>"`
    - optionally `data-default-step="plan|work|..."` (builtin mapping)
- Call `renderActionPalette()`:
  - after `refreshActionsList()` succeeds (so palette updates when actions change)
  - once during `boot()` (so palette appears even before opening the Actions tab)

Notes:
- If `/api/actions` fails (backend down), keep existing static toolbox as a fallback and just don’t append the dynamic section.

### 2) Update Drag/Drop Wiring to Support Dynamically Created Blocks
Edit `pwa/app.js` `bindDnD()`:
- Switch from “attach listeners to existing `.toolbox .block` nodes” to **event delegation** on `els.toolbox` so dynamically injected blocks are draggable without re-binding.
- Encode drag payload so drop handler can distinguish:
  - normal palette block types (`plan`, `work`, `metatasks_generator`, ...)
  - action palette blocks (action id)
  Example approach:
  - `text/plain` = `block:<type>` or `action:<id>` (simple string protocol)
- Update drop handler:
  - For `action:<id>`:
    - choose a default step type:
      - builtin id mapping -> phase type
      - otherwise default to `"work"`
    - create a new leaf block: `{ type: <stepType>, action_ref: { id: <id> } }`
    - append to top-level `program` (keep v0 “no drag-to-nest” scope)
  - Preserve existing special handling:
    - `update_readme` prompts for workspace slug
    - control-flow blocks use `makeBlockFromType()`

### 3) Make Canvas Blocks Editable (Binding + Parameters)
Edit `pwa/app.js` `renderProgram()`:
- Keep current `Bind` flow for leaf step blocks (already satisfies “editable binding”).
- Add a minimal `Edit` button for blocks that have parameters:
  - `update_readme`: edit `workspace` via existing workspace prompt + validation (`parseWorkspaceSlug()`), then persist.
  - `metatasks_generator`: prompt for:
    - `n_round` (int, clamp 1..10)
    - `task_list_path` (string, non-empty, repo-relative-ish)
    - keep children structure; if `n_round` changes, also update nested `for_n_round.n_round` and pad/truncate its `body` to match the new N.
  - `for_n_round`: prompt for `n_round`; pad/truncate `body` to match.
  - `if_else`: prompt for condition (v0 default `on_debug_failure`), and keep else-body empty.
- Add English-only i18n keys for the new button/prompt labels:
  - `pwa/i18n.js` (en pack): `ui.btn.edit`, `ui.prompt.n_round`, `ui.prompt.task_list_path`, `ui.prompt.if_condition`
  - (Other languages can fallback via `t()`.)

Optional small enhancement (if still small):
- For leaf step blocks, allow changing the *phase* type (plan/work/...) via an `Edit` prompt (only for leaf step blocks).

### 4) Ensure Built-in Clone-On-Edit is Reflected in Palette
No new backend work expected (Task 051 already provides clone endpoint).
Edit `pwa/app.js` to ensure palette refresh happens after:
- create/update/delete action flows (already call `refreshActionsList()`; ensure `renderActionPalette()` is invoked from there)
- clone-on-save flows (Task 051 logic in `saveActionFromForm()`)

### 5) (If Needed) Small Docs Note
If UX changes are user-visible enough, add a short note to `pwa/README.md`:
- toolbox includes dynamically loaded Actions from backend
- dragging an action creates a bound step block

## Verification (DEBUG/VERIFY Phase)
Static checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/i18n.js
```

Manual smoke (with backend running):
1. Open PWA:
  - toolbox shows dynamic action blocks (builtins + any DB actions)
2. Drag a user-created action onto canvas:
  - a step appears with label showing binding (`-> #<id> <title>`)
3. Edit block parameters:
  - update_readme workspace can be changed via Edit
  - meta-round `n_round` and `task_list_path` can be changed via Edit and the nested round body resizes
4. Built-in action clone-on-edit:
  - select a builtin action in Actions tab, change prompt/title, click Save
  - confirms “cloned and saved”, and the palette now includes the cloned editable action

## Acceptance Checklist
- [ ] Toolbox shows actions fetched from `/api/actions` (includes built-ins).
- [ ] Dragging an action adds a new bound block on the canvas.
- [ ] Leaf step blocks can be rebound/cleared (binding editable).
- [ ] Parameterized blocks (`update_readme`, meta-round containers) are editable in the canvas.
- [ ] Editing a built-in action results in a cloned editable copy (no direct mutation).

