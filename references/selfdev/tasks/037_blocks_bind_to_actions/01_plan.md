# Plan: 037 blocks_bind_to_actions

## Goal
Allow a PWA block instance (a STEP on the canvas) to **reference an action definition** from the action registry (by `id` or a future `slug`) and ensure exports (IR + AAPS script) **include that reference**, while remaining backwards compatible for existing “simple” blocks.

Acceptance:
- Blocks can store an action reference (id/slug) in the UI
- Exported IR/AAPS include the reference
- Blocks without a reference export exactly as before (backwards compatible)

## Current State (References)
- Action registry API (definitions):
  - `backend/app.py` (`ActionsHandler`, `ActionHandler`)
  - `docs/api-contracts.md` (`GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`)
- PWA program model and exports:
  - `pwa/app.js`
    - `program` is an array of block objects: `{ type: "work" }`, `{ type: "update_readme", workspace: "..." }`
    - Export:
      - `programToIr()` builds `autoappdev_ir` (one ACTION per STEP today; mostly `{kind:"noop"}`)
      - `programToAapsScript()` writes `STEP ...` + `ACTION ...` lines
    - Import:
      - `irToProgram()` converts IR back to blocks (special-cases `update_readme`)
- Backend AAPS parser supports optional `ACTION.meta` (passes through):
  - `backend/pipeline_parser.py` (`meta` is accepted as object; unknown keys allowed)

## Data Model (PWA)
Extend each block instance in `program` with an optional action reference:
```js
{ type: "work", action_ref: { id: 12 } }
// or:
{ type: "work", action_ref: { slug: "my_action" } }
```

Notes:
- Keep existing fields unchanged (`type`, `workspace` for `update_readme`).
- Do not require the Actions tab to be opened first; binding should fetch list as-needed.

## Wire-Up Strategy (Minimal UI)
Add a small per-block “Bind” affordance in the Program canvas list.

### 1) Canvas UI: Bind/Clear Action Ref
Edit `pwa/app.js`:
- Update `renderProgram()` to include a new button on each `.prog-block` row (next to remove):
  - label: `Bind`
  - click behavior: open `prompt()` asking for an action ref (id or slug); blank clears
- Parsing rules:
  - If input matches `^[0-9]+$`, store as `{ id: Number(...) }`
  - Else store as `{ slug: "<trimmed>" }` (limit length, e.g. 200 chars; reject empty)
  - Clearing: delete `block.action_ref`
- Display:
  - Update `formatProgramBlockLabel()` so bound blocks show a suffix like:
    - `Work -> #12 My action title` (title resolved if available)
    - `Work -> slug: my_action` (when slug binding used)
- Action title lookup:
  - Reuse the in-memory list from the Actions tab (`actionsIndex`) if present.
  - If `actionsIndex` is empty, fetch `GET /api/actions?limit=200` once before showing the prompt so the user can see a short list of ids/titles in the prompt text.

Keep it minimal:
- No new “block property panel” yet; use `prompt()` and inline label suffix.
- Do not add binding UI for `update_readme` block in v0 (it already expands to a concrete executor action).

### 2) Minimal CSS (Only If Needed)
If adding a button in the program rows requires styling:
- Edit `pwa/styles.css` to add a `.prog-bind` button style based on `.prog-remove` (small, consistent on colored blocks).

## Export Changes (IR + AAPS)
Edit `pwa/app.js`:

### 3) Export: Include `meta.action_ref`
Update `programToIr()` and `programToAapsScript()`:
- For “simple” blocks (plan/work/debug/fix/summary/commit_push):
  - Keep the existing default `ACTION` as-is (`{kind:"noop", params:{}}`)
  - If `block.action_ref` exists, attach:
    - `ACTION.meta = { action_ref: { id: 12 } }` or `{ action_ref: { slug: "..." } }`
- For `update_readme`:
  - Keep the current behavior (STEP.block becomes `"summary"`, ACTION.kind `"update_readme"` with params).
  - Ignore `action_ref` for this block type in v0.

Backwards compatibility:
- If no `action_ref` on the block, export is byte-for-byte identical to today’s output for that block type.

## Import Changes (IR -> Blocks)
Edit `pwa/app.js`:

### 4) Import: Preserve `meta.action_ref` Into Block Instances
Update `irToProgram()`:
- For each STEP, inspect `step.actions` and find the first action where:
  - `action.meta.action_ref` exists and is `{id:number}` or `{slug:string}`
- When creating the block instance for that STEP, carry it into the program:
  - `{ type: step.block, action_ref: ... }`
- Preserve existing `update_readme` detection first (special-case stays highest priority).

## Docs (Small, Optional But Recommended)
Edit `docs/pipeline-formatted-script-spec.md`:
- Document optional `ACTION.meta.action_ref`:
  - Shape: `{ "id": 123 }` or `{ "slug": "my_action" }`
  - Example AAPS line showing meta:
    - `ACTION {"id":"a1","kind":"noop","meta":{"action_ref":{"id":1}}}`
- Clarify that engines may resolve this reference to an action registry entry, but the formatted script remains deterministic and execution-agnostic.

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Static JS syntax check
timeout 10s node --check pwa/app.js

# Ensure action_ref appears where expected
timeout 10s rg -n \"action_ref|meta\\s*:\\s*\\{\\s*action_ref\" pwa/app.js

# If docs updated:
timeout 10s rg -n \"action_ref\" docs/pipeline-formatted-script-spec.md
```

## Acceptance Checks
Manual smoke (with backend running so the registry list can be fetched):
1. Open PWA, create a simple block program (e.g. `Work`).
2. Click `Bind` on a block and enter a valid action id (e.g. `1`).
3. Export AAPS (`From Blocks` / `Download AAPS`) and confirm the emitted `ACTION ...` JSON includes:
   - `"meta":{"action_ref":{"id":1}}`
4. Paste that AAPS into Script tab and `Parse AAPS -> Blocks`:
   - The corresponding block on the canvas shows it is bound (label suffix).
5. Clear binding (Bind -> blank) and confirm export no longer includes `meta.action_ref`.
6. Confirm a program without any bindings exports exactly as before (still `noop` actions, no new fields).

