# Summary: 023 pipeline_formatted_script_spec

## What Changed
- Added a spec for a deterministic formatted pipeline script (AAPS v1) and canonical IR schema:
  - `docs/pipeline-formatted-script-spec.md`: defines `AUTOAPPDEV_PIPELINE 1` scripts with `TASK/STEP/ACTION` JSON statements, and the canonical IR shape `autoappdev_ir` (`TASK -> STEP -> ACTION`).
- Added complete examples:
  - `examples/pipeline_formatted_script_v1.aaps`: full example formatted script.
  - `examples/pipeline_ir_v1.json`: equivalent IR JSON (valid JSON).
- Linked the spec from the repo entrypoint:
  - `README.md`: added `docs/pipeline-formatted-script-spec.md` to Contents.

## Why
To establish a stable, versioned contract for converting between:
- human-editable pipeline scripts,
- a canonical IR (`TASK -> STEP -> ACTION`), and
- the Scratch-like PWA blocks (`plan/work/debug/fix/summary/commit_push`).

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
test -f docs/pipeline-formatted-script-spec.md
test -f examples/pipeline_formatted_script_v1.aaps
python3 -m json.tool examples/pipeline_ir_v1.json >/dev/null
rg -n 'pipeline-formatted-script-spec\\.md' README.md
```

