# AutoAppDev API Contracts

This document defines the minimal request/response shapes used by the AutoAppDev controller PWA.

## Conventions
- Base URL (dev): `http://127.0.0.1:8788`
- Content type: `application/json`
- Errors: non-2xx responses typically return JSON like:

```json
{ "error": "some_code_or_message" }
```

## Settings (Config)

### GET /api/config
Returns current key/value configuration.

Response:
```json
{
  "config": {
    "agent": "codex",
    "model": "gpt-5.3-codex"
  }
}
```

### POST /api/config
Upserts one or more config keys.

Request (JSON object):
```json
{
  "agent": "codex",
  "model": "gpt-5.3-codex"
}
```

Response:
```json
{ "ok": true }
```

## Plan Payload

### GET /api/plan
Returns the currently stored plan payload (or `null` if none).

Response:
```json
{
  "plan": {
    "kind": "autoappdev_plan",
    "version": 1,
    "steps": [
      { "id": 1, "block": "plan" },
      { "id": 2, "block": "work" }
    ]
  }
}
```

### POST /api/plan
Stores the current plan payload.

Request:
```json
{
  "kind": "autoappdev_plan",
  "version": 1,
  "steps": [
    { "id": 1, "block": "plan" },
    { "id": 2, "block": "work" }
  ]
}
```

Response:
```json
{ "ok": true }
```

Response (error examples):
```json
{ "error": "invalid_json" }
```
```json
{ "error": "invalid_kind" }
```
```json
{ "error": "invalid_version" }
```
```json
{ "error": "steps_must_be_list" }
```

## Scripts

Pipeline scripts are persisted in Postgres for later reload.

### GET /api/scripts?limit=N
Lists recent scripts (metadata only).

Response:
```json
{
  "scripts": [
    {
      "id": 1,
      "title": "My script",
      "script_version": 1,
      "script_format": "aaps",
      "created_at": "2026-02-15T12:00:00+00:00",
      "updated_at": "2026-02-15T12:00:00+00:00"
    }
  ]
}
```

### POST /api/scripts
Creates a new script record.

Request:
```json
{
  "title": "My script",
  "script_text": "AUTOAPPDEV_PIPELINE 1\\n\\nTASK {\"id\":\"t1\",\"title\":\"Demo\"}\\n",
  "script_version": 1,
  "script_format": "aaps",
  "ir": { "kind": "autoappdev_ir", "version": 1, "tasks": [] }
}
```

Response:
```json
{ "ok": true, "script": { "id": 1, "title": "My script", "script_text": "...", "ir": { } } }
```

### GET /api/scripts/<id>
Fetches a single script by id.

Response:
```json
{ "script": { "id": 1, "title": "My script", "script_text": "...", "ir": { } } }
```

### PUT /api/scripts/<id>
Updates a script (partial updates supported).

Request:
```json
{ "title": "Renamed", "ir": null }
```

Response:
```json
{ "ok": true, "script": { "id": 1, "title": "Renamed", "script_text": "...", "ir": null } }
```

### DELETE /api/scripts/<id>
Deletes a script.

Response:
```json
{ "ok": true }
```

### POST /api/scripts/parse
Parses a formatted pipeline script (AAPS v1) into canonical IR (`autoappdev_ir` v1).

Request:
```json
{ "script_text": "AUTOAPPDEV_PIPELINE 1\\n\\nTASK {\"id\":\"t1\",\"title\":\"Demo\"}\\n" }
```

Response:
```json
{ "ok": true, "ir": { "kind": "autoappdev_ir", "version": 1, "tasks": [ ... ] } }
```

Response (error example):
```json
{ "ok": false, "error": "invalid_header", "line": 1, "detail": "expected header: AUTOAPPDEV_PIPELINE 1" }
```

### POST /api/scripts/import-shell
Best-effort import from an annotated shell script into canonical IR.

Notes:
- Only `# AAPS:` comment lines are extracted (no bash parsing).
- On error, `line` refers to the original **shell** line number.

Request:
```json
{ "shell_text": "#!/usr/bin/env bash\\n# AAPS: AUTOAPPDEV_PIPELINE 1\\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\\n" }
```

Response:
```json
{
  "ok": true,
  "script_format": "aaps",
  "script_text": "AUTOAPPDEV_PIPELINE 1\\n\\nTASK {\"id\":\"t1\",\"title\":\"Demo\"}\\n",
  "ir": { "kind": "autoappdev_ir", "version": 1, "tasks": [ ... ] },
  "warnings": []
}
```

