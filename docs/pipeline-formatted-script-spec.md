# Pipeline Formatted Script Spec (v1) + IR Schema

This document defines:
1. A **formatted pipeline script**: human-editable text that is deterministic to parse.
2. A canonical **IR (Intermediate Representation)** schema: `TASK -> STEP -> ACTION`.

Design goals:
- Deterministic parsing (no execution, no templating).
- Versioned and forwards-compatible.
- Maps cleanly to the Scratch-like PWA blocks.

## 1) Formatted Script (AAPS) v1

### 1.1 File Extension
Recommended extension: `.aaps` (AutoAppDev Pipeline Script).

### 1.2 Header
The first non-comment line must be:
```
AUTOAPPDEV_PIPELINE 1
```

### 1.3 Comments and Blank Lines
- Blank lines are ignored.
- Lines starting with `#` are ignored.

### 1.4 Statement Lines
Each non-comment line is a statement:
```
KEYWORD <json-object>
```

Where:
- `KEYWORD` is one of: `TASK`, `STEP`, `ACTION`
- `<json-object>` is a single JSON object on the same line.

Indentation is allowed but not semantically meaningful. Example:
```
TASK  {"id":"t1","title":"Example task"}
  STEP {"id":"s1","title":"Plan","block":"plan"}
    ACTION {"id":"a1","kind":"note","params":{"text":"hello"}}
```

### 1.5 Nesting Rules
Nesting is defined by the most recent preceding statement:
- `TASK` starts a new task context.
- `STEP` belongs to the most recent `TASK`.
- `ACTION` belongs to the most recent `STEP`.

Validation:
- `STEP` must not appear before the first `TASK`.
- `ACTION` must not appear before the first `STEP`.

### 1.6 Required Keys (v1)

`TASK` JSON:
- `id` (string, required): unique within file.
- `title` (string, required)
- `meta` (object, optional)

`STEP` JSON:
- `id` (string, required): unique within its task.
- `title` (string, required)
- `block` (string, required): must be one of the PWA palette keys:
  - `plan`, `work`, `debug`, `fix`, `summary`, `commit_push`
- `meta` (object, optional)

`ACTION` JSON:
- `id` (string, required): unique within its step.
- `kind` (string, required): action type (data only; execution is an engine concern).
- `params` (object, optional): action parameters.
- `meta` (object, optional)

Optional convention (v0):
- `ACTION.meta.action_ref` (object, optional): binds this step to an action definition in the action registry.
  - By id: `{ "id": 123 }`
  - By slug: `{ "slug": "my_action" }` (reserved for a future slug field; stored as data only)

### 1.7 Shell Annotations v0 (Import Helper)
To import from a `.sh` file without parsing bash, embed AAPS lines as structured comments:

```bash
# AAPS: AUTOAPPDEV_PIPELINE 1
# AAPS:
# AAPS: TASK {"id":"t1","title":"Demo"}
# AAPS: STEP {"id":"s1","title":"Plan","block":"plan"}
# AAPS: ACTION {"id":"a1","kind":"noop"}
```

Extraction rule:
- For each line matching `^\s*#\s*AAPS:\s*(.*)$`, capture the remainder as one AAPS line.
- Join captured lines with `\n` to produce the AAPS `script_text`, then parse as AAPS v1.

Limitations:
- Unannotated shell code is ignored.
- No shell parsing or execution; only the embedded AAPS is validated.

## 2) Canonical IR Schema (autoappdev_ir v1)

### 2.1 Top-Level Shape
```json
{
  "kind": "autoappdev_ir",
  "version": 1,
  "tasks": [
    {
      "id": "t1",
      "title": "Task title",
      "meta": {},
      "steps": [
        {
          "id": "s1",
          "title": "Step title",
          "block": "plan",
          "meta": {},
          "actions": [
            { "id": "a1", "kind": "note", "params": { "text": "..." }, "meta": {} }
          ]
        }
      ]
    }
  ]
}
```

### 2.2 Field Notes
- `kind` is always `autoappdev_ir`.
- `version` is always `1` for this spec.
- `meta` fields are optional extensibility points; engines should ignore unknown meta keys.

## 3) Mapping Rules

### 3.1 Script -> IR
Parsing algorithm (conceptual):
1. Verify header `AUTOAPPDEV_PIPELINE 1`.
2. Iterate lines in order, skipping blank/comment lines.
3. For each statement:
   - `TASK`: create new task in `ir.tasks`.
   - `STEP`: append step to current task.
   - `ACTION`: append action to current step.

Invalid input should return actionable errors:
- `STEP` before `TASK`
- `ACTION` before `STEP`
- Missing required keys
- Unknown `STEP.block`

### 3.2 IR -> PWA Scratch-like Blocks
PWA palette keys are the canonical step block names:
- `STEP.block = "plan"` maps to the PWA block `data-block="plan"`
- `STEP.block = "work"` maps to the PWA block `data-block="work"`
- `STEP.block = "debug"` maps to the PWA block `data-block="debug"`
- `STEP.block = "fix"` maps to the PWA block `data-block="fix"`
- `STEP.block = "summary"` maps to the PWA block `data-block="summary"`
- `STEP.block = "commit_push"` maps to the PWA block `data-block="commit_push"`

Reference:
- `pwa/index.html`: toolbox blocks use `data-block` keys
- `pwa/app.js`: `BLOCK_META` defines labels/styles for the same keys

### 3.3 IR -> Existing Plan Payload (Lossy Projection)
The existing plan payload (`autoappdev_plan` v1) is a simple linear list:
```json
{ "kind": "autoappdev_plan", "version": 1, "steps": [ { "id": 1, "block": "plan" } ] }
```

Projection rule (lossy):
- Flatten tasks/steps in-order to `plan.steps`.
- Preserve only the `block` type (drop task/step titles and all actions).

## 4) Complete Example

### 4.1 Example Script (`examples/pipeline_formatted_script_v1.aaps`)
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}

STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}

STEP  {"id":"s2","title":"Work","block":"work"}
ACTION {"id":"a1","kind":"run","params":{"cmd":"echo work"}}

STEP  {"id":"s3","title":"Debug","block":"debug"}
ACTION {"id":"a1","kind":"run","params":{"cmd":"echo debug"}}

STEP  {"id":"s4","title":"Summary","block":"summary"}
ACTION {"id":"a1","kind":"note","params":{"text":"Write summary + verification steps."}}

STEP  {"id":"s5","title":"Release","block":"commit_push"}
ACTION {"id":"a1","kind":"note","params":{"text":"Commit/push is handled by driver scripts."}}
```

### 4.2 Equivalent IR (`examples/pipeline_ir_v1.json`)
See `examples/pipeline_ir_v1.json` (valid JSON).

## 5) Meta-round Templates (Convention v0)
Some pipelines want a "rounds" / meta-loop:
- For `N_ROUND`: generate/refine a task list from a goal + shared context.
- Then, for each task: run a standard per-task template (plan/work/debug/fix/translate/summary/log/commit).

This spec intentionally keeps AAPS parsing deterministic (no templating). Meta-round behavior is represented as **engine conventions** using existing `meta` fields:
- `TASK.meta` / `STEP.meta` / `ACTION.meta` can carry loop/template configuration.
- Engines should ignore unknown `meta` keys they do not understand.

Reference convention:
- `docs/meta-round-templates.md` defines a standard `meta_round_v0` convention, including how to represent:
  - `N_ROUND` and task list artifacts
  - per-task templates without introducing new `STEP.block` values
  - `translate` and `log` as action slots inside existing blocks (typically `summary` and `commit_push`)
