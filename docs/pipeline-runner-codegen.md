# Pipeline Runner Codegen (v0)

This repo includes a small, deterministic code generator that converts canonical IR (`autoappdev_ir` v1) into a runnable bash driver script.

## Files
- `scripts/pipeline_codegen/generate_runner_from_ir.py`: generator (stdlib-only)
- `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`: runner template
- `scripts/pipeline_codegen/smoke_codegen.sh`: deterministic smoke check
- `examples/pipeline_ir_codegen_demo_v0.json`: example IR that includes a `codex_exec` action

## Generate A Runner
From repo root:
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
```

Determinism smoke check:
```bash
scripts/pipeline_codegen/smoke_codegen.sh
```

## Supported `ACTION.kind` (Runner v0)
The generator currently supports a minimal set:

- `note`
  - required: `params.text` (string)
  - runner behavior: prints a note line to stdout

- `run`
  - required: `params.cmd` (string)
  - runner behavior: runs `bash -lc <cmd>`

- `codex_exec`
  - required: `params.prompt` (string)
  - optional: `params.model` (string)
  - optional: `params.reasoning` (string: `low|medium|high|xhigh`)
  - runner behavior: calls `codex exec` non-interactively and writes JSONL output under `runtime/logs/`

Unknown action kinds fail generation (fast and explicit).

## Runtime Conventions

### Pause/Resume
The runner respects a pause flag file:
- `RUNTIME_DIR="${AUTOAPPDEV_RUNTIME_DIR:-<repo>/runtime}"`
- If `"$RUNTIME_DIR/PAUSE"` exists, the runner sleeps until the file is removed.

### Outbox (Progress Updates)
Generated runners can publish operator-facing progress updates without HTTP by writing message files under:
- `"$AUTOAPPDEV_RUNTIME_DIR/outbox/"` (file-queue ingested by the backend; see `docs/api-contracts.md`)

Runner v0 includes a best-effort helper:
- `outbox_write <content> [role]`
  - writes `runtime/outbox/<ts>_<role>.md` using an atomic rename pattern
  - `role` defaults to `pipeline` (allowlist: `pipeline`, `system`)

`meta_round_v0` loops use this helper to emit `META_TASK ... start/done` (and skip) updates so the PWA can observe progress via `/api/outbox`.

### Codex Wrapper Environment
`codex_exec` uses these environment variables (with defaults):
- `AUTOAPPDEV_CODEX_MODEL` (default: `gpt-5.3-codex`)
- `AUTOAPPDEV_CODEX_REASONING` (default: `medium`)
- `AUTOAPPDEV_CODEX_SESSION_FILE` (default: `$RUNTIME_DIR/.codex_pipeline_session`)
- `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` (default: `0`) to pass `--skip-git-repo-check`
- `AUTOAPPDEV_CODEX_FULL_AUTO` (default: `1`) to pass `--full-auto`

Artifacts written by `codex_exec`:
- `runtime/logs/codex_<n>.prompt.txt`
- `runtime/logs/codex_<n>.jsonl`
- `runtime/logs/codex_stderr.log` (append)

## Placeholder Substitution (v0)
Generated runners perform strict placeholder substitution (Convention v0) inside:
- `ACTION.kind="run"`: `params.cmd`
- `ACTION.kind="codex_exec"`: `params.prompt`

Syntax and conventions:
- See `docs/aaps-numbering-placeholders.md` for the `{{...}}` syntax and guidance.
- Whitespace inside braces is ignored, e.g. `{{ task.id }}`.

Supported keys:
- `{{runtime_dir}}` (resolved runtime dir)
- `{{task.id}}`, `{{task.title}}`, `{{task.acceptance}}`
- `{{step.id}}`, `{{step.title}}`, `{{step.block}}`
- `{{action.id}}`, `{{action.kind}}`

Behavior:
- Unknown placeholder keys are an error (fail fast).
- `AUTOAPPDEV_CODEX_DISABLE=1` skips invoking `codex` and prints the substituted prompt (useful for smoke tests).

## Conditional Steps (v0)
Generated runners may interpret `STEP.meta.conditional` (engine convention) to decide whether to run a step.

Supported conditionals:
- `on_debug_failure`
  - Meaning: run the step only if the most recent `STEP.block="debug"` in the same task had any action exit non-zero.
  - Runner behavior: debug-step action failures are captured so the runner can continue to a conditional fix step.

Behavior:
- Unknown conditional values cause the runner to exit non-zero (fail fast).

## Meta-round Loops (meta_round_v0) (v0)
Generated runners may implement the `meta_round_v0` convention (see `docs/meta-round-templates.md`):
- A controller task defines `TASK.meta.meta_round_v0.task_list_path` (string).
- A template task is marked with `TASK.meta.task_template_v0` (boolean/object).

Runner behavior (v0, minimal):
1. Run the controller task steps in-order (typically writing/updating `task_list_path`).
2. Read `task_list_path` as an `autoappdev_task_list` v0 JSON file.
3. For each task list item `{id,title,acceptance}`:
   - export `AUTOAPPDEV_CTX_TASK_ID/TITLE/ACCEPTANCE` from the task list item
   - run the template task steps/actions (placeholders apply as usual)
4. Persist resume state under the runtime dir so reruns skip already completed task ids:
   - default: `$AUTOAPPDEV_RUNTIME_DIR/meta_round_v0_resume.json`
   - override: `AUTOAPPDEV_META_ROUND_RESUME_FILE=/path/to/resume.json`

Notes:
- Resume keys off task list `id`; stable ids are required for meaningful skipping.
- Unknown/missing task list shape is a hard error (fail fast).
- Current generator limitation: meta-round mode expects exactly 2 tasks in IR: the controller + the template.
