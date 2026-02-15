# Work Notes: 045 runner_template_substitution

## Implementation Notes
- Added strict `{{...}}` placeholder substitution inside generated runners (implemented in `scripts/pipeline_codegen/templates/runner_v0.sh.tpl` via a small `python3` helper).
- Substitution is applied at runtime in:
  - `action_run()` (before `bash -lc`)
  - `action_codex_exec()` (before writing the prompt file)
- Added `AUTOAPPDEV_CODEX_DISABLE=1` mode so runners can be smoke-tested without invoking `codex` (writes + prints the substituted prompt and returns success).
- Updated runner codegen to export per-action context variables so placeholders have deterministic inputs:
  - `AUTOAPPDEV_CTX_TASK_*`, `AUTOAPPDEV_CTX_STEP_*`, `AUTOAPPDEV_CTX_ACTION_*`
  - `task.acceptance` is sourced from `task.meta.acceptance` (optional; defaults to empty string).
- Added a dedicated placeholder smoke IR + smoke script to validate substitution and ensure no `{{...}}` remains in runner output.
- Updated `docs/pipeline-runner-codegen.md` to document supported placeholder keys and behavior.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Smoke / verification
chmod +x scripts/pipeline_codegen/smoke_placeholders.sh
timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_placeholders_smoke_v0.json >/dev/null
timeout 20s scripts/pipeline_codegen/smoke_placeholders.sh
timeout 20s scripts/pipeline_codegen/smoke_codegen.sh
```

