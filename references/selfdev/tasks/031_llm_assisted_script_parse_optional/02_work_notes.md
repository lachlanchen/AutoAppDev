# Work Notes: 031 llm_assisted_script_parse_optional

## Summary
- Added an optional Codex-powered parse fallback endpoint: `POST /api/scripts/parse-llm`.
- Endpoint is **disabled by default** and guarded by `AUTOAPPDEV_ENABLE_LLM_PARSE=1`.
- The endpoint stores provenance artifacts (prompt/input/raw JSONL/extracted AAPS/provenance JSON) under `AUTOAPPDEV_RUNTIME_DIR/logs/llm_parse/<id>/`.
- Updated docs for the new endpoint + env flag.

## Changes Made
- `backend/llm_assisted_parse.py`
  - Implements:
    - prompt builder (`build_prompt`)
    - AAPS extractor (`extract_aaps`) that looks for `AUTOAPPDEV_PIPELINE 1`
    - non-interactive Codex runner (`run_codex_to_jsonl`) with timeout
    - artifact writer (`write_artifacts`) for provenance/prompt capture
    - typed error (`LlmParseError`)
- `backend/app.py`
  - Added `ScriptsParseLlmHandler`:
    - Validates request (`source_text`, size limit 100k, timeout clamp 5-120s).
    - Runs `codex exec --json` (no `--full-auto`).
    - Extracts AAPS and validates via deterministic `parse_aaps_v1`.
    - Writes provenance artifacts under `runtime/logs/llm_parse/<id>/`.
    - Optional `save=true` persists the script + IR into `pipeline_scripts`.
  - Wired route: `POST /api/scripts/parse-llm`.
- `docs/env.md`
  - Documented `AUTOAPPDEV_ENABLE_LLM_PARSE` and Codex default env vars.
- `docs/api-contracts.md`
  - Documented `POST /api/scripts/parse-llm` contract and error modes.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/llm_assisted_parse.py
rg -n "parse-llm|AUTOAPPDEV_ENABLE_LLM_PARSE|llm_parse" backend/app.py backend/llm_assisted_parse.py docs/env.md docs/api-contracts.md
```

