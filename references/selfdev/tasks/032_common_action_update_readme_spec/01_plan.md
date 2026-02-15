# Plan: 032 common_action_update_readme_spec

## Goal
Define a **common pipeline ACTION** named `update_readme` so pipelines can update a workspace README in a safe, deterministic way.

Acceptance:
- Docs define an `update_readme` ACTION including:
  - the **marker strings** used for the auto-managed README block
  - a canonical **Philosophy** section to include in that block
  - safe targeting of a workspace README under `auto-apps/` (no arbitrary path writes)

## Current State (References)
- Controller repo README already uses marker-based patching for an auto-generated status block:
  - Markers: `<!-- AUTOAPPDEV:STATUS:BEGIN -->` / `<!-- AUTOAPPDEV:STATUS:END -->`: `README.md`
  - Patch logic: `scripts/auto-autoappdev-development.sh` (`update_readme_autogen`)
- Workspace path conventions are documented:
  - Workspaces live under `auto-apps/`: `docs/workspace-layout.md`
- Pipeline scripts/IR already support arbitrary `ACTION.kind` strings:
  - AAPS + IR schema: `docs/pipeline-formatted-script-spec.md`

## Documentation Design (Spec v0)
Create a new doc that acts as the canonical spec for this action:
- New file: `docs/common-actions.md`
  - Add a section: `## update_readme`
  - Define:
    1. **Purpose**: keep workspace `README.md` current (status + workflow philosophy) without touching other files.
    2. **Target path rule** (no arbitrary writes):
       - Required param: `params.workspace` (string slug; **single path segment**, no `/`, no `..`)
       - Target file is always: `auto-apps/<workspace>/README.md`
       - No `params.path` field in the spec (explicitly forbidden).
       - Mention that backend implementations MUST validate resolved paths remain under `auto-apps/`.
    3. **Markers** for the auto-managed block (distinct from controller self-dev markers):
       - Begin: `<!-- AUTOAPPDEV:README:BEGIN -->`
       - End:   `<!-- AUTOAPPDEV:README:END -->`
       - Semantics:
         - Content between markers is owned by `update_readme` and may be replaced wholesale.
         - Content outside markers is user-owned and must be preserved.
         - If markers are missing, the implementation should insert them (recommended: after the first H1 if present, else at top).
    4. **Required Philosophy section** (canonical text):
       - Include a `## Philosophy` section inside the marker block.
       - Reuse the same high-level loop as the controller README (`README.md#Philosophy`), adapted to “workspace/pipeline” wording.
    5. **Action payload schema** (minimal, future-proof):
       - `ACTION.kind = "update_readme"`
       - `params.workspace` (required string)
       - `params.block_markdown` (required string): exact markdown to place between markers.
         - Doc provides a recommended template that includes Philosophy + a Status subsection.
    6. **Examples**:
       - Example AAPS line:
         - `ACTION {"id":"a1","kind":"update_readme","params":{"workspace":"my_workspace","block_markdown":"...markdown..."}}`
       - Example resulting README snippet showing markers + Philosophy section.

## Implementation Steps (Next Phase: WORK)
1. Add the new action spec doc
   - Create `docs/common-actions.md` with:
     - `update_readme` definition (markers, params, philosophy text, examples).
     - Explicit safety constraints (workspace slug restrictions; no arbitrary paths).
     - Cross-links to: `docs/workspace-layout.md`, `docs/pipeline-formatted-script-spec.md`.

2. Link from repo index
   - Update `README.md` Contents list to include:
     - `docs/common-actions.md`: Common action specs (includes `update_readme`)

Notes:
- Keep this task doc-only (no backend/PWA changes).
- Backend endpoint/API contract for executing `update_readme` is deferred to task 033.

## Commands To Run (Verification)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/common-actions.md

# Ensure the doc defines markers + action kind + philosophy.
rg -n \"\\bupdate_readme\\b\" docs/common-actions.md
rg -n \"AUTOAPPDEV:README:BEGIN|AUTOAPPDEV:README:END\" docs/common-actions.md
rg -n \"^## Philosophy\\b\" docs/common-actions.md
rg -n \"\\bauto-apps/\\b\" docs/common-actions.md

# Ensure README links the doc.
rg -n \"docs/common-actions\\.md\" README.md
```

## Acceptance Checklist
- [ ] `docs/common-actions.md` defines `update_readme` action kind + params.
- [ ] Doc defines marker strings and replacement semantics.
- [ ] Doc includes a canonical `## Philosophy` section for workspaces.
- [ ] Doc defines safe targeting of `auto-apps/<workspace>/README.md` without allowing arbitrary paths.
- [ ] `README.md` links to `docs/common-actions.md`.

