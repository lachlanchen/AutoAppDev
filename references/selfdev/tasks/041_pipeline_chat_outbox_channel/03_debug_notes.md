# Debug Notes: 041 pipeline_chat_outbox_channel

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python -m py_compile backend/app.py backend/storage.py
OK: py_compile

timeout 10s node --check pwa/app.js
OK: node --check pwa/app.js
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s rg -n "/api/outbox|outbox_messages|runtime/outbox" backend/app.py backend/storage.py backend/schema.sql pwa/app.js docs/api-contracts.md docs/workspace-layout.md | head -n 120
```

Result (excerpt):
```text
backend/app.py:1390:            (r"/api/outbox", OutboxHandler, {"storage": storage}),
backend/storage.py:613:                    "insert into outbox_messages(role, content) values($1, $2)",
pwa/app.js:1408:      api("/api/outbox?limit=80").catch(() => ({ messages: [] })),
docs/api-contracts.md:484:- `/api/outbox` is the first-class outbox persistence API.
docs/api-contracts.md:536:### File Queue: runtime/outbox/
backend/schema.sql:23:create table if not exists outbox_messages (
docs/workspace-layout.md:43:- `runtime/outbox/` for a file-based outbox queue ...
```

Smoke test: runtime/outbox file ingestion (no DB; uses `runtime/state.json` fallback in `Storage`):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python - <<'PY'
import asyncio
import json
from pathlib import Path
import tempfile

from backend.storage import Storage
from backend.app import _ingest_outbox_files

async def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        runtime_dir = Path(td)
        storage = Storage(database_url="", runtime_dir=runtime_dir)
        await storage.start()

        outbox = runtime_dir / "outbox"
        outbox.mkdir(parents=True, exist_ok=True)

        (outbox / "1730000000000_pipeline.md").write_text("hello from file pipeline\n", "utf-8")
        (outbox / "1730000000001_system.txt").write_text("hello from file system\n", "utf-8")

        await _ingest_outbox_files(storage=storage, runtime_dir=runtime_dir, max_files=50)

        msgs = await storage.list_outbox_messages(limit=10)
        print(json.dumps(msgs, ensure_ascii=False, indent=2))

asyncio.run(main())
PY
```

Result:
```json
[
  { "role": "pipeline", "content": "hello from file pipeline" },
  { "role": "system", "content": "hello from file system" }
]
```

## Issue Found + Fix
- Issue: outbox file role inference incorrectly defaulted to `pipeline` for filenames like `*_system.txt`.
- Cause: regex in `backend/app.py:_infer_outbox_role_from_name` used `r"...\\."` (expected a backslash before the extension), so filenames didn’t match the expected `<ts>_<role>.ext` pattern.
- Fix: changed it to `r"...\."` so the dot before the extension is matched and the role is extracted correctly.
  - File: `backend/app.py`
