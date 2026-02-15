# Plan: 049 runner_outbox_progress_helper

## Goal
Add a small, runner-native helper to publish **progress updates** to the file-based outbox queue:
- Write progress messages to `"$AUTOAPPDEV_RUNTIME_DIR/outbox/"` using the atomic rename pattern (no HTTP/curl required).
- Update the generated runner’s `meta_round_v0` loop to use this helper so the PWA (via backend `/api/outbox` ingestion) can observe meta-task progress.

Acceptance:
- Runner template adds a helper to write progress updates to `runtime/outbox/`.
- Meta-round loop uses the helper so the PWA can observe progress (via file queue ingestion).

## Current State (Relevant Files)
- Outbox queue contract + ingestion:
  - `docs/api-contracts.md` (runtime outbox file queue format and atomic write pattern)
  - `docs/workspace-layout.md` (runtime/outbox in runtime contract)
  - `backend/app.py` (`_ingest_outbox_files()` ingests `runtime/outbox/<ts>_<role>.md|.txt` into DB)
  - `pwa/app.js` (`loadChat()` fetches `/api/outbox` and renders it in Inbox/Chat tab)
- Runner + meta-round loop:
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl` (generated runner template; meta-round loop lives here)
  - `scripts/pipeline_codegen/generate_runner_from_ir.py` (enables meta-round mode and calls `meta_round_run_template_tasks`)
  - `scripts/pipeline_codegen/smoke_meta_round_v0.sh` (current smoke for loop + resume)

## Proposed Minimal Design
1. Add a bash helper to the runner template:
   - `outbox_write <content> [role]`
   - Writes a single message file into `"$RUNTIME_DIR/outbox/"` as:
     - `<ts>_<role>.md` where `<ts>` is digits (we can use a nanosecond timestamp for uniqueness).
   - Uses atomic write: write to a temp file in `runtime/outbox/`, then rename into place.
   - Best-effort: failures should not crash the runner (progress is auxiliary).
   - Restrict role to backend allowlist (`pipeline|system`), default `pipeline`.

2. Use the helper from the meta-round loop:
   - In `meta_round_run_template_tasks()` emit outbox progress messages for:
     - skip: `SKIP META_TASK <id>: already completed`
     - start: `META_TASK <id>: start` (optionally include title)
     - done: `META_TASK <id>: done`
   - Keep stdout logs as-is; the outbox is an additional operator channel.

3. Update smoke to prove files are written:
   - Extend `scripts/pipeline_codegen/smoke_meta_round_v0.sh` to assert:
     - after first run, `"$runtime_dir/outbox/"` contains at least one `^[0-9]+_pipeline\\.(md|txt)$` file
     - file contents include `META_TASK t1` / `META_TASK t2` (start/done), and on second run include `SKIP META_TASK t1` / `t2` if you also emit skip updates.
   - Keep existing resume assertions unchanged.

4. Docs (minimal, runner-focused):
   - Update `docs/pipeline-runner-codegen.md` (Runtime Conventions) to mention:
     - generated runners include an outbox helper for writing status/progress to `runtime/outbox/`
     - meta-round loop emits progress messages there (so PWA can observe without HTTP calls).

## Implementation Steps (Next Phase: WORK)

### 1) Runner Template: Add Outbox Helper
Edit `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`:
- Add an `OUTBOX_DIR="$RUNTIME_DIR/outbox"` variable near other runtime paths.
- Add function:
  - `outbox_write()`:
    - `mkdir -p "$OUTBOX_DIR"` (best-effort)
    - generate unique `<ts>` (recommend: `python3 - <<'PY' ... time.time_ns() ...`)
    - write content to `"$OUTBOX_DIR/.tmp.<ts>.$$"` then `mv` to `"$OUTBOX_DIR/<ts>_<role>.md"`
    - on failure: print a warning via `log` and return 0.

### 2) Meta-round Loop: Emit Progress Updates
Edit `scripts/pipeline_codegen/templates/runner_v0.sh.tpl` in `meta_round_run_template_tasks()`:
- On skip: call `outbox_write "SKIP META_TASK $task_id: already completed" pipeline`
- Before running the template: call `outbox_write "META_TASK $task_id: start\\n$task_title" pipeline` (or single-line)
- After successful completion: call `outbox_write "META_TASK $task_id: done" pipeline`

### 3) Smoke: Validate Outbox Messages Are Written
Edit `scripts/pipeline_codegen/smoke_meta_round_v0.sh`:
- After run #1:
  - `test -d "$runtime_dir/outbox"`
  - `ls "$runtime_dir/outbox" | rg -n '^[0-9]+_pipeline\\.(md|txt)$'`
  - `rg -n 'META_TASK t1' "$runtime_dir/outbox"/*.md` (and `t2`)
- After run #2:
  - If emitting skip messages: `rg -nF 'SKIP META_TASK t1: already completed' "$runtime_dir/outbox"/*.md`
  - Keep existing stdout-based skip assertions unchanged (they’re still useful).

### 4) Docs
Edit `docs/pipeline-runner-codegen.md`:
- Add a short section under Runtime Conventions describing `runtime/outbox/` helper and that meta-round uses it for progress.

## Verification Commands (DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
timeout 10s bash -n scripts/pipeline_codegen/templates/runner_v0.sh.tpl

timeout 30s bash scripts/pipeline_codegen/smoke_meta_round_v0.sh

# Optional regressions
timeout 20s bash scripts/pipeline_codegen/smoke_conditional_steps.sh
timeout 20s bash scripts/pipeline_codegen/smoke_placeholders.sh
timeout 20s bash scripts/pipeline_codegen/smoke_codegen.sh
```

## Acceptance Checklist
- [ ] Generated runner template includes an outbox helper that writes `runtime/outbox/<ts>_pipeline.md` using atomic rename.
- [ ] In meta-round mode, the runner emits outbox progress messages for template task start/done (and optionally skip).
- [ ] `smoke_meta_round_v0.sh` demonstrates outbox files being created alongside existing loop+resume behavior.

