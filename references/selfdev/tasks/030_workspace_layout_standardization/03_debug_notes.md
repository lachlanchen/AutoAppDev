# Debug Notes: 030 workspace_layout_standardization

## Verification (Smallest Smoke)
- Verified the new doc exists, is linked from `README.md`, and mentions every required standard folder name.

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/workspace-layout.md && echo "doc_exists_ok"
# -> doc_exists_ok

timeout 10s rg -n "docs/workspace-layout\\.md" README.md && echo "readme_link_ok"
# -> (match line) + readme_link_ok

timeout 10s rg -n "materials/" docs/workspace-layout.md
timeout 10s rg -n "interactions/" docs/workspace-layout.md
timeout 10s rg -n "outputs/" docs/workspace-layout.md
timeout 10s rg -n "docs/" docs/workspace-layout.md
timeout 10s rg -n "references/" docs/workspace-layout.md
timeout 10s rg -n "scripts/" docs/workspace-layout.md
timeout 10s rg -n "tools/" docs/workspace-layout.md
timeout 10s rg -n "logs/" docs/workspace-layout.md
timeout 10s rg -n "auto-apps/" docs/workspace-layout.md >/dev/null && echo "folders_mentioned_ok"
# -> folders_mentioned_ok
```

## Issues Found
- None.

