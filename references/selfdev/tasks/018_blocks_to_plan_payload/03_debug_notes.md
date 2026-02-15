# Debug Notes: 018 blocks_to_plan_payload

## What I Verified (Smallest Possible)
This sandbox disallows binding sockets, so I could not run an end-to-end HTTP smoke test for `POST /api/plan`. Verification here is limited to:
- Backend route + handler existence and syntax
- PWA UI wiring (`Send Plan` button) + transformation function presence and syntax
- Docs updated with the new endpoint
- Service worker cache name bump present (helps manual verification outside sandbox)

## Commands Run + Results

Backend handler + route wiring:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'class PlanHandler|\\(r\"/api/plan\"|/api/plan' backend/app.py
```

Result (exit 0):
```text
184:class PlanHandler(BaseHandler):
621:            (r"/api/plan", PlanHandler, {"storage": storage}),
```

PWA UI wiring + endpoint usage:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'btn-send-plan|programToPlan\\(|/api/plan' pwa/index.html pwa/app.js
```

Result (exit 0):
```text
pwa/index.html:78:            <button class="btn btn--ghost" id="btn-send-plan">Send Plan</button>
pwa/app.js:15:  sendPlanBtn: document.getElementById("btn-send-plan"),
pwa/app.js:100:function programToPlan(prog) {
pwa/app.js:114:  const payload = programToPlan(program);
pwa/app.js:116:    const ack = await api("/api/plan", { method: "POST", body: JSON.stringify(payload) });
```

PWA plan transformation excerpt:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
sed -n '90,150p' pwa/app.js
```

Result (exit 0; excerpt):
```text
function programToPlan(prog) {
  const steps = (Array.isArray(prog) ? prog : []).map((b, idx) => ({
    id: idx + 1,
    block: String((b && b.type) || ""),
  }));
  return { kind: "autoappdev_plan", version: 1, steps };
}
```

Backend validation excerpt:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
sed -n '160,250p' backend/app.py
```

Result (exit 0; excerpt):
```text
class PlanHandler(BaseHandler):
    ...
    async def post(self) -> None:
        ...
        if body.get("kind") != "autoappdev_plan":
            self.write_json({"error": "invalid_kind"}, status=400)
            return
        if body.get("version") != 1:
            self.write_json({"error": "invalid_version"}, status=400)
            return
        ...
        await self.storage.set_config("pipeline_plan", body)
        self.write_json({"ok": True})
```

Docs updated:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n '## Plan Payload|GET /api/plan|POST /api/plan' docs/api-contracts.md
```

Result (exit 0):
```text
45:## Plan Payload
47:### GET /api/plan
64:### POST /api/plan
```

Service worker cache name bump (helps manual verification):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'CACHE_NAME|api-client\\.js|app\\.js|index\\.html' pwa/service-worker.js
```

Result (exit 0):
```text
6:const CACHE_NAME = "autoappdev-shell-v2";
8:  "./index.html",
10:  "./api-client.js",
11:  "./app.js",
46:      fetch(req).catch(() => caches.match("./index.html", { ignoreSearch: true }))
```

Syntax checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
timeout 5s node --check pwa/api-client.js
timeout 5s python3 -m py_compile backend/app.py
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
1. Start backend and PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`, drag blocks into the canvas.
3. Click “Send Plan” and confirm:
   - `POST /api/plan` returns `{ "ok": true }`.
   - The ack renders in the UI (in the export panel) without a page reload.
4. (Optional) `GET /api/plan` returns the stored payload.