Response (error example):
```json
{ "ok": false, "error": "missing_annotations", "line": 1, "detail": "expected at least one \"# AAPS:\" annotation line" }
```

### POST /api/scripts/parse-llm (optional)
LLM-assisted parse fallback for arbitrary “pipeline-like” text/scripts.

Notes:
- **Disabled by default.** Requires `AUTOAPPDEV_ENABLE_LLM_PARSE=1`.
- Uses `codex exec` non-interactively with a strict timeout.
- Stores provenance artifacts under `AUTOAPPDEV_RUNTIME_DIR/logs/llm_parse/<id>/` (prompt, input, raw JSONL, extracted AAPS, provenance JSON).
- The LLM output is post-validated by the deterministic AAPS parser (`parse_aaps_v1`); invalid output returns a parse error.

Request:
```json
{
  "source_text": "#!/usr/bin/env bash\\necho hello\\n",
  "source_format": "shell",
  "save": false
}
```

Response:
```json
{
  "ok": true,
  "script_format": "aaps",
  "script_text": "AUTOAPPDEV_PIPELINE 1\\n\\nTASK {\"id\":\"t1\",\"title\":\"Imported\"}\\n...",
  "ir": { "kind": "autoappdev_ir", "version": 1, "tasks": [ ... ] },
  "warnings": [],
  "provenance": {
    "id": "20260215T123456Z_abcd1234",
    "artifacts": { "dir": ".../runtime/logs/llm_parse/20260215T123456Z_abcd1234", "prompt": "...", "codex_jsonl": "..." }
  }
}
```

Response (error: disabled):
```json
{ "ok": false, "error": "disabled" }
```

Response (error: timeout):
```json
{ "ok": false, "error": "timeout", "detail": "codex exec exceeded timeout_s=45.0" }
```

## Actions

`/api/actions` refers to the **action registry** (stored definitions). Some executor endpoints also live under `/api/actions/*` (for example `update-readme`).

### GET /api/actions?limit=N
Lists registered action definitions (metadata only; does not include `spec`).

Notes:
- The backend may also expose **built-in** default actions in this list.
- Built-in actions are marked `readonly:true` and cannot be updated/deleted directly.

Response:
```json
{
  "actions": [
    {
      "id": 1,
      "title": "My prompt action",
      "kind": "prompt",
      "enabled": true,
      "readonly": false,
      "created_at": "2026-02-15T12:00:00+00:00",
      "updated_at": "2026-02-15T12:00:00+00:00"
    }
  ]
}
```

### POST /api/actions
Creates a new action definition.

Request:
```json
{
  "title": "My action",
  "kind": "prompt",
  "enabled": true,
  "spec": { "prompt": "..." }
}
```

Response:
```json
{ "ok": true, "action": { "id": 1, "title": "...", "kind": "prompt", "spec": { }, "enabled": true } }
```

### GET /api/actions/<id>
Fetches a single action definition (includes `spec`).

Response:
```json
{ "action": { "id": 1, "title": "...", "kind": "prompt", "spec": { }, "enabled": true, "readonly": false } }
```

### PUT /api/actions/<id>
Updates an action definition (partial update supported for `title`, `enabled`, and `spec`).

Request (example):
```json
{ "enabled": false }
```

Response:
```json
{ "ok": true, "action": { "id": 1, "enabled": false } }
```

Response (error: readonly):
```json
{ "error": "readonly", "detail": "built-in actions are read-only; clone to edit" }
```

### DELETE /api/actions/<id>
Deletes an action definition.

Response:
```json
{ "ok": true }
```

Response (error: readonly):
```json
{ "error": "readonly", "detail": "built-in actions are read-only; clone to edit" }
```

### POST /api/actions/<id>/clone
Clones a readonly built-in action into a new editable action definition stored in the DB.

Response:
```json
{ "ok": true, "action": { "id": 123, "title": "...", "kind": "prompt", "spec": { }, "enabled": true, "readonly": false } }
```

### POST /api/actions/update-readme
Safely upserts the owned README block for a workspace under `auto-apps/` (see `docs/common-actions.md`).

Request:
```json
{
  "workspace": "my_workspace",
  "block_markdown": "## Workspace Status...\\n\\n## Philosophy\\n..."
}
```

Response (success):
```json
{
  "ok": true,
  "workspace": "my_workspace",
  "path": "auto-apps/my_workspace/README.md",
  "updated": true,
  "markers_preexisted": false,
  "artifacts": { "dir": ".../runtime/logs/update_readme/<id>" }
}
```

