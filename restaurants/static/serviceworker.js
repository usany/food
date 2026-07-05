// Cache name (update version to bust cache)
const CACHE_NAME = "django-pwa-cache-v1";
 
// Assets to cache on service worker install
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        "/",
        "/static/css/style.css",
        "/static/js/main.js",
        "/static/images/icon-192x192.png",
        "/static/images/icon-512x512.png",
        // Add other critical assets
      ]);
    })
  );
});
 
// Fetch strategy: Serve cached assets first, fall back to network
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
 
// Clean up old caches (when service worker is activated)
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.filter((name) => name !== CACHE_NAME).map((name) => caches.delete(name))
      );
    })
  );
});
