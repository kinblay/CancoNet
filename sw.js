const CACHE = 'canconet-v56'; // v56: reorg de modes del menú (Copa a properament, sense Mundials, roscos reestilats)
const ASSETS = ['/', '/index.html', '/manifest.json'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => { if (e.request.method !== 'GET') return; if (e.request.url.includes('api.deezer.com')) return; if (e.request.url.includes('supabase.co')) return; e.respondWith(caches.match(e.request).then(cached => cached || fetch(e.request))); });
