# Meta-round Pipeline Templates (v0)

This document defines a **standard, engine-agnostic** convention for expressing a multi-round pipeline template:
- For `N_ROUND`: generate/refine a task list from a `goal` + shared context.
- For each resulting task: execute a configurable per-task template:
  `plan -> work -> debug -> fix -> translate -> summary -> log -> commit`.

Important:
- AAPS/IR (`TASK -> STEP -> ACTION`) remain **data-only** and deterministic to parse.
- Meta-round loops and templates are expressed via `meta` fields (engine conventions), not by adding templating to the parser.

Related docs:
- `docs/pipeline-formatted-script-spec.md` (AAPS + IR schema)
- `docs/workspace-layout.md` (workspace + runtime dir conventions)
- `docs/api-contracts.md` (includes `/api/outbox` and `runtime/outbox/` queue)

## Terms
- **Round**: one pass of "synthesize/refine tasks" using the current task list as input.
- **Task list artifact**: a durable representation of tasks produced by the round loop (JSON recommended; see below).
- **Per-task template**: the standard phase sequence applied to each task.
- **Shared context**: durable, read-only inputs used for task synthesis (docs, reference code, constraints).
- **Materials**: workspace-specific inputs (screenshots, datasets, external docs).

## Standard Meta-round Workflow (v0)

### Inputs (Recommended)
The meta-round controller needs:
- `goal` (string): what we are trying to achieve.
- `shared_context_paths` (string[]): repo/workspace files to treat as context (read-only).
- `materials_paths` (string[], optional): workspace materials (read-only).
- `n_round` (int): number of refinement rounds (`N_ROUND`), recommended `1..5`.
- `task_limit` (int, optional): cap produced tasks to keep the pipeline bounded.
- `language` (string, optional): base language for artifacts (default: `en`).
- `target_languages` (string[], optional): for the translate slot; default pack:
  `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `vi`, `ar`, `fr`, `es`.
- `task_list_path` (string): where to write the refined task list artifact.
  - Recommended: `references/meta_round/tasks_v0.json` under a workspace root.

### Task List Artifact Format (Recommended)
To keep loops explicit and resumable, store a durable task list artifact.

Recommended v0 JSON shape:
```json
{
  "kind": "autoappdev_task_list",
  "version": 0,
  "round": 2,
  "goal": "...",
  "tasks": [
    { "id": "t1", "title": "Short title", "acceptance": "Testable acceptance criteria" }
  ]
}
```

Notes:
- `id` should be stable within the artifact (string).
- Engines may add additional fields (priority, tags, estimated_cost), but should preserve the core shape.

### Per-round Behavior
For each round `r`:
1. Read inputs:
   - `goal`
   - shared context files
   - previous `task_list_path` (if present; empty list for round 1)
2. Run a synthesis/refinement action (engine-specific):
   - typically an LLM-backed action (`ACTION.kind: "codex_exec"`) that writes the next `tasks_v0.json`
3. Persist the updated artifact and record a lightweight progress log entry (see "Log slot").

After the final round:
- Execute the per-task template for each task in the final artifact, in-order.

## Per-task Template (v0)

### Phase Ordering (Standard)
The standard per-task phases are:
1. `plan`: outline changes + exact verification commands (with timeouts).
2. `work`: implement the smallest change set to meet acceptance.
3. `debug`: run the smallest verification; record results.
4. `fix`: conditional; only if debug finds issues.
5. `translate`: run before summary/log by default (configurable).
6. `summary`: concise summary of what changed, why, and how to verify.
7. `log`: publish status to the operator UI (outbox) and/or durable logs.
8. `commit`: optional and policy-driven.

### Mapping To AAPS/IR (No New `STEP.block` Keys)
The AAPS v1 spec constrains `STEP.block` to the existing palette keys:
`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`.

To keep the contract stable:
- `translate` is represented as an **action slot** within the `summary` step (runs before summary actions).
- `log` is represented as an **action slot** within the `commit_push` step (or as the last action in `summary` if no commit phase exists).
- `commit` is represented as an optional action in `commit_push` (or omitted entirely if handled externally).

In other words, the per-task template is expressed as:
- `STEP.block=plan` (plan)
- `STEP.block=work` (work)
- `STEP.block=debug` (debug)
- `STEP.block=fix` (fix, optional)
- `STEP.block=summary` (translate + summary actions)
- `STEP.block=commit_push` (log + commit actions)

### Log Slot (Outbox)
Preferred log channel: the outbox API/queue defined in:
- `docs/api-contracts.md` (`POST /api/outbox` and `runtime/outbox/<ts>_<role>.md|.txt`)

Recommended patterns for a pipeline script:
- HTTP:
  - `curl -sS -X POST http://127.0.0.1:8788/api/outbox -H 'content-type: application/json' -d '{"role":"pipeline","content":"..."}'`
