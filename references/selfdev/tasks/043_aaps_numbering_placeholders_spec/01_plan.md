# Plan: 043 aaps_numbering_placeholders_spec

## Goal
Update documentation to define:
1. A **Scratch-like “numbered + indented” AAPS convention** that remains **AAPS v1-compatible** (i.e., valid for the existing `KEYWORD <json-object>` parser).
2. A **minimal placeholder syntax** for use inside `ACTION.params.prompt` / `ACTION.params.cmd` strings (e.g. `{{task.title}}`, `{{task.acceptance}}`, `{{runtime_dir}}`).
3. At least one **complete example script** that:
  - uses `meta_round_v0`, and
  - includes **conditional fix steps** (`STEP.meta.conditional`).

Constraints:
- Docs-only in this task (no engine implementation required).
- Keep changes minimal and consistent with existing AAPS/IR and meta-round docs.

## Current State (Relevant Files)
- AAPS grammar + IR schema:
  - `docs/pipeline-formatted-script-spec.md`
  - Notes: indentation is already allowed; comment lines are ignored.
- Meta-round convention (for-loops) + conditional fix example exists:
  - `docs/meta-round-templates.md` (uses `TASK.meta.meta_round_v0` and `STEP.meta.conditional`).
- Deterministic parser confirms the current strict grammar:
  - `backend/pipeline_parser.py` (`parse_aaps_v1()`): ignores leading indentation; ignores lines starting with `#`; requires first token to be `TASK|STEP|ACTION`.
- There is currently **no** placeholder spec for `{{...}}` in docs (only mentioned in):
  - `scripts/auto-autoappdev-development.sh` lines 288-294 (product requirements).

## Proposed Minimal Design (Docs-Only)

### A) “Numbered + Indented” Convention That Stays AAPS v1-Compatible
Because `backend/pipeline_parser.py` requires `TASK|STEP|ACTION` to be the first token (after indentation), we cannot prefix statement lines with `1.` without changing the grammar.

Instead, define a **display-only numbering convention using comment lines**, which AAPS v1 already ignores:
- Use indentation to show nesting (already allowed):
  - `TASK` at 0 spaces
  - `STEP` indented 2 spaces
  - `ACTION` indented 4 spaces
- Add a numbering “prefix” as a standalone comment line immediately above the statement:
  - `# 1`, `# 1.1`, `# 1.1.1`, etc.

This achieves “Scratch-like numbered blocks” while remaining fully parseable by current AAPS v1 tooling.

### B) Minimal Placeholder Syntax (Convention v0)
Define a placeholder expansion convention for engines/runners:
- Syntax: `{{path}}` where `path` is a dot-separated identifier (e.g. `task.title`).
- Expansion occurs only inside **string fields** (not in JSON structure): primarily `ACTION.params.prompt` and `ACTION.params.cmd`.
- Required placeholders for this task:
  - `{{task.title}}` (from current task’s `title`)
  - `{{task.acceptance}}` (recommended source: `TASK.meta.acceptance` string)
  - `{{runtime_dir}}` (from `AUTOAPPDEV_RUNTIME_DIR` env var; default `./runtime` per `docs/env.md`)
- Behavior on unknown placeholders:
  - Specify a strict default: treat unknown placeholders as an error (fail fast), with an optional “lenient” mode left engine-defined.
- Safety note (docs only): placeholder values are untrusted strings; shell commands should quote appropriately.

### C) Example Script
Add a single, complete AAPS v1 script that demonstrates:
- meta-round controller task (`TASK.meta.meta_round_v0`)
- conditional fix step (`STEP.meta.conditional: "on_debug_failure"`)
- numbering comments + indentation
- placeholders used inside `ACTION.params.prompt` and `ACTION.params.cmd`

## Implementation Steps (Next Phase: WORK)

