# Work Notes: 050 scratch_like_control_flow_blocks_v0

## Summary of Changes
- Added 4 new control-flow blocks to the PWA toolbox and block metadata:
  - `metatasks_generator`, `for_n_round`, `for_each_task`, `if_else`.
- Kept `program` as a plain array, but allowed **nested container nodes** (children/body/if_body/else_body) to support a minimal Scratch-like control-flow view without a larger storage refactor.
- Seeded a default meta-round nested template on first load (when no `autoappdev_program` exists in localStorage).
- Updated the canvas renderer to display nested structure with indentation, hide `Bind` for containers, and allow removing nested nodes.
- Updated export/import so meta-round templates round-trip via **AAPS v1 + canonical IR**:
  - `metatasks_generator` exports as a 2-task IR using `TASK.meta.meta_round_v0` (controller) and `TASK.meta.task_template_v0` (template).
  - `if_else` exports as a `fix` step with `STEP.meta.conditional="on_debug_failure"`.
  - Import detects those meta fields and reconstructs the nested container structure.

## Files Changed
- `pwa/index.html`
  - Added draggable toolbox entries for the 4 new control-flow block types.
- `pwa/i18n.js`
  - Added English labels for the new block types.
- `pwa/app.js`
  - Extended `BLOCK_META` with the new types.
  - Added nested-program helpers (`defaultMetaRoundProgram`, `makeBlockFromType`, `flattenLeafBlocks`, etc.).
  - `loadProgram()` now seeds the default nested meta-round program if no stored program exists.
  - `renderProgram()` now recursively renders nested blocks with indentation; `Bind` is shown only for leaf step blocks.
  - Drag/drop now uses `makeBlockFromType()` to create container defaults.
  - Export now goes `program -> IR -> AAPS` (multi-task supported via `irToAapsText()`).
  - Import detects meta-round IR shape and reconstructs the nested template blocks.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

sed -n '1,200p' references/selfdev/tasks/050_scratch_like_control_flow_blocks_v0/context.md
sed -n '1,240p' references/selfdev/tasks/050_scratch_like_control_flow_blocks_v0/01_plan.md

git diff --stat
git diff -- pwa/app.js | sed -n '1,200p'
git diff -- pwa/index.html | sed -n '1,160p'
git diff -- pwa/i18n.js | sed -n '1,120p'

rg -n "function renderProgram\\b|function bindDnD\\b|function persistProgram\\b|function loadProgram\\b|function programToIr\\b|function programToAapsScript\\b|function irToProgram\\b" pwa/app.js
rg -n "fillScriptFromBlocks|exportAapsFile|exportRunnerFile|parseAapsToBlocks|importShellToBlocks" pwa/app.js

sed -n '380,760p' pwa/app.js
sed -n '1120,1380p' pwa/app.js
sed -n '1420,1545p' pwa/app.js
tail -n 80 pwa/app.js

sed -n '1,240p' docs/meta-round-templates.md
sed -n '1,200p' docs/aaps-numbering-placeholders.md
sed -n '1,240p' docs/pipeline-formatted-script-spec.md

sed -n '1,260p' backend/pipeline_parser.py
rg -n "autoappdev_plan" -S backend | head -n 50
sed -n '300,380p' backend/app.py

ls -1 pwa | head
rg -n "prog-block|prog-label|program" pwa/styles.css | head -n 50
sed -n '260,320p' pwa/styles.css

ls -l references/selfdev/tasks/050_scratch_like_control_flow_blocks_v0

node --check pwa/app.js
```

## Notes / Design Constraints
- AAPS v1 `STEP.block` remains constrained to existing palette keys (`plan|work|debug|fix|summary|commit_push`); control-flow is expressed via `meta` fields only (per `docs/meta-round-templates.md`).
- v0 UI supports nested *display* and default template seeding, but does not implement drag-to-nest editing (drops append at top level).

