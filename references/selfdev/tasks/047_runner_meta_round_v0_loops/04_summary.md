# Summary: 047 runner_meta_round_v0_loops

## What Changed (And Why)
- Added runner/codegen support for `meta_round_v0` loops so a controller task can generate a `autoappdev_task_list` JSON (`task_list_path`) and the runner can iterate that list by executing a template task marked `TASK.meta.task_template_v0`, with per-task placeholder substitution via `AUTOAPPDEV_CTX_TASK_{ID,TITLE,ACCEPTANCE}`.
- Implemented a runtime resume file (default: `$AUTOAPPDEV_RUNTIME_DIR/meta_round_v0_resume.json`) so reruns skip already-completed meta tasks by id.
- Added a deterministic demo IR + smoke script to validate loop + resume behavior, and updated docs to describe the new runner behavior and current limitation (meta-round IR currently requires exactly 2 tasks: controller + template).

## Files Touched
- Updated: `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
- Updated: `scripts/pipeline_codegen/generate_runner_from_ir.py`
- Added: `examples/pipeline_ir_meta_round_v0_demo_v0.json`
- Added: `scripts/pipeline_codegen/smoke_meta_round_v0.sh`
- Updated: `docs/pipeline-runner-codegen.md`
- Updated: `docs/meta-round-templates.md`

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_meta_round_v0_demo_v0.json >/dev/null
timeout 30s bash scripts/pipeline_codegen/smoke_meta_round_v0.sh
```

