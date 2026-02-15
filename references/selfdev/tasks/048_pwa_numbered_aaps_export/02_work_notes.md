# Work Notes: 048 pwa_numbered_aaps_export

## Implementation Notes
- Updated the PWA AAPS generator to output **numbering as comments** plus **indentation** for readability (no semantic changes):
  - `programToAapsScript()` now emits `# 1`, `# 1.N`, `# 1.N.1` comment lines and indents `STEP` by 2 spaces and `ACTION` by 4 spaces.
  - This keeps the script AAPS v1 compatible because numbering is display-only (`# ...`), and the backend parser ignores comment lines and tolerates indentation.
- Import tolerance for numeric prefixes (e.g. `1.2 STEP {...}`) is already handled by the backend AAPS parser (`backend/pipeline_parser.py`), so no UI changes were required for that part.

## Files Changed
- Updated: `pwa/app.js`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
python3 - <<'PY'
from pathlib import Path
s = Path("pwa/app.js").read_text("utf-8")
assert "# 1 Task" in s
assert "lines.push(`# 1.${stepNo} Step`)" in s
assert "lines.push(`# 1.${stepNo}.1 Action`)" in s
print("OK")
PY
```

