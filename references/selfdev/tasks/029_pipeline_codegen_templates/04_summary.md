# Summary: 029 pipeline_codegen_templates

## What Changed
- Added deterministic runner codegen:
  - `scripts/pipeline_codegen/generate_runner_from_ir.py` generates a runnable bash script from `autoappdev_ir` v1 JSON.
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl` provides the runner skeleton with pause/resume and reusable helpers.
- Added smoke tooling + example input:
  - `scripts/pipeline_codegen/smoke_codegen.sh` verifies determinism (generate twice + diff) and `bash -n` syntax.
  - `examples/pipeline_ir_codegen_demo_v0.json` exercises `note`, `run`, and `codex_exec`.
- Documented usage:
  - `docs/pipeline-runner-codegen.md` and linked from `README.md`.

## Why
To enable reproducible generation of runnable pipeline drivers from the canonical pipeline IR, including non-interactive `codex exec` actions and standard pause/resume behavior.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m json.tool examples/pipeline_ir_codegen_demo_v0.json >/dev/null
timeout 10s scripts/pipeline_codegen/smoke_codegen.sh
```

