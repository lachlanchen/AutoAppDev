# Debug Notes: 051 builtin_readonly_default_actions_clone_on_edit

## Verification Commands + Results

### Static Checks
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

(timeout 10s python3 -m py_compile backend/app.py backend/builtin_actions.py backend/action_registry.py backend/storage.py); echo "exit=$?"
# exit=0

(timeout 10s node --check pwa/app.js); echo "exit=$?"
# exit=0
```

### Built-in Actions + Validator Smoke
Confirms:
- built-ins list is non-empty
- `readonly` built-in IDs are detectable
- built-in spec validates via `validate_action_create()` (same path used by clone endpoint)

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 - <<'PY'
from pathlib import Path

from backend.action_registry import validate_action_create
from backend.builtin_actions import BUILTIN_ID_BASE, get_builtin_action, is_builtin_action_id, list_builtin_action_summaries

items = list_builtin_action_summaries()
assert len(items) >= 1
bid = items[0]["id"]
assert is_builtin_action_id(bid)
assert not is_builtin_action_id(BUILTIN_ID_BASE - 1)

full = get_builtin_action(bid)
assert full and isinstance(full.get("spec"), dict)

# Smoke: cloning a builtin uses validate_action_create; ensure builtin spec validates.
body = {
    "title": str(full.get("title") or "Action") + " (copy)",
    "kind": str(full.get("kind") or "prompt"),
    "enabled": bool(full.get("enabled", True)),
    "spec": full.get("spec"),
}

title, kind, spec, enabled = validate_action_create(body, repo_root=Path(".").resolve(), cfg={})
assert title and kind in ("prompt", "command")
assert isinstance(spec, dict)
assert enabled is True
print("ok", "builtin_id=", bid, "validated_kind=", kind)
PY
```

Result:
```text
ok builtin_id= 9000000001 validated_kind= prompt
```

## Issues Found
- None in static checks.

## Manual Verification (Outside Sandbox)
When backend + PWA are running:
1. In Actions tab, confirm built-in actions show as `readonly`.
2. Select a builtin, edit title/prompt, click Save:
   - UI should clone it via `POST /api/actions/<id>/clone` and then save edits to the cloned id.
3. Confirm Delete is disabled for readonly actions and enabled for cloned actions.

