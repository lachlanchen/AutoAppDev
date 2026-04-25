/* Dev-friendly PWA shell cache.
   Normal refresh should fetch fresh shell assets. Cache is only an offline fallback.
*/

const CACHE_NAME = "autoappdev-shell-v14";
const PRECACHE_URLS = [
  "./index.html",
  "./styles.css",
  "./api-client.js",
  "./i18n.js",
  "./app.js",
  "./favicon.svg",
  "./manifest.json",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.map((k) => (k === CACHE_NAME ? null : caches.delete(k)))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("message", (event) => {
  const data = event.data || {};
  if (data && data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

async function cacheFreshResponse(req, fallbackUrl) {
  const cache = await caches.open(CACHE_NAME);
  try {
    const res = await fetch(req, { cache: "no-store" });
    if (res && res.ok) {
      cache.put(req, res.clone()).catch(() => {});
    }
    return res;
  } catch (e) {
    return (
      (await caches.match(req, { ignoreSearch: true })) ||
      (fallbackUrl ? await caches.match(fallbackUrl, { ignoreSearch: true }) : undefined) ||
      Response.error()
    );
  }
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Only handle same-origin requests.
  if (url.origin !== self.location.origin) {
    return;
  }

  // Network-first for navigations. Cache is only the offline fallback.
  if (req.mode === "navigate") {
    event.respondWith(cacheFreshResponse(req, "./index.html"));
    return;
  }

  // Network-first for known shell assets so normal refresh sees current code.
  const isPrecached = PRECACHE_URLS.some((p) => url.pathname.endsWith(p.replace("./", "")));
  if (isPrecached) {
    event.respondWith(cacheFreshResponse(req));
    return;
  }

  // Default: network.
});
