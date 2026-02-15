# Work Notes: 049 runner_outbox_progress_helper

## Implementation Notes
- Added a runner-native, best-effort outbox helper in the generated runner template:
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
    - new `OUTBOX_DIR="$RUNTIME_DIR/outbox"`
    - new `outbox_write <content> [role]` that writes `runtime/outbox/<ts>_<role>.md` using an atomic rename pattern (no HTTP required).
- Wired meta-round loop progress to the outbox so the PWA can observe meta-task progress via backend outbox ingestion:
  - `meta_round_run_template_tasks()` now emits outbox messages for:
    - `META_TASK <id>: start (...)`
    - `META_TASK <id>: done`
    - `SKIP META_TASK <id>: already completed`
- Extended the meta-round smoke to assert outbox files are created and contain the expected progress lines:
  - `scripts/pipeline_codegen/smoke_meta_round_v0.sh`
- Updated docs to document the runner outbox progress helper:
  - `docs/pipeline-runner-codegen.md`

## Files Changed
- Updated: `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
- Updated: `scripts/pipeline_codegen/smoke_meta_round_v0.sh`
- Updated: `docs/pipeline-runner-codegen.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Initial run (failed due to an over-escaped rg pattern in the smoke script; fixed below)
timeout 30s bash scripts/pipeline_codegen/smoke_meta_round_v0.sh

# Diagnose the failing assertion
timeout 30s bash -x scripts/pipeline_codegen/smoke_meta_round_v0.sh

# Re-run after fixing the smoke rg pattern
timeout 30s bash scripts/pipeline_codegen/smoke_meta_round_v0.sh
```

