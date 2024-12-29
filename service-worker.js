// Define the cache name and assets
const CACHE_NAME = "sanctum-cache-v3"; // Increment this version for updates
const ASSETS = [
  "/", // Root
  "/manifest.json",
  "/lib/resources/images/icon-192.png?v=2",
  "/lib/resources/images/icon-512.png?v=2",
  "/lib/resources/images/favicon.ico",
  "/styles.css",
  "/script.js",
];

const DEBUG = false; // Set to true to enable console logs for debugging

// Install event: Cache assets
self.addEventListener("install", (event) => {
  if (DEBUG) console.log("Service Worker: Installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      if (DEBUG) console.log("Service Worker: Caching assets");
      return cache.addAll(ASSETS);
    })
  );
});

// Activate event: Clean up old caches
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
  return self.clients.claim(); // Take control immediately
});

// Fetch event: Serve cached assets or let browser fetch uncached resources
self.addEventListener("fetch", (event) => {
  // Exclude Font Awesome CDN resources from Service Worker handling
  if (event.request.url.startsWith("https://cdnjs.cloudflare.com/")) {
    if (DEBUG)
      console.log(
        "Service Worker: Skipping Font Awesome fetch:",
        event.request.url
      );
    return; // Allow the browser to handle these requests directly
  }

  // Default fetch handling
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        if (DEBUG)
          console.log("Service Worker: Serving from cache:", event.request.url);
        return cachedResponse; // Serve from cache
      }
      if (DEBUG)
        console.log(
          "Service Worker: Fetching from network:",
          event.request.url
        );
      return fetch(event.request); // Fetch from network if not cached
    })
  );
});