### 1) Add a New Doc Explaining Both Conventions
Create `docs/aaps-numbering-placeholders.md`:
- Section: “Numbered + indented AAPS (display-only)”
  - Re-state the base grammar from `docs/pipeline-formatted-script-spec.md`
  - Define indentation levels and the numbering comment pattern (`# 1.2.3`)
  - Call out “still AAPS v1-compatible” explicitly and why (comments ignored; keywords unchanged)
- Section: “Placeholders (convention v0)”
  - Define syntax (`{{...}}`), allowed locations (`ACTION.params.prompt`, `ACTION.params.cmd`)
  - Define the minimal placeholder set and sources:
    - `task.acceptance` sourced from `TASK.meta.acceptance`
    - `runtime_dir` sourced from `AUTOAPPDEV_RUNTIME_DIR` with default
  - Define error handling for unknown placeholders
  - Include a short safety/quoting note for `cmd`
- Section: “Complete example”
  - Reference an example file under `examples/` (next step), or embed the full script if we decide to avoid adding a file.

### 2) Link From the Canonical AAPS Spec
Update `docs/pipeline-formatted-script-spec.md`:
- Add a short section after “1.4 Statement Lines” or near the end:
  - Point to `docs/aaps-numbering-placeholders.md` for the display-only numbering + placeholder conventions.
  - Reiterate these are **conventions** that do not change the grammar.

### 3) Add A Complete Example Script File
Add `examples/pipeline_meta_round_numbered_placeholders_v0.aaps` containing:
- Header: `AUTOAPPDEV_PIPELINE 1`
- Numbering comments (`# 1`, `# 1.1`, …) + indentation
- Meta-round controller task:
  - `TASK {"id":"meta", ... "meta":{"meta_round_v0":{...}}}`
  - At least 2 round steps (`STEP.block="plan"`, `STEP.meta.round`)
- Expanded per-task steps including:
  - `TASK.meta.acceptance` so `{{task.acceptance}}` is meaningful
  - `STEP.block="fix"` with `STEP.meta.conditional="on_debug_failure"`
  - Placeholder usage inside actions, e.g.:
    - `{"prompt":"Plan: {{task.title}}\\nAcceptance: {{task.acceptance}}\\nRuntime: {{runtime_dir}}"}`
    - `{"cmd":"printf 'done: {{task.title}}\\n' > {{runtime_dir}}/outbox/.tmp"}`

Note: placeholders are not executed in this task; the goal is to define the contract.

### 4) (Optional) Cross-link From Meta-round Doc
If the example benefits from discoverability:
- Add a short “See also” link in `docs/meta-round-templates.md` pointing to `docs/aaps-numbering-placeholders.md`.

Keep optional to minimize diff.

## Verification Commands (DEBUG/VERIFY Phase)
Docs-only verification:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s rg -n "Numbered|numbering|\\{\\{task\\.title\\}\\}|\\{\\{task\\.acceptance\\}\\}|\\{\\{runtime_dir\\}\\}" \
  docs/aaps-numbering-placeholders.md docs/pipeline-formatted-script-spec.md examples/pipeline_meta_round_numbered_placeholders_v0.aaps
```

Ensure the example is truly AAPS v1-parseable (despite numbering comments/placeholders):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_meta_round_numbered_placeholders_v0.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
assert ir["tasks"]
print("OK: example parses as AAPS v1")
PY
```

## Acceptance Checklist
- [ ] Docs define a numbered + indented AAPS convention that remains AAPS v1-compatible (no grammar changes).
- [ ] Docs define minimal placeholder syntax including:
  - [ ] `{{task.title}}`
  - [ ] `{{task.acceptance}}` (with a clear source, e.g. `TASK.meta.acceptance`)
  - [ ] `{{runtime_dir}}` (linked to `AUTOAPPDEV_RUNTIME_DIR`)
- [ ] At least one complete example script exists and includes:
  - [ ] `meta_round_v0`
  - [ ] conditional fix steps (`STEP.meta.conditional`)
  - [ ] numbering + indentation
  - [ ] placeholder usage in prompt/cmd strings

