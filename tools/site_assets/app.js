/* Brain reader - theme, reading progress, claim filter, offline search, mermaid.
   Everything degrades: with JS off the pages are still complete documents. */

(function () {
  var BASE = window.SITE_BASE || "./";

  /* ---- theme ---------------------------------------------------------- */
  var btn = document.getElementById("theme");
  if (btn) {
    btn.addEventListener("click", function () {
      var cur = document.documentElement.dataset.theme;
      if (!cur) {
        cur = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }
      var next = cur === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem("brain-theme", next); } catch (e) {}
    });
  }

  /* ---- reading progress ----------------------------------------------- */
  var bar = document.querySelector(".progress i");
  if (bar) {
    var tick = function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      bar.style.width = (h > 40 ? Math.min(100, (scrollY / h) * 100) : 0) + "%";
    };
    addEventListener("scroll", tick, { passive: true });
    addEventListener("resize", tick);
    tick();
  }

  /* ---- claim filter ---------------------------------------------------- */
  var filter = document.getElementById("claim-filter");
  if (filter) {
    filter.addEventListener("click", function (e) {
      var chip = e.target.closest(".chip");
      if (!chip) return;
      filter.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("on"); });
      chip.classList.add("on");
      var want = chip.dataset.filter;
      document.querySelectorAll(".claim").forEach(function (c) {
        c.hidden = want !== "*" && c.dataset.topic !== want;
      });
    });
  }

  /* ---- search ---------------------------------------------------------- */
  var q = document.getElementById("q");
  if (q) {
    var results = document.getElementById("results");
    var status = document.getElementById("q-status");
    var index = null;

    var load = fetch(BASE + "search.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { index = d; if (q.value) run(); })
      .catch(function () { if (status) status.textContent = "Search index unavailable offline yet - open once online."; });

    var esc = function (s) {
      return s.replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    };

    function snippet(text, term) {
      var i = text.toLowerCase().indexOf(term);
      if (i < 0) return esc(text.slice(0, 150));
      var s = Math.max(0, i - 60);
      return (s ? "..." : "") + esc(text.slice(s, i)) +
        "<mark>" + esc(text.substr(i, term.length)) + "</mark>" +
        esc(text.slice(i + term.length, i + term.length + 110)) + "...";
    }

    function run() {
      var term = q.value.trim().toLowerCase();
      if (!index) return;
      if (term.length < 2) {
        results.innerHTML = "";
        if (status) status.textContent = "Type to search the whole brain. Works offline.";
        return;
      }
      var hits = [];
      for (var i = 0; i < index.length; i++) {
        var e = index[i];
        var t = e.t.toLowerCase().indexOf(term);
        var x = e.x.toLowerCase().indexOf(term);
        if (t < 0 && x < 0) continue;
        hits.push({ e: e, score: (t >= 0 ? 1000 - t : 0) + (x >= 0 ? 100 : 0) });
      }
      hits.sort(function (a, b) { return b.score - a.score; });
      if (status) status.textContent = hits.length + (hits.length === 1 ? " result" : " results");
      results.innerHTML = hits.slice(0, 60).map(function (h) {
        return '<a class="row hit" href="' + BASE + h.e.u + '"><div class="row-main">' +
          "<h3>" + esc(h.e.t) + "</h3><p>" + snippet(h.e.x, term) + "</p></div>" +
          '<div class="row-side"><span class="pill">' + esc(h.e.k) + "</span></div></a>";
      }).join("");
    }

    var timer;
    q.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(run, 90);
    });
    var pre = new URLSearchParams(location.search).get("q");
    if (pre) { q.value = pre; }
    q.focus();
  }

  /* ---- mermaid (lazy: only pages that actually hold a diagram) ---------- */
  if (window.HAS_MERMAID && document.querySelector("pre.mermaid")) {
    var s = document.createElement("script");
    s.src = BASE + "assets/mermaid.min.js";
    s.onload = function () {
      var dark = document.documentElement.dataset.theme
        ? document.documentElement.dataset.theme === "dark"
        : matchMedia("(prefers-color-scheme: dark)").matches;
      window.mermaid.initialize({
        startOnLoad: true,
        securityLevel: "loose",
        theme: dark ? "dark" : "neutral",
        fontFamily: "inherit",
      });
    };
    s.onerror = function () {
      document.querySelectorAll("pre.mermaid").forEach(function (p) {
        p.classList.remove("mermaid");
      });
    };
    document.head.appendChild(s);
  }

  /* ---- offline ---------------------------------------------------------- */
  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    addEventListener("load", function () {
      navigator.serviceWorker.register(BASE + "sw.js", { scope: BASE }).catch(function () {});
    });
  }
})();
