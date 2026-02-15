# Plan: 016 pwa_chat_inbox_ui

## Goal
Add an “Inbox” UI in the PWA that:
- Shows a list of recent inbox messages.
- Provides a compose box to send a new message.
- Posts the message to the backend and updates the list without a full page reload.

Acceptance:
- PWA shows inbox list and compose box.
- Sending a message posts to backend and appears in list without full page reload.
- Default PWA theme remains light.

## Current State (References)
- Backend supports inbox persistence:
  - `GET /api/inbox?limit=N` and `POST /api/inbox { "content": "..." }` in `backend/app.py` (`InboxHandler`).
  - Contract documented in `docs/api-contracts.md` (“Inbox Messages” section).
- PWA currently has a “Chat” tab with an existing list + compose box:
  - UI: `pwa/index.html` `#tab-chat` with `#chatlog`, `#chat-input`, `#chat-send`.
  - Logic: `pwa/app.js` `loadChat()` / `sendChat()` currently call `/api/chat`.
  - Periodic refresh: `boot()` calls `loadChat()` once and periodically refreshes when the tab is visible.
- PWA API calls should go through the client introduced in task 015:
  - `pwa/app.js` uses `api()` which delegates to `window.AutoAppDevApi.requestJson()`.

## Approach (Minimal / Incremental)
Repurpose the existing “Chat” tab as the “Inbox” tab by switching it from `/api/chat` to `/api/inbox` and updating the UI copy. Keep the existing DOM IDs and tab switching logic to minimize changes (no redesign, no new panel).

## Implementation Steps (Next Phase)
1. Update `pwa/index.html` (UI copy only).
   - Change the visible tab label text from `Chat` to `Inbox` (keep `data-tab="chat"` to avoid JS churn).
   - Update the compose placeholder to be explicitly “Inbox” oriented (ex: “Send a message to the pipeline inbox…”).
   - (Optional) Update the Status hintbox copy to say “Inbox” instead of “Chat” so the UI language is consistent.

2. Update `pwa/app.js` to use the inbox API.
   - Change `loadChat()` to fetch inbox messages:
     - `GET /api/inbox?limit=50` (keep existing rendering loop; response shape is the same `{ messages: [...] }`).
   - Change `sendChat()` to post to inbox:
     - `POST /api/inbox` with `body: JSON.stringify({ content })`.
     - After successful post, refresh the list (`await loadChat()` or rename to `loadInbox()`).
   - Ensure “appears in list without full page reload”:
     - Keep the existing re-render-in-place behavior (clear + re-add DOM nodes).
     - Optionally, optimistically append the message before the reload, but keep it minimal unless needed.

3. Optional small UX improvements (only if still minimal).
   - Display a short inline error message if the backend returns `{ error: "empty"|"too_long"|... }` instead of silently `console.warn`.
   - If added, place it inside `#tab-chat` under the compose row and style it using existing theme tokens in `pwa/styles.css`.

4. Keep the light theme default unchanged.
   - Do not modify `<body data-theme="light">` or theme tokens.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Confirm PWA now uses inbox endpoints
rg -n '/api/chat' pwa/app.js || true
rg -n '/api/inbox' pwa/app.js

# Confirm Inbox UI is present (label/placeholder)
rg -n 'data-tab=\"chat\"' pwa/index.html
rg -n '>Inbox<' pwa/index.html
rg -n 'chat-input' pwa/index.html

# Ensure default theme is still light
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

# JS syntax
node --check pwa/app.js
```

Manual browser verification (required to prove “posts + appears without reload”):
1. Start backend and PWA normally (outside this sandbox which cannot bind ports):
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/` -> `Inbox` tab.
3. Send a message; confirm:
   - Network request `POST /api/inbox` returns `{ "ok": true }`.
   - The message appears in the list without a full page reload.
4. Refresh the page and confirm the message persists (loaded from `GET /api/inbox?limit=50`).

## Acceptance Checklist
- [ ] Inbox list + compose box are visible in the PWA.
- [ ] Sending uses `POST /api/inbox` and the message appears in the list without a full page reload.
- [ ] Default theme remains light.

