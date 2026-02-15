# Work Notes: 029 pipeline_codegen_templates

## Summary
- Added a repo-local, deterministic code generator that converts `autoappdev_ir` v1 JSON into a runnable bash pipeline runner.
- Added a runner template with reusable helpers (`note`, `run`, `codex_exec`) and pause/resume support (`runtime/PAUSE`).
- Documented usage + provided a minimal smoke harness and example IR that includes a `codex_exec` action.

## Changes Made
- `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - Runner skeleton (`set -euo pipefail`, runtime dirs, pause loop).
  - Action helpers: `action_note`, `action_run`, `action_codex_exec`.
  - `codex exec` wrapper follows existing repo patterns (`--json`, optional `--full-auto`, optional session reuse via `codex exec resume`).
  - `__PIPELINE_BODY__` placeholder for generated content.
- `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - stdlib-only deterministic generator.
  - Validates minimal IR shape and supported action kinds.
  - Emits trace comments and action calls with stable bash single-quote escaping.
- `scripts/pipeline_codegen/smoke_codegen.sh`
  - Generates twice + `diff` for determinism and `bash -n` syntax check (no codex execution).
- `examples/pipeline_ir_codegen_demo_v0.json`
  - Small IR sample exercising `note`, `run`, and `codex_exec`.
- `docs/pipeline-runner-codegen.md`
  - Usage, supported action kinds, and environment variables.
- `README.md`
  - Linked `docs/pipeline-runner-codegen.md` in Contents.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

sed -n '1,200p' references/selfdev/tasks/029_pipeline_codegen_templates/context.md
sed -n '1,200p' references/selfdev/tasks/029_pipeline_codegen_templates/01_plan.md
ls -la references/selfdev/tasks/029_pipeline_codegen_templates

rg -n "\\bcodex\\s+exec\\b" -S scripts | head
sed -n '320,460p' scripts/app-auto-development.sh

ls -la docs | head
sed -n '1,200p' README.md
ls -la scripts | head -n 50
sed -n '1,200p' scripts/pipeline_demo.sh
sed -n '1,220p' docs/pipeline-formatted-script-spec.md
cat examples/pipeline_ir_v1.json

mkdir -p scripts/pipeline_codegen/templates
chmod +x scripts/pipeline_codegen/generate_runner_from_ir.py scripts/pipeline_codegen/smoke_codegen.sh
find scripts/pipeline_codegen -maxdepth 3 -type f -print
```

