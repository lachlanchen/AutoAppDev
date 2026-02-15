# Debug Notes: 034 pwa_update_readme_block

## Verification (Smallest Smoke)
- Static JS syntax check for the updated PWA script.
- Grep checks confirming the new palette block exists and the export code includes `block_markdown`.
- Backend parser smoke check proving an `ACTION.kind="update_readme"` can be represented in AAPS with `STEP.block="summary"` (allowed) and parses successfully (no server required).

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 5s node --check pwa/app.js && echo "node_check_ok"
# -> node_check_ok

timeout 10s rg -n 'data-block=\"update_readme\"' pwa/index.html
# -> 72:          <div class="block block--summary" draggable="true" data-block="update_readme">Update README</div>

timeout 10s rg -n 'kind\\\":\\s*\\\"update_readme\\\"|block_markdown|Workspace slug' pwa/app.js
# -> 230:            block_markdown: defaultUpdateReadmeBlockMarkdown({ workspace: ws }),
# -> 268:          block_markdown: defaultUpdateReadmeBlockMarkdown({ workspace: ws }),
# -> 694:      const raw = window.prompt("Workspace slug for auto-apps/<workspace>/README.md?", "my_workspace");

timeout 10s python3 - <<'PY'
import json
from backend.pipeline_parser import parse_aaps_v1

block_markdown = "## Workspace Status (Auto-Updated)\\n\\n- Updated: <utc-iso-timestamp>\\n\\n## Philosophy\\nX\\n"

script = "\\n".join(
    [
        "AUTOAPPDEV_PIPELINE 1",
        "",
        "TASK  " + json.dumps({"id": "t1", "title": "Demo"}, separators=(",", ":")),
        "",
        "STEP  " + json.dumps({"id": "s1", "title": "Update README", "block": "summary"}, separators=(",", ":")),
        "ACTION "
        + json.dumps(
            {
                "id": "a1",
                "kind": "update_readme",
                "params": {"workspace": "my_workspace", "block_markdown": block_markdown},
            },
            separators=(",", ":"),
        ),
        "",
    ]
) + "\\n"

ir = parse_aaps_v1(script)
step = ir["tasks"][0]["steps"][0]
assert step["block"] == "summary"
assert step["actions"][0]["kind"] == "update_readme"
assert step["actions"][0]["params"]["workspace"] == "my_workspace"
print("ok")
PY
# -> ok
```

## Issues Found
- None in these smoke checks.