Notes:
- `workspace` must be a single path segment (no `/` or `\\`, no `.` or `..`).
- Only the block between `<!-- AUTOAPPDEV:README:BEGIN -->` and `<!-- AUTOAPPDEV:README:END -->` is replaced/owned.
- `block_markdown` must include a `## Philosophy` section and must not contain the marker strings.

Response (error examples):
```json
{ "ok": false, "error": "invalid_workspace" }
```
```json
{ "ok": false, "error": "missing_philosophy", "detail": "block_markdown must include a '## Philosophy' section" }
```
```json
{ "ok": false, "error": "marker_mismatch", "detail": "expected exactly one begin+end marker; got begin=1 end=0" }
```

## Workspaces

Workspace configuration is stored per workspace under `auto-apps/<workspace>/` and validated with safe path rules.

### GET /api/workspaces/<workspace>/config
Fetches the stored config for a workspace. If none exists yet, returns defaults with `exists:false`.

Response (not found yet):
```json
{
  "ok": true,
  "workspace": "my_workspace",
  "exists": false,
  "config": {
    "materials_paths": ["materials"],
    "shared_context_text": "",
    "shared_context_path": "",
    "default_language": "en"
  },
  "updated_at": null
}
```

Response (found):
```json
{
  "ok": true,
  "workspace": "my_workspace",
  "exists": true,
  "config": {
    "materials_paths": ["materials", "materials/screenshots"],
    "shared_context_text": "...\n",
    "shared_context_path": "docs/shared_context.md",
    "default_language": "en"
  },
  "updated_at": "2026-02-15T12:00:00+00:00"
}
```

### POST /api/workspaces/<workspace>/config
Upserts workspace config. Partial updates are allowed; backend applies defaults and normalizes/validates paths.

Request:
```json
{
  "materials_paths": ["materials"],
  "shared_context_path": "docs/shared_context.md",
  "default_language": "en"
}
```

Response:
```json
{ "ok": true, "workspace": "my_workspace", "config": { }, "updated_at": "..." }
```

