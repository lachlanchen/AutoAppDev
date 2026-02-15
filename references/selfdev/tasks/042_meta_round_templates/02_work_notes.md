# Work Notes: 042 meta_round_templates

## Implementation Notes
- Added `docs/meta-round-templates.md` defining a standard meta-round pipeline convention:
  - `N_ROUND` task synthesis/refinement loop from `goal` + shared context.
  - Standard per-task phase template: `plan -> work -> debug -> fix -> translate -> summary -> log -> commit`.
  - Explicit mapping to existing AAPS/IR without adding new `STEP.block` keys:
    - `translate` modeled as actions inside the `summary` step.
    - `log` and optional `commit` modeled as actions inside the `commit_push` step.
  - Log slot references `/api/outbox` and `runtime/outbox/` (per existing API/runtime docs).
- Updated `docs/pipeline-formatted-script-spec.md` with a short section linking to the meta-round template convention and clarifying it is `meta`-driven (engine-defined).

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

sed -n '1,240p' references/selfdev/tasks/042_meta_round_templates/01_plan.md
tail -n 80 docs/pipeline-formatted-script-spec.md

timeout 10s rg -n "Meta-round|meta[- ]round|N_ROUND|multi[- ]round" docs/pipeline-formatted-script-spec.md docs/meta-round-templates.md && timeout 10s rg -n "plan/work/debug/fix/translate/summary/log/commit" docs/meta-round-templates.md && timeout 10s rg -n "runtime/outbox|/api/outbox" docs/meta-round-templates.md docs/api-contracts.md docs/workspace-layout.md

timeout 10s rg -n "plan/work/debug/fix/translate/summary/log/commit|plan -> work -> debug -> fix -> translate -> summary -> log -> commit" docs/meta-round-templates.md docs/pipeline-formatted-script-spec.md && timeout 10s rg -n "runtime/outbox|/api/outbox" docs/meta-round-templates.md docs/api-contracts.md docs/workspace-layout.md | head -n 80
```

