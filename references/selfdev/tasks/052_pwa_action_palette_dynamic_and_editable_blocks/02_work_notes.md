# Work Notes: 052 pwa_action_palette_dynamic_and_editable_blocks

## Summary of Changes
- Added a dynamic **Actions palette** to the PWA toolbox, sourced from `GET /api/actions` (built-ins + user actions).
- Enabled drag/drop of action palette items to create a normal step block pre-bound via `action_ref`.
- Added a minimal in-canvas `Edit` flow for parameterized blocks:
  - `update_readme.workspace`
  - `metatasks_generator.n_round` + `metatasks_generator.task_list_path` (also syncs nested `for_n_round`)
  - `for_n_round.n_round` (resizes round body and syncs parent meta generator when nested)
  - `if_else.condition` (v0 supports only `on_debug_failure`)
- Ensured the palette is loaded once on boot (so it appears without opening the Actions tab).
- Added English i18n keys for the new Edit button and prompts.
- Documented the dynamic Actions palette behavior in `pwa/README.md`.

## Implementation Details
- Kept the existing “program = step blocks” model:
  - Action palette items are shortcuts that drop a leaf step block `{ type: <phase>, action_ref: { id } }`.
  - Built-in action IDs are mapped to sensible default step types (plan/work/debug/fix/summary/commit_push); other actions default to `work`.
- Drag/drop uses a small string protocol in `text/plain`:
  - `block:<type>` for static toolbox blocks
  - `action:<id>` for dynamically injected action items
- Edit UI is prompt-based to stay consistent with existing `Bind` and `update_readme` flows and keep the change small.

## Files Changed
- Updated: `pwa/app.js`
- Updated: `pwa/i18n.js`
- Updated: `pwa/README.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

sed -n '1,200p' references/selfdev/tasks/052_pwa_action_palette_dynamic_and_editable_blocks/context.md
sed -n '1,200p' references/selfdev/tasks/052_pwa_action_palette_dynamic_and_editable_blocks/01_plan.md

rg -n "renderActionPalette|BUILTIN_ACTION_ID_TO_STEP_TYPE|defaultStepTypeForActionId|action:<" -n pwa/app.js
sed -n '250,360p' pwa/app.js
sed -n '1080,1280p' pwa/app.js
sed -n '1660,1880p' pwa/app.js

rg -n "function boot\\b|boot\\(" pwa/app.js | head
sed -n '2060,2145p' pwa/app.js

rg -n "function renderProgram\\b" -n pwa/app.js
sed -n '400,620p' pwa/app.js

rg -n "function makeBlockFromType\\b" -n pwa/app.js
sed -n '180,260p' pwa/app.js

rg -n "for_n_round"
sed -n '620,920p' pwa/app.js

sed -n '1,240p' pwa/i18n.js
rg -n "function t\\(" -n pwa/app.js
sed -n '60,140p' pwa/app.js

rg -n "function updateReadmeTargetPath|defaultUpdateReadmeBlockMarkdown" -n pwa/app.js
sed -n '360,420p' pwa/app.js

rg -n "\\.prog-" pwa/styles.css | head -n 50
sed -n '260,330p' pwa/styles.css

ls -1 pwa
sed -n '1,200p' pwa/README.md

ls -1 references/selfdev/tasks/052_pwa_action_palette_dynamic_and_editable_blocks
sed -n '1,120p' references/selfdev/tasks/051_builtin_readonly_default_actions_clone_on_edit/02_work_notes.md

sed -n '1,220p' pwa/index.html
sed -n '1,180p' references/selfdev/tasks/050_scratch_like_control_flow_blocks_v0/01_plan.md

rg -n '\"ui\\.btn\\.bind\"' -n pwa/i18n.js
sed -n '108,150p' pwa/i18n.js
```

