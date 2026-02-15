# Plan: 030 workspace_layout_standardization

## Goal
Document a standard AutoAppDev workspace layout (folders + contracts) so pipelines are portable/resumable and file writes stay safe/predictable.

Acceptance:
- Docs define standard folders: `materials/`, `interactions/`, `outputs/`, `docs/`, `references/`, `scripts/`, `tools/`, `logs/`, `auto-apps/`
- Docs explain how AutoAppDev uses each folder.
- Docs include a simple initialization checklist (commands ok).

## Current State (References)
- Repo root currently contains: `docs/`, `scripts/`, `references/`, `runtime/`, `backend/`, `pwa/`, `examples/`.
- Runtime conventions are already implemented:
  - Backend computes runtime/log paths from `AUTOAPPDEV_RUNTIME_DIR` (default `./runtime`): `backend/app.py` (`_compute_paths`, `PipelineControl.pause_flag`, log tailers).
  - Pause/resume uses `runtime/PAUSE`: `backend/app.py` + `scripts/pipeline_demo.sh` + generated runners (`scripts/pipeline_codegen/templates/runner_v0.sh.tpl`).
  - Inbox bridge writes `runtime/inbox/*_user.md`: `docs/api-contracts.md` (inbox/chat notes).
- Generated-app workspace root is already assumed by existing scripts:
  - `scripts/app-auto-development.sh` uses `--auto-apps-root` default `auto-apps/` and creates `auto-apps/backend`, `auto-apps/pwa`, etc.
  - `scripts/setup_backend_env.sh` expects `auto-apps/backend/requirements.txt`.

## Deliverable (Docs Only)
1. Add a dedicated workspace contract doc
   - Create: `docs/workspace-layout.md`
   - Include sections:
     - Terms: “controller repo” vs “generated app workspace”, and “runtime (ephemeral) vs workspace (durable)”.
     - Standard folders table (path, purpose, producer/consumer, committed vs ephemeral).
     - Safety/guardrails:
       - Actions should only write within a declared workspace root (future enforcement), and never arbitrary absolute paths.
       - Runtime writes go under `AUTOAPPDEV_RUNTIME_DIR` only.
     - Concrete examples that reference real code:
       - `AUTOAPPDEV_RUNTIME_DIR` usage: `docs/env.md`, `backend/app.py`.
       - Pause flag file: `backend/app.py`, `scripts/pipeline_demo.sh`.
       - Codex action artifacts under runtime logs: `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`.
     - “Init checklist” (simple + deterministic):
       - Repo init: copy `.env`, ensure runtime dirs exist.
       - Workspace init: ensure `auto-apps/` exists and create the standard subfolders under the chosen workspace root.
       - Explicitly note that `runtime/` is gitignored by default (`.gitignore`), so it must be created locally.
     - Optional: a short “What goes where?” example (1-2 `tree` snippets).

2. Link the new doc from the main index
   - Update `README.md` Contents list to add:
     - `docs/workspace-layout.md`: Standard workspace folders + contracts (materials/interactions/outputs/…)

3. Keep changes minimal
   - Do not create new top-level directories in this task (docs only).
   - Do not change backend/PWA behavior; only document the established conventions and the intended contract.

## Commands To Run (Verification)
Doc-only verification:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/workspace-layout.md

# Ensure the doc mentions every required standard folder name at least once.
rg -n \"\\bmaterials/\\b\" docs/workspace-layout.md
rg -n \"\\binteractions/\\b\" docs/workspace-layout.md
rg -n \"\\boutputs/\\b\" docs/workspace-layout.md
rg -n \"\\bdocs/\\b\" docs/workspace-layout.md
rg -n \"\\breferences/\\b\" docs/workspace-layout.md
rg -n \"\\bscripts/\\b\" docs/workspace-layout.md
rg -n \"\\btools/\\b\" docs/workspace-layout.md
rg -n \"\\blogs/\\b\" docs/workspace-layout.md
rg -n \"\\bauto-apps/\\b\" docs/workspace-layout.md

# Ensure README links it in Contents.
rg -n \"docs/workspace-layout\\.md\" README.md
```

## Acceptance Checklist
- [ ] `docs/workspace-layout.md` exists and clearly defines the standard folders and their roles.
- [ ] The doc explicitly explains runtime vs workspace storage and references current implementations (`backend/app.py`, `docs/env.md`, `docs/api-contracts.md`, `scripts/app-auto-development.sh`).
- [ ] The doc includes a simple init checklist with concrete commands.
- [ ] `README.md` links to the new doc.

