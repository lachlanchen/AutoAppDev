# Debug Notes: 032 common_action_update_readme_spec

## Verification (Smallest Smoke)
- Verified the new action spec doc exists and contains the expected contract elements (action kind, markers, Philosophy section, safe `auto-apps/<workspace>/README.md` targeting).
- Verified repo `README.md` links the new spec doc.

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s test -f docs/common-actions.md && echo "doc_exists_ok"
# -> doc_exists_ok

timeout 10s rg -n "\\bupdate_readme\\b" docs/common-actions.md
# -> 13:## update_readme
# -> 53:- `"update_readme"`
# -> 107:ACTION {"id":"a1","kind":"update_readme","params":{"workspace":"my_workspace","block_markdown":"...markdown..."}}
# -> 114:  "kind": "update_readme",

timeout 10s rg -n "AUTOAPPDEV:README:BEGIN|AUTOAPPDEV:README:END" docs/common-actions.md
# -> 42:- Begin marker: `<!-- AUTOAPPDEV:README:BEGIN -->`
# -> 43:- End marker: `<!-- AUTOAPPDEV:README:END -->`
# -> 89:<!-- AUTOAPPDEV:README:BEGIN -->
# -> 102:<!-- AUTOAPPDEV:README:END -->

timeout 10s rg -n "^## Philosophy\\b" docs/common-actions.md
# -> 73:## Philosophy
# -> 94:## Philosophy

timeout 10s rg -n "auto-apps/" docs/common-actions.md
# -> 21:This action targets a workspace README under the controller repo's `auto-apps/` container.
# -> 25:  - A **workspace slug** identifying a child directory under `auto-apps/`.
# -> 29:- `auto-apps/<workspace>/README.md`
# -> 37:- reject any resolved paths outside `auto-apps/`

timeout 10s rg -n "block_markdown" docs/common-actions.md
# -> 57:- `block_markdown` (required string)
# -> 61:### Recommended block_markdown Template (Includes Philosophy)
# -> 62:A recommended `block_markdown` template is:
# -> 107:ACTION {"id":"a1","kind":"update_readme","params":{"workspace":"my_workspace","block_markdown":"...markdown..."}}
# -> 115:  "params": { "workspace": "my_workspace", "block_markdown": "...markdown..." }

timeout 10s rg -n "docs/common-actions\\.md" README.md
# -> 39:- `docs/common-actions.md`: Common action contracts/specs (includes `update_readme`).

timeout 10s python3 - <<'PY'
import pathlib
p = pathlib.Path('docs/common-actions.md')
text = p.read_text('utf-8')
bad = sorted({ch for ch in text if ord(ch) > 127})
print('non_ascii_count', sum(1 for ch in text if ord(ch) > 127))
print('unique_non_ascii', bad)
PY
# -> non_ascii_count 0
# -> unique_non_ascii []
```

## Issues Found
- Initial spec had `block_markdown` marked optional and examples omitted it; updated `docs/common-actions.md` to match the plan (required `block_markdown` + added README snippet with markers).

