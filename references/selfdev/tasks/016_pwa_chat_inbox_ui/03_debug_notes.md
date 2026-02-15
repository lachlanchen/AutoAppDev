# Debug Notes: 016 pwa_chat_inbox_ui

## What I Verified (Smallest Possible)
This sandbox disallows binding sockets, so I could not run a real HTTP/browser smoke test. Verification here is limited to:
- PWA wiring now targets `/api/inbox` (not `/api/chat`)
- UI copy reflects “Inbox” and the compose placeholder is updated
- Default theme remains light
- JS syntax check passes

## Commands Run + Results

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n '/api/(chat|inbox)' pwa/app.js
```

Result (exit 0):
```text
192:    const data = await api("/api/inbox?limit=50");
212:    await api("/api/inbox", { method: "POST", body: JSON.stringify({ content }) });
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n '>Chat<|>Inbox<' pwa/index.html
```

Result (exit 0):
```text
94:          <button class="tab" data-tab="chat">Inbox</button>
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'chat-input|placeholder=' pwa/index.html | head
```

Result (exit 0):
```text
123:            <input class="input" id="chat-input" placeholder="Send a message to the pipeline inbox..." />
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n '<body[^>]*data-theme="light"' pwa/index.html
```

Result (exit 0):
```text
19:  <body data-theme="light">
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s node --check pwa/app.js
```

Result (exit 0): no output.

Docs consistency check:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'current PWA uses' docs/api-contracts.md
```

Result (exit 0):
```text
49:- `/api/chat` is a simple chat log API (older UI); the current PWA uses `/api/inbox` for guidance messages.
```

Attempted local serving (blocked by sandbox socket restrictions):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 3s bash -lc 'cd pwa && python3 -m http.server 5173 --bind 127.0.0.1'
```

Result (exit 1):
```text
PermissionError: [Errno 1] Operation not permitted
```

## Manual Verification (Outside This Sandbox)
1. Start backend and PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/` -> `Inbox` tab.
3. Send a message and confirm it appears in the list without a full page reload.
   - Network: `POST /api/inbox` returns `{ "ok": true }`.
   - List refreshes in-place (via `loadChat()` re-render).

