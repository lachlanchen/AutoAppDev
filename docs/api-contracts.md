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

## Inbox Messages
The UI refers to “Chat/Inbox”.

- `/api/inbox` is the first-class inbox persistence API.
- `/api/chat` is the chat log API used by the current PWA.

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
