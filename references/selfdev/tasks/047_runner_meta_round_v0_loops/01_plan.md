# Plan: 047 runner_meta_round_v0_loops

## Goal
Extend runner codegen so **generated bash runners** can execute the `meta_round_v0` convention:
1. Run the controller task’s “round” steps.
2. Read the controller’s `task_list_path` JSON (`autoappdev_task_list` v0).
3. Loop the produced tasks and execute a template task marked by `TASK.meta.task_template_v0`, with the existing `{{...}}` placeholder substitution.
4. Persist resume state under the runtime dir so reruns skip already-completed tasks.

Acceptance:
- Generated runners implement `meta_round_v0` looping and template task application.
- Placeholder substitution uses the task-list item fields (id/title/acceptance) while running the template.
- Resume state is persisted under runtime; a second run skips tasks already completed.
- Include an example IR + generated runner smoke demonstrating behavior.

## Current State (Relevant Files)
- Runner generator:
  - `scripts/pipeline_codegen/generate_runner_from_ir.py`
  - Already exports task/step/action context vars for placeholder substitution.
  - Already supports conditional steps (`STEP.meta.conditional`) and debug failure capture.
- Runner template:
  - `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`
  - Has strict placeholder substitution (`subst_placeholders`) and conditional-step support (`step_should_run`).
- Meta-round convention (docs-only today):
  - `docs/meta-round-templates.md`
  - Defines `TASK.meta.meta_round_v0` and a task-list artifact (`autoappdev_task_list` v0).
  - Mentions conditional fix steps (`STEP.meta.conditional="on_debug_failure"`).

## Proposed Minimal Design
Implement a runner-only “meta-round mode” when the IR contains:
- Exactly one controller task: `TASK.meta.meta_round_v0` (object; must include `task_list_path`).
- Exactly one template task: `TASK.meta.task_template_v0` (boolean or object; treated as a marker).

Behavior in meta-round mode:
1. Execute controller task steps (in-order) normally.
2. Read `task_list_path` JSON and extract `tasks[]` items `{id,title,acceptance}`.
3. For each produced task:
   - If already completed per runtime resume state: log skip and continue.
   - Else: execute the template task steps/actions with context variables set from the produced task:
     - `AUTOAPPDEV_CTX_TASK_ID`, `AUTOAPPDEV_CTX_TASK_TITLE`, `AUTOAPPDEV_CTX_TASK_ACCEPTANCE`
4. After a produced task completes successfully: mark it completed in the runtime resume file.

Resume storage (runtime-scoped, gitignored):
- Default file: `"$RUNTIME_DIR/meta_round_v0_resume.json"`
- JSON shape (v0, minimal):
  - `{ "kind":"autoappdev_meta_round_resume", "version":0, "completed_task_ids":[...], "updated_at":"..." }`

Path resolution:
- Treat `task_list_path` as a literal path string as provided in the IR.
- For the smoke example, run the generated runner from a temporary working directory so relative `task_list_path` does not touch repo files.

## Implementation Steps (Next Phase: WORK)

### 1) Runner Template: Meta-round Helpers + Resume State IO
Edit `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`:
- Add `META_ROUND_RESUME_FILE="${AUTOAPPDEV_META_ROUND_RESUME_FILE:-$RUNTIME_DIR/meta_round_v0_resume.json}"`.
- Add helper functions (bash wrappers around small `python3` snippets):
  - `meta_round_read_task_list <path>`:
    - validates `kind=="autoappdev_task_list"` and `version==0`
    - emits tasks as a robust stream for bash iteration (recommended: NUL-delimited triplets: `id\\0title\\0acceptance\\0...`)
  - `meta_round_is_completed <task_id> <resume_file>`:
    - returns 0/1 based on membership in `completed_task_ids`
  - `meta_round_mark_completed <task_id> <resume_file>`:
    - atomically updates JSON (write `*.tmp` then rename)
- Add a runner-level function `meta_round_run_template_tasks <task_list_path>` that:
  - iterates produced tasks
  - calls `run_task_template_v0 "$id" "$title" "$acceptance"`
  - marks completion on success
  - logs `SKIP META_TASK ...` lines for resumability visibility

