# Plan: 034 pwa_update_readme_block

## Goal
Add an **Update README** block to the PWA palette and ensure it exports into AAPS v1 / IR v1 as an `ACTION.kind="update_readme"` with the required params. The UI must make clear which workspace README is targeted (`auto-apps/<workspace>/README.md`).

Acceptance:
- PWA palette includes an “Update README” block.
- Export to formatted script/IR includes `ACTION.kind="update_readme"` with `params.workspace` and `params.block_markdown`.
- UI clearly indicates the workspace target for the block.

## Key Constraints / Facts
- AAPS parsing enforces `STEP.block` is one of: `plan`, `work`, `debug`, `fix`, `summary`, `commit_push`:
  - `backend/pipeline_parser.py` (`ALLOWED_BLOCKS`).
- The `update_readme` spec is an **ACTION** contract:
  - `docs/common-actions.md` (`## update_readme`).
- Therefore: the PWA block must export a step whose `block` is allowed (recommended: `summary`) and include `update_readme` as the step’s action (not as `STEP.block`).

## Current State (References)
- PWA block palette + canvas:
  - `pwa/index.html` (`#toolbox`, draggable blocks)
  - `pwa/app.js` (`BLOCK_META`, `bindDnD()`, `renderProgram()`)
- Export paths:
  - `pwa/app.js`:
    - `programToIr()` emits a single `noop` action per step today.
    - `programToAapsScript()` emits `STEP {...block...}` + `ACTION {...noop...}` today.
    - `irToProgram()` currently visualizes steps only (ignores actions).
- Backend endpoint exists (not required to call in this task, but useful context):
  - `POST /api/actions/update-readme` documented in `docs/api-contracts.md`.

## Implementation Steps (Next Phase: WORK)
1. Add “Update README” to the palette
   - `pwa/index.html`:
     - Add a new draggable block to `#toolbox`:
       - `data-block="update_readme"`
       - Label: `Update README`
       - Styling: reuse an existing class (recommended: `block--summary`) to keep CSS changes minimal.

2. Teach the PWA about the new block type
   - `pwa/app.js`:
     - Add `update_readme` to `BLOCK_META` with label `Update README`.
     - Update `bindDnD()` drop handler:
       - When dropping `update_readme`, prompt for `workspace` (single path segment).
       - Validate in UI (trim; reject empty, `.`, `..`, any `/` or `\\`).
       - Store block instance as: `{ type: "update_readme", workspace: "<slug>" }`.
       - If user cancels or validation fails: do not add the block; optionally `alert()` the error.
     - Update `renderProgram()` so the block label includes the target, e.g.:
       - `Update README (auto-apps/<workspace>/README.md)`
       - This is the primary “UI makes clear target” requirement.

3. Export update_readme blocks into IR and AAPS (required)
   - `pwa/app.js`:
     - Add a small helper to build a deterministic default `block_markdown` that satisfies the spec:
       - Include a minimal status header and a required `## Philosophy` section.
       - Prefer placeholder timestamp text (e.g. `<utc-iso-timestamp>`) to keep exports stable.
       - Must not include marker strings.
     - Update `programToIr()`:
       - For non-`update_readme` blocks: keep current behavior.
       - For `update_readme` blocks:
         - Emit `STEP.block = "summary"` (allowed by backend parser).
         - Emit `ACTION.kind = "update_readme"` with:
           - `params.workspace = <workspace>`
           - `params.block_markdown = <default markdown>`
     - Update `programToAapsScript()` similarly:
       - `STEP` line uses allowed block (`summary`).
       - `ACTION` line uses `update_readme` + required params.
     - Update `programToPlan()` (optional but recommended for consistency):
       - Map `update_readme` blocks to plan step `block: "summary"` so sending plans remains compatible with the existing step-phase model.

4. (Optional but low-cost) Preserve the block when importing scripts
   - `pwa/app.js`:
     - Update `irToProgram()` to detect steps containing an `ACTION.kind === "update_readme"`:
       - Produce `{ type: "update_readme", workspace: action.params.workspace }` instead of `{ type: step.block }`.
     - This makes “Parse AAPS -> Blocks” round-trip for this action even though the canvas is mostly step-level.
   - If implemented, consider updating the Script tab hint in `pwa/index.html` to mention:
     - Update README is special-cased; other actions remain non-visualized.

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Static JS sanity
timeout 5s node --check pwa/app.js

# Ensure palette block exists and handlers reference it
timeout 10s rg -n 'data-block=\"update_readme\"|update_readme' pwa/index.html pwa/app.js

# Ensure exports contain ACTION.kind="update_readme" with required params
timeout 10s rg -n 'kind\"\\s*:\\s*\"update_readme\"|\\\"update_readme\\\"' pwa/app.js
```

Manual UI check (outside sandbox, requires serving the PWA):
1. `python3 -m backend.app`
2. `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
3. Open `http://127.0.0.1:5173/`:
   - Drag “Update README” onto the canvas; enter workspace slug.
   - Confirm the block displays `auto-apps/<workspace>/README.md`.
   - Go to Script tab and click “From Blocks”; confirm the script includes `ACTION {"kind":"update_readme", "params":{"workspace":"...", "block_markdown":"...## Philosophy..."}}`.
   - (If step 4 implemented) Paste the script back and click “Parse AAPS -> Blocks”; confirm it recreates an Update README block with the workspace shown.

## Acceptance Checklist
- [ ] `pwa/index.html` toolbox includes `data-block="update_readme"`.
- [ ] Dropping the block prompts for workspace and stores it on the block instance.
- [ ] Canvas rendering shows the target `auto-apps/<workspace>/README.md`.
- [ ] Exported IR/AAPS represent Update README as `ACTION.kind="update_readme"` with `params.workspace` + `params.block_markdown`.
- [ ] Exported AAPS remains parseable by backend (`STEP.block` stays within allowed blocks).

