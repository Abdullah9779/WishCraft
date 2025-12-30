const CACHE_NAME = "wishcraft-v10";

// Only cache real static files (HTML pages optional)
const ASSETS = [
  "/",
  "/my-templates",
  "/about",
  "/contact",
  "/privacy",
  "/blog",
  "/install"
];

// Only allow http(s)
const isHttp = (req) =>
  req.url.startsWith("http://") || req.url.startsWith("https://");

// INSTALL — Pre-cache assets
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// ACTIVATE — Clear old caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// FETCH — Network-first for HTML, Cache-first for everything else
self.addEventListener("fetch", (event) => {
  const req = event.request;

  if (!isHttp(req)) return; // Skip extension/websocket/etc

  // ✅ Network-first for page navigations
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then((res) => {
          caches.open(CACHE_NAME).then((cache) => cache.put(req, res.clone()));
          return res;
        })
        .catch(() => caches.match(req) || caches.match("/"))
    );
    return;
  }

  // ✅ Cache-first for static assets (CSS, JS, images)
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;

      return fetch(req)
        .then((res) => {
          if (res.status === 200 && isHttp(req)) {
            const clone = res.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          }
          return res;
        })
        .catch(() => cached); // last fallback
    })
  );
});