Notes:
- `workspace` must be a single path segment (no `/` or `\\`, no `.` or `..`).
- `materials_paths` entries and `shared_context_path` are workspace-relative, but are validated to resolve under `auto-apps/<workspace>/` (no traversal/outside writes).
- `default_language` must be one of: `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `vi`, `ar`, `fr`, `es`.

## Inbox Messages
The UI refers to “Chat/Inbox”.

- `/api/inbox` is the first-class inbox persistence API.
- `/api/chat` is a simple chat log API (older UI); the current PWA uses `/api/inbox` for guidance messages.

Side effect:
- When a user posts to `/api/inbox` or `/api/chat`, the backend also writes a `runtime/inbox/*_user.md` file so pipeline scripts can consume guidance.

### GET /api/inbox?limit=N
Lists recent inbox messages.

Request:
- Query string: `limit` (default 50)

Response:
```json
{
  "messages": [
    {
      "id": 123,
      "role": "user",
      "content": "hello inbox",
      "created_at": "2026-02-15T12:34:56.789+00:00"
    }
  ]
}
```

### POST /api/inbox
Adds an inbox message.

Request:
```json
{ "content": "hello inbox" }
```

Response:
```json
{ "ok": true }
```

Response (error examples):
```json
{ "error": "invalid_body" }
```
```json
{ "error": "empty" }
```
```json
{ "error": "too_long" }
```

## Outbox Messages
Pipeline -> UI message channel.

- `/api/outbox` is the first-class outbox persistence API.
- Pipelines can write to outbox either:
  - via HTTP `POST /api/outbox`, or
  - by writing files under `runtime/outbox/` (see below).

### GET /api/outbox?limit=N
Lists recent outbox messages.

Request:
- Query string: `limit` (default 50)

Response:
```json
{
  "messages": [
    {
      "id": 123,
      "role": "pipeline",
      "content": "hello from pipeline",
      "created_at": "2026-02-15T12:34:56.789+00:00"
    }
  ]
}
```

### POST /api/outbox
Adds an outbox message.

Request:
```json
{ "role": "pipeline", "content": "hello from pipeline" }
```

Notes:
- `role` is optional and defaults to `pipeline` (allowlist: `pipeline`, `system`).

Response (success):
```json
{ "ok": true }
```

Response (error examples):
```json
{ "error": "invalid_body" }
```
```json
{ "error": "empty" }
```
```json
{ "error": "too_long" }
```

### File Queue: runtime/outbox/
If you prefer not to call HTTP from a pipeline, you can write an outbox message file:
- Path: `runtime/outbox/<ts>_<role>.md` (or `.txt`)
  - Example: `runtime/outbox/1739655400123_pipeline.md`
- The backend periodically ingests these files into `/api/outbox` and moves them to:
  - `runtime/outbox/processed/`

Recommended atomic write pattern:
1. Write to a temp file, then rename into `runtime/outbox/`:
```bash
printf 'hello\n' > runtime/outbox/.tmp && mv runtime/outbox/.tmp runtime/outbox/$(date +%s%3N)_pipeline.md
```

### GET /api/chat?limit=N
Lists recent chat messages.

Request:
- Query string: `limit` (default 50)

Response:
```json
{
  "messages": [
    {
      "id": 123,
      "role": "user",
      "content": "Please focus on the next small task.",
      "created_at": "2026-02-15T12:34:56.789+00:00"
    }
  ]
}
```

### POST /api/chat
Adds a chat message.

Request:
```json
{ "content": "Please focus on the next small task." }
```

Response (success):
```json
{ "ok": true }
```

Response (error example):
```json
{ "error": "empty" }
```

## Pipeline

### GET /api/pipeline
Returns the current pipeline state and timestamps.

Response:
```json
{
  "pipeline": {
    "state": "stopped",
    "pid": null,
    "run_id": null,
    "started_at": null,
    "paused_at": null,
    "resumed_at": null,
    "stopped_at": "2026-02-15T12:00:02.345+00:00",
    "updated_at": "2026-02-15T12:00:02.345+00:00"
  }
}
```

### GET /api/pipeline/status
Returns the latest pipeline run state.

Response:
```json
{
  "status": {
    "running": false,
    "pid": null,
    "run_id": null,
    "state": "idle"
  }
}
```

### POST /api/pipeline/start
Starts the pipeline subprocess.

Request (all fields optional):
```json
{
  "script": "scripts/auto-autoappdev-development.sh",
  "cwd": "/home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev",
  "args": []
}
```

Response (success):
```json
{ "ok": true, "pid": 4242, "run_id": 7 }
```

Response (error examples):
```json
{ "ok": false, "error": "already_running" }
```
```json
{ "ok": false, "error": "args_must_be_list" }
```
```json
{ "ok": false, "error": "script_outside_repo" }
```
```json
{ "ok": false, "error": "script_not_found", "path": "/abs/path/to/script" }
```

### POST /api/pipeline/stop
Stops the running pipeline.

Request:
```json
{}
```

Response:
```json
{ "ok": true }
```

Response (invalid transition example):
```json
{
  "ok": false,
  "error": "invalid_transition",
  "from": "stopped",
  "action": "stop",
  "detail": "cannot stop when stopped"
}
```

### POST /api/pipeline/pause
Pauses the pipeline (implemented as a runtime pause flag).

Request:
```json
{}
```

Response:
```json
{ "ok": true }
```

### POST /api/pipeline/resume
Resumes the pipeline (removes the runtime pause flag).

Request:
```json
{}
```

Response:
```json
{ "ok": true }
```

## Logs

### GET /api/logs?source=pipeline&since=<id>&limit=N
Returns incremental log entries after `since` for a given source.

Response:
```json
{
  "source": "pipeline",
  "since": 0,
  "next": 12,
  "lines": [
    { "id": 11, "ts": "2026-02-15T12:00:00+00:00", "source": "pipeline", "line": "line 1" },
    { "id": 12, "ts": "2026-02-15T12:00:01+00:00", "source": "pipeline", "line": "line 2" }
  ]
}
```

### GET /api/logs/tail?name=pipeline|backend&lines=N
Returns the last N lines of a named log.

Request:
- Query string:
  - `name`: `pipeline` or `backend`
  - `lines`: clamped to 10..2000

Response:
```json
{
  "name": "pipeline",
  "lines": [
    "line 1",
    "line 2"
  ]
}
```

Response (error example):
```json
{ "error": "unknown_log" }
```

## Appendix: Version + Health
Not required by this task, but useful for UI status.

### GET /api/version
Response:
```json
{
  "ok": true,
  "app": "autoappdev",
  "service": "autoappdev-backend",
  "version": "dev",
  "build": "2026-02-15T12:00:00+00:00",
  "started_at": "2026-02-15T12:00:00+00:00"
}
```

### GET /api/health
Response:
```json
{
  "ok": true,
  "service": "autoappdev-backend",
  "db": { "ok": true, "time": "2026-02-15T12:00:01.234+00:00" }
}
```
