/**
 * 2BAC Maroc 2026 - Service Worker PWA (v2.7.1)
 * Support 100% Hors-Ligne, Cache résilient & Compatibilité Cloudflare Pages
 */

const CACHE_NAME = 'bac-maroc-v2.7.1';

const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './favicon.ico',
  './icon.svg',
  './js/pdf.min.js',
  './js/pdf.worker.min.js',
  './js/qcm_engine.js',
  './js/pdf_catalogue.js'
];

// 1. Installation résiliente (avec suivi des redirections HTTP)
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const asset of ASSETS_TO_CACHE) {
        try {
          const response = await fetch(asset, { redirect: 'follow' });
          if (response.ok) {
            await cache.put(asset, response);
          }
        } catch (err) {
          console.warn('SW: mise en cache ignorée pour', asset, err);
        }
      }
    }).then(() => self.skipWaiting())
  );
});

// 2. Activation & Purge des anciens caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Stratégie de requête (Cache First avec fallback Navigation pour / et index.html)
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Requêtes internes à l'application
  if (url.origin === location.origin) {
    event.respondWith(
      (async () => {
        // A. Correspondance exacte dans le cache
        let cached = await caches.match(event.request);
        if (cached) return cached;

        // B. Gestion canonique de la racine / et index.html
        if (url.pathname === '/' || url.pathname === '/index.html' || url.pathname.endsWith('/')) {
          cached = (await caches.match('./')) || (await caches.match('./index.html')) || (await caches.match('/'));
          if (cached) return cached;
        }

        // C. Requête réseau avec suivi automatique des redirections
        try {
          const networkResponse = await fetch(event.request, { redirect: 'follow' });
          if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(event.request, networkResponse.clone());
          }
          return networkResponse;
        } catch (err) {
          // D. Fallback hors-ligne pour la navigation
          if (event.request.mode === 'navigate') {
            const fallback = (await caches.match('./')) || (await caches.match('./index.html'));
            if (fallback) return fallback;
          }
          throw err;
        }
      })()
    );
  } else {
    // Ressources externes (Vidéos YouTube, AlloSchool, Google Fonts)
    event.respondWith(
      fetch(event.request).catch(async () => {
        // En cas de coupure réseau pour Google Fonts, laisser le CSS utiliser le fallback système
        return new Response('Connexion internet requise pour cette ressource externe.', {
          status: 503,
          statusText: 'Service Unavailable',
          headers: new Headers({ 'Content-Type': 'text/plain; charset=utf-8' })
        });
      })
    );
  }
});
