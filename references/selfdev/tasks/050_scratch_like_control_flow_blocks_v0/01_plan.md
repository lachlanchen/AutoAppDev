# Plan: 050 scratch_like_control_flow_blocks_v0

## Goal
Introduce a minimal “Scratch-like” control-flow experience in the PWA:
- Add control-flow blocks to the toolbox: **metatasks generator**, **For N_ROUND**, **For each task**, **If/Else**.
- Seed a default nested program on a fresh load (two nested “for” loops).
- Ensure export/import round-trips through **AAPS v1 + canonical IR** (no new AAPS grammar; control flow is encoded via `meta` fields per `docs/meta-round-templates.md`).

Acceptance:
- Add the control-flow blocks listed above.
- Default canvas shows a nested two-for template.
- Export/import round-trips via AAPS+IR (blocks -> AAPS -> backend parse -> IR -> blocks yields the same nested structure).

## Current State (Relevant Files)
- PWA blocks are currently a **flat array** (`program: []`) and render as a linear list:
  - `pwa/app.js`: `program`, `renderProgram()`, `bindDnD()`, `persistProgram()/loadProgram()`.
  - `pwa/index.html`: toolbox blocks (Plan/Work/Debug/Fix/Summary/Update README/Commit+Push).
- Export/import today:
  - `pwa/app.js`: `programToIr()`, `programToAapsScript()`, `irToProgram()`.
  - Script tab:
    - `Parse AAPS -> Blocks`: `/api/scripts/parse` returns IR; PWA uses `irToProgram()`.
    - `From Blocks`: uses `programToAapsScript()`.
- Backend parsing already supports “display-only” numbering and numeric-prefix tolerance:
  - `backend/pipeline_parser.py`: ignores `# ...` comment numbering; accepts optional numeric prefixes like `1.2 STEP {...}`.
- Meta-round and conditional conventions are already defined and runner-supported:
  - `docs/meta-round-templates.md`: `TASK.meta.meta_round_v0` and `TASK.meta.task_template_v0`.
  - Runner support (already implemented in prior tasks): `meta_round_v0`, `STEP.meta.conditional="on_debug_failure"`.

## Minimal v0 Design (Keep AAPS Deterministic)
Key constraint: AAPS v1 `STEP.block` must stay in the existing palette (`plan|work|debug|fix|summary|commit_push`). Therefore:
- The new control-flow blocks are **UI-only** constructs.
- Export encodes control flow using existing IR/AAPS `meta` fields:
  - `TASK.meta.meta_round_v0`: controller config (includes `n_round` and `task_list_path`).
  - `TASK.meta.task_template_v0`: template task marker (applied “for each task” by runners).
  - `STEP.meta.round`: marks controller round steps (1..N).
  - `STEP.meta.conditional="on_debug_failure"`: represents If/Else (v0 = “IF debug failed …”; ELSE branch is empty in v0).

Deliberate v0 limitations (to keep scope small):
- If/Else supports only one condition: `on_debug_failure` (else branch is display-only/empty).
- Meta-round UI assumes the “2-task” pattern:
  - one controller task + one template task (matches current runner/generator limitation).
- No arbitrary variables/custom blocks; this is a structured template view over AAPS/IR.

## Implementation Steps (Next Phase: WORK)

### 1) Add New Block Types + Labels
Edit `pwa/app.js`:
- Extend `BLOCK_META` with new types:
  - `metatasks_generator` (cls: `block--loop`)
  - `for_n_round` (cls: `block--loop`)
  - `for_each_task` (cls: `block--loop`)
  - `if_else` (cls: `block--loop` or a new cls if desired)
- Add display label helpers for container blocks (include parameters like `N=2`).

Edit `pwa/index.html`:
- Add new draggable toolbox entries with `data-block="..."` for the four new blocks.

Edit `pwa/i18n.js`:
- Add **English** keys for the new blocks (other languages will fall back to `en` via `t()`):
  - `ui.block.metatasks_generator`
  - `ui.block.for_n_round`
  - `ui.block.for_each_task`
  - `ui.block.if_else`

### 2) Introduce A Nested “Program AST” (Versioned) With Backward Compatibility
Edit `pwa/app.js`:
- Replace the flat `program: []` with a versioned object, e.g.:
  - `{ kind: "autoappdev_program", version: 1, blocks: BlockNode[] }`
- Define `BlockNode` shapes (minimal):
  - Leaf phase blocks (existing): `{ type: "plan" | "work" | ... , action_ref?, workspace? }`
  - Containers:
    - `metatasks_generator`: `{ type, n_round, task_list_path, rounds: BlockNode[], each_task: BlockNode[] }`
    - `for_n_round`: `{ type, n_round, body: BlockNode[] }` (body will hold round steps)
    - `for_each_task`: `{ type, body: BlockNode[] }`
    - `if_else`: `{ type, if_body: BlockNode[], else_body: BlockNode[] }` (else may remain empty in v0)
- Update `persistProgram()/loadProgram()`:
  - If localStorage value is an array (old format), wrap it into the new format as a flat `blocks` list.
  - If empty/missing, initialize to the default nested template (Step 4).

