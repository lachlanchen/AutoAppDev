# Summary: 043 aaps_numbering_placeholders_spec

## What Changed
- Added `docs/aaps-numbering-placeholders.md` defining two AAPS v1-compatible conventions:
  - Scratch-like **numbering** via `# 1.2.3` comment lines plus indentation (display-only; parser ignores comments).
  - Minimal `{{...}}` **placeholder** syntax for strings in `ACTION.params.prompt` / `ACTION.params.cmd`:
    - `{{task.title}}`, `{{task.acceptance}}` (from `TASK.meta.acceptance`), `{{runtime_dir}}` (from `AUTOAPPDEV_RUNTIME_DIR`, default `./runtime`).
- Updated `docs/pipeline-formatted-script-spec.md` to link the above conventions (section “1.8 Numbering + Placeholders”).
- Added a complete example AAPS script:
  - `examples/pipeline_meta_round_numbered_placeholders_v0.aaps` (includes `meta_round_v0`, conditional fix step via `STEP.meta.conditional`, numbering comments, indentation, and placeholder usage).

## Why
Task 043 acceptance requires docs to define a Scratch-like numbered/indented AAPS convention (still AAPS v1-compatible) and a minimal placeholder syntax used in prompts/cmds, plus at least one complete example using `meta_round_v0` and conditional fix steps.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s rg -n "AAPS Numbering|Numbered \\+ indented|\\{\\{task\\.title\\}\\}|\\{\\{task\\.acceptance\\}\\}|\\{\\{runtime_dir\\}\\}" \
  docs/aaps-numbering-placeholders.md docs/pipeline-formatted-script-spec.md examples/pipeline_meta_round_numbered_placeholders_v0.aaps

timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_meta_round_numbered_placeholders_v0.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
print("OK")
PY
```

