// Service worker : met l'appli en cache pour qu'elle marche hors ligne.
// Change VERSION à chaque mise à jour pour forcer le rafraîchissement.
const VERSION = "budget-v4";
const FILES = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
// Réseau d'abord pour les fichiers de l'appli (pour avoir les mises à jour), cache si hors ligne.
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  // news.json est appelé avec ?t=... à chaque fois : le mettre en cache ajouterait une copie à chaque ouverture.
  // L'appli garde déjà la dernière version des actus de son côté.
  if (url.pathname.endsWith("/news.json")) return;
  e.respondWith(
    fetch(e.request).then(r => {
      if (r.ok) { const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); }
      return r;
    }).catch(() => caches.match(e.request).then(r => r || (e.request.mode === "navigate" ? caches.match("index.html") : Response.error())))
  );
});
