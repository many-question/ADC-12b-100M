/* Theme toggle, the embedded RNL schematic viewer, copy buttons and the figure lightbox. No dependencies. */
(function () {
  "use strict";
  var VIEWER = "https://rich-netlist.github.io/rnl/viewer/";
  var VIEWER_ORIGIN = new URL(VIEWER).origin;
  var root = document.documentElement;

  /* ---------- theme */
  function theme() {
    var t = root.dataset.theme;
    if (t) return t;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var themeListeners = [];
  var btn = document.getElementById("theme");
  if (btn) btn.addEventListener("click", function () {
    var next = theme() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
    themeListeners.forEach(function (f) { f(next); });
  });
  if (window.matchMedia) matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if (!root.dataset.theme) themeListeners.forEach(function (f) { f(theme()); });
  });

  /* ---------- netlist locations */
  var meta = document.querySelector('meta[name="netlist-base"]');
  var base = new URL(meta ? meta.content : "repo/", document.baseURI).href;
  function netlistUrl(path) { return new URL(path, base).href; }
  /* the standalone viewer opens the design through a manifest (manifests/<netlist>.json, see site/sitegen/manifest.py);
     a build that has no address for the files falls back to the single netlist */
  var mfMeta = document.querySelector('meta[name="manifest-base"]');
  var mfBase = mfMeta ? new URL(mfMeta.content, document.baseURI).href : null;
  function mfName(path) { return path.replace(/\.[^./]+$/, "").replace(/\//g, "-"); }
  /* f: {path, level, mf, url}; mf names the manifest, url is the netlist's own address (a PR preview's files are not under the site) */
  function fullLink(path, level, f) {
    var lv = level ? "&level=" + encodeURIComponent(level) : "";
    if (mfBase) return VIEWER + "?manifest=" + encodeURIComponent(new URL(((f && f.mf) || mfName(path)) + ".json", mfBase).href) + lv;
    return VIEWER + "?url=" + encodeURIComponent((f && f.url) || netlistUrl(path)) + lv;
  }
  document.querySelectorAll("[data-top-viewer]").forEach(function (a) {
    a.href = fullLink("design/top/adc_top.scs", "adc_top");
  });

  /* ---------- viewers */
  var activeViewers = [];
  document.addEventListener("pointerdown", function (e) {                    // a click or tap outside a viewer ends its operation
    activeViewers.forEach(function (v) { if (v.el.classList.contains("active") && !v.el.contains(e.target)) v.deactivate(); });
  }, true);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") activeViewers.forEach(function (v) { v.deactivate(); });
  });
  document.addEventListener("adc-tab-shown", function () { activeViewers.forEach(function (v) { v.deactivate(); }); });
  function initViewer(el) {
    var files = JSON.parse(el.dataset.files);
    var frame = el.querySelector("iframe");
    var status = el.querySelector(".viewer-status");
    var tabs = el.querySelectorAll(".tabs button");
    var full = el.querySelector('[data-act="full"]');
    var src = el.querySelector('[data-act="src"]');
    var lvlBox = el.querySelector(".lvl");
    var lvlSel = lvlBox.querySelector("select");
    var activate = el.querySelector(".viewer-activate");
    var exitBtn = el.querySelector('[data-act="exit"]');
    var ready = false, started = false, cur = 0, reqId = 0, timer = null, wantLevel = null;

    function say(msg, cls) {
      status.textContent = msg;
      status.className = "viewer-status" + (cls ? " " + cls : "");
    }
    function post(msg) {
      msg.rnl = 1;
      frame.contentWindow.postMessage(msg, VIEWER_ORIGIN);
    }
    function frameSrc(i) {
      var u = new URL(VIEWER);
      u.searchParams.set("embed", "1");
      u.searchParams.set("origin", location.origin);
      u.searchParams.set("background", theme());
      u.searchParams.set("url", files[i].url || netlistUrl(files[i].path));
      if (files[i].level) u.searchParams.set("level", files[i].level);
      return u.href;
    }
    function links(i) {
      full.href = fullLink(files[i].path, files[i].level, files[i]);
      src.href = files[i].src;
    }
    function select(i) {
      cur = i;
      tabs.forEach(function (b, k) { b.setAttribute("aria-selected", k === i ? "true" : "false"); });
      links(i);
      lvlBox.hidden = true;
      say("正在加载 " + files[i].label + " …");
      if (ready) {
        wantLevel = files[i].level;
        post({ type: "open", url: files[i].url || netlistUrl(files[i].path), requestId: "r" + (++reqId) });
      }
    }
    function start() {
      if (started) return;
      started = true;
      frame.src = frameSrc(cur);
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (!ready) say("查看器没有响应：请检查网络，或点击右上角“完整查看器”在新标签页打开。", "err");
      }, 25000);
    }

    /* click to activate: an inactive viewer (iframe pointer-events: none, a button over it) lets the page scroll with wheel,
       touch and keys; a click, tap or Enter on the button activates it. It ends on a click outside this viewer, Esc on the page
       or the "结束操作" button (keys typed inside the cross-origin frame never reach the page, hence the button). */
    function setActive(on, fromKeyboard) {
      if (el.classList.contains("active") === on) return;
      el.classList.toggle("active", on);
      if (exitBtn) exitBtn.hidden = !on;
      if (on) {
        activeViewers.forEach(function (o) { if (o !== api) o.deactivate(); });
        start();
        if (fromKeyboard) try { frame.focus(); } catch (e) {}          // keyboard users: keys go to the viewer; a mouse click keeps Esc on the page
      } else if (activate && el.contains(document.activeElement) && document.activeElement === frame) {
        activate.focus();
      }
    }
    var api = { el: el, deactivate: function () { setActive(false); } };
    activeViewers.push(api);
    if (activate) activate.addEventListener("click", function (e) { setActive(true, e.detail === 0); });
    if (exitBtn) exitBtn.addEventListener("click", function () { setActive(false); });

    tabs.forEach(function (b) { b.addEventListener("click", function () { start(); select(+b.dataset.i); }); });
    el.querySelector('[data-act="grow"]').addEventListener("click", function (e) {
      var on = el.classList.toggle("grown");
      e.currentTarget.setAttribute("aria-pressed", on ? "true" : "false");
      e.currentTarget.textContent = on ? "缩小" : "放大";
      if (ready) post({ type: "fit" });
    });
    lvlSel.addEventListener("change", function () { post({ type: "level", name: lvlSel.value }); });
    themeListeners.push(function (t) { if (ready) post({ type: "background", value: t }); });

    /* a viewer that finished loading in a hidden tab is fitted when its tab is first shown */
    var loadedHidden = false;
    document.addEventListener("adc-tab-shown", function () {
      if (loadedHidden && ready && el.offsetParent !== null) { loadedHidden = false; setTimeout(function () { post({ type: "fit" }); }, 60); }
    });
    window.addEventListener("message", function (ev) {
      if (ev.source !== frame.contentWindow || ev.origin !== VIEWER_ORIGIN || !ev.data || ev.data.rnl !== 1) return;
      var d = ev.data;
      if (d.type === "ready") {
        ready = true;
      } else if (d.type === "loaded") {
        var n = (d.errors || 0), w = (d.warnings || 0);
        say(files[cur].label + (n || w ? " · " + n + " 个错误，" + w + " 个警告" : " · 已加载"), n ? "err" : "ok");
        var levels = d.levels || [];
        if (levels.length > 1) {
          lvlSel.innerHTML = "";
          levels.forEach(function (l) { var o = document.createElement("option"); o.value = l; o.textContent = l; lvlSel.appendChild(o); });
          lvlSel.value = d.level || levels[0];
          lvlBox.hidden = false;
        }
        if (wantLevel && levels.indexOf(wantLevel) >= 0 && d.level !== wantLevel) {
          post({ type: "level", name: wantLevel });
        }
        wantLevel = null;
        loadedHidden = el.offsetParent === null;
        setTimeout(function () { post({ type: "fit" }); }, 120);   // the first paint can be taken before the frame has its size
      } else if (d.type === "level") {
        if (lvlSel.querySelector('option[value="' + CSS.escape(d.name) + '"]')) lvlSel.value = d.name;
      } else if (d.type === "error" && d.reason !== "superseded") {
        say("加载失败：" + d.message, "err");
      }
    });

    links(0);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es, o) {
        if (es.some(function (e) { return e.isIntersecting; })) { o.disconnect(); start(); }
      }, { rootMargin: "300px" }).observe(el);
    } else {
      start();
    }
  }
  document.querySelectorAll(".viewer").forEach(initViewer);

  /* ---------- block page tabs (main / draft PRs): the tab is in the URL hash, #pr<N> for a draft, none for main */
  document.querySelectorAll("[data-tabs]").forEach(function (wrap) {
    var tabs = Array.prototype.slice.call(wrap.querySelectorAll(":scope > .tabbar > [role=\"tab\"]"));      // not the viewers' own tabs
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });
    function show(i, focus) {
      tabs.forEach(function (t, k) {
        t.setAttribute("aria-selected", k === i ? "true" : "false");
        t.tabIndex = k === i ? 0 : -1;
        panels[k].hidden = k !== i;
      });
      if (focus) tabs[i].focus();
      document.dispatchEvent(new CustomEvent("adc-tab-shown", { detail: panels[i] }));
    }
    function indexOfHash() {
      var id = "";
      try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) {}
      if (!id) return 0;
      var k = panels.findIndex(function (p) { return p.id === id; });
      if (k >= 0) return k;
      var el = document.getElementById(id);                  // an anchor inside a panel: open that panel
      k = el ? panels.findIndex(function (p) { return p.contains(el); }) : -1;
      return k >= 0 ? k : 0;
    }
    function setHash(i) {
      try { history.replaceState(null, "", i === 0 ? location.pathname + location.search : "#" + panels[i].id); } catch (e) {}
    }
    function fromHash() {
      show(indexOfHash(), false);
      var id = location.hash.slice(1), el = id && document.getElementById(id);
      if (el && panels.indexOf(el) < 0) {
        for (var d = el.closest("details"); d; d = d.parentElement && d.parentElement.closest("details")) d.open = true;   // a candidate's section
        el.scrollIntoView();
      }
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { show(i, false); setHash(i); });
      t.addEventListener("keydown", function (e) {
        var n = tabs.length, k = i;
        if (e.key === "ArrowRight") k = (i + 1) % n;
        else if (e.key === "ArrowLeft") k = (i + n - 1) % n;
        else if (e.key === "Home") k = 0;
        else if (e.key === "End") k = n - 1;
        else return;
        e.preventDefault();
        show(k, true); setHash(k);
      });
    });
    window.addEventListener("hashchange", fromHash);
    fromHash();
  });

  /* ---------- copy buttons */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.dataset.copy, label = b.textContent;
      function done(ok) {
        b.textContent = ok ? "已复制" : "请手动复制";
        setTimeout(function () { b.textContent = label; }, 1800);
      }
      function fallback() {
        var t = document.createElement("textarea");
        t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
        document.body.appendChild(t); t.select();
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) {}
        t.remove(); done(ok);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
      else fallback();
    });
  });

  /* ---------- figure lightbox: a click on a thumbnail shows the PNG large; without JavaScript the link opens the file */
  var box = null;
  function lightbox() {
    if (box) return box;
    box = document.createElement("dialog");
    box.className = "lightbox";
    box.innerHTML = '<img alt=""><p></p><button type="button" class="btn small" aria-label="关闭">关闭 ✕</button>';
    box.addEventListener("click", function (e) { if (e.target !== box.querySelector("img")) box.close(); });
    document.body.appendChild(box);
    return box;
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-zoom]");
    if (!a || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var d = lightbox();
    if (!d.showModal) return;                       // very old browser: follow the link
    e.preventDefault();
    var img = d.querySelector("img");
    img.src = a.href; img.alt = a.dataset.caption || "";
    d.querySelector("p").textContent = a.dataset.caption || "";
    d.showModal();
  });
})();
