# Plan: 026 pipeline_shell_script_import_v0

## Goal
Implement a **best-effort importer** that converts an **annotated shell script** (bash) into canonical IR (`autoappdev_ir` v1), without executing anything.

Acceptance:
- Backend can import an annotated shell pipeline script (via structured comments) into IR with clear limitations.
- At least one example imports successfully.

## Current State (References)
- AAPS v1 + IR spec:
  - `docs/pipeline-formatted-script-spec.md`
- Deterministic AAPS v1 parser:
  - `backend/pipeline_parser.py` (`parse_aaps_v1`, `ParseError`)
- Parse API exists:
  - `POST /api/scripts/parse` in `backend/app.py`
- Example AAPS artifacts:
  - `examples/pipeline_formatted_script_v1.aaps`
  - `examples/pipeline_ir_v1.json`

## Import Format (Shell Annotations v0)
Use structured comment lines inside a `.sh` file:
- Only lines matching `^\s*#\s*AAPS:\s*(.*)$` are considered annotations.
- The captured remainder is treated as an **AAPS line** (may be blank).
- All captured AAPS lines are concatenated (in-order) into `script_text` and parsed via `parse_aaps_v1`.

Limitations (document explicitly):
- **No shell parsing.** Unannotated shell code is ignored (no inference of tasks/steps/actions from bash).
- **No execution.** Import is parse-only and deterministic.
- Only the embedded AAPS is validated; `source`, `bash`, `set -e`, functions, loops are not interpreted.

## Implementation Steps (Next Phase: WORK)
1. Add importer module: `backend/pipeline_shell_import.py`
   - Implement:
     - `extract_aaps_from_shell(shell_text: str) -> tuple[str, list[int]]`
       - Returns `(aaps_text, shell_line_map)` where `shell_line_map[i]` is the 1-based shell line number for `aaps_text` line `i+1`.
       - Raise a structured error if no `# AAPS:` lines are present (e.g. `missing_annotations`).
     - `import_shell_annotated_to_ir(shell_text: str) -> dict[str, Any]`
       - Uses `parse_aaps_v1(aaps_text)` to produce IR.
       - On `ParseError`, translate `e.line` (AAPS line) to the original **shell line** via `shell_line_map` and re-raise (or wrap) so API returns the shell line number.
       - Return `{ "aaps_text": "...", "ir": {...}, "warnings": [...] }`.
   - Keep it pure and deterministic (no file I/O, no subprocess).

2. Add backend endpoint: `backend/app.py`
   - Add `ScriptsImportShellHandler`:
     - `POST /api/scripts/import-shell`
     - Request JSON: `{ "shell_text": "..." }`
     - Validate:
       - JSON object body
       - `shell_text` is a string and `len(shell_text) <= 200_000` (match existing script limits)
     - Call `import_shell_annotated_to_ir(shell_text)`
     - Response (success):
       - `{ "ok": true, "script_format": "aaps", "script_text": "<extracted aaps>", "ir": {...}, "warnings": [...] }`
     - Response (error):
       - `400` with `{ "ok": false, "error": "<code>", "line": <shell_line>, "detail": "<detail>" }`
   - Register route in `make_app()` near existing `/api/scripts*` routes.

3. Add at least one importing example
   - Create `examples/pipeline_shell_annotated_v0.sh` containing:
     - A shebang and basic shell body (can be minimal).
     - A valid embedded AAPS v1 header + statements via `# AAPS:` lines.
   - The embedded AAPS should produce at least:
     - 1 TASK
     - 2 STEPs with blocks in the allowed set (`plan/work/debug/fix/summary/commit_push`)
     - 1 ACTION per step

4. Update docs (clear limitations + how-to)
   - `docs/pipeline-formatted-script-spec.md`
     - Add a short section describing “Shell Annotations v0” and the exact `# AAPS:` format + limitations.
   - `docs/api-contracts.md`
     - Document `POST /api/scripts/import-shell` with request/response + error shape.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n \"import-shell|ScriptsImportShellHandler\" backend/app.py docs/api-contracts.md
timeout 10s python3 -m py_compile backend/app.py backend/pipeline_parser.py backend/pipeline_shell_import.py
```

Functional smoke (no server required):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_shell_import import import_shell_annotated_to_ir

shell_text = Path('examples/pipeline_shell_annotated_v0.sh').read_text('utf-8')
res = import_shell_annotated_to_ir(shell_text)
assert res['aaps_text'].lstrip().startswith('AUTOAPPDEV_PIPELINE 1')
ir = res['ir']
assert ir['kind'] == 'autoappdev_ir' and ir['version'] == 1
assert ir['tasks'] and ir['tasks'][0]['steps']
print('OK')
PY
```

Manual HTTP verification (outside this sandbox; requires running the backend):
```bash
curl -sS -X POST 'http://127.0.0.1:8788/api/scripts/import-shell' \
  -H 'content-type: application/json' \
  -d @- <<'JSON'
{ "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n" }
JSON
```

## Acceptance Checklist
- [ ] `POST /api/scripts/import-shell` exists and returns `{ok:true, script_text, ir}` for a valid annotated shell script.
- [ ] Importer never executes code (parse-only) and documents limitations.
- [ ] At least one repo example imports successfully (`examples/pipeline_shell_annotated_v0.sh`).
- [ ] Invalid annotations return actionable 400 errors including a **shell** line number.

