/* SABRMOTION style kit v1 (2026-10-25)
   Reusable caption / motion modules distilled from pro reference reels
   (editorial poster, motion-blur slide stack, dim-karaoke stack) plus new futuristic ones.
   Every function writes into one GSAP timeline: SK.use(tl) once, then call modules with times in seconds.
   Docs: vault/03-techniques/style-kit.md · tools/style-kit/README.md */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  let tl, defs, uid = 0;
  const SK = {};
  SK.C = { yellow: "#EAD43A", red: "#E5162B", green: "#19C46B", ink: "#0E0E10", white: "#FFFFFF", paper: "#F6F5F1" };
  SK.use = (t) => { tl = t; return SK; };

  // ── helpers ─────────────────────────────────────────────
  function defsEl() {
    if (defs) return defs;
    const s = document.createElementNS(NS, "svg");
    s.setAttribute("width", "0"); s.setAttribute("height", "0");
    s.style.cssText = "position:absolute;left:0;top:0;width:0;height:0";
    defs = document.createElementNS(NS, "defs"); s.appendChild(defs); document.body.appendChild(s);
    return defs;
  }
  // directional (motion) blur: returns the feGaussianBlur node; filter is attached only while it moves
  function mb(el) {
    const id = "skmb" + uid++;
    const f = document.createElementNS(NS, "filter");
    f.setAttribute("id", id); f.setAttribute("x", "-60%"); f.setAttribute("y", "-60%");
    f.setAttribute("width", "220%"); f.setAttribute("height", "220%");
    f.setAttribute("color-interpolation-filters", "sRGB");
    const g = document.createElementNS(NS, "feGaussianBlur"); g.setAttribute("stdDeviation", "0.01 0.01");
    f.appendChild(g); defsEl().appendChild(f);
    return { g, url: `url(#${id})` };
  }
  function blurMove(el, at, dur, from, to = "0.01 0.01", ease = "power3.out") {
    const m = mb(el);
    tl.set(el, { filter: m.url }, at);
    tl.fromTo(m.g, { attr: { stdDeviation: from } }, { attr: { stdDeviation: to }, duration: dur, ease, immediateRender: false }, at);
    if (to === "0.01 0.01") tl.set(el, { filter: "none" }, at + dur + 0.001);
  }
  SK.mk = (parent, cls, html, css) => {
    const d = document.createElement("div");
    if (cls) d.className = cls;
    if (html != null) d.innerHTML = html;
    if (css) Object.assign(d.style, css);
    (typeof parent === "string" ? document.querySelector(parent) : parent).appendChild(d);
    return d;
  };
  // decorative copy: never counted as a readable unit (no id / .cap / data-read)
  function ghost(el) {
    const c = el.cloneNode(true); c.removeAttribute("id"); c.classList.remove("cap"); delete c.dataset.read;
    c.querySelectorAll("[id],.cap,[data-read]").forEach((x) => { x.removeAttribute("id"); x.classList.remove("cap"); delete x.dataset.read; });
    c.setAttribute("aria-hidden", "true"); return c;
  }
  const $ = (x) => (typeof x === "string" ? document.querySelector(x) : x);
  const hide = (el) => gsap.set(el, { autoAlpha: 0 });

  // ── ENTRANCES (each hides the element first, returns the time it settles) ──
  // E1 pop: overshoot scale + vertical blur (editorial poster words)
  SK.pop = (el, at, o = {}) => {
    el = $(el); hide(el); const d = o.dur ?? 0.3;
    tl.set(el, { autoAlpha: 1 }, at);
    tl.fromTo(el, { scale: o.from ?? 0.55, y: o.y ?? 26 }, { scale: 1, y: 0, duration: d, ease: `back.out(${o.back ?? 2.4})`, immediateRender: false }, at);
    blurMove(el, at, d * 0.7, o.blur ?? "0.01 14");
    return at + d;
  };
  // E2 bounce: drop in from above and bounce on the baseline
  SK.bounce = (el, at, o = {}) => {
    el = $(el); hide(el); const d = o.dur ?? 0.55;
    tl.set(el, { autoAlpha: 1 }, at);
    tl.fromTo(el, { y: o.y ?? -220 }, { y: 0, duration: d, ease: "bounce.out", immediateRender: false }, at);
    tl.fromTo(el, { scaleY: 1.18, scaleX: 0.9 }, { scaleY: 1, scaleX: 1, duration: d, ease: "elastic.out(1,0.35)", immediateRender: false }, at + d * 0.35);
    blurMove(el, at, d * 0.35, "0.01 18", "0.01 0.01", "none");
    return at + d;
  };
  // E3 elastic: scale from 0 with elastic spring (stickers, icons, chips)
  SK.spring = (el, at, o = {}) => {
    el = $(el); hide(el); const d = o.dur ?? 0.7;
    tl.set(el, { autoAlpha: 1 }, at);
    tl.fromTo(el, { scale: 0, rotation: o.rot ?? -12 }, { scale: 1, rotation: 0, duration: d, ease: "elastic.out(1,0.45)", immediateRender: false }, at);
    return at + d * 0.5;
  };
  // E4 slide: horizontal slide with motion blur and a 3D swing (slide stack)
  SK.slide = (el, at, o = {}) => {
    el = $(el); hide(el); const d = o.dur ?? 0.34, dir = o.dir ?? 1;
    tl.set(el, { autoAlpha: 1 }, at);
    tl.fromTo(el, { x: 300 * dir, rotationY: -40 * dir, transformPerspective: 900 }, { x: 0, rotationY: 0, duration: d, ease: "expo.out", immediateRender: false }, at);
    blurMove(el, at, d * 0.75, "28 0.01");
    return at + d;
  };
  // E5 depth: comes from far (defocus zoom), futuristic
  SK.depth = (el, at, o = {}) => {
    el = $(el); hide(el); const d = o.dur ?? 0.45;
    tl.fromTo(el, { autoAlpha: 0, scale: o.from ?? 2.4, filter: "blur(18px)" }, { autoAlpha: 1, scale: 1, filter: "blur(0px)", duration: d, ease: "expo.out", immediateRender: false }, at);
    tl.set(el, { filter: "none" }, at + d + 0.001);
    return at + d;
  };
  // E6 slice: three horizontal slices slide in from alternating sides and lock (futuristic)
  SK.slice = (el, at, o = {}) => {
    el = $(el); hide(el); const d = o.dur ?? 0.42, n = 3, parts = [];
    for (let i = 0; i < n; i++) {
      const c = ghost(el); c.classList.add("sk-slice");
      c.style.clipPath = `inset(${(i * 100) / n}% 0 ${100 - ((i + 1) * 100) / n}% 0)`;
      el.parentNode.insertBefore(c, el.nextSibling); parts.push(c); hide(c);
      tl.set(c, { autoAlpha: 1 }, at);
      tl.fromTo(c, { x: (i % 2 ? -1 : 1) * (o.dist ?? 380) }, { x: 0, duration: d, ease: "expo.out", delay: i * 0.035, immediateRender: false }, at);
      blurMove(c, at + i * 0.035, d * 0.7, "26 0.01", "0.01 0.01");
      tl.set(c, { autoAlpha: 0 }, at + d * 0.6 + 0.07);   // полосы почти сошлись → подменяем целым словом (без швов по краям клипа)
    }
    tl.set(el, { autoAlpha: 1 }, at + d * 0.6 + 0.07);
    return at + d;
  };
  // E7 scan: revealed left→right behind a bright scan line (futuristic)
  SK.scan = (el, at, o = {}) => {
    el = $(el); hide(el); const d = o.dur ?? 0.4;
    const ln = SK.mk(el.parentNode, "sk-scanline", null, {});
    // рамка самих букв в координатах родителя (родитель может быть уже масштабирован)
    const pr = el.parentNode.getBoundingClientRect(), k = el.parentNode.offsetWidth / (pr.width || 1);
    const g = document.createRange(); g.selectNodeContents(el); const q = g.getBoundingClientRect();
    const r = { left: (q.left - pr.left) * k, top: (q.top - pr.top) * k, width: q.width * k, height: q.height * k };
    Object.assign(ln.style, { left: r.left + "px", top: r.top - 10 + "px", height: r.height + 20 + "px", background: o.color ?? SK.C.white });
    hide(ln);
    tl.set([el, ln], { autoAlpha: 1 }, at);
    tl.fromTo(el, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: d, ease: "power2.inOut", immediateRender: false }, at);
    tl.fromTo(ln, { x: 0 }, { x: r.width, duration: d, ease: "power2.inOut", immediateRender: false }, at);
    tl.to(ln, { autoAlpha: 0, duration: 0.12 }, at + d);
    return at + d;
  };
  // E8 rgb: chromatic split that converges with a spring (futuristic, keep short)
  SK.rgb = (el, at, o = {}) => {
    el = $(el); const d = o.dur ?? 0.5;
    const ghosts = [["#FF2D55", -1], ["#29E7FF", 1]].map(([col, s]) => {
      const c = ghost(el); c.classList.add("sk-ghost"); c.style.color = col; c.style.textShadow = "none"; c.style.mixBlendMode = "screen";
      el.parentNode.insertBefore(c, el); hide(c);
      tl.set(c, { autoAlpha: 0.9 }, at);
      tl.fromTo(c, { x: 22 * s, y: -6 * s }, { x: 0, y: 0, duration: d, ease: "elastic.out(1,0.5)", immediateRender: false }, at);
      tl.to(c, { autoAlpha: 0, duration: 0.12 }, at + d * 0.6);
      return c;
    });
    SK.spring(el, at, { dur: d + 0.2, rot: 0 });
    return at + d;
  };
  // E9 letters: per-letter bounce wave (headline only; small text never per-letter)
  SK.letters = (el, at, o = {}) => {
    el = $(el); const txt = el.textContent; el.textContent = ""; el.dataset.text = txt;
    const spans = [...txt].map((ch) => { const s = document.createElement("span"); s.textContent = ch; s.style.display = "inline-block"; if (ch === " ") s.style.width = ".28em"; el.appendChild(s); return s; });
    hide(el); tl.set(el, { autoAlpha: 1 }, at);
    spans.forEach((s, i) => {
      gsap.set(s, { autoAlpha: 0 });
      const t = at + i * (o.stagger ?? 0.035);
      tl.set(s, { autoAlpha: 1 }, t);
      tl.fromTo(s, { y: o.y ?? 90, scaleY: 1.4 }, { y: 0, scaleY: 1, duration: 0.5, ease: "back.out(3)", immediateRender: false }, t);
    });
    return at + spans.length * (o.stagger ?? 0.035) + 0.3;
  };
  // E10 type: typed characters (UI windows)
  SK.type = (el, at, o = {}) => {
    el = $(el); const txt = el.textContent; const cps = o.cps ?? 28;
    hide(el); tl.set(el, { autoAlpha: 1 }, at);
    const obj = { n: 0 };
    tl.fromTo(obj, { n: 0 }, { n: txt.length, duration: txt.length / cps, ease: "none", immediateRender: false, onUpdate: () => (el.textContent = txt.slice(0, Math.round(obj.n))) }, at);
    gsap.set(el, { textContent: "" });
    return at + txt.length / cps;
  };

  // ── EXITS ─────────────────────────────────────────────
  // whip: fast move with motion blur in a direction ('down','up','left','right')
  SK.whip = (els, at, dir = "down", o = {}) => {
    const d = o.dur ?? 0.22, dist = o.dist ?? 520;
    const v = { down: [0, 1], up: [0, -1], left: [-1, 0], right: [1, 0] }[dir];
    (Array.isArray(els) ? els : [els]).map($).forEach((el) => {
      tl.to(el, { x: `+=${v[0] * dist}`, y: `+=${v[1] * dist}`, duration: d, ease: "power3.in" }, at);
      blurMove(el, at, d, v[0] ? "0.01 0.01" : "0.01 0.01", v[0] ? "40 0.01" : "0.01 40", "power3.in");
      tl.set(el, { autoAlpha: 0 }, at + d);
    });
    return at + d;
  };
  SK.fade = (els, at, d = 0.12) => { tl.to((Array.isArray(els) ? els : [els]).map($), { autoAlpha: 0, duration: d }, at); return at + d; };
  SK.shrink = (els, at, d = 0.2) => { tl.to((Array.isArray(els) ? els : [els]).map($), { scale: 0, autoAlpha: 0, duration: d, ease: "back.in(2)" }, at); return at + d; };

  // ── CAMERA ────────────────────────────────────────────
  // punch: hard punch-in/out with a short zoom blur (holds must stay ≤1.12 — sharpness guard)
  SK.punch = (wrap, at, scale, o = {}) => {
    wrap = $(wrap); const d = o.dur ?? 0.16;
    tl.to(wrap, { scale, duration: d, ease: "expo.out" }, at);
    tl.fromTo(wrap, { filter: "blur(7px)" }, { filter: "blur(0px)", duration: d + 0.06, ease: "power2.out", immediateRender: false }, at);
    tl.set(wrap, { filter: "none" }, at + d + 0.07);
    return at + d;
  };
  SK.push = (wrap, a, b, to, ease = "sine.inOut") => { tl.to($(wrap), { scale: to, duration: b - a, ease }, a); };
  // flash: full-frame colour flash (2–3 frames)
  SK.flash = (el, at, color = "#fff", d = 0.1) => {
    el = $(el); hide(el);
    tl.set(el, { autoAlpha: 1, backgroundColor: color }, at);
    tl.to(el, { autoAlpha: 0, duration: d, ease: "power1.in" }, at + 0.033);
  };
  // leak: smooth warm light sweep (no grain)
  SK.leak = (el, at, d = 0.6) => {
    el = $(el); hide(el);
    tl.fromTo(el, { autoAlpha: 0, x: -700 }, { autoAlpha: 1, x: 0, duration: d * 0.45, ease: "power2.out", immediateRender: false }, at);
    tl.to(el, { autoAlpha: 0, x: 600, duration: d * 0.55, ease: "power2.in" }, at + d * 0.45);
  };

  // ── OBJECTS ───────────────────────────────────────────
  // window: floating app window (style 'glass' = futuristic dark glass, 'retro' = classic OS)
  SK.win = (parent, o) => {
    const w = SK.mk(parent, `sk-win sk-win-${o.style ?? "glass"}`, null, { left: o.x + "px", top: o.y + "px", width: o.w + "px", height: o.h + "px" });
    if (o.id) w.id = o.id;
    const bar = SK.mk(w, "sk-bar", `<i></i><i></i><i></i><b>${o.title ?? ""}</b>`);
    bar.setAttribute("aria-hidden", "true");
    const body = SK.mk(w, "sk-body");
    if (o.html) body.innerHTML = o.html;
    hide(w);
    return w;
  };
  SK.open = (w, at, o = {}) => {
    w = $(w); const d = o.dur ?? 0.5;
    tl.set(w, { autoAlpha: 1 }, at);
    tl.fromTo(w, { scale: 0.15, rotation: o.rot ?? -8, y: 60 }, { scale: 1, rotation: o.endRot ?? 0, y: 0, duration: d, ease: "back.out(1.9)", immediateRender: false }, at);
    blurMove(w, at, d * 0.5, "0.01 10");
    return at + d;
  };
  // cursor: arrow that glides and clicks
  SK.cursor = (parent) => {
    const c = SK.mk(parent, "sk-cursor", `<svg viewBox="0 0 24 24" width="70" height="70"><path d="M4 2 L4 20 L9 15.5 L12.5 22 L15.5 20.6 L12.2 14 L19 14 Z" fill="#fff" stroke="#0E0E10" stroke-width="1.6" stroke-linejoin="round"/></svg>`);
    hide(c); return c;
  };
  SK.glide = (c, at, x, y, d = 0.45) => { tl.set(c, { autoAlpha: 1 }, at); tl.to(c, { x, y, duration: d, ease: "power3.inOut" }, at); return at + d; };
  SK.click = (c, at) => { tl.to(c, { scale: 0.8, duration: 0.06, yoyo: true, repeat: 1, ease: "power1.inOut" }, at); };
  // counter: rolling number
  SK.count = (el, at, from, to, d = 0.5, fmt = (v) => Math.round(v).toLocaleString("ru-RU")) => {
    el = $(el); const obj = { v: from };
    tl.fromTo(obj, { v: from }, { v: to, duration: d, ease: "power3.out", immediateRender: false, onUpdate: () => (el.textContent = fmt(obj.v)) }, at);
  };
  // karaoke stack: all words of a line visible dim, the spoken one lights up
  SK.karaoke = (words, o = {}) => {
    words.forEach(([el, t], i) => {
      el = $(el);
      gsap.set(el, { color: o.dim ?? "rgba(255,255,255,.38)" });
      tl.to(el, { color: o.on ?? "#fff", textShadow: o.glow ?? "0 0 22px rgba(255,255,255,.45)", duration: 0.08 }, t);
      tl.fromTo(el, { scale: 1 }, { scale: 1.08, duration: 0.09, yoyo: true, repeat: 1, ease: "power1.out", immediateRender: false }, t);
    });
  };

  window.SK = SK;
})();
