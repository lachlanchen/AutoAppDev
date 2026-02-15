# Debug Notes: 014 pwa_shell_light_theme

## What I Verified (Smallest Possible)
Because this sandbox disallows creating/binding sockets, I could not serve `pwa/` over HTTP to do a real browser offline reload test. Verification here is limited to static checks (file presence, wiring, and JS syntax).

## Commands Run + Results

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
ls -la pwa
```

Result (exit 0):
```text
total 56
drwxrwxr-x 2 lachlan lachlan 4096 Feb 15 17:18 .
drwxrwxr-x 9 lachlan lachlan 4096 Feb 15 16:10 ..
-rw-rw-r-- 1 lachlan lachlan  275 Feb 15 17:18 README.md
-rw-rw-r-- 1 lachlan lachlan 8465 Feb 15 17:18 app.js
-rw-rw-r-- 1 lachlan lachlan  523 Feb 15 15:42 favicon.svg
-rw-rw-r-- 1 lachlan lachlan 5415 Feb 15 17:18 index.html
-rw-rw-r-- 1 lachlan lachlan  324 Feb 15 17:17 manifest.json
-rw-rw-r-- 1 lachlan lachlan 1533 Feb 15 17:18 service-worker.js
-rw-rw-r-- 1 lachlan lachlan 8814 Feb 15 15:42 styles.css
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
bash -lc 'test -s pwa/manifest.json && echo manifest_ok'
bash -lc 'test -s pwa/service-worker.js && echo sw_ok'
```

Result (exit 0):
```text
manifest_ok
sw_ok
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'rel="manifest"' pwa/index.html
rg -n 'theme-color' pwa/index.html
rg -n 'serviceWorker\\.register' pwa/app.js
rg -n '<body[^>]*data-theme="light"' pwa/index.html
```

Result (exit 0):
```text
8:    <link rel="manifest" href="manifest.json" />
9:    <meta name="theme-color" content="#2767ff" />
261:    navigator.serviceWorker.register("./service-worker.js").catch((e) => {
18:  <body data-theme="light">
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 5s node --version
timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Result (exit 0):
```text
v22.21.0
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 3s bash -lc 'cd pwa && python3 -m http.server 5173 --bind 127.0.0.1'
```

Result (exit 1; sandbox restriction prevents sockets):
```text
Traceback (most recent call last):
  File "/home/lachlan/miniconda3/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/home/lachlan/miniconda3/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/home/lachlan/miniconda3/lib/python3.10/http/server.py", line 1307, in <module>
    test(
  File "/home/lachlan/miniconda3/lib/python3.10/http/server.py", line 1258, in test
    with ServerClass(addr, HandlerClass) as httpd:
  File "/home/lachlan/miniconda3/lib/python3.10/socketserver.py", line 448, in __init__
    self.socket = socket.socket(self.address_family,
  File "/home/lachlan/miniconda3/lib/python3.10/socket.py", line 232, in __init__
    _socket.socket.__init__(self, family, type, proto, fileno)
PermissionError: [Errno 1] Operation not permitted
```

## Issue Found + Minimal Fix
- Issue: `pwa/service-worker.js` originally had `"./"` in `PRECACHE_URLS`, and the `endsWith()` match logic made `isPrecached` true for all same-origin requests (because any string endsWith `""`).
- Fix: removed `"./"` from `PRECACHE_URLS` so `isPrecached` only matches the intended shell assets.

## Manual Verification (Outside This Sandbox)
1. `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/` in a browser.
3. DevTools: Application -> Service Workers: confirm it installs.
4. DevTools Network: toggle Offline, reload.
5. Expect: the shell (top bar + panels) still loads offline (API calls may fail, but UI shell should render).

