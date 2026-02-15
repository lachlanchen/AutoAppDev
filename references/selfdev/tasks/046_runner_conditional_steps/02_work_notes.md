# Work Notes: 046 runner_conditional_steps

## Implementation Notes
- Added runner support for `STEP.meta.conditional` (v0), with initial conditional:
  - `on_debug_failure` (used by meta-round templates for conditional fix steps).
- Updated runner codegen so debug steps capture action failures (no early exit) and set a per-task flag used for conditional evaluation.
- Added a focused example IR + smoke script demonstrating:
  - fix step skipped when debug passes
  - fix step runs when debug fails
- Documented runner conditional behavior in `docs/pipeline-runner-codegen.md`.

## Files Changed / Added
- Updated:
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - `docs/pipeline-runner-codegen.md`
- Added:
  - `examples/pipeline_ir_conditional_steps_demo_v0.json`
  - `scripts/pipeline_codegen/smoke_conditional_steps.sh`

## Commands Run
Work phase focused on implementation; no verification commands run yet (reserved for DEBUG/VERIFY phase).

