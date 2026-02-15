# Workspace Layout Contract (v0)

AutoAppDev runs long-lived pipelines. To keep pipelines portable, resumable, and safe, we standardize a small set of folders and what belongs in each.

This document defines:
- A **workspace root** layout (durable, project-scoped).
- A separate **runtime dir** layout (ephemeral, run-scoped).

## Terms
- **Controller repo**: this repository (`/home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev`), which contains the backend + PWA + scripts.
- **Workspace root**: a directory that a pipeline/action treats as the boundary for allowed file reads/writes. Workspaces are intended to live under `auto-apps/` in the controller repo.
- **Runtime dir**: an ephemeral directory used for live pipeline control (pause/resume), live logs, and file-based inbox/outbox queues.

## Standard Workspace Folders
These folders are defined relative to a workspace root:

| Path | Purpose | Typical producer/consumer | Durability |
|---|---|---|---|
| `materials/` | Input assets: screenshots, docs, datasets, reference code, etc. | User, pipeline reads | Durable |
| `interactions/` | Human-in-the-loop records: user messages, decisions, approvals, “why” notes. | Pipeline writes; human reads | Durable |
| `outputs/` | Exported artifacts: builds, reports, generated packages, exports for sharing. | Pipeline writes | Durable (often not committed) |
| `docs/` | Human-readable documentation for the workspace/app. | Pipeline writes; human reads | Durable |
| `references/` | Machine-oriented state: task contexts, prompts, summaries, run metadata. | Pipeline writes/reads | Durable (often committed selectively) |
| `scripts/` | Runnable drivers, generated helpers, one-off reproducible scripts. | Pipeline writes; pipeline/human runs | Durable |
| `tools/` | Reusable tools invoked by scripts/actions (wrappers, helpers, skills). | Pipeline/human runs | Durable |
| `logs/` | Durable/archived logs (distinct from runtime live logs). | Pipeline writes | Durable (often not committed) |

### `auto-apps/` (Workspace Container)
In the controller repo, `auto-apps/` is the conventional container for one or more workspace roots (generated apps/workspaces).

Existing scripts already assume this convention:
- `scripts/app-auto-development.sh` defaults `--auto-apps-root` to `auto-apps/` and creates `auto-apps/backend`, `auto-apps/pwa`, etc.
- `scripts/setup_backend_env.sh` currently points at `auto-apps/backend/requirements.txt`.

## Runtime Dir (Ephemeral)
Runtime paths are not part of the durable workspace contract. They are for live operation.

AutoAppDev uses:
- `AUTOAPPDEV_RUNTIME_DIR` (defaults to `./runtime`) to select the runtime dir. See `docs/env.md` and `backend/app.py` (`_compute_paths`).
- `runtime/PAUSE` as the pause flag file for pipeline pause/resume. See `backend/app.py` (`PipelineControl.pause_flag`) and `scripts/pipeline_demo.sh`.
- `runtime/logs/` for live log tailing (pipeline + backend). See `backend/app.py` (log tailers) and generated runners such as `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`.
- `runtime/inbox/` for a file-based inbox queue (`*_user.md`) written when users post messages. See `backend/app.py` (`_write_inbox_message`) and the note in `docs/api-contracts.md`.
- `runtime/outbox/` for a file-based outbox queue (`<ts>_<role>.md` / `.txt`) written by pipeline scripts. The backend ingests these into `/api/outbox` and moves processed files to `runtime/outbox/processed/` (see `docs/api-contracts.md`).

By default, `runtime/` is gitignored (see `.gitignore`), so it should be created locally and treated as ephemeral.

## Safety / Guardrails (Contract Intent)
- Actions and generated scripts should treat **workspace root** as the maximum allowed write scope.
- Avoid writing to arbitrary absolute paths; prefer relative paths under the workspace root or runtime dir.
- Live operational files (pause flag, live logs, inbox queue) belong under the runtime dir, not under the workspace root.

Future tasks will harden these rules (safe path checks, rejection of writes outside `auto-apps/`, etc.), but the contract is defined here so behavior remains consistent.

## Init Checklist (Simple)
From the controller repo root:

1. Create local env config:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
cp .env.example .env
```

2. Ensure runtime dirs exist (ephemeral; gitignored):
```bash
mkdir -p runtime/logs runtime/inbox runtime/outbox
```

3. Create a new workspace root under `auto-apps/` (durable):
```bash
WS="auto-apps/my_workspace"
mkdir -p "$WS"/{materials,interactions,outputs,docs,references,scripts,tools,logs}
```

4. (Optional) Run the demo pipeline and verify pause behavior:
- Pipeline pause flag: create/remove `runtime/PAUSE`
- Demo runner: `scripts/pipeline_demo.sh`
