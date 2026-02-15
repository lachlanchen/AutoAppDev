# Plan: 017 scratch_like_block_palette

## Goal
Ensure the PWA has a Scratch-like minimal block palette and workspace:
- Palette shows 3-6 draggable blocks.
- Blocks can be dragged into the workspace canvas.
- Workspace can be serialized to JSON.

Acceptance:
- PWA renders a minimal block palette (3-6 blocks).
- Supports dragging blocks into a workspace.
- Workspace serializes to JSON.
- Default theme remains light.

## Current State (References)
- Block palette + workspace already exist in `pwa/index.html`:
  - Palette container: `#toolbox` (`.panel--toolbox`).
  - Current palette includes 8 blocks (`Plan`, `Work`, `Debug`, `Fix`, `Summary`, `Commit+Push`, `While`, `Wait Input`) which exceeds the acceptance target.
  - Workspace canvas: `#canvas` with empty-state copy and “Export JSON” button (`#btn-export`).
- Drag and drop + serialization already exist in `pwa/app.js`:
  - Palette metadata: `BLOCK_META`.
  - DnD: `bindDnD()` uses `.toolbox .block` `dragstart` + `#canvas` `drop`.
  - Workspace persistence: `persistProgram()` / `loadProgram()` using `localStorage`.
  - JSON export: `#btn-export` shows `JSON.stringify({ program }, ...)` into `#export`.

## Approach (Minimal / Incremental)
Keep the existing DnD and serialization code, and only trim the visible block palette down to 6 blocks to meet the acceptance criteria.

Recommended visible blocks (6):
- `plan`, `work`, `debug`, `fix`, `summary`, `commit_push`

Defer advanced control blocks for later tasks:
- Remove `while_loop` and `wait_input` from the palette UI for now.

## Implementation Steps (Next Phase)
1. Trim palette to 6 blocks in `pwa/index.html`.
   - In the `#toolbox` section, remove:
     - the divider
     - `While` (`data-block="while_loop"`)
     - `Wait Input` (`data-block="wait_input"`)
   - Keep the remaining 6 blocks and their `data-block` values unchanged.

2. Align metadata in `pwa/app.js` (optional but recommended for clarity).
   - Update `BLOCK_META` to match the 6 visible palette blocks.
   - Ensure `renderProgram()` still renders any previously persisted blocks safely (fallback meta already exists).

3. No functional changes expected to DnD/serialization.
   - `bindDnD()` / `persistProgram()` / export behavior should remain unchanged.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Count palette blocks (should be 3-6; target 6)
rg -n 'data-block=\"' pwa/index.html | wc -l

# Ensure DnD hooks exist
rg -n 'function bindDnD\\(|dragstart|addEventListener\\(\"drop\"' pwa/app.js

# Ensure serialization/export exists
rg -n 'persistProgram\\(|loadProgram\\(|btn-export|Export JSON' pwa/app.js pwa/index.html

# Ensure default theme is still light
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

# JS syntax
node --check pwa/app.js
```

Manual UI verification (outside this sandbox, which cannot bind ports):
1. Serve the PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`.
3. Confirm the palette shows 6 blocks.
4. Drag 2-3 blocks into the canvas; confirm the program list renders.
5. Click “Export JSON”; confirm a JSON payload appears and includes the expected `program` array.
6. Reload; confirm the program persists (loaded from `localStorage`).

## Acceptance Checklist
- [ ] Palette shows 3-6 blocks (target 6).
- [ ] Dragging blocks into canvas adds them to the workspace list.
- [ ] “Export JSON” outputs the workspace JSON.
- [ ] Default theme remains light.

