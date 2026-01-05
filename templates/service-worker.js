/* ============================================================
   WishCraft – Production PWA Service Worker
   Safe updates • SEO-friendly • Offline support • Scalable
   ============================================================ */

const VERSION = 'wishcraft-2.0.0';

const STATIC_CACHE = `wishcraft-static-${VERSION}`;
const RUNTIME_CACHE = `wishcraft-runtime-${VERSION}`;

const PRECACHE_URLS = [
  '/',
  '/about',
  '/contact',
  '/privacy',
  '/blog',
  '/install',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then(cache => cache.addAll(PRECACHE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => !key.includes(VERSION))
          .map(key => caches.delete(key))
      )
    )
  );

  self.clients.claim();

  self.clients.matchAll().then(clients => {
    clients.forEach(client =>
      client.postMessage({ type: 'WISHCRAFT_UPDATED' })
    );
  });
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== 'GET' || url.origin !== location.origin) return;

  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request));
    return;
  }

  if (
    url.pathname.endsWith('.js') ||
    url.pathname.endsWith('.css')
  ) {
    event.respondWith(staleWhileRevalidate(request));
    return;
  }

  if (request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(networkFirst(request));
    return;
  }

  event.respondWith(cacheFirst(request));
});

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(RUNTIME_CACHE);
    cache.put(request, response.clone());
    return response;
  } catch {
    return (
      caches.match(request) ||
      new Response('Offline', { status: 503 })
    );
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(RUNTIME_CACHE);
  const cached = await cache.match(request);

  const networkFetch = fetch(request).then(response => {
    if (response && response.status === 200) {
      cache.put(request, response.clone());
    }
    return response;
  });

  return cached || networkFetch;
}

async function cacheFirst(request) {
  const cached = await caches.match(request);
  return cached || fetch(request);
}

console.log('WishCraft Service Worker loaded');
