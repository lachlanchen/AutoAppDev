# Summary: 031 llm_assisted_script_parse_optional

## What Changed
- Added optional LLM-assisted parse fallback:
  - New module: `backend/llm_assisted_parse.py` (Codex runner, AAPS extractor, provenance artifact writer).
  - New endpoint: `POST /api/scripts/parse-llm` in `backend/app.py` (disabled unless `AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Updated docs:
  - `docs/env.md` documents `AUTOAPPDEV_ENABLE_LLM_PARSE` and optional Codex defaults.
  - `docs/api-contracts.md` documents `POST /api/scripts/parse-llm`.

## Why
To provide a “best effort” import path for arbitrary pipeline-like scripts while keeping safety high:
Codex output is constrained to AAPS v1 text and then validated by the deterministic `parse_aaps_v1` parser before producing canonical IR.

## How To Verify
Static (no Codex invocation):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 -m py_compile backend/app.py backend/llm_assisted_parse.py
timeout 10s rg -n "parse-llm|AUTOAPPDEV_ENABLE_LLM_PARSE" backend/app.py docs/api-contracts.md docs/env.md
```

Manual (requires `codex` on PATH; optional):
```bash
export AUTOAPPDEV_ENABLE_LLM_PARSE=1

# Start backend, then:
curl -fsS -X POST http://127.0.0.1:8788/api/scripts/parse-llm \\
  -H 'Content-Type: application/json' \\
  -d '{\"source_text\":\"#!/usr/bin/env bash\\necho hello\\n\",\"source_format\":\"shell\"}'
ls -la runtime/logs/llm_parse | tail
```

