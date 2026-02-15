# Work Notes: 037 blocks_bind_to_actions

## What Changed
- Added per-block action binding in the PWA program canvas:
  - Each non-`update_readme` block row now has a `Bind` button to store `block.action_ref` as `{id:number}` or `{slug:string}`.
  - Block labels show the binding suffix (e.g. `Work -> #12` or `Work -> slug: my_action`). If the Actions list was loaded, id bindings show the title too.
- Updated exports to include the reference:
  - `programToIr()` and `programToAapsScript()` now emit `ACTION.meta.action_ref` when a block has `action_ref`.
  - Blocks without bindings export exactly as before (no `meta` field added).
- Updated imports:
  - `irToProgram()` now preserves `ACTION.meta.action_ref` back into block instances.
- Documented the convention:
  - `docs/pipeline-formatted-script-spec.md` now describes optional `ACTION.meta.action_ref`.

## Files Touched
- `pwa/app.js`
- `pwa/styles.css`
- `docs/pipeline-formatted-script-spec.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

timeout 10s rg -n 'action_ref|meta\\s*:\\s*\\{\\s*action_ref' pwa/app.js docs/pipeline-formatted-script-spec.md
```

Results:
- `node --check` exited `0` (syntax OK).
- `rg` confirms `action_ref` storage + export/import wiring and spec documentation.

