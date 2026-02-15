# Work Notes: 023 pipeline_formatted_script_spec

## Summary
- Added a docs spec for a deterministic, versioned formatted pipeline script (“AAPS”) and the canonical IR schema (`TASK -> STEP -> ACTION`).
- Included a complete example (script + equivalent IR JSON) and explicitly mapped `STEP.block` to the current PWA block palette keys.
- Added example artifacts under `examples/` and linked the spec from `README.md`.

## Changes Made
- `docs/pipeline-formatted-script-spec.md`
  - Defines:
    - Script header: `AUTOAPPDEV_PIPELINE 1`
    - Line format: `TASK|STEP|ACTION <json-object>`
    - Nesting rules and required keys
    - Canonical IR: `{ kind:"autoappdev_ir", version:1, tasks:[{steps:[{actions:[]}]}] }`
    - Explicit mapping of `STEP.block` to PWA blocks: `plan/work/debug/fix/summary/commit_push`
    - Lossy projection to existing `autoappdev_plan` payload
- `examples/pipeline_formatted_script_v1.aaps`
  - Full example script used by the spec.
- `examples/pipeline_ir_v1.json`
  - Equivalent IR JSON example (valid JSON).
- `README.md`
  - Linked `docs/pipeline-formatted-script-spec.md` in the Contents list.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/pipeline-formatted-script-spec.md
test -f examples/pipeline_formatted_script_v1.aaps
test -f examples/pipeline_ir_v1.json

rg -n 'AUTOAPPDEV_PIPELINE\\s+1|\\bTASK\\b|\\bSTEP\\b|\\bACTION\\b' docs/pipeline-formatted-script-spec.md
rg -n 'autoappdev_ir|\"tasks\"\\s*:' docs/pipeline-formatted-script-spec.md
rg -n 'plan\\b|work\\b|debug\\b|fix\\b|summary\\b|commit_push\\b' docs/pipeline-formatted-script-spec.md

python3 -m json.tool examples/pipeline_ir_v1.json >/dev/null
rg -n 'pipeline-formatted-script-spec\\.md' README.md
```

