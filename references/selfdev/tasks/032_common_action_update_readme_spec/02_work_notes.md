# Work Notes: 032 common_action_update_readme_spec

## Summary
- Added a doc spec for the common `update_readme` action (markers, safe target path under `auto-apps/`, and a canonical Philosophy section).
- Linked the new doc from `README.md` Contents.

## Changes Made
- `docs/common-actions.md`
  - Defined `ACTION.kind="update_readme"` contract.
  - Defined workspace-safe targeting rule: `auto-apps/<workspace>/README.md` (no arbitrary path params).
  - Defined marker strings: `<!-- AUTOAPPDEV:README:BEGIN -->` / `<!-- AUTOAPPDEV:README:END -->`.
  - Included a default block template containing a canonical `## Philosophy` section.
- `README.md`
  - Added `docs/common-actions.md` to Contents.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/common-actions.md && echo "doc_exists_ok"

timeout 10s rg -n "\\bupdate_readme\\b" docs/common-actions.md
timeout 10s rg -n "AUTOAPPDEV:README:BEGIN|AUTOAPPDEV:README:END" docs/common-actions.md
timeout 10s rg -n "^## Philosophy\\b" docs/common-actions.md
timeout 10s rg -n "auto-apps/" docs/common-actions.md

timeout 10s rg -n "docs/common-actions\\.md" README.md

# (Internal consistency) ensure new doc is ASCII-only
python3 - <<'PY'
import pathlib
p = pathlib.Path('docs/common-actions.md')
text = p.read_text('utf-8')
bad = sorted({ch for ch in text if ord(ch) > 127})
print('non_ascii_count', sum(1 for ch in text if ord(ch) > 127))
print('unique_non_ascii', bad)
PY
```
