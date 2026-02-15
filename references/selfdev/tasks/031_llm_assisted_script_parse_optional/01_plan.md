# Plan: 031 llm_assisted_script_parse_optional

## Goal
Add an **optional** backend endpoint that uses **Codex (non-interactive CLI)** to convert an arbitrary “pipeline-like” script/text into the canonical pipeline IR (`autoappdev_ir` v1).

Acceptance:
- Backend exposes an optional endpoint that runs `codex exec` non-interactively to perform the conversion.
- The endpoint runs with strict guardrails + timeouts.
- The endpoint stores provenance + prompts (artifacts) for later audit/debug.

## Current State (References)
- Deterministic parsers already exist (no execution):
  - AAPS v1 parser: `backend/pipeline_parser.py` (`parse_aaps_v1`)
  - Annotated shell import v0: `backend/pipeline_shell_import.py` (extract `# AAPS:` only)
  - Endpoints: `backend/app.py`
    - `POST /api/scripts/parse`
    - `POST /api/scripts/import-shell`
- Canonical script + IR spec:
  - `docs/pipeline-formatted-script-spec.md`
- Script UX currently expects AAPS -> IR to render blocks:
  - PWA Script tab calls `/api/scripts/parse` and `/api/scripts/import-shell`: `pwa/app.js`
- Storage is available if we want to optionally persist results:
  - `pipeline_scripts` table: `backend/schema.sql`
  - `Storage.create_pipeline_script(...)`: `backend/storage.py`

## Design Choice (Minimal + Safer)
Have Codex output **AAPS v1 text**, then validate it with the existing deterministic parser:
1. `codex exec` produces a candidate AAPS v1 script.
2. Backend extracts the AAPS region (strip fences / extra text).
3. Backend runs `parse_aaps_v1(script_text)` to produce IR.

This keeps the LLM output constrained and reuses existing validation/error reporting.

## Endpoint Contract (Proposed)
Add:
- `POST /api/scripts/parse-llm` (optional; disabled by default)

Request (JSON):
```json
{
  "source_text": "<arbitrary text or script>",
  "source_format": "shell|aaps|unknown",
  "title": "Optional title for saving",
  "save": false,
  "model": "gpt-5.3-codex",
  "reasoning": "medium",
  "timeout_s": 45
}
```

Response (success):
```json
{
  "ok": true,
  "script_format": "aaps",
  "script_text": "AUTOAPPDEV_PIPELINE 1\\n...",
  "ir": { "kind": "autoappdev_ir", "version": 1, "tasks": [ ... ] },
  "warnings": [],
  "provenance": {
    "id": "20260215T123456Z_abcd1234",
    "model": "gpt-5.3-codex",
    "reasoning": "medium",
    "timeout_s": 45,
    "source_sha256": "...",
    "artifacts": {
      "dir": "runtime/logs/llm_parse/<id>/",
      "prompt": "runtime/logs/llm_parse/<id>/prompt.txt",
      "source": "runtime/logs/llm_parse/<id>/source.txt",
      "codex_jsonl": "runtime/logs/llm_parse/<id>/codex.jsonl",
      "aaps": "runtime/logs/llm_parse/<id>/result.aaps",
      "provenance": "runtime/logs/llm_parse/<id>/provenance.json"
    }
  },
  "script": { "id": 123, "title": "...", "script_text": "...", "ir": { ... } }
}
```
`script` is only returned when `save=true`.

Response (errors):
- `403` `{ "ok": false, "error": "disabled" }` if not enabled
- `503` `{ "ok": false, "error": "codex_not_found" }` if `codex` isn’t on `PATH`
- `408/504` `{ "ok": false, "error": "timeout" }` if Codex exceeds the timeout
- `400` with existing AAPS parse errors if the LLM output can’t be parsed

## Guardrails
1. Opt-in enable flag (default off)
   - Require `AUTOAPPDEV_ENABLE_LLM_PARSE=1` or return `403 disabled`.
   - Document this in `docs/env.md`.

2. Strict timeout
   - Default `timeout_s` (e.g. 45s) and hard-cap (e.g. 120s).
   - Enforce with `asyncio.wait_for(...)` and kill the subprocess on timeout.

3. Input size limits
   - Enforce `source_text` max bytes (e.g. 100k) to avoid runaway prompts and giant artifacts.

