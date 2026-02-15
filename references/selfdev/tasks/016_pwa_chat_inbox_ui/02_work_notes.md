# Work Notes: 016 pwa_chat_inbox_ui

## Summary of Changes
- Repurposed the existing PWA “Chat” tab into an “Inbox” UI (minimal change):
  - `pwa/index.html` changes the tab label text to `Inbox` and updates the hint/placeholder copy.
  - `pwa/app.js` switches message list + send actions from `/api/chat` to `/api/inbox`.
- Updated docs to match the new behavior:
  - `docs/api-contracts.md` now states the current PWA uses `/api/inbox` (not `/api/chat`).

This keeps the existing layout/IDs and updates the message list in-place after sending (no full page reload).

## Files Changed
- Updated: `pwa/index.html`
- Updated: `pwa/app.js`
- Updated: `docs/api-contracts.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n "Chat" pwa/index.html
rg -n '/api/chat' pwa/app.js || true
rg -n '/api/inbox' pwa/app.js
rg -n '>Inbox<' pwa/index.html
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html
timeout 5s node --check pwa/app.js
```

