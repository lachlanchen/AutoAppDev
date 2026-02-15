# Plan: 039 pwa_workspace_context_settings

## Goal
Add a minimal PWA UI to manage **workspace-scoped settings** backed by the new backend workspace config API:
- Select a workspace (slug)
- Set materials path(s)
- Edit shared context
- Choose default language

Acceptance:
- Settings persist via backend (`/api/workspaces/<workspace>/config`)
- Selected workspace persists across reload (localStorage)
- Generated IR/AAPS scripts include workspace + config metadata so later prompt/script generation can use it

## Current State (References)
- Backend workspace config API (task 038):
  - Route: `GET /api/workspaces/<workspace>/config`
  - Route: `POST /api/workspaces/<workspace>/config`
  - Implemented in `backend/app.py` (`WorkspaceConfigHandler`) and `backend/workspace_config.py`
  - Documented in `docs/api-contracts.md` under `## Workspaces`
- PWA structure:
  - UI markup: `pwa/index.html` (right panel tabs + `#tab-status`)
  - Logic: `pwa/app.js` (vanilla JS; `api()` wrapper; localStorage persistence for program/theme)
  - Styles: `pwa/styles.css` (already has generic form/button styles; uses light theme by default)
- Workspace slug validation exists in PWA:
  - `pwa/app.js:parseWorkspaceSlug()` (single path segment; no control chars; max len)

## UX Design (Minimal v0)
Add a “Workspace” section inside the existing **Status** tab (no new tab):
- Workspace slug input + `Load` + `Save` buttons
- Materials paths input (one per line or comma-separated)
- Default language select (allowed list)
- Shared context textarea (saved as `shared_context_text`)
- Optional shared context path input (saved as `shared_context_path`, validated by backend)
- Inline message area for errors/success

Persist behavior:
- Selected workspace slug: localStorage key `autoappdev_workspace`
- Workspace config: persisted in backend; UI loads it on demand and on boot if workspace is set.

## Implementation Steps (Next Phase: WORK)
### 1) Add workspace settings UI to Status tab
Edit `pwa/index.html` under `#tab-status` (below the existing KV status rows):
- Add a divider and a small toolbar:
  - `#ws-slug` (input)
  - `#ws-load` (button)
  - `#ws-save` (button)
- Add fields:
  - `#ws-materials` (textarea or input; one path per line; workspace-relative)
  - `#ws-language` (select with: `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `vi`, `ar`, `fr`, `es`)
  - `#ws-context-text` (textarea; shared context text)
  - `#ws-context-path` (input; optional workspace-relative path like `docs/shared_context.md`)
- Add message element:
  - `#ws-msg` (use existing `.script-msg` styling for consistent inline errors)
- Add a hintbox describing constraints:
  - paths are workspace-relative, validated under `auto-apps/<workspace>/`
  - backend will reject traversal/out-of-workspace paths

### 2) Minimal styling (reuse existing primitives)
Edit `pwa/styles.css` only if necessary:
- Prefer reusing existing classes (`.scriptbar`, `.actiongrid`, `.action-text`, `.script-msg`, `.divider`, `.hintbox`).
- If needed, add a tiny `.ws-text` class (monospace textarea) or `.wsbar` (flex toolbar) mirroring `.scriptbar`.

### 3) Add workspace state + API wiring in PWA
Edit `pwa/app.js`:

1. Extend `els` with new DOM references:
   - `wsSlug`, `wsLoad`, `wsSave`, `wsMaterials`, `wsLanguage`, `wsContextText`, `wsContextPath`, `wsMsg`

2. Add local state:
   - `let workspaceSlug = ""`
   - `let workspaceConfig = null` (last loaded normalized config)

3. Helpers:
   - `setWsMsg(text, { error } = {})` (pattern matches `setScriptMsg` / `setActionsMsg`)
   - `loadWorkspaceSlugFromStorage()` / `saveWorkspaceSlugToStorage(slug)`
   - `parseMaterialsPaths(text)`:
     - split by newline and commas, trim, drop empties
     - default to `["materials"]` when empty
   - `fillWorkspaceForm(cfg)`:
     - populate UI fields from `cfg` (materials paths join with `\n`)
   - `buildWorkspacePayloadFromForm()`:
     - create body for POST:
       - `materials_paths` (array)
       - `default_language`
       - `shared_context_text`
       - `shared_context_path` (optional; send `""` to clear)

4. API calls:
   - `async loadWorkspaceConfig(slug)`:
     - validate via `parseWorkspaceSlug`
     - `api(\`/api/workspaces/${encodeURIComponent(slug)}/config\`)`
     - store `workspaceSlug`, `workspaceConfig`, fill form, persist slug in localStorage
   - `async saveWorkspaceConfig()`:
     - validate slug
     - POST to `/api/workspaces/<workspace>/config` with payload
     - update `workspaceConfig` with response config and show success message

5. Bind controls in `bindControls()`:
   - `#ws-load` click -> `loadWorkspaceConfig(els.wsSlug.value)`
   - `#ws-save` click -> `saveWorkspaceConfig()`
   - Optionally save-on-enter for slug input.

6. Boot integration:
   - On `boot()`, load saved workspace slug from localStorage; if present, call `loadWorkspaceConfig(slug)` once.

### 4) Use workspace settings when generating scripts (IR + AAPS)
Edit `pwa/app.js` generation functions:

- In `programToIr(prog, title)`:
  - When building the single task, include `task.meta` if a workspace is selected:
    - `meta: { workspace: "<slug>", workspace_config: <config object> }`
  - Only include this meta when `workspaceSlug` is non-empty (keep backwards compatibility when unset).

- In `programToAapsScript(prog, title)`:
  - Include the same metadata in the `TASK ...` JSON:
    - `TASK {"id":"t1","title":"...","meta":{...}}`
  - Again, only include when workspace is selected to avoid changing output for users not using the feature.

Optional small QoL (still minimal):
- Update the `update_readme` block drop prompt default value to the selected workspace slug (if set), so users don’t retype it.

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

# Confirm new UI ids + endpoint usage are present
timeout 10s rg -n \"ws-slug|ws-load|ws-save|ws-materials|ws-language|ws-context-text|ws-context-path|/api/workspaces\" pwa/index.html pwa/app.js
```

Manual smoke (requires backend running + Postgres + `DATABASE_URL`):
1. Open PWA -> Status tab.
2. Enter workspace slug (e.g. `my_workspace`) -> click `Load`:
   - should populate defaults from backend (`exists:false` case).
3. Edit:
   - materials paths (e.g. `materials` and `docs`)
   - default language (e.g. `fr`)
   - shared context text
   - click `Save` and confirm success message.
4. Click `From Blocks` / `Download AAPS`:
   - confirm the `TASK ...` line includes `meta.workspace` and `meta.workspace_config`.
5. Try an invalid path (e.g. materials path `../secrets`) and confirm the UI shows backend validation error.

## Acceptance Checklist
- [ ] Status tab includes workspace slug + config form with Load/Save.
- [ ] Selected workspace slug persists across reload (localStorage).
- [ ] Workspace config persists in backend via `/api/workspaces/<workspace>/config`.
- [ ] Generated IR and AAPS include workspace/config metadata when workspace selected; unchanged output when not selected.
- [ ] Invalid workspace/path/language inputs surface clear inline errors.

