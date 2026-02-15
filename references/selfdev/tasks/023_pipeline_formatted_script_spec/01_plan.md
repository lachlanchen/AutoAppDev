# Plan: 023 pipeline_formatted_script_spec

## Goal
Define (in docs) a standardized, versioned “formatted pipeline script” and its canonical IR schema:
- Script format: human-editable text that is deterministic to parse into IR.
- IR schema: `TASK -> STEP -> ACTION` JSON structure.
- Include at least one complete example (script + equivalent IR).
- Explicitly map `STEP.block` values to the PWA Scratch-like blocks.

Acceptance:
- Docs define the formatted script + IR schema (TASK->STEP->ACTION).
- At least one complete example is included.
- Mapping to Scratch-like blocks is explicit.

## Current State (References)
- PWA block palette keys (these must be the canonical `STEP.block` values):
  - `pwa/index.html`: `.toolbox .block[data-block="plan|work|debug|fix|summary|commit_push"]`
  - `pwa/app.js`: `BLOCK_META` includes these block types/labels.
- Backend already stores minimal plans as a flat list of blocks:
  - `docs/api-contracts.md`: “Plan Payload” uses `{ kind:"autoappdev_plan", version:1, steps:[{id, block}] }`
- No existing doc describes a parseable pipeline script format or IR schema beyond the flat plan payload.

## Approach (Minimal / Deterministic)
1. Add one new doc that defines:
   - A versioned, line-oriented script format that is easy to parse (no YAML).
   - A canonical IR JSON shape (TASK->STEP->ACTION).
   - Clear constraints and mapping to existing PWA blocks.
2. Add small example artifacts to keep the spec honest:
   - A sample formatted script file.
   - A sample IR JSON file (validated with `python -m json.tool`).
3. Link the new doc from `README.md` for discoverability.

## Implementation Steps (Next Phase)
1. Add the spec doc.
   - Create `docs/pipeline-formatted-script-spec.md` with:
     - **Overview / design goals**: deterministic parsing, versioning, safety (data only, not executable).
     - **Versioning**:
       - Header line required, e.g. `AUTOAPPDEV_PIPELINE 1`.
     - **Script format (v1)**:
       - Statement lines: `TASK`, `STEP`, `ACTION`.
       - Each statement is `KEYWORD <json-object>` (JSON for attributes).
       - Indentation is allowed for readability but not semantically required.
       - Comments: lines beginning with `#` are ignored.
       - Required keys:
         - `TASK`: `{ "id": "...", "title": "..." }`
         - `STEP`: `{ "id": "...", "title": "...", "block": "plan|work|debug|fix|summary|commit_push" }`
         - `ACTION`: `{ "id": "...", "kind": "...", "params": { ... } }`
       - Validation rules:
         - IDs must be unique within their scope.
         - `STEP.block` must be one of the PWA palette keys above.
         - Order is significant (steps/actions executed top-to-bottom).
     - **Canonical IR schema (v1)**:
       - Top-level object, e.g.:
         - `{ "kind": "autoappdev_ir", "version": 1, "tasks": [ ... ] }`
       - `Task` object contains `steps`; `Step` contains `actions`.
       - Include field tables with types and required/optional fields.
     - **Mapping sections**:
       - Script -> IR mapping rules (how statements nest; how to handle missing context).
       - IR -> PWA mapping:
         - `STEP.block` maps 1:1 to PWA blocks (`plan/work/debug/fix/summary/commit_push`).
         - Mention the existing flat plan payload (`autoappdev_plan`) as a lossy projection: IR steps -> plan.steps.
     - **Complete example**:
       - One full formatted script example (TASK with 4-6 steps matching the palette).
       - The equivalent IR JSON example.
       - Optional: show derived `autoappdev_plan` steps for the same example.

2. Add example artifacts (to validate the spec content).
   - Add `examples/pipeline_formatted_script_v1.aaps`:
     - Contains the same example script shown in the doc.
   - Add `examples/pipeline_ir_v1.json`:
     - Contains the same IR JSON shown in the doc.
     - Keep it valid JSON so `python3 -m json.tool` can validate it.

3. Link from the main README.
   - Update `README.md` “Contents” to include:
     - `docs/pipeline-formatted-script-spec.md`

4. Keep changes docs/examples only.
   - No PWA or backend behavior changes in this task.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/pipeline-formatted-script-spec.md
test -f examples/pipeline_formatted_script_v1.aaps
test -f examples/pipeline_ir_v1.json

# Ensure key concepts exist in the spec
rg -n 'AUTOAPPDEV_PIPELINE\\s+1|\\bTASK\\b|\\bSTEP\\b|\\bACTION\\b' docs/pipeline-formatted-script-spec.md
rg -n 'autoappdev_ir|\"tasks\"\\s*:' docs/pipeline-formatted-script-spec.md
rg -n 'plan\\b|work\\b|debug\\b|fix\\b|summary\\b|commit_push\\b' docs/pipeline-formatted-script-spec.md

# Validate example JSON is actually valid
python3 -m json.tool examples/pipeline_ir_v1.json >/dev/null

# Confirm README links the new doc
rg -n 'pipeline-formatted-script-spec\\.md' README.md
```

## Acceptance Checklist
- [ ] `docs/pipeline-formatted-script-spec.md` defines a versioned formatted script and the IR schema (TASK->STEP->ACTION).
- [ ] Spec includes at least one complete example (script + equivalent IR).
- [ ] Spec explicitly maps `STEP.block` values to the current PWA blocks (`plan/work/debug/fix/summary/commit_push`).
- [ ] Example IR JSON validates via `python3 -m json.tool`.

