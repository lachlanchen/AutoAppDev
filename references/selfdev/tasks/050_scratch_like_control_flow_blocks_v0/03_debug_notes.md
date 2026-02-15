# Debug Notes: 050 scratch_like_control_flow_blocks_v0

## Verification Commands + Results

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

(timeout 10s node --check pwa/app.js); echo "exit=$?"
# exit=0

(timeout 10s node --check pwa/i18n.js); echo "exit=$?"
# exit=0

(timeout 10s python3 -m py_compile backend/pipeline_parser.py); echo "exit=$?"
# exit=0
```

### Meta-round AAPS Parser Smoke (Backend)
Ensures backend AAPS v1 parser accepts multi-task scripts with `meta_round_v0` + `task_template_v0` and conditional `fix` meta.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 - <<'PY'
from backend.pipeline_parser import parse_aaps_v1

script = """AUTOAPPDEV_PIPELINE 1

# 1 Task
TASK {"id":"meta","title":"Meta-round controller","meta":{"meta_round_v0":{"n_round":2,"task_list_path":"references/meta_round/tasks_v0.json"}}}

# 1.1 Step
  STEP {"id":"r1","title":"Round 1: Plan","block":"plan","meta":{"round":1}}
# 1.1.1 Action
    ACTION {"id":"a1","kind":"noop","params":{}}

# 1.2 Step
  STEP {"id":"r2","title":"Round 2: Plan","block":"plan","meta":{"round":2}}
# 1.2.1 Action
    ACTION {"id":"a1","kind":"noop","params":{}}

# 2 Task
TASK {"id":"template","title":"Task template","meta":{"task_template_v0":true}}

# 2.1 Step
  STEP {"id":"s1","title":"Plan","block":"plan"}
# 2.1.1 Action
    ACTION {"id":"a1","kind":"noop","params":{}}

# 2.2 Step
  STEP {"id":"s2","title":"Fix (if needed)","block":"fix","meta":{"conditional":"on_debug_failure"}}
# 2.2.1 Action
    ACTION {"id":"a1","kind":"noop","params":{}}
"""

ir = parse_aaps_v1(script)
print("kind=", ir.get("kind"))
print("tasks=", len(ir.get("tasks") or []))
print("t1_steps=", len((ir["tasks"][0].get("steps") or [])))
print("t2_steps=", len((ir["tasks"][1].get("steps") or [])))
PY
```

Result:
```text
kind= autoappdev_ir
tasks= 2
t1_steps= 2
t2_steps= 2
```

## Issues Found
- None in static checks.

## Manual Verification (Outside Sandbox)
1. Open PWA and confirm a fresh load shows the nested default template:
   `Meta Tasks -> For N_ROUND -> For each task -> If/Else`.
2. Script tab:
   - Click `From Blocks`, confirm exported AAPS contains 2 tasks and `TASK.meta.meta_round_v0` / `TASK.meta.task_template_v0`.
   - Click `Parse AAPS -> Blocks`, confirm nested structure is reconstructed.

