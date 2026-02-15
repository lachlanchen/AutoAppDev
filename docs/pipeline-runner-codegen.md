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
