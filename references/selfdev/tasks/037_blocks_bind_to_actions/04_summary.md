# Summary: 037 blocks_bind_to_actions

## What Changed
- PWA blocks can now store an optional action registry reference:
  - `block.action_ref = { id: <number> }` or `{ slug: <string> }`
  - A new `Bind` button appears per block row (except `update_readme`) to set/clear this reference.
- Exports now include the binding when present:
  - `programToIr()` and `programToAapsScript()` attach `ACTION.meta.action_ref` on the default `noop` action.
  - Unbound blocks export exactly as before (no `meta` added).
- Imports preserve bindings:
  - `irToProgram()` reads `ACTION.meta.action_ref` back into block instances.
- Spec docs updated:
  - `docs/pipeline-formatted-script-spec.md` documents optional `ACTION.meta.action_ref`.

Files:
- `pwa/app.js`
- `pwa/styles.css`
- `docs/pipeline-formatted-script-spec.md`

## Why
This is the bridge between reusable action definitions (action registry) and the Scratch-like block program: blocks can reference an action definition and carry that reference through IR/AAPS exports for future execution engines.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
timeout 10s rg -n \"action_ref\" pwa/app.js docs/pipeline-formatted-script-spec.md
```

Manual smoke:
1. Add a `Work` block on the canvas.
2. Click `Bind` and enter an id like `1`.
3. Export AAPS and confirm the `ACTION ...` line includes: `"meta":{"action_ref":{"id":1}}`.
4. Parse that AAPS back into blocks; the block should show the binding in its label.

