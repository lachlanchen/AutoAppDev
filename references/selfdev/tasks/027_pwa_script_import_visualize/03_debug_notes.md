# Debug Notes: 027 pwa_script_import_visualize

Date: 2026-02-15

## Commands Run

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && rg -n 'data-tab="script"|id="tab-script"|id="script-text"|/api/scripts/parse|/api/scripts/import-shell' pwa/index.html pwa/app.js docs/end-to-end-demo-checklist.md
```

Output:
```text
pwa/index.html:97:          <button class="tab" data-tab="script">Script</button>
pwa/index.html:150:        <div class="tabview" id="tab-script" hidden>
pwa/index.html:173:            id="script-text"
pwa/app.js:285:    const res = await api("/api/scripts/parse", { method: "POST", body: JSON.stringify({ script_text }) });
pwa/app.js:306:    const res = await api("/api/scripts/import-shell", { method: "POST", body: JSON.stringify({ shell_text }) });
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s node --check pwa/app.js
```

Result: exit 0, no output.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s node --check pwa/service-worker.js && timeout 10s node --check pwa/api-client.js
```

Result: exit 0, no output.

## Notes / Limitations
- Full end-to-end verification (PWA in browser calling backend endpoints) requires running a local backend and a static server for `pwa/`. This sandbox environment cannot bind/listen on ports, so verification here is limited to static checks.

