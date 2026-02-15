# Plan: 048 pwa_numbered_aaps_export

## Goal
Update the PWA **Script** tab so AAPS export/import is more Scratch-like:
- Export/generate AAPS text in the textarea and downloads as **numbered + indented** AAPS v1 (display-only formatting).
- Import/parse continues to work when users paste scripts that include **optional numeric prefixes** (e.g. `1.2 STEP {...}`).
- UI formatting must not change pipeline semantics (JSON content stays the same; numbering/indent is whitespace/comments only).

Acceptance:
- Script panel exports numbered+indented AAPS lines.
- Import tolerates optional numeric prefixes.
- UI renders numbering/indent for readability without changing semantics.

## Current State (Relevant Files)
- Script tab UI and behavior:
  - `pwa/index.html` (buttons: Parse/Import/From Blocks/Download AAPS/Download Runner; textarea `#script-text`)
  - `pwa/app.js`
    - `programToAapsScript()` generates AAPS v1 text from the current block program (currently un-numbered, minimal spacing).
    - `fillScriptFromBlocks()`, `exportAapsFile()`, `exportRunnerFile()` all use `programToAapsScript()`.
    - `parseAapsToBlocks()` posts textarea to `/api/scripts/parse`.
    - `importShellToBlocks()` posts textarea to `/api/scripts/import-shell`.
- Backend AAPS parsing already supports the import requirement:
  - `backend/pipeline_parser.py`:
    - ignores comment numbering lines (`# ...`)
    - accepts optional numeric prefix token before `TASK|STEP|ACTION` (e.g. `1.2 STEP {...}`)
- Existing conventions/docs/examples:
  - `docs/aaps-numbering-placeholders.md` (recommended: comment numbering + indentation)
  - `examples/pipeline_meta_round_numbered_placeholders_v0.aaps` (comment numbering + indentation example)
  - `examples/pipeline_formatted_script_numbered_prefix_v1.aaps` (numeric-prefix example)

## Proposed Minimal Design
Prefer the **spec-compatible** numbering convention for export (comment numbering + indentation), while keeping the backend’s numeric-prefix tolerance for imports.

Output format for scripts generated from blocks:
```text
AUTOAPPDEV_PIPELINE 1

# 1 Task
TASK {...}

# 1.1 Step
  STEP {...}

# 1.1.1 Action
    ACTION {...}
```

Rules:
- Indentation:
  - `TASK`: 0 spaces
  - `STEP`: 2 spaces
  - `ACTION`: 4 spaces
- Numbering is derived from order:
  - task number: `1` (PWA canvas currently models a single task)
  - step number: `idx+1`
  - action number: `1` (PWA currently emits a single action per step)
- Semantics unchanged:
  - do not change JSON objects (`id`, `title`, `block`, `kind`, `params`, `meta`)
  - only add comment lines and indentation whitespace

## Implementation Steps (Next Phase: WORK)

### 1) Update AAPS Export Formatter
Edit `pwa/app.js` in `programToAapsScript(prog, title)`:
- Keep existing object construction logic (task meta via `workspaceTaskMeta()`, step titles via `canonicalBlockTitle()`, update_readme special-casing).
- Change emitted lines to include:
  - numbering comment lines (`# 1 ...`, `# 1.1 ...`, `# 1.1.1 ...`)
  - indentation on `STEP`/`ACTION` statement lines
- Keep a trailing newline and retain `AUTOAPPDEV_PIPELINE 1` header.

### 2) Ensure Script Tab Uses The New Formatting Everywhere It Generates AAPS
No wiring changes expected (already uses `programToAapsScript()`), but confirm these paths now produce numbered output:
- `fillScriptFromBlocks()` (textarea rendering)
- `exportAapsFile()` (downloads `.aaps`)
- `exportRunnerFile()` (embeds `# AAPS:` annotations; should now include numbered/indented lines)
- `saveScript()` (stores `script_text`; it is fine for this to become numbered+indented since it remains AAPS v1-parseable)

### 3) Import Tolerance For Numeric Prefixes (No Code Change Expected)
- Confirm backend parse endpoint still accepts `examples/pipeline_formatted_script_numbered_prefix_v1.aaps`.
- (Optional) add a one-line note to docs if this UI capability needs clarification, but avoid i18n churn in the PWA placeholder strings.

### 4) Docs (Optional, Minimal)
If the numbered export is user-visible enough to warrant it, update:
- `docs/end-to-end-demo-checklist.md` to note that exported AAPS may include numbering comments + indentation (still parseable).

## Verification Commands (DEBUG/VERIFY Phase)
Static checks (no servers):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
```

Parser regression checks for import tolerance:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 -m py_compile backend/pipeline_parser.py

timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
for p in [
  "examples/pipeline_meta_round_numbered_placeholders_v0.aaps",
  "examples/pipeline_formatted_script_numbered_prefix_v1.aaps",
]:
  ir = parse_aaps_v1(Path(p).read_text("utf-8"))
  assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
print("OK")
PY
```

Manual UI acceptance (outside this sandbox):
1. Run backend + serve `pwa/` locally (see `pwa/README.md`).
2. In the Script tab:
   - Add 2-3 blocks on canvas, click `From Blocks`.
   - Verify textarea shows `# 1 ...` / `# 1.1 ...` numbering comments and STEP/ACTION indentation.
   - Click `Download AAPS` and verify the downloaded file matches the textarea formatting.
   - Click `Parse AAPS -> Blocks` on the generated script; verify the blocks remain unchanged (same count/types).
   - Paste `examples/pipeline_formatted_script_numbered_prefix_v1.aaps` into textarea; click `Parse AAPS -> Blocks`; verify it parses successfully.

## Acceptance Checklist
- [ ] `From Blocks` generates numbered + indented AAPS text in the textarea.
- [ ] `Download AAPS` downloads numbered + indented AAPS text.
- [ ] Parsing the generated script produces the same block semantics (no semantic changes).
- [ ] Importing/parsing AAPS with numeric prefixes (`1.2 STEP ...`) succeeds.

