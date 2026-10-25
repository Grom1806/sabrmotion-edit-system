#!/usr/bin/env node
// Проверка «успел ли зритель прочитать и увидеть» для HyperFrames-композиции.
//
// Открывает index.html в Chromium, перематывает GSAP-таймлайн window.__timelines.root
// с шагом 1/30 с и для каждой надписи меряет время «полностью видна и стоит на месте» (дрейф ≤5 px/кадр = ≤150 px/с читается).
// Норма из vault/01-rules/reading-time.md:
//   надпись: 0.6 с + 0.2 с/слово (+0.3 если есть цифры), CTA (data-read="cta") +0.6;
//   субтитр (.cap): от первого слова до ухода ≥ 0.15 + 0.2 с/слово;
//   видео-вставка (<video data-start>, кроме #head): на экране ≥1.0 с.
// Надписи = самые глубокие элементы с id и текстом + .cap + [data-read]; aria-hidden (декор, призраки) не считаются.
// Видимость меряется по рамке букв (Range), а не по блоку.
// Видимость честная: прозрачность всех предков, обрезка overflow:hidden и clip-path inset, край кадра.
//
// Запуск: node readcheck.mjs путь/к/композиции [--fps 30] [--out readcheck.tsv]
// SAFE = надпись или окно/чип/стикер стоит под интерфейсом Reels/TikTok (шапка <210, низ >1480, колонка кнопок x>910 при y 640–1480).
// OVERLAP = две надписи видны одновременно и наезжают друг на друга (>10 % площади меньшей).
// Код возврата 1, если есть FAIL, OVERLAP или SAFE. NEVER = ни разу не видна целиком (проверить глазами).
import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

// playwright: локальный, а если нет — глобальный (npm i -g playwright)
const req = createRequire(import.meta.url);
let pw;
try { pw = req("playwright"); }
catch { pw = req(req.resolve("playwright", { paths: [execSync("npm root -g").toString().trim()] })); }
const { chromium } = pw;

const args = process.argv.slice(2);
const comp = resolve(args[0] || ".");
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const fps = +opt("--fps", 30), out = opt("--out", "readcheck.tsv");

const JS_UNITS = () => {
  const all = [...document.querySelectorAll('#root [id], #root .cap, #root [data-read]')];
  const hasText = e => (e.textContent || '').trim().length > 0;
  // декоративные копии (aria-hidden: призраки slice/rgb из SABR-kit, подписи окон) — не надписи
  const deco = e => !!e.closest('[aria-hidden="true"]');
  const units = all.filter(e => !deco(e) && e.tagName !== 'VIDEO' && e.tagName !== 'svg' && hasText(e) && e.id !== 'root' &&
    !([...e.querySelectorAll('[id], .cap, [data-read]')].some(c => hasText(c))) );
  units.forEach((e, i) => e.dataset.rc = i);
  return units.map(e => ({ i: +e.dataset.rc, id: e.id || ('cap' + e.dataset.rc),
    cls: e.className && e.className.baseVal === undefined ? e.className : '',
    kind: e.dataset.read || (e.classList.contains('cap') ? 'cap' : 'text'),
    // текст без призраков; data-text = исходное слово, разбитое на буквы (SK.letters)
    text: (() => { const p = [];
      const walk = n => { if (n.nodeType === 3) { if (n.textContent.trim()) p.push(n.textContent.trim()); return; }
        if (n.nodeType !== 1 || n.getAttribute('aria-hidden') === 'true') return;
        if (n.dataset && n.dataset.text) { p.push(n.dataset.text); return; }
        n.childNodes.forEach(walk); };
      walk(e); return p.join(' ').replace(/\s+/g, ' '); })() }));
};

