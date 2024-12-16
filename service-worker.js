// Define the cache name and assets
const CACHE_NAME = "sanctum-cache-v2"; // Increment this version for updates
const ASSETS = [
  "/",
  "/manifest.json",
  "lib/resources/images/icon-192.png?v=2",
  "lib/resources/images/icon-512.png?v=2",
  "lib/resources/images/favicon.ico", // Add favicon explicitly to the cache
  "/styles.css",
  "/script.js",
];

// Install event: Cache assets
self.addEventListener("install", (event) => {
  console.log("Service Worker: Installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Service Worker: Caching assets");
      return cache.addAll(ASSETS);
    })
  );
});

// Activate event: Clean up old caches
self.addEventListener("activate", (event) => {
  console.log("Service Worker: Activating...");
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log("Service Worker: Removing old cache", cache);
            return caches.delete(cache);
          }
        })
      )
    )
  );
  return self.clients.claim(); // Take control immediately
});

// Fetch event: Serve cached assets or fall back to the network
self.addEventListener("fetch", (event) => {
  // Redirect /favicon.ico requests to the correct path
  if (event.request.url.endsWith("/favicon.ico")) {
    console.log("Service Worker: Redirecting favicon.ico request");
    event.respondWith(fetch("lib/resources/images/favicon.ico"));
    return;
  }

  // Default fetch handling
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse; // Serve from cache
      }
      console.log("Service Worker: Fetching from network", event.request.url);
      return fetch(event.request); // Fetch from network if not cached
    })
  );
});
