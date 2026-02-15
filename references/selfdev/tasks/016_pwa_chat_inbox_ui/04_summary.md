# Summary: 016 pwa_chat_inbox_ui

## What Changed
- Repurposed the existing PWA “Chat” tab into an “Inbox” UI:
  - `pwa/app.js` now uses `GET /api/inbox?limit=50` for the message list and `POST /api/inbox` for sending.
  - `pwa/index.html` updates the tab label and copy to say “Inbox” and adjusts the compose placeholder.
- Updated docs to match:
  - `docs/api-contracts.md` now notes the current PWA uses `/api/inbox` (and `/api/chat` is older).

## Why
To meet the requirement that the PWA show an inbox list + compose box, and that sending a message posts to the backend and appears in the list without a full page reload.

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n '/api/(chat|inbox)' pwa/app.js
rg -n '>Inbox<' pwa/index.html
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html
node --check pwa/app.js
```

Manual UI check (outside this sandbox, which cannot bind ports):
1. Start backend and PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/` -> `Inbox` tab.
3. Send a message and confirm it appears in the list without a full page reload (`POST /api/inbox` then in-place list refresh).

