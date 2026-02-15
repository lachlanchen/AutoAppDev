# Debug Notes: 015 pwa_api_client_and_status

## What I Verified (Smallest Possible)
This sandbox disallows binding sockets, so I could not run a real browser/HTTP smoke test. Verification here is limited to:
- Static wiring checks (HTML/CSS/JS references)
- JS syntax checks
- Confirming the polling interval meets the 2s acceptance

## Commands Run + Results

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
bash -lc 'test -s pwa/api-client.js && echo api_client_ok && test -s pwa/index.html && echo index_ok && test -s pwa/app.js && echo app_ok && test -s pwa/styles.css && echo css_ok'
```

Result (exit 0):
```text
api_client_ok
index_ok
app_ok
css_ok
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'api-client\\.js' pwa/index.html
rg -n 'id="db-health"' pwa/index.html
rg -n 'badge--ok|badge--warn|badge--err' pwa/styles.css
rg -n 'AutoAppDevApi\\.requestJson|api_client_not_loaded' pwa/app.js
rg -n 'setInterval\\(refreshHealth, 2000\\)|setInterval\\(refreshStatus, 2000\\)' pwa/app.js
rg -n '<body[^>]*data-theme="light"' pwa/index.html
rg -n 'api-client\\.js' pwa/service-worker.js
```

Result (exit 0):
```text
16:    <script src="api-client.js" defer></script>
105:            <div class="v badge badge--unknown" id="db-health">unknown</div>
344:.badge--ok {
349:.badge--warn {
354:.badge--err {
93:  if (!window.AutoAppDevApi || typeof window.AutoAppDevApi.requestJson !== "function") {
94:    throw new Error("api_client_not_loaded");
96:  return await window.AutoAppDevApi.requestJson(path, opts);
299:  window.setInterval(refreshHealth, 2000);
300:  window.setInterval(refreshStatus, 2000);
19:  <body data-theme="light">
10:  "./api-client.js",
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s node --check pwa/api-client.js
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Result (exit 0): no output.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s python3 -m json.tool pwa/manifest.json > /tmp/autoappdev_manifest_checked.json && echo manifest_json_ok
```

Result (exit 0):
```text
manifest_json_ok
```

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
3. Confirm Status shows 3 badges (Backend, DB, Pipeline) and updates within ~2 seconds.
4. Confirm DB badge reflects the `/api/health` response (`db.ok` / `db.time` / `db.error`):
   - `ok` when Postgres is reachable
   - `error` (and tooltip) if DB check fails