const JS_SAMPLE = (t) => {
  const tl = window.__timelines.root; tl.pause(); tl.seek(t, false);
  const W = 1080, H = 1920, out = [];
  const glyphs = el => {            // рамка самих букв, а не блока (блок на всю ширину кадра не считается «обрезанным»)
    const g = document.createRange(); g.selectNodeContents(el); const q = g.getBoundingClientRect();
    return q.width > 0 && q.height > 0 ? q : el.getBoundingClientRect();
  };
  const vis = el => {               // эффективная видимость одного элемента
    let op = 1, r = glyphs(el);
    let L = r.left, T = r.top, R = r.right, B = r.bottom;
    for (let a = el; a && a !== document.body; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.display === 'none' || cs.visibility === 'hidden') return 0;
      op *= parseFloat(cs.opacity);
      if (a !== el && cs.overflow !== 'visible') {
        const p = a.getBoundingClientRect();
        L = Math.max(L, p.left); T = Math.max(T, p.top); R = Math.min(R, p.right); B = Math.min(B, p.bottom);
      }
      const cp = cs.clipPath;
      if (cp && cp.startsWith('inset(')) {
        const v = cp.slice(6, -1).split(' round')[0].trim().split(/\s+/).map(parseFloat); const p = a.getBoundingClientRect();
        const [it, ir, ib, il] = [v[0], v[1] ?? v[0], v[2] ?? v[0], v[3] ?? v[1] ?? v[0]];
        L = Math.max(L, p.left + il); T = Math.max(T, p.top + it); R = Math.min(R, p.right - ir); B = Math.min(B, p.bottom - ib);
      }
    }
    L = Math.max(L, 0); T = Math.max(T, 0); R = Math.min(R, W); B = Math.min(B, H);
    const area = (r.right - r.left) * (r.bottom - r.top);
    const shown = area > 0 ? Math.max(0, R - L) * Math.max(0, B - T) / area : 0;
    return op * Math.min(1, shown);
  };
  document.querySelectorAll('[data-rc]').forEach(e => {
    // самый «невидимый» кусок текста внутри (пословные субтитры, маски)
    const leaves = [...e.querySelectorAll('*')].filter(c => !c.closest('[aria-hidden="true"]') && [...c.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
    if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && leaves.length === 0) leaves.push(e);
    if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) leaves.push(e);
    const vs = leaves.map(vis), v = Math.min(...vs), vmax = Math.max(...vs);
    const r = e.getBoundingClientRect();
    out.push([+e.dataset.rc, Math.round(v * 100) / 100, Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(vmax * 100) / 100, Math.round(r.height),
      ...(() => { const g = document.createRange(); g.selectNodeContents(e); const q = g.getBoundingClientRect();  // рамка самих букв
        return [Math.round(q.left), Math.round(q.top + q.height * .2), Math.round(q.width), Math.round(q.height * .6)]; })(),
      ...(() => {  // для SAFE: только видимые буквы (текстовые узлы видимых слов, без призраков), ядро 60 % высоты
        const rs = [];
        const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
        while (w.nextNode()) {
          const n = w.currentNode; if (!n.textContent.trim() || n.parentElement.closest('[aria-hidden="true"]')) continue;
          let op = 1; for (let a = n.parentElement; a && a !== document.body; a = a.parentElement) { const cs = getComputedStyle(a); if (cs.visibility === 'hidden' || cs.display === 'none') { op = 0; break; } op *= parseFloat(cs.opacity); }
          if (op < 0.5) continue;
          const g = document.createRange(); g.selectNodeContents(n);
          for (const q of g.getClientRects()) if (q.width) rs.push([Math.round(q.left), Math.round(q.top + q.height * .2), Math.round(q.width), Math.round(q.height * .6)]);
        }
        return [rs]; })()]);  // без межстрочных полей
  });
  return out;
};

const normFor = u => {
  // субтитр читается по мере речи: от первого слова до ухода ≥ 0.15 + 0.2 с/слово
  if (u.kind === "cap") return Math.round((0.15 + 0.2 * u.text.split(" ").length) * 100) / 100;
  let n = 0.6 + 0.2 * u.text.split(" ").length;
  if (/\d/.test(u.text)) n += 0.3;
  if (u.kind === "cta") n += 0.6;
  return Math.round(n * 100) / 100;
};

