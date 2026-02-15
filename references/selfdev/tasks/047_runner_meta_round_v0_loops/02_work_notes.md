# Work Notes: 047 runner_meta_round_v0_loops

## Implementation Notes
- Implemented runner-side support for `meta_round_v0` loops:
  - Controller task runs first (static IR).
  - Runner reads `task_list_path` (`autoappdev_task_list` v0 JSON) and loops the produced tasks.
  - A template task marked by `TASK.meta.task_template_v0` is executed once per produced task list item by generating a `run_task_template_v0()` function in the runner body.
  - Resume state is persisted under the runtime dir (default: `$AUTOAPPDEV_RUNTIME_DIR/meta_round_v0_resume.json`), so reruns skip already completed task ids.
- Placeholder substitution for template tasks uses the task list item fields by exporting:
  - `AUTOAPPDEV_CTX_TASK_ID`, `AUTOAPPDEV_CTX_TASK_TITLE`, `AUTOAPPDEV_CTX_TASK_ACCEPTANCE`
- Added a deterministic example IR and a smoke script for the meta-round loop + resume behavior.
- Updated docs to describe runner meta-round behavior and conventions.

## Files Changed / Added
- Updated:
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - `docs/pipeline-runner-codegen.md`
  - `docs/meta-round-templates.md`
- Added:
  - `examples/pipeline_ir_meta_round_v0_demo_v0.json`
  - `scripts/pipeline_codegen/smoke_meta_round_v0.sh`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_meta_round_v0_demo_v0.json >/dev/null
timeout 10s python3 scripts/pipeline_codegen/generate_runner_from_ir.py --in examples/pipeline_ir_meta_round_v0_demo_v0.json --out /tmp/autoappdev_runner_meta_round_v0_tmp.sh
bash -n /tmp/autoappdev_runner_meta_round_v0_tmp.sh
```

