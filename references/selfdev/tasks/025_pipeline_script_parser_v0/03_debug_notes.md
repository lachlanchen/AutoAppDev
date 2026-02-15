# Debug Notes: 025 pipeline_script_parser_v0

Date: 2026-02-15

## Commands Run

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && test -f backend/pipeline_parser.py && echo 'pipeline_parser.py exists'
```

Output:
```text
pipeline_parser.py exists
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && rg -n "class ParseError|def parse_aaps_v1" backend/pipeline_parser.py
```

Output:
```text
10:class ParseError(Exception):
44:def parse_aaps_v1(text: str) -> dict[str, Any]:
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && rg -n "/api/scripts/parse" backend/app.py docs/api-contracts.md
```

Output:
```text
backend/app.py:787:            (r"/api/scripts/parse", ScriptsParseHandler),
docs/api-contracts.md:169:### POST /api/scripts/parse
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s python3 -m py_compile backend/app.py backend/pipeline_parser.py
```

Result: exit 0, no output.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path('examples/pipeline_formatted_script_v1.aaps').read_text('utf-8')
ir = parse_aaps_v1(text)
assert ir['kind'] == 'autoappdev_ir' and ir['version'] == 1
assert ir['tasks'] and ir['tasks'][0]['steps']
print('OK', len(ir['tasks']), 'tasks')
PY
```

Output:
```text
OK 1 tasks
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s python3 - <<'PY'
from backend.pipeline_parser import parse_aaps_v1, ParseError

try:
    parse_aaps_v1('TASK {"id":"t1","title":"X"}\n')
except ParseError as e:
    print('ERR', e.code, e.line)
    print(e.to_dict())
else:
    raise SystemExit('expected error')
PY
```

Output:
```text
ERR invalid_header 1
{'ok': False, 'error': 'invalid_header', 'line': 1, 'detail': 'expected header: AUTOAPPDEV_PIPELINE 1'}
```

## Notes

- Full HTTP verification of `POST /api/scripts/parse` requires running the backend server; this sandbox environment cannot bind/listen on ports, so verification here is limited to static checks and direct function smoke tests.