const browser = await chromium.launch();
const pg = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await pg.goto(pathToFileURL(resolve(comp, "index.html")).href);
await pg.waitForTimeout(1500);
await pg.evaluate(() => document.fonts.ready);
const dur = await pg.evaluate(() => parseFloat(document.querySelector("#root").dataset.duration));
const units = await pg.evaluate(JS_UNITS);
const vids = await pg.evaluate(() => [...document.querySelectorAll("video[data-start]")].filter(v => v.id !== "head")
  .map(v => ({ id: v.id, s: +v.dataset.start, d: +v.dataset.duration })));
const step = 1 / fps, T = [];
for (let i = 0; i <= Math.floor(dur * fps); i++) T.push(+(i * step).toFixed(4));
const series = Object.fromEntries(units.map(u => [u.i, []]));
const overlaps = new Map();  // две надписи видны одновременно и наезжают друг на друга
// Безопасная зона Reels + TikTok (1080×1920): сверху шапка, снизу ник/подпись, справа колонка лайк/коммент/репост
const SAFE = { top: 210, bottom: 1480, left: 40, right: 1040, btnX: 910, btnY0: 640, btnY1: 1480 };
const outSafe = (x, y, w, h, obj) => {
  const z = [];
  if (!obj && y < SAFE.top) z.push("верх");
  if (y + h > SAFE.bottom) z.push("низ");
  if (!obj && (x < SAFE.left || x + w > SAFE.right)) z.push("край");
  if (x + w > SAFE.btnX && y + h > SAFE.btnY0 && y < SAFE.btnY1) z.push("кнопки справа");
  return z;
};
const safeHits = new Map(), prevR = new Map();
const JS_OBJ = () => [...document.querySelectorAll('#root .sk-win, #root .chip, #root .stop, #root .tile, #root [data-safe]')].map((e, k) => {
  let op = 1; for (let a = e; a && a !== document.body; a = a.parentElement) { const cs = getComputedStyle(a); if (cs.display === 'none' || cs.visibility === 'hidden') { op = 0; break; } op *= parseFloat(cs.opacity); }
  const r = e.getBoundingClientRect(); return ['obj' + k + (e.id ? ':' + e.id : ':' + e.className.split(' ').pop()), op, Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)];
});
const hit = (key, t, z) => { const o = safeHits.get(key) || [t, t, new Set()]; o[1] = t; z.forEach(v => o[2].add(v)); safeHits.set(key, o); };
for (const t of T) {
  const smp = await pg.evaluate(JS_SAMPLE, t);
  for (const [i, v, x, y, w, vmax] of smp) series[i].push([t, v, x, y, w, vmax]);
  for (const r of smp) {               // надпись стоит (не летит) и видна → должна быть в безопасной зоне
    const i = r[0], vmax = r[5], rs = r[11], key = JSON.stringify(rs), p = prevR.get(i); prevR.set(i, rs);
    if (vmax < 0.9 || !rs.length || !p || p.length !== rs.length || rs.some((q, k) => Math.abs(q[0] - p[k][0]) > 5 || Math.abs(q[1] - p[k][1]) > 5)) continue;
    const z = [...new Set(rs.flatMap(q => outSafe(q[0], q[1], q[2], q[3], false)))]; if (z.length) hit('u' + i, t, z);
  }
  for (const [k, op, x, y, w, h] of await pg.evaluate(JS_OBJ)) {
    if (op < 0.9) continue; const p = prevR.get(k); prevR.set(k, [x, y, w]);
    if (!p || Math.abs(p[0] - x) > 5 || Math.abs(p[1] - y) > 5) continue;
    const z = outSafe(x, y, w, h, true); if (z.length) hit(k, t, z);
  }
  const on = smp.filter(r => r[5] >= 0.2 && r[9] > 0 && r[10] > 0).map(r => [r[0], 0, r[7], r[8], r[9], 0, r[10]]);
  for (let p = 0; p < on.length; p++) for (let q = p + 1; q < on.length; q++) {
    const [i, , x1, y1, w1, , h1] = on[p], [j, , x2, y2, w2, , h2] = on[q];
    const ix = Math.max(0, Math.min(x1 + w1, x2 + w2) - Math.max(x1, x2)), iy = Math.max(0, Math.min(y1 + h1, y2 + h2) - Math.max(y1, y2));
    if (ix * iy > 0.1 * Math.min(w1 * h1, w2 * h2)) {
      const k = i < j ? `${i}|${j}` : `${j}|${i}`; const o = overlaps.get(k) || [t, t]; o[1] = t; overlaps.set(k, o);
    }
  }
}
await browser.close();

