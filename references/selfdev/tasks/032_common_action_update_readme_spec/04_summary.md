# Summary: 032 common_action_update_readme_spec

## What Changed
- Added `docs/common-actions.md` defining the common `ACTION.kind="update_readme"` contract:
  - Safe targeting rule: only `auto-apps/<workspace>/README.md` (workspace slug is a single path segment; no traversal; no arbitrary path params).
  - Owned-block markers: `<!-- AUTOAPPDEV:README:BEGIN -->` / `<!-- AUTOAPPDEV:README:END -->` and replacement semantics.
  - Required `block_markdown` payload with a canonical `## Philosophy` section, plus a recommended template and README snippet example.
- Updated `README.md` to link `docs/common-actions.md` from Contents.

## Why
To standardize a safe, deterministic way for pipelines to update a workspace README without enabling arbitrary filesystem writes, and to give backend/PWA implementations a shared contract (to be implemented in subsequent tasks).

## How To Verify (Smallest Smoke)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s test -f docs/common-actions.md
timeout 10s rg -n "\\bupdate_readme\\b" docs/common-actions.md
timeout 10s rg -n "AUTOAPPDEV:README:BEGIN|AUTOAPPDEV:README:END" docs/common-actions.md
timeout 10s rg -n "^## Philosophy\\b" docs/common-actions.md
timeout 10s rg -n "auto-apps/" docs/common-actions.md
timeout 10s rg -n "docs/common-actions\\.md" README.md
```

