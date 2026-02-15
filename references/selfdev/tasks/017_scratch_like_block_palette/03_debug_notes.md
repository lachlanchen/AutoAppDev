# Debug Notes: 017 scratch_like_block_palette

## What I Verified (Smallest Possible)
This sandbox disallows binding sockets, so I could not run a real browser/HTTP smoke test. Verification here is limited to:
- Palette block count is now within acceptance (3-6)
- Drag/drop handlers still exist
- Workspace serialization/export hooks still exist
- JS syntax check passes

## Commands Run + Results

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'data-block=\"' pwa/index.html
```

Result (exit 0):
```text
63:          <div class="block block--plan" draggable="true" data-block="plan">Plan</div>
64:          <div class="block block--work" draggable="true" data-block="work">Work</div>
65:          <div class="block block--debug" draggable="true" data-block="debug">Debug</div>
66:          <div class="block block--fix" draggable="true" data-block="fix">Fix</div>
67:          <div class="block block--summary" draggable="true" data-block="summary">Summary</div>
68:          <div class="block block--release" draggable="true" data-block="commit_push">Commit+Push</div>
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'function bindDnD\\(|dragstart|addEventListener\\(\"drop\"' pwa/app.js
```

Result (exit 0):
```text
154:function bindDnD() {
156:    el.addEventListener("dragstart", (ev) => {
167:  els.canvas.addEventListener("drop", (ev) => {
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'btn-export|Export JSON|persistProgram\\(|loadProgram\\(' pwa/app.js pwa/index.html
```

Result (exit 0):
```text
pwa/index.html:77:            <button class="btn btn--ghost" id="btn-export">Export JSON</button>
pwa/app.js:14:  exportBtn: document.getElementById("btn-export"),
pwa/app.js:70:      persistProgram();
pwa/app.js:79:function persistProgram() {
pwa/app.js:83:function loadProgram() {
pwa/app.js:172:    persistProgram();
pwa/app.js:242:    persistProgram();
pwa/app.js:279:  loadProgram();
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s node --check pwa/app.js
```

Result (exit 0): no output.

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
1. `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`.
3. Confirm palette shows 6 blocks, dragging into the canvas adds blocks, and “Export JSON” shows the serialized program.

