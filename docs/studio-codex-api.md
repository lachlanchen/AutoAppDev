# Studio Codex API

AutoAppDev keeps the browser deterministic and moves agent work into a local, file-backed API.

## Routes

- `POST /api/codex/respond`: synchronous response wrapper for `codex exec`; default model `gpt-5.5`, reasoning `medium`, read-only sandbox.
- `POST /api/codex/jobs`: durable async job API; use `tool:"assistant"` for high-reasoning delegated work.
- `GET /api/codex/jobs`: list recent jobs.
- `GET /api/codex/job?id=<job-id>`: inspect status, logs, and output.
- `GET /api/codex/result?id=<job-id>`: fetch output once ready.
- `POST /api/studio/chat/new`: start a new tab-scoped chat session.
- `GET|POST /api/studio/chat`: load or append Studio chat messages; optional `assistant_enabled:true` queues a delegated assistant.
- `GET /api/studio/preview`: tab-specific preview for Notes, Design, AutoPilot Loop, and Setup.
- `GET /api/studio/agent/status`: recent job counts for the UI badge.

## Storage

Codex jobs are stored under `runtime/codex-jobs/<job-id>/` with `input.json`, `prompt.txt`, `job.json`, logs, and `output.json`. Studio chats are stored under `runtime/studio-chats/<session-id>/`. Both are runtime artifacts and remain ignored by Git.

## AutoPilot Loop Safety

The strict editable schema is AAPS v1. Accepted/proposed loop files live in `references/autopilot/loop/`:

- `accepted.aaps`: active parseable loop.
- `proposed.aaps`: written only after backend grammar validation passes.
- `history/*.aaps`: append-only recovery snapshots.
- `edits.jsonl`: append-only edit ledger.

Use `scripts/validate_autopilot_loop.sh` before committing. Set `AUTOAPPDEV_VALIDATE_IN_DOCKER=1` to validate inside Docker when available. The backend can optionally auto-commit accepted loop changes with `AUTOAPPDEV_AUTOPILOT_AUTOCOMMIT=1`, but it never pushes silently.
