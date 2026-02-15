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