4. “No side effects” prompt
   - Prompt must explicitly instruct:
     - Do not read/write files.
     - Do not run shell commands.
     - Output only AAPS v1 text (no Markdown fences, no commentary).
   - Run codex without `--full-auto` to reduce tool execution risk.
   - Set `cwd` for the subprocess to the per-request artifact dir under `runtime/logs/llm_parse/<id>/`.

## Provenance + Prompt Storage
Write artifacts per request under:
- `runtime/logs/llm_parse/<id>/`

Files to write:
- `source.txt`: raw input `source_text`
- `prompt.txt`: exact prompt sent to Codex (includes instructions + input)
- `codex.jsonl`: raw `codex exec --json` output
- `result.aaps`: extracted AAPS script returned by Codex
- `provenance.json`: metadata (id, hashes, model, reasoning, timeout, extraction notes, parse result status)

Rationale:
- `runtime/` is already the home for operational logs and is gitignored by default (`.gitignore`).

## Implementation Steps (Next Phase: WORK)
1. Add a small Codex runner + extractor module
   - New file: `backend/llm_assisted_parse.py`
   - Implement:
     - `async run_codex_to_text(prompt: str, *, model: str, reasoning: str, timeout_s: float, cwd: Path, extra_args: list[str]) -> tuple[str, str]`
       - returns `(assistant_text, jsonl_text)` or raises a typed error.
     - `extract_aaps(text: str) -> tuple[str, list[str]]`
       - find the first line equal to `AUTOAPPDEV_PIPELINE 1` and return from there onward.
       - strip common code fences if present.
       - return warnings when cleanup occurs.
     - `write_provenance_artifacts(...)` helper to create the per-request directory and write files.
     - Minimal JSONL parsing to get the last agent message (similar structure to existing selfdev JSONL logs).

2. Add an optional endpoint handler
   - Update `backend/app.py`:
     - Add `ScriptsParseLlmHandler` (or similar) that:
       - checks `AUTOAPPDEV_ENABLE_LLM_PARSE`
       - validates request payload and clamps limits
       - calls Codex runner
       - extracts AAPS text and parses via `parse_aaps_v1`
       - writes artifacts to runtime logs
       - optionally saves to `pipeline_scripts` via `Storage.create_pipeline_script(...)` when `save=true`
     - Wire route in `make_app(...)`:
       - `(r"/api/scripts/parse-llm", ScriptsParseLlmHandler, {"storage": storage, "runtime_dir": runtime_dir})`

3. Update docs
   - `docs/api-contracts.md`:
     - Add `POST /api/scripts/parse-llm` contract (request/response + error modes + “optional/unsafe by default” note).
   - `docs/env.md`:
     - Add optional `AUTOAPPDEV_ENABLE_LLM_PARSE` (and optionally `AUTOAPPDEV_LLM_PARSE_TIMEOUT_S` default behavior if implemented).

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

python3 -m py_compile backend/app.py backend/llm_assisted_parse.py
rg -n \"parse-llm\" backend/app.py docs/api-contracts.md
```

Manual check (outside sandbox; requires `codex` on PATH and working `.env` DB):
```bash
export AUTOAPPDEV_ENABLE_LLM_PARSE=1

# Start backend (e.g. via tmux script) then:
curl -fsS -X POST http://127.0.0.1:8788/api/scripts/parse-llm \\
  -H 'Content-Type: application/json' \\
  -d '{\"source_text\":\"#!/usr/bin/env bash\\necho hello\\n\"}'

# Confirm artifacts were written:
ls -la runtime/logs/llm_parse | tail
```

## Acceptance Checklist
- [ ] `POST /api/scripts/parse-llm` exists and is disabled unless `AUTOAPPDEV_ENABLE_LLM_PARSE=1`.
- [ ] Endpoint runs `codex exec --json` with an enforced timeout and returns actionable errors.
- [ ] Endpoint returns validated AAPS (`script_text`) + canonical IR (`ir`) on success.
- [ ] Endpoint writes provenance artifacts (source/prompt/jsonl/result/provenance.json) under `runtime/logs/llm_parse/<id>/`.
- [ ] Docs updated: `docs/api-contracts.md` + `docs/env.md`.

