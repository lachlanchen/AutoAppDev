# Debug Notes: 028 pwa_script_export_generate

Date: 2026-02-15

## Commands Run

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && rg -n "script-download-aaps|script-download-runner|Download AAPS|Download Runner" pwa/index.html pwa/app.js
```

Output:
```text
pwa/index.html:175:              id="script-download-aaps"
pwa/index.html:178:              Download AAPS
pwa/index.html:182:              id="script-download-runner"
pwa/index.html:185:              Download Runner
pwa/app.js:40:  scriptDownloadAaps: document.getElementById("script-download-aaps"),
pwa/app.js:41:  scriptDownloadRunner: document.getElementById("script-download-runner"),
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s node --check pwa/app.js
```

Result: exit 0, no output.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s node --check pwa/service-worker.js
```

Result: exit 0, no output.

Attempted (non-browser) runner generation smoke via `vm` (fails because `pwa/app.js` calls `boot()` and expects real DOM nodes):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s node - <<'NODE'
// Minimal smoke: ensure runner generation function exists and returns a bash script header.
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync('pwa/app.js', 'utf8');

// Very small DOM stub for the top-level `els = { document.getElementById(...) }`.
const noop = () => null;
const context = {
  console,
  window: {},
  document: {
    getElementById: noop,
    querySelectorAll: () => [],
    body: { dataset: {} },
    createElement: () => ({ setAttribute() {}, appendChild() {}, remove() {}, click() {} }),
  },
  navigator: {},
  localStorage: { getItem() { return null; }, setItem() {} },
  URL: { createObjectURL() { return 'blob:fake'; }, revokeObjectURL() {} },
  Blob: function () {},
  setTimeout() {},
};
vm.createContext(context);
vm.runInContext(code, context);

if (typeof context.generateRunnerScript !== 'function') {
  throw new Error('generateRunnerScript missing');
}
const script = context.generateRunnerScript([{ type: 'plan' }, { type: 'work' }], {
  title: 'Demo',
  aapsText: 'AUTOAPPDEV_PIPELINE 1\n',
});
if (!String(script).includes('#!/usr/bin/env bash')) throw new Error('missing shebang');
console.log('OK');
NODE
```

Output (abbrev):
```text
TypeError: Cannot read properties of null (reading 'querySelectorAll')
...
```

Follow-up static smoke (no DOM execution):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s node -e "const fs=require('fs'); const code=fs.readFileSync('pwa/app.js','utf8'); if(!code.includes('function generateRunnerScript')) throw new Error('missing generateRunnerScript'); if(!code.includes('#!/usr/bin/env bash')) throw new Error('missing shebang'); console.log('OK');"
```

Output:
```text
OK
```

## Notes / Limitations
- Full functional verification (downloads in browser) requires running a static server for `pwa/` and opening the PWA in a browser. This sandbox environment cannot bind/listen on ports, so verification here is limited to static checks.

