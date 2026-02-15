# Plan: 042 meta_round_templates

## Goal
Define (in docs) a **standard multi-round pipeline template**:
- For `N_ROUND`: generate/refine a task list from a goal + shared context.
- For each resulting task: run a configurable action template: `plan -> work -> debug -> fix -> translate -> summary -> log -> commit`.

Acceptance:
- Documentation clearly defines the multi-round template and how it maps onto the existing AAPS/IR concepts (TASK/STEP/ACTION) without changing runtime behavior.

## Current State (Relevant Files)
- Canonical pipeline schema is AAPS/IR (`TASK -> STEP -> ACTION`):
  - `docs/pipeline-formatted-script-spec.md` (no standard meta-round/template convention yet; `meta` is “engine-defined”).
- Runner codegen supports only a minimal set of action kinds:
  - `docs/pipeline-runner-codegen.md` (`note`, `run`, `codex_exec`).
- Outbox channel exists for “log/status back to UI”:
  - `docs/api-contracts.md` (`/api/outbox`, `runtime/outbox/` file queue semantics).
  - `docs/workspace-layout.md` (documents `runtime/outbox/`).
- Common actions doc exists but does not define translate/log actions yet:
  - `docs/common-actions.md` (currently only `update_readme`).

## Proposed Minimal Design (Docs-Only)
Add a **doc-defined convention** for meta-round pipelines that:
- Keeps AAPS/IR parsing deterministic (no templating in the parser).
- Uses `meta` fields (already allowed by the spec) to express:
  - the meta-round loop configuration (`N_ROUND`, goal/context inputs, where the refined task list is written), and
  - the per-task “standard action template” (how steps/actions are structured and where translate/log fit).

Important: this task is docs-only; it will not add new `STEP.block` values beyond the existing palette keys.
- Map `translate` and `log` to **actions within existing steps** (typically within `summary` and/or `commit_push`) so docs remain consistent with `docs/pipeline-formatted-script-spec.md` and the PWA block palette.

## Implementation Steps (Next Phase: WORK)

### 1) Add a New Doc: `docs/meta-round-templates.md`
Create `docs/meta-round-templates.md` containing:
- **Definitions**:
  - “Round”, “Task list”, “Task template”, “Action template”, “Shared context”, “Materials”.
- **Standard multi-round workflow (v0)**:
  1. Inputs: `goal` (string), `shared_context_paths` (list), `materials_paths` (optional), `N_ROUND` (int), `language` (optional), `workspace` (optional), `limits` (max tasks, max chars).
  2. For each round `r in 1..N_ROUND`:
     - run a “task synthesis/refinement” action (engine-specific; described as data using `ACTION.kind` such as `codex_exec`)
     - output a refined task list artifact (document a recommended location under `references/` or `runtime/`).
  3. After final round: for each task, execute the standard per-task template.
- **Standard per-task template (v0)**:
  - `plan`: produce step plan + acceptance checks for the task (typically `codex_exec`).
  - `work`: implement changes within safe boundaries.
  - `debug`: smallest verification (with timeouts); capture results.
  - `fix`: conditional; only if debug finds issues.
  - `translate`: run before summary/log by default (can be a `codex_exec` action that rewrites the summary into target languages; keep it optional/configurable).
  - `summary`: concise summary + “how to verify”.
  - `log`: publish status updates (prefer `/api/outbox` or `runtime/outbox/<ts>_pipeline.md` per `docs/api-contracts.md`).
  - `commit`: optional and policy-driven (note: AutoAppDev selfdev driver handles git; meta template should make “commit” pluggable).
- **Concrete example**:
  - Include a full example showing:
    - a “meta-round controller” expressed via `TASK.meta` (convention name e.g. `meta_round_v0`) and
    - at least one sample task expanded into normal AAPS `TASK/STEP/ACTION` lines using existing `STEP.block` values (`plan/work/debug/fix/summary/commit_push`) and actions that cover translate/log inside those steps.
  - Explicitly show how action registry binding works using existing convention:
    - `ACTION.meta.action_ref` (id-based) for the configurable actions used by the template.

### 2) Link From the Canonical Spec
Edit `docs/pipeline-formatted-script-spec.md`:
- Add a short section near the end (e.g. new `## 5) Meta-round Templates (Convention v0)`) that:
  - states meta-round loops are represented via `meta` fields and are **engine conventions** (data-only),
  - links to `docs/meta-round-templates.md`,
  - reiterates no new `STEP.block` keys are introduced by the convention (translate/log are actions inside existing blocks).

### 3) (Optional, If It Helps Clarity) Add an Example File
If the example is too long for the doc:
- Add `examples/pipeline_meta_round_template_v0.aaps` and reference it from `docs/meta-round-templates.md`.

Keep this optional to minimize changes; prefer embedding the example in the doc unless it gets unwieldy.

## Verification Commands (DEBUG/VERIFY Phase)
Docs-only checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s rg -n \"Meta-round|meta[- ]round|N_ROUND|multi[- ]round\" docs/pipeline-formatted-script-spec.md docs/meta-round-templates.md
timeout 10s rg -n \"plan/work/debug/fix/translate/summary/log/commit\" docs/meta-round-templates.md
timeout 10s rg -n \"runtime/outbox|/api/outbox\" docs/meta-round-templates.md docs/api-contracts.md docs/workspace-layout.md
```

If an example `.aaps` file is added:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s rg -n \"AUTOAPPDEV_PIPELINE 1\" examples/pipeline_meta_round_template_v0.aaps
```

## Acceptance Checklist
- [ ] `docs/meta-round-templates.md` defines:
  - [ ] `N_ROUND` loop to generate/refine tasks from goal + shared context.
  - [ ] A per-task configurable template covering `plan/work/debug/fix/translate/summary/log/commit`.
  - [ ] “translate before summary/log” default behavior (as a convention).
  - [ ] How to “log” via `/api/outbox` or `runtime/outbox/`.
- [ ] `docs/pipeline-formatted-script-spec.md` references the convention and remains consistent with existing `STEP.block` palette keys.