const rows = []; let fails = 0;
for (const u of units) {
  let best = [0, 0, 0], run = null, prev = null;
  for (const [t, v, x, y, w, vmax] of series[u.i]) {
    const settled = !prev || (Math.abs(x - prev[0]) <= 5 && Math.abs(y - prev[1]) <= 5 && Math.abs(w - prev[2]) <= 5);
    const ok = u.kind === "cap" ? vmax >= 0.9 : v >= 0.9 && settled;
    if (ok && run === null) run = t;
    if (!ok && run !== null) { if (t - run > best[0]) best = [t - run, run, t]; run = null; }
    prev = [x, y, w];
  }
  const end = T[T.length - 1] + step;
  if (run !== null && end - run > best[0]) best = [end - run, run, end];
  const hold = Math.round(best[0] * 100) / 100, need = normFor(u);
  const st = hold === 0 ? "NEVER" : hold + 1e-6 >= need ? "ok" : "FAIL";
  if (st === "FAIL") fails++;
  rows.push([st, u.id, u.kind, best[1].toFixed(2), best[2].toFixed(2), hold, need, u.text.slice(0, 60)]);
}
for (const v of vids) {
  const st = v.d >= 1.0 ? "ok" : "FAIL"; if (st === "FAIL") fails++;
  rows.push([st, v.id, "video", v.s.toFixed(2), (v.s + v.d).toFixed(2), v.d, 1.0, "вставка"]);
}
const byI = Object.fromEntries(units.map(u => [u.i, u]));
for (const [k, [a, b]] of overlaps) {
  const [i, j] = k.split("|").map(Number); fails++;
  rows.push(["OVERLAP", `${byI[i].id}+${byI[j].id}`, "both", a.toFixed(2), (b + step).toFixed(2), 0, 0, `${byI[i].text.slice(0, 25)} / ${byI[j].text.slice(0, 25)}`]);
}
for (const [k, [a, b2, z]] of safeHits) {
  if (b2 - a < 2 * step) continue;   // 1 кадр на вылете не считаем
  fails++; const u = k[0] === 'u' ? byI[+k.slice(1)] : null;
  rows.push(["SAFE", u ? u.id : k, u ? u.kind : "object", a.toFixed(2), (b2 + step).toFixed(2), 0, 0, `${[...z].join("+")}: ${u ? u.text.slice(0, 40) : k}`]);
}
rows.sort((a, b) => a[3] - b[3]);
writeFileSync(out, "status\tid\tkind\tfull_from\tleaves_at\thold_s\tneed_s\ttext\n" + rows.map(r => r.join("\t")).join("\n") + "\n");
for (const r of rows) if (r[0] !== "ok") console.log(r.join("\t"));
console.log(`надписей ${units.length}, вставок ${vids.length}, FAIL ${fails}, NEVER ${rows.filter(r => r[0] === "NEVER").length} → ${out}`);
process.exit(fails ? 1 : 0);
