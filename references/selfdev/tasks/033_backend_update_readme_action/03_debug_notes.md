# Debug Notes: 033 backend_update_readme_action

## Verification (Smallest Smoke)
- Static compile of backend modules changed in this task.
- Pure-function smoke test for workspace slug validation, block markdown validation, safe path resolution, marker upsert behavior (create/insert/replace), mismatch handling, and artifact writing (no server, no DB).
- Grep check confirming the endpoint route is wired and documented.

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/update_readme_action.py && echo "py_compile_ok"
# -> py_compile_ok

timeout 10s python3 - <<'PY'
from pathlib import Path
import tempfile

from backend.update_readme_action import (
    README_BEGIN,
    README_END,
    UpdateReadmeError,
    make_update_id,
    resolve_workspace_readme_path,
    upsert_readme_block,
    validate_block_markdown,
    validate_workspace_slug,
    write_update_artifacts,
)

assert validate_workspace_slug("ok_slug") == "ok_slug"
for bad in ["", ".", "..", "../x", "a/b", "a\\b", " x/y "]:
    try:
        validate_workspace_slug(bad)
        raise AssertionError(f"expected invalid_workspace for {bad!r}")
    except UpdateReadmeError as e:
        assert e.code == "invalid_workspace"

validate_block_markdown("## Philosophy\ntext\n")
for bad_block in ["", "no philosophy here", f"## Philosophy\n{README_BEGIN}\n"]:
    try:
        validate_block_markdown(bad_block)
        raise AssertionError("expected error")
    except UpdateReadmeError as e:
        assert e.code in {"invalid_block_markdown", "missing_philosophy"}

with tempfile.TemporaryDirectory() as td:
    repo_root = Path(td) / "repo"
    runtime_dir = Path(td) / "runtime"
    repo_root.mkdir(parents=True, exist_ok=True)
    (repo_root / "auto-apps").mkdir(parents=True, exist_ok=True)

    target = resolve_workspace_readme_path(repo_root, "ws1")
    assert str(target).endswith("/auto-apps/ws1/README.md")

    after0, meta0 = upsert_readme_block(None, workspace="ws1", block_markdown="## Philosophy\nX\n")
    assert after0.startswith("# ws1\n")
    assert README_BEGIN in after0 and README_END in after0
    assert meta0.get("mode") == "create"

    before1 = "# Title\n\nUser intro.\n"
    after1, meta1 = upsert_readme_block(before1, workspace="ws1", block_markdown="## Philosophy\nX\n")
    assert after1.index(README_BEGIN) > after1.index("# Title")
    assert meta1.get("mode") == "insert_after_h1"

    after2, meta2 = upsert_readme_block(after1, workspace="ws1", block_markdown="## Philosophy\nY\n")
    assert "Y" in after2 and "X" not in after2
    assert meta2.get("mode") == "replace"

    try:
        upsert_readme_block(f"{README_BEGIN}\nonly begin\n", workspace="ws1", block_markdown="## Philosophy\nZ\n")
        raise AssertionError("expected marker_mismatch")
    except UpdateReadmeError as e:
        assert e.code == "marker_mismatch"

    uid = make_update_id(workspace="ws1", block_markdown="## Philosophy\nY\n")
    arts = write_update_artifacts(runtime_dir, uid, before=before1, after=after2, meta={"id": uid})
    assert arts.before.exists() and arts.after.exists() and arts.diff.exists() and arts.meta.exists()

print("ok")
PY
# -> ok

timeout 10s rg -n "/api/actions/update-readme" backend/app.py docs/api-contracts.md
# -> backend/app.py:1132:            (r"/api/actions/update-readme", UpdateReadmeHandler, {"runtime_dir": runtime_dir}),
# -> docs/api-contracts.md:260:### POST /api/actions/update-readme
```

## Issues Found
- None in these smoke checks.

