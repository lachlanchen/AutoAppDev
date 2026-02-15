# Common Actions (v0)

This document defines a small set of **common** `ACTION.kind` values used in AutoAppDev pipelines.

Notes:
- In the AAPS/IR schema, actions are **data**. Execution is an engine concern.
- These specs define **contracts** so the PWA, backend, and runner generators can agree on behavior.

Related docs:
- `docs/pipeline-formatted-script-spec.md` (AAPS + IR schema)
- `docs/workspace-layout.md` (workspace root + safe folder conventions)

## update_readme

### Purpose
Keep a workspace README current and reproducible by upserting an auto-managed block containing:
- a canonical `## Philosophy` section (how the workspace is meant to be developed/run)
- a status/progress section (optional; engine-specific)

### Target Path (No Arbitrary Writes)
This action targets a workspace README under the controller repo's `auto-apps/` container.

Parameters:
- `params.workspace` (required, string)
  - A **workspace slug** identifying a child directory under `auto-apps/`.
  - Must be a **single path segment** (no `/` or `\\`), and must not be `.` or `..`.

Resolved target file:
- `auto-apps/<workspace>/README.md`

Forbidden:
- Any parameter that supplies an arbitrary filesystem path (e.g. `path`, `readme_path`, `output_path`).

Implementations MUST:
- resolve the path under the controller repo root
- reject any path traversal attempts
- reject any resolved paths outside `auto-apps/`

### Markers (Owned Block)
The content updated by this action is delimited by fixed HTML comment markers:

- Begin marker: `<!-- AUTOAPPDEV:README:BEGIN -->`
- End marker: `<!-- AUTOAPPDEV:README:END -->`

Semantics:
- Content **between** markers is owned by AutoAppDev and may be replaced wholesale.
- Content **outside** markers is user-owned and must be preserved.
- If markers do not exist, implementations should insert them (recommended location: after the first H1 if present; otherwise at top).
- If the file does not exist, implementations should create it with a minimal heading and the marker block.

### Action Payload
`ACTION.kind`:
- `"update_readme"`

`params`:
- `workspace` (required string; see "Target Path")
- `block_markdown` (optional string)
  - If provided: the exact markdown to place between the markers.
  - If omitted/empty: the engine/backend should use the **default block template** below.

### Default Block Template (Includes Philosophy)
The default block content between markers should be:

```md
## Workspace Status (Auto-Updated)

- Updated: <utc-iso-timestamp>
- Pipeline state: <stopped|running|paused> (optional)

This section is updated by AutoAppDev.
Do not edit content between the markers.

## Philosophy
AutoAppDev treats agents as tools and keeps work stable via a strict, resumable loop:
1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push (if used by the workflow)
```

Engines may add additional workspace-specific info (links to logs, run ids, etc.), but should keep the Philosophy section present and stable.

### Example (AAPS v1)
```text
ACTION {"id":"a1","kind":"update_readme","params":{"workspace":"my_workspace"}}
```

### Example (IR v1)
```json
{
  "id": "a1",
  "kind": "update_readme",
  "params": { "workspace": "my_workspace" }
}
```
