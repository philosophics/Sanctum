const CACHE_NAME = "sanctum-cache-v7";
const ASSETS = [
  "/",
  "/manifest.json",
  "/lib/resources/images/icon-192.png?v=2",
  "/lib/resources/images/icon-512.png?v=2",
  "/lib/resources/images/favicon.ico",
  "/assets/styles.css",
  "/assets/script.js",
];

const DEBUG = false;

self.addEventListener("install", (event) => {
  if (DEBUG) console.log("Service Worker: Installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      if (DEBUG) console.log("Service Worker: Caching assets");
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener("activate", (event) => {
  if (DEBUG) console.log("Service Worker: Activating...");
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            if (DEBUG) console.log("Service Worker: Removing old cache", cache);
            return caches.delete(cache);
          }
        })
      )
    )
  );
  return self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.url.startsWith("https://cdnjs.cloudflare.com/")) {
    if (DEBUG) console.log("Service Worker: Skipping Font Awesome fetch:", event.request.url);
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        if (DEBUG) console.log("Service Worker: Serving from cache:", event.request.url);
        return cachedResponse;
      }
      if (DEBUG) console.log("Service Worker: Fetching from network:", event.request.url);
      return fetch(event.request);
    })
  );
});
