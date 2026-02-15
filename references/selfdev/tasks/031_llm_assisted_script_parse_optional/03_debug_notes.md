# Debug Notes: 031 llm_assisted_script_parse_optional

## Verification (Smallest Smoke)
- Static compile of the backend modules changed in this task.
- Pure-function smoke test for AAPS extraction/prompt builder (does not invoke `codex`).
- Grep check confirming route + docs mention the enable flag.

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/llm_assisted_parse.py && echo "py_compile_ok"
# -> py_compile_ok

timeout 10s python3 - <<'PY'
from backend.llm_assisted_parse import LlmParseError, build_prompt, extract_aaps

sample = """Some preface.

```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"X"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"hi"}}
```
"""

aaps, warnings = extract_aaps(sample)
assert aaps.startswith("AUTOAPPDEV_PIPELINE 1\n")
assert "TASK" in aaps
assert "stripped_code_fences" in warnings

try:
    extract_aaps("no header here")
    raise AssertionError("expected LlmParseError")
except LlmParseError as e:
    assert e.code == "missing_aaps_header"

p = build_prompt(source_text="#!/usr/bin/env bash\necho hi\n", source_format="shell")
assert "Do NOT run shell commands" in p
assert "Output ONLY the AAPS v1 text" in p

print("ok")
PY
# -> ok

timeout 10s rg -n "parse-llm|AUTOAPPDEV_ENABLE_LLM_PARSE" backend/app.py docs/api-contracts.md docs/env.md
# -> shows route + docs/env.md + docs/api-contracts.md mentions
```

## Issues Found
- None in these smoke checks.

