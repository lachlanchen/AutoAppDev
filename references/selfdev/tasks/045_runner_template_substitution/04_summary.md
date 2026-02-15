# Summary: 045 runner_template_substitution

Generated bash runners now perform deterministic `{{...}}` placeholder substitution for `ACTION.kind="run"` (`params.cmd`) and `ACTION.kind="codex_exec"` (`params.prompt`), using the current task/step/action context and the resolved runtime directory.

## What Changed
- `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - Added strict placeholder expansion (`subst_placeholders`) and applied it in `action_run()` and `action_codex_exec()`.
  - Added `AUTOAPPDEV_CODEX_DISABLE=1` to skip invoking `codex` (writes + prints substituted prompt) for smoke testing.
- `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - Exports context variables before each action so placeholders have stable inputs:
    - task: `AUTOAPPDEV_CTX_TASK_ID`, `AUTOAPPDEV_CTX_TASK_TITLE`, `AUTOAPPDEV_CTX_TASK_ACCEPTANCE` (from `task.meta.acceptance`, optional)
    - step: `AUTOAPPDEV_CTX_STEP_ID`, `AUTOAPPDEV_CTX_STEP_TITLE`, `AUTOAPPDEV_CTX_STEP_BLOCK`
    - action: `AUTOAPPDEV_CTX_ACTION_ID`, `AUTOAPPDEV_CTX_ACTION_KIND`
- `examples/pipeline_ir_placeholders_smoke_v0.json` + `scripts/pipeline_codegen/smoke_placeholders.sh`
  - Added a focused smoke test that generates a runner and proves substitution happens (no raw `{{...}}` left).
- `docs/pipeline-runner-codegen.md`
  - Documented supported placeholder keys and behavior.

## Why
This enables reusable prompt/command templates in IR-generated runners while keeping execution deterministic and testable (including in environments without `codex` installed).

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_placeholders_smoke_v0.json >/dev/null
chmod +x scripts/pipeline_codegen/smoke_placeholders.sh
timeout 20s scripts/pipeline_codegen/smoke_placeholders.sh

# Optional: existing determinism smoke
timeout 20s scripts/pipeline_codegen/smoke_codegen.sh
```

