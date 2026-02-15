# Summary: 049 runner_outbox_progress_helper

## What Changed (And Why)
- Added a runner-native, best-effort helper to publish progress updates to the file-based outbox queue (no HTTP required):
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl` now includes `outbox_write <content> [role]` which writes `runtime/outbox/<ts>_<role>.md` using an atomic rename pattern.
- Wired `meta_round_v0` loops to emit outbox progress messages so the PWA can observe meta-task progress via backend `/api/outbox` ingestion:
  - `META_TASK <id>: start/done` and skip messages are written to `runtime/outbox/`.
- Extended the meta-round smoke to assert outbox files are created and contain progress lines.
- Documented the runner outbox helper in `docs/pipeline-runner-codegen.md`.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
timeout 10s bash -n scripts/pipeline_codegen/templates/runner_v0.sh.tpl
timeout 30s bash scripts/pipeline_codegen/smoke_meta_round_v0.sh
```

