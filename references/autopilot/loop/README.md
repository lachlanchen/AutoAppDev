# AutoPilot Loop Store

This folder stores the source-controlled AutoPilot loop schema used by AutoAppDev Studio.

- `accepted.aaps` is the active, parseable AAPS v1 loop.
- `proposed.aaps` is generated only after backend grammar validation succeeds.
- `validation.json` records the latest validation or acceptance result.
- `history/` keeps append-only snapshots so a bad proposal can be recovered.
- `edits.jsonl` is an append-only internal edit ledger.

The backend never accepts a loop update unless `backend.pipeline_parser.parse_aaps_v1` can parse it. Commit and push these files deliberately after review.
