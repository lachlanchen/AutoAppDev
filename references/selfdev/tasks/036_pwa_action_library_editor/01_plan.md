# Plan: 036 pwa_action_library_editor

## Goal
Add a minimal “Action library editor” UI to the PWA so a user can **list/create/edit/delete** action definitions (prompt + command) via the backend action registry API **without reloading** the page.

Acceptance:
- PWA lists action definitions from the registry
- PWA can create a new action definition (prompt or command)
- PWA can edit an existing action definition (title, enabled, spec fields) and persist via backend without reload
- PWA can delete an action definition

## Current State (References)
- Backend action registry API (already implemented):
  - `GET /api/actions?limit=N` (metadata list; no `spec`)
  - `POST /api/actions` (create; returns full record including `spec`)
  - `GET /api/actions/<id>` (fetch full record including `spec`)
  - `PUT /api/actions/<id>` (partial update; **kind changes disallowed**)
  - `DELETE /api/actions/<id>`
  - Implemented in `backend/app.py` (`ActionsHandler`, `ActionHandler`)
  - Validation rules in `backend/action_registry.py`
- Action spec shapes/constraints:
  - `kind="prompt"`: `spec.prompt` required; optional `agent`, `model`, `reasoning` (`low|medium|high|xhigh`), `timeout_s` (clamped 5..300)
  - `kind="command"`: `spec.cmd` required; `shell` only `"bash"`; `cwd` must stay repo-relative; `timeout_s` clamped 1..3600
- PWA is static/vanilla:
  - UI markup: `pwa/index.html` (right panel tabs: Status/Inbox/Logs/Script)
  - UI logic: `pwa/app.js` (tabs, API wrapper `api()`, status/chat/logs/script tooling)
  - Styling: `pwa/styles.css` (tabs currently `grid-template-columns: repeat(4, 1fr)`)
  - API wrapper: `pwa/api-client.js` (`window.AutoAppDevApi.requestJson`)

## UI Design (Minimal v0)
Implement the editor as a new right-panel tab named **Actions**:
- Tab shows:
  1. A scrollable list of action definitions (id/title/kind/enabled).
  2. An editor form for the selected action (or “New action” mode).
  3. Buttons: `Refresh`, `New`, `Save`, `Delete`.
- No reload is needed: after create/update/delete, the list refreshes and selection updates in-place.

Notes / guardrails:
- Existing actions cannot change `kind` (backend rejects it); UI should disable kind changes for loaded actions and show a hint (“create a new action to change kind”).
- “Command/script reference” is represented as `kind="command"` + `spec.cmd` (e.g. `bash scripts/my_tool.sh` or `python3 tools/foo.py`). `spec.cwd` remains repo-relative (backend enforces).

## Implementation Steps (Next Phase: WORK)
### 1) Add Actions tab markup
Edit `pwa/index.html`:
- Add a new tab button in the right panel:
  - In `.tabs`: add `<button class="tab" data-tab="actions">Actions</button>` (place between Logs and Script or at the end).
- Add a new tab view container:
  - `<div class="tabview" id="tab-actions" hidden> ... </div>`
  - Inside it, add elements with stable IDs so `pwa/app.js` can bind:
    - Toolbar: `#actions-refresh`, `#actions-new`, `#actions-save`, `#actions-delete`
    - List container: `#actions-list` (clickable rows)
    - Editor fields:
      - `#action-id` (read-only display)
      - `#action-title` (input)
      - `#action-enabled` (checkbox)
      - `#action-kind` (select: `prompt|command`; enabled only in “New” mode)
      - Prompt fields section (shown when kind=prompt):
        - `#action-prompt` (textarea)
        - `#action-agent` (input, optional; omit on create if blank)
        - `#action-model` (input, optional; omit on create if blank)
        - `#action-reasoning` (select: `low|medium|high|xhigh`)
        - `#action-timeout` (number, optional; omit on create if blank)
      - Command fields section (shown when kind=command):
        - `#action-cmd` (textarea)
        - `#action-shell` (read-only display or disabled input; always `bash`)
        - `#action-cwd` (input; repo-relative)
        - `#action-timeout-cmd` (number, optional)
    - Message area: `#actions-msg` (`aria-live="polite"`)
    - Hint box describing constraints (kind immutability; command cwd/shell rules).

### 2) Minimal styling for the editor
Edit `pwa/styles.css`:
- Update `.tabs` to fit the new 5th tab:
  - Either change to `grid-template-columns: repeat(5, 1fr);` (smallest diff), or make it future-proof with `repeat(auto-fit, minmax(0, 1fr))`.
