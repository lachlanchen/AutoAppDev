# Plan: 046 runner_conditional_steps

## Goal
Update runner codegen so **generated bash runners** respect `STEP.meta.conditional`, with initial support for:
- `on_debug_failure`: run the step only if the immediately preceding **debug step** in the same task had a failing action.

Acceptance:
- Generated runners respect `STEP.meta.conditional` (e.g. `on_debug_failure`) so fix steps run only when previous debug/run actions fail.
- Include an example IR + generated runner demonstrating both paths (skip vs run).

## Current State (Relevant Files)
- Runner template (execution semantics live here):
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - Currently: linear execution with `set -euo pipefail`; any failing `run` aborts the script (so fix steps can’t run after a failing debug).
- Runner generator (emits task/step/action blocks into the template):
  - `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - Currently: ignores `STEP.meta` entirely.
- Convention reference (already used by meta-round templates):
  - `docs/meta-round-templates.md` uses `STEP.meta.conditional="on_debug_failure"` for the fix step.
- Runner docs:
  - `docs/pipeline-runner-codegen.md` (needs a conditional-steps section once implemented).

## Proposed Minimal Design
Implement conditional steps as a **runner v0 extension** with minimal branching:
1. Generator reads `step.meta.conditional` (optional string) and emits it as a context export:
   - `export AUTOAPPDEV_CTX_STEP_CONDITIONAL='on_debug_failure'` (or empty).
2. Template implements:
   - `step_should_run <conditional>`: returns success if the step should execute; errors on unknown conditionals.
   - Per-task state: `AUTOAPPDEV_TASK_LAST_DEBUG_FAILED` (0/1), reset at the start of each task.
3. Debug-step execution is changed so failures are **captured** (no early exit), enabling the fix step to run:
   - For steps with `block=="debug"`: wrap each action call so non-zero exit sets `step_failed=1` but the runner continues.
   - After a debug step: set `AUTOAPPDEV_TASK_LAST_DEBUG_FAILED="$step_failed"`.
4. Conditional behavior:
   - `on_debug_failure`: run the step only when `AUTOAPPDEV_TASK_LAST_DEBUG_FAILED==1`.
   - default/empty: run always.

This keeps all semantics deterministic and runner-local, without changing the IR schema (just interpreting existing `meta`).

## Implementation Steps (Next Phase: WORK)

### 1) Runner Template: Add Conditional Step Helpers + State
Edit `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`:
- Add state variables (runner-global):
  - `AUTOAPPDEV_TASK_LAST_DEBUG_FAILED=0` (reset by generated body at each `TASK` start; see step 2).
- Add helper functions:
  - `step_should_run()`: implements the conditional evaluation.
    - empty/absent: run.
    - `on_debug_failure`: run iff `$AUTOAPPDEV_TASK_LAST_DEBUG_FAILED = 1`.
    - unknown: print error and exit non-zero.

### 2) Generator: Emit Conditional Metadata + Task Reset
Edit `scripts/pipeline_codegen/generate_runner_from_ir.py`:
- Parse step meta:
  - `step.meta` must be an object if present.
  - `step.meta.conditional` must be a string if present.
- At each task start, emit:
  - `AUTOAPPDEV_TASK_LAST_DEBUG_FAILED=0`
- For each step, emit:
  - `export AUTOAPPDEV_CTX_STEP_CONDITIONAL='<conditional-or-empty>'`
  - Wrap the step body in:
    - `if step_should_run "$AUTOAPPDEV_CTX_STEP_CONDITIONAL"; then ... else log "SKIP ..." fi`
- For debug steps (`STEP.block == "debug"`), emit action calls in a failure-capturing form:
  - `step_failed=0`
  - `if ! action_run ...; then step_failed=1; fi` (same pattern for `action_codex_exec` if present)
  - `AUTOAPPDEV_TASK_LAST_DEBUG_FAILED="$step_failed"`

### 3) Add Example IR Demonstrating Skip vs Run
Add `examples/pipeline_ir_conditional_steps_demo_v0.json`:
- Must be valid `autoappdev_ir` v1 JSON.
- Include two tasks (to demonstrate both paths in a single runner invocation):
  1. Task where debug succeeds and fix step is skipped.
  2. Task where debug fails (e.g. `cmd: "echo debug_fail; false"`) and fix step runs.
- Fix step should be:
  - `block: "fix"`
  - `meta: { "conditional": "on_debug_failure" }`
  - `actions`: `run` action that prints a sentinel string, e.g. `FIX_RAN`.

### 4) Add Smoke Script That Proves Conditional Execution
Add `scripts/pipeline_codegen/smoke_conditional_steps.sh`:
- Generate runner to `/tmp/autoappdev_runner_conditional.sh` from the new IR.
- `bash -n` the runner.
- Run with `timeout` and isolated runtime dir in `/tmp`.
- Assert via `rg` on captured output that:
  - “FIX_RAN” does **not** appear for the first task.
  - “FIX_RAN” **does** appear for the second task.
  - A “SKIP” log line appears for the skipped fix step.

### 5) Document Runner Conditional Support
Update `docs/pipeline-runner-codegen.md`:
- Add a short “Conditional steps (v0)” section:
  - Supported conditionals (initially `on_debug_failure`).
  - Definition of “debug failure” (any non-zero action exit inside a debug step; runner continues to allow fix).
  - Mention that unknown `STEP.meta.conditional` values fail fast.

## Verification Commands (DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_conditional_steps_demo_v0.json >/dev/null

chmod +x scripts/pipeline_codegen/smoke_conditional_steps.sh
timeout 20s scripts/pipeline_codegen/smoke_conditional_steps.sh

# Optional: keep existing generator determinism smoke
timeout 20s scripts/pipeline_codegen/smoke_codegen.sh
```

## Acceptance Checklist
- [ ] Generator reads `STEP.meta.conditional` and generates conditional gating code for steps.
- [ ] Debug-step failures are captured so the runner can continue to a conditional fix step.
- [ ] `on_debug_failure` fix steps are skipped on passing debug and executed on failing debug.
- [ ] Example IR + smoke script demonstrate behavior deterministically (with timeouts).
- [ ] `docs/pipeline-runner-codegen.md` documents supported conditional keys and semantics.

