# Plan: 029 pipeline_codegen_templates

## Goal
Add a deterministic, repo-local code generator that converts canonical IR (`autoappdev_ir` v1) into a runnable shell driver that:
- Interprets IR `TASK -> STEP -> ACTION` in-order.
- Uses **Codex non-interactively** for prompt-based actions.
- Provides **reusable action helpers** (note/run/codex) inside the generated script (or sourced from a shared template library).

Acceptance:
- Repo includes a script/template that generates a runnable shell driver from IR.
- Generated driver includes Codex non-interactive calls + reusable actions.
- Generation is deterministic (same IR -> identical output bytes).

## Current State (References)
- Canonical IR shape is defined in `docs/pipeline-formatted-script-spec.md` (top-level `kind:"autoappdev_ir", version:1, tasks:[...]`).
- Example IR exists: `examples/pipeline_ir_v1.json` (uses `ACTION.kind: note|run`).
- Existing Codex non-interactive shell patterns exist:
  - `scripts/auto-autoappdev-development.sh` (session reuse, JSONL capture, prompt files)
  - `scripts/app-auto-development.sh` (non-interactive shared-session flow)
- Pipeline runtime pause/resume convention:
  - `backend/app.py` toggles `runtime/PAUSE`
  - `scripts/pipeline_demo.sh` respects `$AUTOAPPDEV_RUNTIME_DIR/PAUSE`

## Output Contract (Runner v0)
Generated shell runner should:
- Start with `#!/usr/bin/env bash` and `set -euo pipefail`.
- Respect pause:
  - `RUNTIME_DIR="${AUTOAPPDEV_RUNTIME_DIR:-<repo>/runtime}"`
  - `PAUSE_FLAG="$RUNTIME_DIR/PAUSE"` and loop while present.
- Log to stdout/stderr (backend captures into `runtime/logs/pipeline.log`).
- Provide reusable action helpers:
  - `action_note <text>`: print a note line.
  - `action_run <cmd>`: run a command deterministically (`bash -lc ...`) with correct quoting.
  - `action_codex_exec <prompt>`: run codex non-interactively with stable defaults and optional session reuse.

Supported `ACTION.kind` (minimal set for v0):
- `note`: `params.text` (string)
- `run`: `params.cmd` (string)
- `codex_exec`: `params.prompt` (string), optional `params.model`, `params.reasoning`, etc.

Unknown action kinds should fail fast with a clear message (so generation/execution is predictable).

## Implementation Steps (Next Phase: WORK)
1. Create a dedicated codegen folder
   - Add directory: `scripts/pipeline_codegen/`
   - Add template file: `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
     - Contains the stable runner skeleton (pause handling, logging, codex wrapper, action helpers).
     - Includes a single placeholder like `__PIPELINE_BODY__` for the generated task/step/action body.

2. Implement the generator (deterministic)
   - Add `scripts/pipeline_codegen/generate_runner_from_ir.py` (stdlib only).
   - Responsibilities:
     - Load IR JSON from a file path (arg `--in <path>`).
     - Validate minimal IR invariants (kind/version/tasks/steps/actions types).
     - Generate a stable bash body:
       - Iterate tasks/steps/actions in file order.
       - Emit comments for traceability: `# TASK t1 ...`, `# STEP s1 ...`, `# ACTION a1 ...`
       - Emit calls to `action_note`, `action_run`, `action_codex_exec` with safe quoting.
     - Read template file and substitute `__PIPELINE_BODY__`.
     - Write to stdout or `--out <path>`.
   - Determinism rules:
     - No timestamps/random IDs in the generated output.
     - Stable quoting function for bash literals (single-quote escape strategy).
     - Stable newline endings (always `\\n` line endings, final trailing newline).

3. Add an example IR that exercises codex actions
   - Add `examples/pipeline_ir_codegen_demo_v0.json`:
     - Includes at least one `codex_exec` action (with a short prompt).
     - Includes at least one `run` action.
   - Keep prompts benign (no git push, no destructive commands).

4. Add a tiny deterministic verification harness (no codex execution)
   - Add `scripts/pipeline_codegen/smoke_codegen.sh` (or a python snippet in docs):
     - Runs generator twice and `diff`s outputs (proves determinism).
     - Runs `bash -n` on the generated runner (syntax check).
     - Optionally `python3 -m json.tool` on the example IR.

5. Document usage + supported action kinds
   - Add `docs/pipeline-runner-codegen.md`:
     - How to run generator from repo root.
     - Supported `ACTION.kind` and required params.
     - Environment variables for codex wrapper (defaults, optional session file).
     - Pause flag behavior (`runtime/PAUSE`).
   - Link doc from `README.md` Contents if there is an existing docs index pattern.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Confirm new files exist after implementation
test -f scripts/pipeline_codegen/generate_runner_from_ir.py
test -f scripts/pipeline_codegen/templates/runner_v0.sh.tpl
test -f examples/pipeline_ir_codegen_demo_v0.json

# Validate IR JSON
python3 -m json.tool examples/pipeline_ir_codegen_demo_v0.json >/dev/null

# Generate twice and confirm deterministic output
timeout 10s python3 scripts/pipeline_codegen/generate_runner_from_ir.py --in examples/pipeline_ir_codegen_demo_v0.json --out /tmp/runner_a.sh
timeout 10s python3 scripts/pipeline_codegen/generate_runner_from_ir.py --in examples/pipeline_ir_codegen_demo_v0.json --out /tmp/runner_b.sh
diff -u /tmp/runner_a.sh /tmp/runner_b.sh

# Shell syntax check
bash -n /tmp/runner_a.sh
```

Manual (outside sandbox): run the generated driver via backend pipeline controls
1. Generate runner to `scripts/generated_demo_runner.sh`.
2. Start backend with `AUTOAPPDEV_PIPELINE_SCRIPT=scripts/generated_demo_runner.sh`.
3. Use PWA Start/Pause/Resume/Stop; confirm logs show steps and pause/resume messages.

## Acceptance Checklist
- [ ] `scripts/pipeline_codegen/generate_runner_from_ir.py` generates a runnable `.sh` from an `autoappdev_ir` JSON file.
- [ ] Generated runner includes non-interactive `codex exec` wrapper function(s) for `ACTION.kind="codex_exec"`.
- [ ] Runner contains reusable action helpers (`action_note`, `action_run`, `action_codex_exec`).
- [ ] Generation is deterministic (byte-identical outputs for the same input).
- [ ] At least one example IR (`examples/pipeline_ir_codegen_demo_v0.json`) generates successfully.