### 3) Render Nested Blocks On The Canvas
Edit `pwa/app.js` `renderProgram()`:
- Replace the flat `.forEach((b, idx) => ...)` with a recursive renderer that:
  - renders container rows and their child blocks (depth indentation via `style.marginLeft`).
  - shows `Bind` only for leaf steps where action binding makes sense.
  - `×` remove deletes a subtree for container nodes.
- Minimal UI affordances:
  - v0 can keep “append at end” insertion (no complex drag-to-nest).
  - Optional: add a small `+` button on containers to append a child step (implemented later if needed).

### 4) Default Nested Two-For Template On Fresh Load
Edit `pwa/app.js` `loadProgram()` (or after load if empty):
- If no stored program exists, set `program` to:
  - `metatasks_generator`
    - `for_n_round` with `n_round=2` and body containing two round steps (e.g. two `plan` leaf nodes labeled “Round 1/2” via title metadata stored in node meta, or derived by index)
    - `for_each_task` containing:
      - `plan`, `work`, `debug`,
      - `if_else` with `if_body=[fix]` and empty `else_body`,
      - `summary`, `commit_push`
- Persist after initialization so refresh keeps it stable.

### 5) Update Export: Program AST -> Canonical IR -> AAPS
Edit `pwa/app.js`:
- Upgrade `programToIr()`:
  - If the root contains a `metatasks_generator` node:
    - Emit `autoappdev_ir` v1 with exactly two tasks:
      1. Controller task:
         - `meta.meta_round_v0 = { n_round, task_list_path, ... }` (store at least these keys).
         - Steps derived from the `for_n_round` body:
           - `STEP.block` from leaf type (likely `plan`), `STEP.meta.round = 1..N`.
      2. Template task:
         - `meta.task_template_v0 = true`
         - Steps derived from the `for_each_task` body:
           - leaf steps map to normal `STEP.block`
           - `if_else` maps to a conditional `fix` step: `STEP.meta.conditional="on_debug_failure"`
    - Actions can remain v0/simple (e.g. existing `noop` with optional `ACTION.meta.action_ref`), preserving semantics and keeping changes minimal.
  - Else fallback to the existing “single task, linear steps” behavior.
- Implement a small `irToAapsText(ir)` serializer in `pwa/app.js`:
  - Emits multi-task AAPS v1 with numbering comments + indentation (follow `docs/aaps-numbering-placeholders.md` and existing task-048 formatting).
  - `programToAapsScript()` becomes:
    - `const ir = programToIr(...)`
    - `return irToAapsText(ir)`

### 6) Update Import: IR -> Program AST (Reconstruct Control-Flow Blocks)
Edit `pwa/app.js` `irToProgram(ir)`:
- Detect meta-round shape:
  - exactly one task with `meta.meta_round_v0` (controller)
  - exactly one task with `meta.task_template_v0` (template)
- If detected:
  - Build `metatasks_generator` + nested `for_n_round` and `for_each_task` blocks.
  - Map template conditional fix step (`STEP.meta.conditional="on_debug_failure"`) into an `if_else` block containing a `fix` leaf.
- Else fallback to the existing flat mapping (keep current behavior for normal scripts).

### 7) Keep Existing Script Tab Wiring Working
Edit `pwa/app.js`:
- Ensure these call updated conversion functions without regressions:
  - `fillScriptFromBlocks()`
  - `exportAapsFile()`
  - `exportRunnerFile()` (embedded `# AAPS:` should reflect the new AAPS text)
  - `saveScript()` (saves `script_text` + `ir`)
  - `parseAapsToBlocks()` / `importShellToBlocks()` (use updated `irToProgram()` path)
- Optionally update the Script tab hint text in `pwa/index.html` to remove “step-level only” claim if it becomes inaccurate.

### 8) Docs (Optional, Minimal)
If needed to keep docs accurate:
- Update `docs/end-to-end-demo-checklist.md` to mention the default meta-round nested program and that Script export/import preserves it.

## Verification (DEBUG/VERIFY Phase)
Static checks (sandbox-friendly):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/i18n.js
timeout 10s python3 -m py_compile backend/pipeline_parser.py
```

Manual browser checks (outside this sandbox, since ports can’t be bound here):
1. Serve `pwa/` and run backend (see `pwa/README.md`).
2. Confirm default canvas shows a nested “metatasks generator -> For N_ROUND -> For each task -> If/Else” template.
3. Script tab:
  - Click `From Blocks`, confirm AAPS contains 2 tasks and meta keys (`meta_round_v0`, `task_template_v0`, `conditional`).
  - Click `Parse AAPS -> Blocks`, confirm the canvas returns to the same nested structure.

## Acceptance Checklist
- [ ] Toolbox includes: metatasks generator, For N_ROUND, For each task, If/Else.
- [ ] Fresh load shows a nested two-for template on the canvas.
- [ ] Export AAPS + parse back yields the same nested structure (round-trip via backend IR).
- [ ] Non-meta-round scripts still import/render as a flat program (no regression).

