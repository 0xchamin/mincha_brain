/* Brain reader - offline cache.
   Text (html/css/js/search index) is precached on install, so the whole brain is
   readable with no network. Images and the 3.4MB mermaid bundle are NOT precached
   - they are cached lazily on first view, which keeps the install cheap on cellular. */

var REV = "__REV__";
var SHELL = "brain-shell-" + REV;
var MEDIA = "brain-media-v1";
var PRECACHE = __PRECACHE__;

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(SHELL).then(function (c) {
      // addAll is all-or-nothing; a single 404 must not sink the whole install.
      return Promise.all(PRECACHE.map(function (u) {
        return c.add(new Request(u, { cache: "reload" })).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== SHELL && k !== MEDIA) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;

  var isMedia = /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(req.url) || /mermaid\.min\.js$/.test(req.url);

  if (isMedia) {
    // Cache-first: bytes that never change under the same name.
    e.respondWith(
      caches.match(req).then(function (hit) {
        return hit || fetch(req).then(function (res) {
          var copy = res.clone();
          caches.open(MEDIA).then(function (c) { c.put(req, copy); });
          return res;
        });
      })
    );
    return;
  }

  // Network-first for documents: a rebuilt brain should win when there is signal.
  e.respondWith(
    fetch(req).then(function (res) {
      var copy = res.clone();
      caches.open(SHELL).then(function (c) { c.put(req, copy); });
      return res;
    }).catch(function () {
      return caches.match(req).then(function (hit) {
        return hit || caches.match(new URL("index.html", req.url).pathname);
      });
    })
  );
});