- File queue (atomic rename recommended):
  - `printf '...\n' > runtime/outbox/.tmp && mv runtime/outbox/.tmp runtime/outbox/$(date +%s%3N)_pipeline.md`

## Convention: Where `meta_round_v0` Lives
Meta-round configuration is stored under `TASK.meta.meta_round_v0` (engine convention).

Recommended keys:
```json
{
  "n_round": 2,
  "goal": "...",
  "shared_context_paths": ["docs/constraints.md"],
  "materials_paths": ["materials/"],
  "task_list_path": "references/meta_round/tasks_v0.json",
  "task_limit": 20,
  "language": "en",
  "target_languages": ["zh-Hans", "zh-Hant", "en", "ja", "ko", "vi", "ar", "fr", "es"]
}
```

## Concrete AAPS Example (v0)
This example is valid AAPS v1 (deterministic to parse). The meta-round behavior is expressed via `meta`.

```text
AUTOAPPDEV_PIPELINE 1

# Meta-round controller task (engine reads TASK.meta.meta_round_v0)
TASK {"id":"meta","title":"Meta-round: derive task list","meta":{"meta_round_v0":{"n_round":2,"goal":"Build feature X","shared_context_paths":["docs/pipeline-formatted-script-spec.md","docs/workspace-layout.md"],"task_list_path":"references/meta_round/tasks_v0.json","task_limit":10,"language":"en","target_languages":["zh-Hans","zh-Hant","en","ja","ko","vi","ar","fr","es"]}}}

STEP {"id":"r1","title":"Round 1: draft tasks","block":"plan","meta":{"round":1}}
ACTION {"id":"a1","kind":"codex_exec","params":{"prompt":"Round 1: from goal+context, write references/meta_round/tasks_v0.json (autoappdev_task_list v0)."}}

STEP {"id":"r2","title":"Round 2: refine tasks","block":"plan","meta":{"round":2}}
ACTION {"id":"a1","kind":"codex_exec","params":{"prompt":"Round 2: refine the existing task list; keep tasks small and testable."}}

# Example expanded task (one task from the final task list)
TASK {"id":"t1","title":"Implement feature X (small step)"}

STEP {"id":"p","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"codex_exec","params":{"prompt":"Write a step plan + acceptance checks for this task."}}

STEP {"id":"w","title":"Work","block":"work"}
ACTION {"id":"a1","kind":"codex_exec","params":{"prompt":"Implement the smallest set of changes for this task."}}

STEP {"id":"d","title":"Debug/Verify","block":"debug"}
ACTION {"id":"a1","kind":"run","params":{"cmd":"timeout 10s python -m py_compile backend/app.py"}}

STEP {"id":"f","title":"Fix (if needed)","block":"fix","meta":{"conditional":"on_debug_failure"}}
ACTION {"id":"a1","kind":"codex_exec","params":{"prompt":"If debug fails, implement minimal fixes and re-run verification."}}

STEP {"id":"s","title":"Translate + Summary","block":"summary"}
ACTION {"id":"t1","kind":"codex_exec","meta":{"slot":"translate"},"params":{"prompt":"Translate the summary into target_languages (optional)."}}
ACTION {"id":"s1","kind":"codex_exec","meta":{"slot":"summary"},"params":{"prompt":"Write a concise summary and how to verify."}}

STEP {"id":"c","title":"Log + Commit","block":"commit_push"}
ACTION {"id":"l1","kind":"run","meta":{"slot":"log"},"params":{"cmd":"printf 'Task t1 complete\\n' > runtime/outbox/.tmp && mv runtime/outbox/.tmp runtime/outbox/$(date +%s%3N)_pipeline.md"}}
ACTION {"id":"g1","kind":"note","meta":{"slot":"commit"},"params":{"text":"Commit is policy-driven; external drivers may handle git."}}
```

Notes:
- `translate`/`log`/`commit` are modeled as **action slots**, not as new `STEP.block` values.
- Engines can bind these slots to an action registry using `ACTION.meta.action_ref` (see `docs/pipeline-formatted-script-spec.md`).

