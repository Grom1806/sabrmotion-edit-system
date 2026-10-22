// sabr.js — помощники композиции HyperFrames + GSAP (система «без After Effects»).
// Собрано из рабочих роликов (plan-2-mosque, be-honest, «Шкала должника») + нормы vault:
//   motion-v3 (кривые 40–55 %, всё с входом, bounce только у героев и ровно 100 % в покое),
//   sharpness-guard (мелкий текст без блюра, блюр букв ≤ 8 px и только у заголовков ≥ 60 px, НИКАКОГО зерна),
//   sfx-expressive (буква = тик в кадр появления, у каждого объекта свой звук, вжух на проезде камеры),
//   reading-time (окна «надпись полностью видна → уходит» пишутся в stats для QA).
// Требует: gsap + CustomEase, глобальные WORDS (из inject.js) и END.
(function () {
  gsap.registerPlugin(CustomEase);
  // Базовая кривая (измерено по рефам профи 2026-10-21): cubic-bezier(.5,.1,.4,.9)
  CustomEase.create("sabr", "M0,0 C0.5,0.1 0.4,0.9 1,1");
  // Камера: резко уходит (1–5 %), долго досаживается (35–80 %)
  CustomEase.create("sabrCam", "M0,0 C0.05,0 0.35,1 1,1");
  // Акцент (expo-out) — только для отдельных ударов
  CustomEase.create("sabrHit", "M0,0 C0.16,1 0.3,1 1,1");

  const tl = gsap.timeline({ paused: true });
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const H = (tag, cls, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
  const SFX = [];                       // [t, вид, дБ, слой]
  const S = (t, k, g = 0, layer = "") => { if (t >= 0 && t < END) SFX.push([+t.toFixed(3), k, g, layer]); return t; };
  const EV = []; const E = t => { EV.push(+t.toFixed(3)); return t; };
  const REVEAL = [];                    // {id, text, words, kind, t0, t1, out}
  const LETTERS = {};                   // id → {letters, ticks}
  const WARN = [];
  const seen = new Set();
  const S0 = (el, v) => { gsap.set(el, v); tl.set(el, v, 0); };
  const FT = (el, from, to, t) => { if (!seen.has(el)) { seen.add(el); S0(el, from); } return tl.fromTo(el, from, Object.assign({ immediateRender: false }, to), t); };
  const norm = x => x.w.toLowerCase().normalize("NFD").replace(/́/g, "").normalize("NFC").replace(/[«»"]/g, "").replace(/[.,:;!?…]+$/, "");
  const W = (re, k = 0) => { const m = (window.WORDS || []).filter(x => re.test(norm(x))); if (!m[k]) throw new Error("нет слова " + re + " #" + k); return m[k]; };
  const w = (re, k = 0) => W(re, k).t, we = (re, k = 0) => W(re, k).e;
  // видимость сцены: a ≤ 0 → через S0 (tl.set на нулевой позиции не рисует кадр 0)
  const show = (sel, a, b) => { S0(sel, { visibility: a <= 0 ? "visible" : "hidden" }); if (a > 0) tl.set(sel, { visibility: "visible" }, a); if (b != null) tl.set(sel, { visibility: "hidden" }, b); };
  const el = x => typeof x === "string" ? $(x) : x;
  const idOf = x => { const e = el(x); return e.id || e.className || "el"; };
  const fontPx = x => parseFloat(getComputedStyle(el(x)).fontSize);

  // ── ТЕКСТ ─────────────────────────────────────────────
  // Побуквенно. Заголовок ≥ 60 px: blur ≤ 8 px, уходит к 50 % непрозрачности; мельче — без блюра (sharpness-guard).
  // Каждая видимая буква = один тик ровно в кадр её появления.
  function letters(sel, t0, o = {}) {
    const e = el(sel), txt = e.textContent, big = fontPx(e) >= 60;
    const st = o.stagger ?? .035, d = o.dur ?? .2, rise = o.rise ?? (big ? 14 : 7), blur = big ? Math.min(o.blur ?? 8, 8) : 0;
    e.textContent = ""; let k = 0, n = 0;
    [...txt].forEach(c => {
      if (c === " ") { H("span", "", " ", e); return; }
      const s = H("span", "", c, e); s.style.display = "inline-block";
      const t = t0 + k * st; k++;
      S0(s, { opacity: 0, y: rise, filter: blur ? `blur(${blur}px)` : "none" });
      tl.to(s, { opacity: 1, y: 0, duration: d, ease: "sabr" }, t);
      if (blur) tl.to(s, { filter: "blur(0px)", duration: d * .5, ease: "power1.out" }, t);   // ноль к середине входа
      if (o.sfx !== false) { S(t + 1 / 30, o.tick || "tick", o.db ?? (big ? -8 : -12), idOf(e)); n++; }
    });
    E(t0); const t1 = t0 + (k - 1) * st + d;
    LETTERS[idOf(e)] = { letters: k, ticks: n, sfx: o.sfx !== false };
    REVEAL.push({ id: idOf(e), text: txt.trim(), words: txt.trim().split(/\s+/).length, kind: o.kind || "body", t0, t1, out: null });
    return t1;
  }
  // По словам: opacity + y 6–8 px, резко с первого кадра; один тихий тик на слово.
  function words(sel, t0, o = {}) {
    const e = el(sel), txt = e.textContent.trim(), st = o.stagger ?? .06, d = o.dur ?? .2;
    e.textContent = ""; const ws = txt.split(/\s+/);
    ws.forEach((x, i) => {
      const s = H("span", "", x, e); s.style.display = "inline-block"; if (i < ws.length - 1) H("span", "", " ", e);
      const t = (o.times ? o.times[i] : t0 + i * st);
      S0(s, { opacity: 0, y: 7 }); tl.to(s, { opacity: 1, y: 0, duration: d, ease: "sabr" }, t);
      if (o.sfx !== false) S(t + 1 / 30, "tickS", o.db ?? -15, idOf(e));
    });
    E(t0); const t1 = (o.times ? o.times[ws.length - 1] : t0 + (ws.length - 1) * st) + d;
    REVEAL.push({ id: idOf(e), text: txt, words: ws.length, kind: o.kind || "body", t0, t1, out: null });
    return t1;
  }
  // Уход надписи/блока: быстрее входа (60–70 %), без bounce. Фиксирует момент ухода для QA чтения.
  function leave(sel, t, o = {}) {
    const r = REVEAL.find(r => r.id === idOf(sel)); if (r) r.out = t;
    tl.to(el(sel), { opacity: 0, y: o.y ?? -10, duration: o.dur ?? .22, ease: "power2.in" }, E(t));
    if (o.sfx) S(t, o.sfx, o.db ?? -14, idOf(sel));
  }

  // ── ОБЪЕКТЫ ───────────────────────────────────────────
  // Поп героя: 0 → перелёт 6 % → ровно 100 % (back.out заканчивается точно на 1 — без «вечных 99.9 %»).
  function pop(sel, t, o = {}) {
    FT(el(sel), { opacity: 0, scale: o.from ?? 0.4 }, { opacity: 1, scale: 1, duration: o.dur ?? .45, ease: o.hero === false ? "sabr" : "back.out(1.4)" }, E(t));
    if (o.sfx !== false) S(t, o.sound || "pop", o.db ?? -8, idOf(sel));
  }
  // Линия → блок (motion-v3 №1): ширина за 45 % времени, потом высота.
  function lineToBlock(sel, t, o = {}) {
    const e = el(sel), wd = e.offsetWidth, ht = e.offsetHeight, d = o.dur ?? .55;
    S0(e, { width: 0, height: 4, opacity: 1 });
    tl.to(e, { width: wd, duration: d * .45, ease: "sabr" }, E(t));
    tl.to(e, { height: ht, duration: d * .55, ease: "sabr" }, t + d * .45);
    S(t, "stroke", -12, idOf(e)); S(t + d * .45, o.sound || "card", -9, idOf(e));
    return t + d;
  }
  // Расширение из точки (плашка/карточка), опционально с героическим перелётом.
  function grow(sel, t, o = {}) {
    FT(el(sel), { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: o.dur ?? .45, ease: o.hero ? "back.out(1.3)" : "sabr" }, E(t));
    if (o.sfx !== false) S(t, o.sound || "card", o.db ?? -9, idOf(sel));
  }
  // Счётчик: цифры фиксированной ширины (font-variant-numeric: tabular-nums), удар в конце.
  function counter(sel, a, b, t, d = 1.2, fmt = v => Math.round(v).toLocaleString("ru-RU")) {
    const e = el(sel), o = { v: a }; e.textContent = fmt(a);
    FT(e, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: .25, ease: "sabr" }, E(t));
    tl.to(o, { v: b, duration: d, ease: "sabrHit", onUpdate: () => { e.textContent = fmt(o.v); } }, t);
    S(t, "roll", -10, idOf(e)); S(t + d, "impact", -4, idOf(e)); E(t + d);
    REVEAL.push({ id: idOf(e), text: fmt(b), words: 1, kind: "number", t0: t, t1: t + d, out: null });
  }
  // Камера: контейнер #world едет между «станциями»; на станции scale ровно 1 (резкость).
  // Вжух пиком в момент максимальной скорости (для sabrCam ≈ 25 % длительности).
  function cam(t, to, d = .8, o = {}) {
    tl.to(o.world || "#world", Object.assign({ duration: d, ease: o.ease || "sabrCam" }, to), E(t));
    if (o.sfx !== false) S(t + d * .25, d > .9 ? "whooshBig" : "whoosh", o.db ?? -8, "camera");
  }
  // Расфокус-переход вместо реза: старая сцена blur+zoom уходит, новая приходит из blur+zoom (0.3–0.5 с).
  function defocus(from, to, tc, d = .4) {
    // перекрытие: новая сцена начинает проявляться до того, как старая исчезла (без пустого кадра на склейке)
    tl.to(from, { filter: "blur(22px)", scale: 1.06, opacity: 0, duration: d * .75, ease: "power2.in" }, E(tc - d / 2));
    FT(to, { filter: "blur(22px)", scale: 1.06, opacity: 0 }, { filter: "blur(0px)", scale: 1, opacity: 1, duration: d * .75, ease: "sabr" }, tc - d / 4);
    S(tc, "whoosh", -8, "transition");
  }

  // ── СУБТИТРЫ (captions-v2): фразами, обычный регистр, без блюра, активное слово ярче ──
  function captions(box, o = {}) {
    const ws = window.WORDS || [], max = o.maxChars ?? 22, chunks = []; let cur = null;
    ws.forEach(x => {
      const d = x.w.replace(/[«»"]/g, ""), len = cur ? cur.ws.reduce((a, y) => a + y.w.length + 1, 0) : 0;
      if (!cur || cur.line !== x.line || len + d.length > max || /[,.:;?!…]$/.test(cur.ws[cur.ws.length - 1].w)) { cur = { line: x.line, ws: [] }; chunks.push(cur); }
      cur.ws.push(x);
    });
    chunks.forEach((c, i) => {
      const e = H("div", "cap", "", el(box)), nx = chunks[i + 1];
      c.ws.forEach(x => { x.el = H("span", "", x.w.replace(/[«»"]/g, ""), e); });
      const t0 = c.ws[0].t - .03, t1 = Math.min(nx ? nx.ws[0].t - .03 : END - .2, c.ws[c.ws.length - 1].e + .45);
      S0(e, { opacity: 0, y: 8 }); tl.to(e, { opacity: 1, y: 0, duration: .15, ease: "sabr" }, Math.max(0, t0));
      tl.set(e, { opacity: 0 }, Math.max(t0 + .1, t1));
      c.ws.forEach((x, k) => { if (k) { S0(x.el, { opacity: .45 }); tl.to(x.el, { opacity: 1, duration: .1 }, x.t - .03); } });
    });
  }

  // ── ФИНАЛ: проверки и выгрузка для dump.js / qa.cjs ──
  function finish() {
    if ($$('[id*="grain"],[class*="grain"],[id*="noise"],[class*="noise"]').length) WARN.push("ЗЕРНО/ШУМ: найден слой grain/noise — запрещено (sharpness-guard)");
    tl.getChildren(true, true, false).forEach(tw => {
      const v = tw.vars || {};
      if (typeof v.scale === "number" && v.scale !== 1 && v.opacity !== 0 && !/exit|out/.test(v.id || "") && tw.endTime() > END - 0.01)
        WARN.push(`масштаб в покое ${v.scale} на ${tw.targets().map(t => t.id || t.className).join(",")} (нужно ровно 1)`);
    });
    // время чтения: момент, когда надпись реально перестаёт быть видна (уход, смена сцены, камера увезла, расфокус)
    const vis = e => { let a = 1; for (let n = e; n && n.nodeType === 1; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.visibility === "hidden" || cs.display === "none") return false; a *= +cs.opacity; if (/blur\((\d+)/.test(cs.filter) && +RegExp.$1 > 4) return false; }
      const r = e.getBoundingClientRect(), R = $("#root").getBoundingClientRect(); return a > .5 && r.bottom > R.top && r.top < R.bottom && r.right > R.left && r.left < R.right; };
    REVEAL.forEach(r => { const e = document.getElementById(r.id) || document.querySelector("." + r.id); if (!e) return;
      for (let t = r.t1 + 1 / 30; t < END; t += 1 / 30) { tl.seek(t, false); if (!vis(e)) { r.out = r.out == null ? +t.toFixed(3) : Math.min(r.out, +t.toFixed(3)); break; } } });
    tl.seek(0, false);
    const evs = [...new Set(EV.filter(t => t >= 0 && t < END).map(t => Math.round(t * 10) / 10))].sort((a, b) => a - b);
    const gaps = []; for (let i = 1; i < evs.length; i++) if (evs[i] - evs[i - 1] > 1.6) gaps.push([evs[i - 1], +(evs[i] - evs[i - 1]).toFixed(2)]);
    $("#stats-dump").textContent = JSON.stringify({ END, events: evs.length, perSec: +(evs.length / END).toFixed(2), gaps, sfx: SFX.length, reveal: REVEAL, letters: LETTERS, warn: WARN });
    $("#sfx-dump").textContent = JSON.stringify(SFX.sort((a, b) => a[0] - b[0]));
    window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl;
  }

  window.SABR = { tl, $, $$, H, S, E, S0, FT, W, w, we, show, letters, words, leave, pop, lineToBlock, grow, counter, cam, defocus, captions, finish };
})();
