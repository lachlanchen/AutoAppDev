/* Minimal shell caching for local dev.
   NOTE: `python -m http.server` does not set all PWA-friendly headers; this is still
   useful for quick offline reloads in modern browsers.
*/

const CACHE_NAME = "autoappdev-shell-v1";
const PRECACHE_URLS = [
  "./index.html",
  "./styles.css",
  "./api-client.js",
  "./app.js",
  "./favicon.svg",
  "./manifest.json",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.map((k) => (k === CACHE_NAME ? null : caches.delete(k))))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Only handle same-origin requests.
  if (url.origin !== self.location.origin) return;

  // For navigations, serve cached shell when offline.
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req).catch(() => caches.match("./index.html", { ignoreSearch: true }))
    );
    return;
  }

  // Cache-first for known shell assets.
  const isPrecached = PRECACHE_URLS.some((p) => url.pathname.endsWith(p.replace("./", "")));
  if (isPrecached) {
    event.respondWith(
      caches.match(req, { ignoreSearch: true }).then((hit) => hit || fetch(req))
    );
    return;
  }

  // Default: network.
});
