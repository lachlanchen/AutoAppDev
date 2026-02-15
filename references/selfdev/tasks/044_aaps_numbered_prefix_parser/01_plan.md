# Plan: 044 aaps_numbered_prefix_parser

## Goal
Extend the deterministic AAPS v1 parser so it accepts an **optional numeric prefix** before the statement keyword:
- Examples:
  - `1 TASK {...}`
  - `1.2 STEP {...}`
  - `3.4.5 ACTION {...}`
  - (optionally) allow a trailing dot: `1.2. STEP {...}`

Acceptance:
- `backend/pipeline_parser.py` accepts optional numeric prefixes before `TASK|STEP|ACTION` while remaining deterministic.
- Add an example under `examples/`.
- Verify parsing via a small Python snippet.

## Current State (Relevant Files)
- Parser (strict today: first token must be `TASK|STEP|ACTION`):
  - `backend/pipeline_parser.py` (`parse_aaps_v1`)
- Shell import uses the same parser:
  - `backend/pipeline_shell_import.py` (`import_shell_annotated_to_ir` -> `parse_aaps_v1`)
- API endpoints depend on the parser:
  - `backend/app.py` (`POST /api/scripts/parse`, and `POST /api/scripts/parse-llm` success path)
- Docs recently added a numbering convention using comment lines:
  - `docs/aaps-numbering-placeholders.md` (currently states inline numeric prefixes won’t parse; this will need a small correction once the parser accepts them)

## Proposed Minimal Design
Keep AAPS v1 semantics unchanged; treat the numeric prefix as **ignored decoration**:
- Parse statement lines as:
  - `KEYWORD <json-object>` (existing), OR
  - `<num-prefix> KEYWORD <json-object>` (new)
- `<num-prefix>` format (minimal, deterministic):
  - `digits` with optional `.<digits>` segments (e.g. `1`, `1.2`, `12.3.4`)
  - optionally allow a trailing dot (e.g. `1.2.`)
  - must be separated from `KEYWORD` by whitespace

Implementation should not change any ID/ordering semantics, only how the keyword+JSON are extracted from each line.

## Implementation Steps (Next Phase: WORK)

### 1) Update `backend/pipeline_parser.py` Statement Tokenization
Edit `backend/pipeline_parser.py` in `parse_aaps_v1` where it currently does:
- `stripped = raw.lstrip()`
- `parts = stripped.split(None, 1)`

Replace with a deterministic tokenization that supports numbered prefixes:
1. `tokens = stripped.split(None, 2)` (max 3 tokens: prefix/keyword/json)
2. Cases:
   - If `len(tokens) == 2` and `tokens[0] in {"TASK","STEP","ACTION"}`:
     - `kw = tokens[0]`, `json_part = tokens[1]` (existing behavior)
   - Else if `len(tokens) == 3` and `tokens[1] in {"TASK","STEP","ACTION"}` and `tokens[0]` matches the numeric-prefix format:
     - `kw = tokens[1]`, `json_part = tokens[2]`
   - Else:
     - raise `ParseError("invalid_statement", lineno, "...")` (update detail to mention optional numeric prefixes)

Add a small helper in the module for readability/testability:
- `_is_numeric_prefix(tok: str) -> bool`
  - strip trailing `.`
  - split by `.`
  - ensure all segments are non-empty digits

Keep the rest of parsing/validation unchanged (JSON parsing, duplicate IDs, allowed blocks, etc.).

### 2) Add Example Script Under `examples/`
Add a new file:
- `examples/pipeline_formatted_script_numbered_prefix_v1.aaps`

Content requirements:
- Valid header: `AUTOAPPDEV_PIPELINE 1`
- At least one `TASK`, `STEP`, and `ACTION` line using numeric prefixes (e.g. `1 TASK ...`, `1.1 STEP ...`, `1.1.1 ACTION ...`)
- Keep IDs valid/non-duplicated (per existing parser rules).

### 3) Minimal Doc Correction (Keep Docs Accurate)
Because `docs/aaps-numbering-placeholders.md` currently claims inline numeric prefixes won’t parse, update it to reflect the new parser behavior:
- Keep “comment numbering” as the most portable convention.
- Add a note that `backend/pipeline_parser.py` also accepts an optional numeric prefix token (deterministic extension) such as `1.2 STEP {...}`.

This should be a small edit limited to that doc section; no new docs required.

## Verification Commands (DEBUG/VERIFY Phase)
Smallest checks that prove acceptance:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Syntax check
timeout 10s python3 -m py_compile backend/pipeline_parser.py

# Parse the new example file
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_formatted_script_numbered_prefix_v1.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
assert ir["tasks"] and ir["tasks"][0]["steps"] and ir["tasks"][0]["steps"][0]["actions"]
print("OK: numbered-prefix example parses")
PY
```

Optional regression sanity:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_formatted_script_v1.aaps").read_text("utf-8")
parse_aaps_v1(text)
print("OK: existing example still parses")
PY
```

## Acceptance Checklist
- [ ] `backend/pipeline_parser.py` accepts `1.2 STEP {...}` style prefixes and remains deterministic.
- [ ] New example file exists under `examples/` and parses successfully via `parse_aaps_v1`.
- [ ] `docs/aaps-numbering-placeholders.md` no longer claims numeric prefixes are unparseable by the backend parser.