### 2) Generator: Detect Controller + Template Tasks and Generate Template Function
Edit `scripts/pipeline_codegen/generate_runner_from_ir.py`:
- Parse controller:
  - detect `tasks[*].meta.meta_round_v0` (object)
  - require `task_list_path` (string, non-empty)
  - (optional) parse `n_round` (int) for logging only; do not enforce in v0
- Parse template:
  - detect `tasks[*].meta.task_template_v0` (present and truthy)
- Validation (fail fast, deterministic):
  - if meta-round controller exists:
    - require exactly one controller + exactly one template task
    - (recommended v0) require no other tasks, or explicitly define how additional tasks are handled
- Codegen output structure (inside `main()` body via `__PIPELINE_BODY__`):
  1. Emit controller TASK/STEP/ACTION blocks as usual.
  2. Emit a bash function definition `run_task_template_v0()` containing the template task’s steps/actions:
     - Signature: `run_task_template_v0 <id> <title> <acceptance>`
     - Inside: export `AUTOAPPDEV_CTX_TASK_*` from args; log `TASK ...`
     - Reuse existing step/action generation logic for steps/actions.
  3. After controller completes, call:
     - `meta_round_run_template_tasks "<task_list_path>"`

### 3) Example IR: Meta-round Controller + Template
Add `examples/pipeline_ir_meta_round_v0_demo_v0.json`:
- Contains:
  - Controller task `meta` with `meta.meta_round_v0.task_list_path` set to a relative file like `task_list.json`.
  - Controller round step(s) that write a deterministic task list via a benign `run` action (python snippet writing JSON).
  - Template task with `meta.task_template_v0` marker and steps/actions that print sentinel output including placeholders:
    - e.g. `echo TEMPLATE_RUN id={{task.id}} title={{task.title}} acceptance={{task.acceptance}}`

### 4) Smoke Script: Demonstrate Loop + Resume Skip
Add `scripts/pipeline_codegen/smoke_meta_round_v0.sh`:
- Generate runner to `/tmp/autoappdev_runner_meta_round_v0.sh` from the example IR.
- Create an isolated temp workdir (`/tmp/...`) and runtime dir (`/tmp/...`).
- Run #1:
  - `cd "$workdir"`
  - run runner with `AUTOAPPDEV_RUNTIME_DIR="$runtime_dir"` and `timeout 20s`
  - assert output contains `TEMPLATE_RUN id=...` for each task list item
- Run #2 (same workdir + same runtime dir):
  - assert output contains `SKIP META_TASK ...` lines
  - assert `TEMPLATE_RUN ...` does **not** reappear (tasks are skipped)

### 5) Docs: Document Runner Meta-round Support
Update docs (minimal, runner-focused):
- `docs/pipeline-runner-codegen.md`:
  - add “Meta-round loops (v0)” section documenting:
    - `TASK.meta.meta_round_v0.task_list_path`
    - `TASK.meta.task_template_v0` marker
    - resume file location + semantics
    - requirement to run from an appropriate working directory for relative `task_list_path`
- `docs/meta-round-templates.md`:
  - add a short note that runners may implement `task_template_v0` to avoid duplicating expanded tasks in static IR, and that resume state is stored under runtime.

## Verification Commands (DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_meta_round_v0_demo_v0.json >/dev/null

chmod +x scripts/pipeline_codegen/smoke_meta_round_v0.sh
timeout 30s scripts/pipeline_codegen/smoke_meta_round_v0.sh

# Optional: keep existing smokes
timeout 20s scripts/pipeline_codegen/smoke_conditional_steps.sh
timeout 20s scripts/pipeline_codegen/smoke_placeholders.sh
timeout 20s scripts/pipeline_codegen/smoke_codegen.sh
```

## Acceptance Checklist
- [ ] Controller task executes and produces/updates `task_list_path`.
- [ ] Runner reads `autoappdev_task_list` v0 and loops tasks deterministically.
- [ ] Template task runs once per produced task with `{{task.*}}` substituted from the task list item.
- [ ] Resume state persists under `AUTOAPPDEV_RUNTIME_DIR`; second run skips already completed tasks.
- [ ] Example IR + smoke script prove behavior without invoking `codex` (use `run` actions only).

