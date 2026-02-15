# Work Notes: 044 aaps_numbered_prefix_parser

## Implementation Notes
- Extended the deterministic AAPS parser to accept optional numeric prefixes before statement keywords:
  - `backend/pipeline_parser.py`: statement tokenization now supports lines like `1.2 STEP {...}` and `1.2. STEP {...}` by treating the numeric prefix as display-only decoration.
- Added a numbered-prefix example script:
  - `examples/pipeline_formatted_script_numbered_prefix_v1.aaps`
- Updated docs to stay accurate about numbering:
  - `docs/aaps-numbering-placeholders.md` no longer claims numeric-prefix lines are unparseable; it still recommends comment numbering as the most portable AAPS v1-compatible convention.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

sed -n '1,120p' docs/aaps-numbering-placeholders.md
timeout 10s python3 -m py_compile backend/pipeline_parser.py
```

