# Plan: 027 pwa_script_import_visualize

## Goal
Add a **Script** panel to the PWA:
- User can paste/import a script.
- PWA calls backend parse/import endpoints.
- Parsed IR is rendered as blocks on the canvas.
- User can switch between editing raw script and viewing blocks (blocks are the canvas; script is the Script tab).

Acceptance:
- Script panel exists in PWA.
- Paste/import -> backend parse -> blocks rendered on canvas.
- User can switch between raw script and blocks view.

## Current State (References)
- PWA blocks canvas is backed by `program` (array of `{type}`):
  - `pwa/app.js`: `program`, `renderProgram()`, `persistProgram()`
- IR <-> blocks mapping is already implemented:
  - `pwa/app.js`: `irToProgram(ir)` reads `STEP.block` only (actions/titles are ignored in visualization)
  - `pwa/app.js`: `programToAapsScript(program)` generates an AAPS v1 script from blocks (lossy)
- Backend parsing/import endpoints exist:
  - `POST /api/scripts/parse` (AAPS v1 -> IR): `backend/app.py`, `backend/pipeline_parser.py`
  - `POST /api/scripts/import-shell` (shell annotations -> AAPS + IR): `backend/app.py`, `backend/pipeline_shell_import.py`
- Right panel uses tabs:
  - `pwa/index.html`: `Status`, `Inbox`, `Logs`
  - `pwa/app.js`: `bindTabs()` toggles `#tab-status`, `#tab-chat`, `#tab-logs`
  - `pwa/styles.css`: `.tabs { grid-template-columns: 1fr 1fr 1fr; }`
- Service worker caches shell assets:
  - `pwa/service-worker.js`: `CACHE_NAME = autoappdev-shell-v6`

## Approach (Minimal / Consistent)
Implement Script UI as a 4th right-panel tab (keeps layout stable):
- Script tab provides a textarea for raw script plus:
  - `Parse AAPS -> Blocks` (calls `/api/scripts/parse`)
  - Optional: `Import Shell -> Blocks` (calls `/api/scripts/import-shell`) to support `.sh` annotations from task 026
  - `From Blocks` (fills textarea using `programToAapsScript(program)` so the user can round-trip)
- On successful parse/import:
  - Convert IR to `program` using existing `irToProgram(ir)`
  - `persistProgram()` + `renderProgram()` updates the canvas
  - Show an inline message (ok/error) with line numbers on failures

Known limitation (document in UI hint text, not new docs unless required):
- Visualization is step-level only: `STEP.block` -> block; task/step titles and actions are not preserved in the block canvas.

## Implementation Steps (Next Phase: WORK)
1. **Add Script tab UI**
   - Update `pwa/index.html`:
     - Add a new tab button: `<button class="tab" data-tab="script">Script</button>`
     - Add `<div class="tabview" id="tab-script" hidden> ... </div>` containing:
       - `<textarea id="script-text">` for raw script text
       - `<input type="file" id="script-file" ...>` (accept `.aaps,.sh,.txt`)
       - Buttons:
         - `#script-parse` (AAPS parse)
         - `#script-import-shell` (shell import; optional but small)
         - `#script-from-blocks` (generate script from current blocks)
       - Inline status/error element: `#script-msg` with `aria-live="polite"`

2. **Style the Script tab**
   - Update `pwa/styles.css`:
     - Change `.tabs` to 4 columns (e.g. `grid-template-columns: repeat(4, 1fr);`)
     - Include `textarea` in the existing form styling rule (`select, input, textarea { ... }`)
     - Add minimal styles for the script controls:
       - `.scriptbar` grid for buttons + file picker
       - `.script-text` sizing: `min-height` and `resize: vertical`
       - `.script-msg` similar to `.ctrl-msg` (including `.is-error` and `:empty` hide)

3. **Wire tab switching + script actions**
   - Update `pwa/app.js`:
     - Extend `els` with:
       - `tabScript`, `scriptText`, `scriptFile`, `scriptParse`, `scriptImportShell`, `scriptFromBlocks`, `scriptMsg`
     - Update `bindTabs()` to handle `script`:
       - Show/hide `#tab-script` alongside existing `#tab-*` views
     - Add helpers:
       - `setScriptMsg(text, {error})`
       - `applyIrToCanvas(ir)`:
         - `const nextProgram = irToProgram(ir)`; set `program = nextProgram` if valid
         - `persistProgram(); renderProgram();`
       - `parseAaps()` calls:
         - `api("/api/scripts/parse", {method:"POST", body: JSON.stringify({script_text})})`
       - `importShell()` calls:
         - `api("/api/scripts/import-shell", {method:"POST", body: JSON.stringify({shell_text})})`
         - On success, also populate textarea with returned `script_text` (extracted AAPS) for transparency
     - Event wiring in `bindControls()`:
       - `#script-parse` click: parse textarea -> apply IR -> message
       - `#script-import-shell` click: import textarea -> apply IR -> message
       - `#script-from-blocks` click: fill textarea using `programToAapsScript(program, title)` (prompt for title optional)
       - `#script-file` change: read file into textarea; optionally auto-run:
         - If filename ends with `.sh`: call import-shell
         - Else: call parse

4. **Bump service worker cache**
   - Update `pwa/service-worker.js`:
     - `CACHE_NAME` from `autoappdev-shell-v6` -> `autoappdev-shell-v7` (or next)

5. (Optional) **Docs**
   - Only if needed for clarity: add a short optional step to `docs/end-to-end-demo-checklist.md` showing “Script tab: paste AAPS -> Parse -> blocks appear”.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n \"data-tab=\\\"script\\\"|tab-script|script-text|/api/scripts/parse|/api/scripts/import-shell\" pwa/index.html pwa/app.js
node --check pwa/app.js
```

Manual browser smoke (outside this sandbox; requires running backend + a static server for `pwa/`):
1. Start backend (as per `docs/end-to-end-demo-checklist.md`).
2. Serve PWA (`cd pwa && python3 -m http.server ...`).
3. In PWA:
   - Open **Script** tab.
   - Paste `examples/pipeline_formatted_script_v1.aaps` content into textarea.
   - Click `Parse AAPS -> Blocks`.
   - Expected: blocks appear on the canvas; script message shows success.
4. (If implemented) import shell:
   - Paste `examples/pipeline_shell_annotated_v0.sh` content.
   - Click `Import Shell -> Blocks`.
   - Expected: blocks appear; message shows success; textarea updates to extracted AAPS.
5. Error handling:
   - Remove/alter header line and re-parse.
   - Expected: message shows `error` + `line` number from backend.

## Acceptance Checklist
- [ ] Script tab exists in the PWA right panel and can be selected.
- [ ] Pasting a valid AAPS v1 script and clicking parse calls backend and renders blocks on the canvas.
- [ ] User can switch between raw script (Script tab textarea) and blocks view (canvas), and can round-trip using `From Blocks`.
- [ ] Invalid script shows actionable error (including line number) without breaking the UI.

