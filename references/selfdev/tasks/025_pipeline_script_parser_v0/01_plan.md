# Plan: 025 pipeline_script_parser_v0

## Goal
Implement a deterministic backend parser for the formatted pipeline script (AAPS v1) into canonical IR (`autoappdev_ir` v1):
- Never executes code (parse only).
- Invalid input returns actionable errors (line number, reason).
- Deterministic: same input -> same IR or same error.

Acceptance:
- Backend parses AAPS v1 into IR.
- Invalid input returns actionable errors.
- Parsing never executes code.

## Current State (References)
- Script + IR spec exists:
  - `docs/pipeline-formatted-script-spec.md`:
    - Header: `AUTOAPPDEV_PIPELINE 1`
    - Statements: `TASK|STEP|ACTION <json-object>`
    - Nesting rules + required keys
    - Canonical IR: `{ kind:"autoappdev_ir", version:1, tasks:[{steps:[{actions:[]}]}] }`
- Example artifacts exist:
  - `examples/pipeline_formatted_script_v1.aaps`
  - `examples/pipeline_ir_v1.json`
- Backend patterns:
  - Tornado handlers in `backend/app.py`
  - Storage/persistence in `backend/storage.py`
  - API contracts in `docs/api-contracts.md`
- Script storage API exists (from task 024):
  - `/api/scripts` persists `script_text` and `ir` (optional).

## Approach (Minimal / Deterministic)
1. Add a small parser module `backend/pipeline_parser.py`:
   - Pure functions, no I/O, no subprocess calls.
   - Parses text into IR or raises a structured `ParseError` including line number and error code.
2. Add a single endpoint to parse arbitrary script text:
   - `POST /api/scripts/parse` with `{ "script_text": "..." }` -> `{ "ok": true, "ir": {...} }`
   - On error: `400` with `{ "ok": false, "error": "...", "line": N, "detail": "..." }`
3. (Optional small win) Allow parsing a stored script by id:
   - `POST /api/scripts/<id>/parse` (fetch script_text from DB, parse, and optionally persist `ir` via `update_pipeline_script(..., ir_set=True)`).
   - Keep optional for later if scope grows; primary acceptance is parsing itself.

## Implementation Steps (Next Phase)
1. Create `backend/pipeline_parser.py`.
   - Define:
     - `class ParseError(Exception): ...` with fields:
       - `code` (string), `line` (int), `detail` (string)
     - `parse_aaps_v1(text: str) -> dict[str, Any]`
   - Parser behavior:
     - Strip UTF-8 BOM if present.
     - Split lines with `splitlines()` preserving line numbers (1-based).
     - Skip blank lines and comment lines (`lstrip().startswith("#")`).
     - First non-comment line must be exactly `AUTOAPPDEV_PIPELINE 1` (case-sensitive).
     - For statement lines:
       - Accept leading indentation.
       - Parse `KEYWORD` as first token.
       - The rest of the line must be JSON object text; parse via `json.loads`.
       - Enforce object type `dict` (not list/str).
     - Maintain current context:
       - current task, current step
       - `STEP` before `TASK` -> error `step_before_task`
       - `ACTION` before `STEP` -> error `action_before_step`
     - Validate required keys/types:
       - `TASK.id/title` strings
       - `STEP.id/title` strings; `block` in allowed set: `plan/work/debug/fix/summary/commit_push`
       - `ACTION.id/kind` strings; `params/meta` if present must be dict
     - Enforce uniqueness:
       - Task IDs unique in file
       - Step IDs unique within task
       - Action IDs unique within step
     - Build canonical IR with minimal optional fields:
       - Always emit `kind:"autoappdev_ir"`, `version:1`, `tasks:[...]`
       - Include `meta` only if present and is an object

2. Add parse endpoint handler in `backend/app.py`.
   - Add `ScriptsParseHandler`:
     - `POST /api/scripts/parse`
       - Parse JSON body, require `script_text` string
       - Call `pipeline_parser.parse_aaps_v1(script_text)`
       - Return `{ "ok": true, "ir": ir }`
       - On `ParseError`: `400` and include `error`, `line`, `detail`
   - Register route in `make_app()` near other `/api/scripts*` routes.

3. Update API docs.
   - `docs/api-contracts.md`:
     - Add to “Scripts” section:
       - `POST /api/scripts/parse`
       - Example request/response and error response.

4. Add a minimal parser unit smoke script (optional, but useful).
   - Add `backend/parse_script_smoketest.py`:
     - Reads `examples/pipeline_formatted_script_v1.aaps`
     - Parses to IR
     - Exits 0 if ok, else prints error and exits non-zero
   - Keep optional if we want to keep changes smallest; `py_compile` + `python -c` smoke may suffice.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f backend/pipeline_parser.py
rg -n 'class ParseError|def parse_aaps_v1' backend/pipeline_parser.py
rg -n '/api/scripts/parse' backend/app.py docs/api-contracts.md

timeout 5s python3 -m py_compile backend/app.py backend/pipeline_parser.py

# Quick functional smoke: parse the example script deterministically
python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_formatted_script_v1.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
assert ir["tasks"] and ir["tasks"][0]["steps"]
print("OK")
PY
```

Manual verification (outside this sandbox, which cannot bind ports):
1. Start backend.
2. `curl -s -X POST http://127.0.0.1:8788/api/scripts/parse -d @- -H 'content-type: application/json' <<<'{\"script_text\":\"AUTOAPPDEV_PIPELINE 1\\n\\nTASK {\\\"id\\\":\\\"t1\\\",\\\"title\\\":\\\"Demo\\\"}\\n\"}' | jq`
3. Confirm it returns `{ ok:true, ir:{...} }`.
4. Send an invalid script and confirm 400 with line number and detail.

## Acceptance Checklist
- [ ] Deterministic parser implemented (`backend/pipeline_parser.py`) and does not execute code.
- [ ] Backend exposes `POST /api/scripts/parse` returning IR or actionable 400 errors with line number.
- [ ] Docs updated (`docs/api-contracts.md`) to document the parse endpoint and error shape.

