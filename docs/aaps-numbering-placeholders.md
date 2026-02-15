# AAPS Numbering + Placeholders (Convention v0)

This document defines two **optional conventions** that make AAPS v1 scripts feel more Scratch-like while remaining **AAPS v1-compatible**:
1. **Numbered + indented formatting** (display-only; parser ignores it).
2. **Minimal `{{...}}` placeholders** for templating strings in prompts/commands (engine-level; not part of parsing).

Related:
- `docs/pipeline-formatted-script-spec.md` (AAPS v1 grammar + IR schema)
- `docs/meta-round-templates.md` (meta_round_v0 + per-task template)
- `docs/env.md` (`AUTOAPPDEV_RUNTIME_DIR`)

## 1) Numbered + Indented AAPS (Display-only)

### Compatibility Constraint (Why Numbering Is In Comments)
AAPS v1 statement lines must be:
```text
KEYWORD <json-object>
```

Where `KEYWORD` is `TASK`, `STEP`, or `ACTION`.

Because the current deterministic parser (`backend/pipeline_parser.py`) expects the first token to be the keyword, a line like:
```text
1. TASK {...}
```
is **not** AAPS v1 and will not parse.

### Convention
To add Scratch-like numbering without changing the grammar:
- Use indentation for human readability:
  - `TASK` at 0 spaces
  - `STEP` at 2 spaces
  - `ACTION` at 4 spaces
- Add numbering as standalone comment lines immediately above statements:
  - `# 1`, `# 1.1`, `# 1.1.1`, ...

Example:
```text
AUTOAPPDEV_PIPELINE 1

# 2 Task
TASK {"id":"t1","title":"Example"}

# 2.1 Step
  STEP {"id":"s1","title":"Plan","block":"plan"}

# 2.1.1 Action
    ACTION {"id":"a1","kind":"note","params":{"text":"hello"}}
```

Notes:
- These numbering comments are **display hints** only (AAPS parsers ignore `# ...`).
- Tools may compute numbering from order anyway; the convention is mainly for humans and stable references.

## 2) Placeholders (Convention v0)

### Syntax
Placeholders are written as:
- `{{path}}`

Where `path` is a dot-separated identifier (e.g. `task.title`).

Whitespace inside braces is ignored by convention:
- `{{task.title}}` is equivalent to `{{ task.title }}`

### Where Placeholders May Appear
Placeholders are expanded inside **string values**, not in JSON structure.

Recommended supported locations:
- `ACTION.params.prompt` (LLM prompt templates)
- `ACTION.params.cmd` (shell command templates)
- optionally `ACTION.params.text` (notes)

### Minimal Placeholder Set (Required By This Convention)
These placeholders are required by convention:
- `{{task.title}}`
  - Source: current `TASK.title`
- `{{task.acceptance}}`
  - Source: `TASK.meta.acceptance` (string). If unset, engines should treat it as empty or error (engine policy).
- `{{runtime_dir}}`
  - Source: `AUTOAPPDEV_RUNTIME_DIR` env var; default `./runtime` (see `docs/env.md`)

### Error Handling
By default (recommended):
- Unknown placeholders are an error (fail fast).

Engines may add a lenient mode, but should keep the strict behavior available for deterministic pipelines.

### Safety Note (Shell)
`ACTION.params.cmd` is shell text. Placeholder expansion must treat placeholder values as **untrusted strings**:
- Prefer substituting into already-quoted positions, or
- Ensure correct shell quoting/escaping in the engine/runner implementation.

## 3) Complete Example Script
See:
- `examples/pipeline_meta_round_numbered_placeholders_v0.aaps`

It demonstrates:
- `meta_round_v0` (for-loop controller task)
- conditional fix steps via `STEP.meta.conditional = "on_debug_failure"`
- numbering comments + indentation
- placeholder usage in `prompt` and `cmd` strings:
  - `{{task.title}}`, `{{task.acceptance}}`, `{{runtime_dir}}`

