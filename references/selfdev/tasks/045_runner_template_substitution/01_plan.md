# Plan: 045 runner_template_substitution

## Goal
Implement deterministic placeholder substitution in **generated runners** for:
- `ACTION.kind="codex_exec"`: substitute inside `params.prompt`
- `ACTION.kind="run"`: substitute inside `params.cmd`

Supported substitution inputs must include:
- task/step ids
- task “list fields” (title + acceptance)
- `runtime_dir`

Acceptance:
- Generated runners apply deterministic placeholder substitution for `codex_exec.prompt` and `run.cmd`.
- Supported placeholder keys are documented.
- Include a smoke check.

## Current State (Relevant Files)
- Runner generator:
  - `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - Emits calls like `action_run '<cmd>'` and `action_codex_exec '<prompt>'`
- Runner template:
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - Defines `action_run()` and `action_codex_exec()` but does no substitution
- Runner docs:
  - `docs/pipeline-runner-codegen.md` (no placeholder substitution section yet)
- Placeholder syntax/convention (docs-only today):
  - `docs/aaps-numbering-placeholders.md` (defines `{{...}}` paths like `{{task.title}}`, `{{task.acceptance}}`, `{{runtime_dir}}`)

## Proposed Minimal Design
Add a deterministic, runtime substitution step inside the generated runner:
1. The generator sets “current context” variables before each action:
   - task: id/title/acceptance
   - step: id/title/block
   - (optional) action: id/kind
2. The runner template expands `{{...}}` placeholders in:
   - `run.cmd` before `bash -lc`
   - `codex_exec.prompt` before writing the prompt file / invoking `codex`

Implementation choice (keep minimal + robust):
- Implement substitution via a small `python3` snippet invoked by the runner (python3 is already required by the template for session id extraction).
- Unknown placeholder keys should fail fast with a clear error.

## Implementation Steps (Next Phase: WORK)

### 1) Runner Template: Add Substitution Helper
Edit `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`:
- Add a function like `subst_placeholders()` that:
  - reads text from stdin
  - replaces `{{ ... }}` placeholders (whitespace-tolerant) using current context values
  - errors on unknown keys (recommended default)
- Define the supported keys (mapping to runtime variables):
  - `runtime_dir` -> resolved runtime dir (the runner’s `RUNTIME_DIR`)
  - `task.id`, `task.title`, `task.acceptance`
  - `step.id`, `step.title`, `step.block`
  - (optional) `action.id`, `action.kind` for completeness
- Ensure the resolved runtime dir is visible to the substitution helper:
  - either `export RUNTIME_DIR`, or set/export a dedicated var like `AUTOAPPDEV_RUNTIME_DIR_RESOLVED="$RUNTIME_DIR"`

### 2) Runner Template: Apply Substitution In Actions
In `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`:
- Update `action_run()` to:
  - substitute placeholders in `cmd` before logging/executing
  - execute the substituted command via `bash -lc`
- Update `action_codex_exec()` to:
  - substitute placeholders in `prompt` before writing the prompt file

For the smoke check (avoid calling `codex`):
- Add a minimal env guard (default off) inside `action_codex_exec()`:
  - If `AUTOAPPDEV_CODEX_DISABLE=1`, log the substituted prompt and return success without invoking `codex`.

### 3) Generator: Emit Context Variables For Substitution
Edit `scripts/pipeline_codegen/generate_runner_from_ir.py`:
- Before each task loop:
  - set variables for task context (quoted):
    - `AUTOAPPDEV_CTX_TASK_ID`
    - `AUTOAPPDEV_CTX_TASK_TITLE`
    - `AUTOAPPDEV_CTX_TASK_ACCEPTANCE` from `task.meta.acceptance` if present and a string (else empty)
- Before each step loop:
  - set variables for step context:
    - `AUTOAPPDEV_CTX_STEP_ID`
    - `AUTOAPPDEV_CTX_STEP_TITLE`
    - `AUTOAPPDEV_CTX_STEP_BLOCK`
- Before each action:
  - (optional) set:
    - `AUTOAPPDEV_CTX_ACTION_ID`
    - `AUTOAPPDEV_CTX_ACTION_KIND`
- Keep actual action calls unchanged (`action_run ...`, `action_codex_exec ...`); the substitution happens in the template functions.

### 4) Add A Placeholder Smoke IR Example
Add `examples/pipeline_ir_placeholders_smoke_v0.json`:
- Must be valid `autoappdev_ir` v1 JSON.
- One task with:
  - `meta.acceptance` string (so `{{task.acceptance}}` has a defined source)
- Include:
  - a `codex_exec` action with `params.prompt` containing placeholders:
    - `{{task.id}}`, `{{step.id}}`, `{{runtime_dir}}`, `{{task.acceptance}}`
  - a `run` action with `params.cmd` containing placeholders and only benign commands:
    - `echo ...` and/or `printf ...`

### 5) Add A Smoke Script That Executes The Runner Deterministically
Add `scripts/pipeline_codegen/smoke_placeholders.sh`:
- Generate a runner to `/tmp/autoappdev_runner_placeholders.sh` from the new IR.
- `bash -n` the runner.
- Run the runner with timeouts and safe env:
  - `AUTOAPPDEV_RUNTIME_DIR=/tmp/autoappdev_runtime_placeholders_$$`
  - `AUTOAPPDEV_CODEX_DISABLE=1` (so the `codex_exec` step doesn’t invoke codex)
  - `timeout 10s bash /tmp/autoappdev_runner_placeholders.sh`
- Assert output contains substituted values (and not raw `{{...}}`), e.g.:
  - runtime dir path appears
  - task/step ids appear
  - `rg -n '{{'` on captured output returns no matches

Keep this smoke separate from `scripts/pipeline_codegen/smoke_codegen.sh` to avoid changing the existing determinism check, unless it’s trivial to chain them.

### 6) Document Supported Keys
Update `docs/pipeline-runner-codegen.md`:
- Add a section “Placeholder substitution (v0)”:
  - lists supported keys (`runtime_dir`, `task.*`, `step.*`, optional `action.*`)
  - states substitution applies to `run.cmd` and `codex_exec.prompt`
  - states unknown keys are an error (fail fast)
  - documents `AUTOAPPDEV_CODEX_DISABLE=1` as a runner-only testing knob (if added)
- Link to `docs/aaps-numbering-placeholders.md` for the `{{...}}` syntax convention.

## Verification Commands (DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Generator/template lint
timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py

# JSON validity
python3 -m json.tool examples/pipeline_ir_placeholders_smoke_v0.json >/dev/null

# Smoke (should exit 0)
timeout 20s scripts/pipeline_codegen/smoke_placeholders.sh
```

Optional: keep existing determinism check:
```bash
scripts/pipeline_codegen/smoke_codegen.sh
```

## Acceptance Checklist
- [ ] Runner template substitutes placeholders in `run.cmd` and `codex_exec.prompt`.
- [ ] Supported keys documented in `docs/pipeline-runner-codegen.md`.
- [ ] Smoke script runs deterministically with timeouts and proves substitution works (no `{{...}}` remains in executed/logged strings).