- Add small, theme-variable-based styles for the actions UI, reusing existing primitives:
  - `.actionbar` (like `.scriptbar`)
  - `.actionlist` (bordered, scrollable)
  - `.actionrow` + `.actionrow.is-selected` (selected highlight using `--blue` and existing stroke/panel colors)
  - `.actionform` / `.actiongrid` (compact two-column grid for small fields like enabled/kind/timeout)
  - `.actions-msg` (mirror `.script-msg` behavior)
Keep the default theme light (no change to `body data-theme="light"`).

### 3) Wire the Actions tab behavior
Edit `pwa/app.js`:
- Extend the `els` map to include new DOM references:
  - `tabActions`, toolbar buttons, `actionsList`, all editor inputs/sections, `actionsMsg`.
- Add local state:
  - `let actionsIndex = [];` (metadata from `GET /api/actions`)
  - `let selectedActionId = null;`
  - `let selectedAction = null;` (full action record from `GET /api/actions/<id>`)
  - `let actionsMode = "view" | "new";` (or boolean `isNew`)
- Add helper functions:
  - `setActionsMsg(text, { error } = {})` (same pattern as `setScriptMsg` / `setCtrlMsg`)
  - `formatApiError(e)` (use `e.data.error` / `e.data.detail` / `e.message`)
  - `renderActionsList()`:
    - Render rows from `actionsIndex` into `#actions-list`
    - Row click loads action (`loadAction(id)`)
  - `async refreshActionsList({ keepSelection } = {})`:
    - Call `api("/api/actions?limit=200")`
    - Update `actionsIndex`, re-render list
  - `async loadAction(id)`:
    - Call `api(\`/api/actions/${id}\`)`
    - Populate form fields and set `actionsMode="view"`
    - Disable kind select when editing an existing action
  - `enterNewActionMode()`:
    - Clear form and set defaults (kind=`prompt`, reasoning=`medium`, shell=`bash`, enabled=true)
    - Enable kind select
  - `buildSpecFromForm(kind)`:
    - For `prompt`: build `{ prompt, agent?, model?, reasoning, timeout_s? }`
    - For `command`: build `{ cmd, shell:"bash", cwd?, timeout_s? }`
    - On create: omit optional fields when blank so backend defaults apply
  - `async saveActionFromForm()`:
    - If `actionsMode==="new"`: `POST /api/actions` with `{title, kind, enabled, spec}`
    - Else: `PUT /api/actions/<id>` with `{title, enabled, spec}` (no kind)
    - On success: refresh list and reselect saved action (no reload)
  - `async deleteSelectedAction()`:
    - Confirm; call `DELETE /api/actions/<id>`; refresh list; clear selection/form
- Update tab switching (`bindTabs()`):
  - Add `els.tabActions.hidden = key !== "actions"`
  - When switching to `actions`:
    - Call `refreshActionsList()` once (or every time) and keep selection if possible.
- Bind controls (`bindControls()`):
  - Hook toolbar buttons and kind select change (toggle prompt/command section visibility).

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Static check: JS syntax
timeout 10s node --check pwa/app.js

# Ensure new tab + wiring exists
timeout 10s rg -n \"data-tab=\\\"actions\\\"|tab-actions|/api/actions\" pwa/index.html pwa/app.js pwa/styles.css
```

Manual smoke (one-time, interactive):
1. Start backend (requires Postgres + `DATABASE_URL`):
   - `python3 -m backend.app`
2. Open `pwa/index.html` (or serve via any static server) and verify in the **Actions** tab:
   - Create prompt action; verify it appears immediately in list without page reload.
   - Edit the action; save; verify list updates (title/enabled).
   - Create command action with `cmd="bash scripts/pipeline_demo.sh"` and `cwd="."`; save; verify.
   - Delete an action; verify it disappears immediately without page reload.

## Acceptance Checklist
- [ ] “Actions” tab is visible and styled consistently in light theme.
- [ ] List loads from `GET /api/actions` and renders rows.
- [ ] Create prompt action (title + prompt) succeeds and shows in list without reload.
- [ ] Create command action (title + cmd) succeeds and shows in list without reload.
- [ ] Editing an action (title/enabled/spec fields) persists via `PUT /api/actions/<id>` without reload.
- [ ] Delete persists via `DELETE /api/actions/<id>` without reload.
- [ ] Kind change is not offered for existing actions (or clearly rejected with an inline error message).
- [ ] Backend validation errors (e.g. `invalid_prompt`, `invalid_cwd`, `invalid_shell`) surface in `#actions-msg`.

