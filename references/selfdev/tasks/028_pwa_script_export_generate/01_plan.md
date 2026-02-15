# Plan: 028 pwa_script_export_generate

## Goal
Enable PWA users to export the current canvas program (blocks) as:
1. A standardized formatted pipeline script (AAPS v1, `.aaps`)
2. A generated runnable shell runner (`.sh`)

Both outputs must be downloadable as files from the PWA.

Acceptance:
- PWA can export current blocks/IR as AAPS v1 and a runnable shell driver.
- Both outputs download as files.

## Current State (References)
- Script import/visualize UI exists:
  - `pwa/index.html`: `#tab-script`, `#script-text`, `#script-msg`
  - `pwa/app.js`: `parseAapsToBlocks()` calls `POST /api/scripts/parse`
  - `pwa/app.js`: `importShellToBlocks()` calls `POST /api/scripts/import-shell`
  - `pwa/app.js`: `fillScriptFromBlocks()` uses `programToAapsScript(program, title)`
- Blocks model is step-only:
  - `pwa/app.js`: `program` is an array of `{ type: "<block>" }`
  - `pwa/app.js`: `BLOCK_META` provides labels; `programToAapsScript()` generates AAPS v1 with `TASK/STEP/ACTION` lines (noop actions)
- Pipeline pause/resume uses a runtime flag file:
  - `backend/app.py`: `runtime/PAUSE` is created/removed by pause/resume
  - `scripts/pipeline_demo.sh`: safe reference implementation of pause + traps
- PWA service worker caches shell assets:
  - `pwa/service-worker.js`: `CACHE_NAME = autoappdev-shell-v7`

## Approach (Minimal / Incremental)
Implement export entirely client-side in the PWA Script tab:
- Add two buttons:
  - `Download AAPS` (download a generated `.aaps`)
  - `Download Runner` (download a generated `.sh`)
- Generation sources:
  - AAPS: use existing `programToAapsScript(program, title)` so it is always valid AAPS v1.
  - Runner: generate a safe bash script that:
    - Prints each step (derived from blocks) to stdout (goes to `runtime/logs/pipeline.log` when run via backend).
    - Respects pause via `${AUTOAPPDEV_RUNTIME_DIR:-...}/PAUSE` (same as backend pause/resume).
    - Traps `INT`/`TERM` and exits cleanly.
    - Optionally embeds the generated AAPS as `# AAPS:` lines at the top so it can be re-imported via `/api/scripts/import-shell`.

No backend changes are required for acceptance.

## Implementation Steps (Next Phase: WORK)
1. Update Script tab UI
  - `pwa/index.html`:
    - Add two buttons inside `.scriptbar` in `#tab-script`:
      - `#script-download-aaps` (label: `Download AAPS`)
      - `#script-download-runner` (label: `Download Runner`)
    - Keep existing parse/import/from-blocks actions unchanged.

2. Add minimal styling (if needed)
  - `pwa/styles.css`:
    - Likely no new CSS required since `.scriptbar` is flex-wrap and uses `.btn`.
    - Only add styles if layout becomes cramped on mobile (keep changes minimal).

3. Wire download actions + generation in `pwa/app.js`
  - Extend `els` with:
    - `scriptDownloadAaps`, `scriptDownloadRunner`
  - Add helper:
    - `downloadTextFile({ filename, content, mime })` using `Blob` + `URL.createObjectURL` + a temporary `<a download>`.
    - `sanitizeFileBase(name)` to produce a safe filename base (letters/digits/`-_`).
  - Implement:
    - `exportAapsFile()`:
      - If `program` is empty, show `setScriptMsg("no blocks on canvas", {error:true})`.
      - Prompt for a title/base name (default `program`).
      - Generate `aaps = programToAapsScript(program, title)` and write to textarea (`#script-text`) for transparency.
      - Download as `${base}.aaps` with `text/plain`.
    - `generateRunnerScript(program, { title, aapsText })`:
      - Produce a bash script string:
        - Shebang, `set -euo pipefail`
        - `RUNTIME_DIR="${AUTOAPPDEV_RUNTIME_DIR:-...}"`, `PAUSE_FLAG="$RUNTIME_DIR/PAUSE"`
        - `trap` cleanup on `INT TERM`
        - Function `pause_if_needed()` that loops while `$PAUSE_FLAG` exists
        - Print start metadata + timestamp
        - Embed AAPS as `# AAPS: ...` lines (header + statements) so it round-trips through task 026 importer
        - For each block in order:
          - Print `[autoappdev] step N <block>`
          - Call `pause_if_needed`
          - Default “work” is a safe placeholder: `echo` + short `sleep 1`
        - Print done
      - Keep it safe: no git, no codex, no external network calls.
    - `exportRunnerFile()`:
      - Require non-empty `program`
      - Reuse same `base` and `title` prompts
      - Use latest generated AAPS text (from `programToAapsScript`) for embedding
      - Download as `${base}.sh` with `text/x-shellscript` (or `text/plain`)
      - In Script msg, include reminder: `chmod +x <file> && ./<file>` (runner is still runnable via `bash <file>` without chmod)
  - Update `bindControls()` to attach click handlers for the new buttons.

4. Bump service worker cache name
  - `pwa/service-worker.js`:
    - Increment `CACHE_NAME` (e.g. `autoappdev-shell-v8`) so browser refresh picks up new UI/JS.

5. Update manual demo docs (optional but small)
  - `docs/end-to-end-demo-checklist.md`:
    - Add a short optional step under Script tab section to click `Download AAPS` / `Download Runner` and verify downloads.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n \"script-download-aaps|script-download-runner|Download AAPS|Download Runner\" pwa/index.html pwa/app.js
rg -n \"downloadTextFile\\(|generateRunnerScript\\(\" pwa/app.js
timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/service-worker.js
```

Manual browser verification (outside this sandbox; requires serving `pwa/`):
1. Open PWA, add a few blocks to the canvas.
2. Go to **Script** tab.
3. Click `Download AAPS`:
  - Expect: a `.aaps` file downloads; opening it shows `AUTOAPPDEV_PIPELINE 1` and `TASK/STEP/ACTION` lines.
4. Click `Download Runner`:
  - Expect: a `.sh` file downloads; opening it shows `#!/usr/bin/env bash`, pause flag logic, and `# AAPS:` embedded lines.
5. Optional run:
  - `bash <downloaded>.sh` prints step lines; creating/removing `runtime/PAUSE` pauses/resumes output.

## Acceptance Checklist
- [ ] PWA Script tab includes `Download AAPS` and `Download Runner`.
- [ ] `Download AAPS` produces a valid AAPS v1 file from the current blocks.
- [ ] `Download Runner` produces a runnable bash script that respects `runtime/PAUSE` and logs step progress.
- [ ] Both outputs download as files from the browser.

