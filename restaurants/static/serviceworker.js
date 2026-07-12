const CACHE_NAME = "khukie-pwa-v2";

const ASSETS = [
  "/ko/se/",
  "/en/se/",
  "/ko/gl/",
  "/en/gl/",
  "/static/manifest.json",
  "/static/styles.css",
  "/static/nav.css",
  "/static/home.css",
  "/static/base.css",
  "/static/icon-192x192.png",
  "/static/icon-512x512.png",
];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request).catch(() => caches.match("/ko/se/"))
    );
  } else {
    event.respondWith(
      caches.match(event.request).then((cached) => cached || fetch(event.request))
        .catch(() => caches.match("/ko/se/"))
    );
  }
});
