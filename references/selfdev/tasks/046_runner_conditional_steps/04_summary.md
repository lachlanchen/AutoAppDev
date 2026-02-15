# Summary: 046 runner_conditional_steps

Generated runners now support conditional steps via `STEP.meta.conditional` (v0). The initial supported conditional is `on_debug_failure`, allowing fix steps to run only when the previous debug step in the same task had any failing action.

## What Changed
- `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - Added `step_should_run` and a per-task debug-failure flag (`AUTOAPPDEV_TASK_LAST_DEBUG_FAILED`).
- `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - Reads `STEP.meta.conditional` and gates step execution with `step_should_run`.
  - Debug steps now capture action failures (instead of aborting) and set `AUTOAPPDEV_TASK_LAST_DEBUG_FAILED`, enabling conditional fix steps.
- `examples/pipeline_ir_conditional_steps_demo_v0.json` + `scripts/pipeline_codegen/smoke_conditional_steps.sh`
  - Added an example IR and smoke test proving the skip vs run behavior.
- `docs/pipeline-runner-codegen.md`
  - Documented conditional step semantics and supported keys.

## Why
Meta-round templates already model fix steps as conditional (`on_debug_failure`). The runner needed a minimal, deterministic way to execute that pattern without changing the IR schema or introducing non-deterministic behavior.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_conditional_steps_demo_v0.json >/dev/null

chmod +x scripts/pipeline_codegen/smoke_conditional_steps.sh
timeout 20s scripts/pipeline_codegen/smoke_conditional_steps.sh

# Optional: keep existing generator smokes
timeout 20s scripts/pipeline_codegen/smoke_placeholders.sh
timeout 20s scripts/pipeline_codegen/smoke_codegen.sh
```

