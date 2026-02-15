# Summary: 042 meta_round_templates

## What Changed
- Added `docs/meta-round-templates.md` documenting a standard meta-round pipeline convention:
  - `N_ROUND` task synthesis/refinement loop (goal + shared context -> refined task list artifact).
  - Standard per-task phase template: `plan -> work -> debug -> fix -> translate -> summary -> log -> commit`.
  - Mapped `translate`/`log`/`commit` into existing AAPS/IR without new `STEP.block` values by modeling them as action slots inside `summary` and `commit_push`.
- Updated `docs/pipeline-formatted-script-spec.md` to reference the meta-round convention and clarify it is represented via `meta` fields (engine-defined; data-only).

## Why
Task 042 acceptance requires docs to define a standard multi-round pipeline template (meta-loop) that stays consistent with the existing deterministic AAPS/IR schema and the current PWA step palette.

## How To Verify
Docs smoke checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s rg -n "Meta-round Templates \\(Convention v0\\)|docs/meta-round-templates\\.md" docs/pipeline-formatted-script-spec.md
timeout 10s rg -n "plan -> work -> debug -> fix -> translate -> summary -> log -> commit" docs/meta-round-templates.md
timeout 10s rg -n "/api/outbox|runtime/outbox" docs/meta-round-templates.md
timeout 10s rg -n "meta_round_v0" docs/meta-round-templates.md docs/pipeline-formatted-script-spec.md
```

