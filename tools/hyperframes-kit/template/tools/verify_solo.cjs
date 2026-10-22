// node tools/verify_solo.cjs — каждый SFX рендерится отдельно той же цепочкой фильтров, что и в миксе;
// точка удара (пик для якоря p, начало −25 дБ для o) сравнивается с моментом события из таймлайна. Допуск ±50 мс.
const fs = require('fs'), { spawnSync } = require('child_process');
const files = JSON.parse(fs.readFileSync('.tmp/mix_files.json', 'utf8'));   // индекс = номер входа в графе микса
const G = fs.readFileSync('.tmp/mix_graph.txt', 'utf8').split(';\n').filter(l => /^\[\d+:a\].*\[s\d+\]$/.test(l));
const P = fs.readFileSync('.tmp/sfx_placement.txt', 'utf8').split('\n').filter(Boolean);
let bad = 0, worst = 0;
G.forEach((l, i) => { const m = l.match(/^\[(\d+):a\](.*)\[s\d+\]$/), f = files[+m[1]], chain = m[2].replace(/volume=[^,]+,/, '');
  const p = P[i].match(/^\s*([\d.]+) (\w+)\s+→ старт ([\d.]+) \(якорь (\w)\+?([\d.]*)/), t = +p[1], mode = p[4], off = +(p[5] || 0), exp = t + off;
  const r = spawnSync('ffmpeg', ['-v', 'error', '-i', f, '-filter_complex', `[0:a]${chain},aresample=8000,pan=mono|c0=0.5*c0+0.5*c1`, '-f', 'f32le', '-'], { maxBuffer: 1 << 28 });
  const b = r.stdout, x = new Float32Array(b.buffer, b.byteOffset, b.length / 4), w = 40, e = []; for (let k = 0; k + w <= x.length; k += w) { let q = 0; for (let j = 0; j < w; j++) q += x[k + j] * x[k + j]; e.push(Math.sqrt(q / w)); }
  const pk = Math.max(...e), got = (mode === 'p' ? e.indexOf(pk) : e.findIndex(v => v >= pk * Math.pow(10, -25 / 20))) * 5 / 1000, d = (got - exp) * 1000;
  worst = Math.max(worst, Math.abs(d)); const fl = Math.abs(d) > 50 ? '  ⚠' : ''; if (fl) bad++;
  console.log(`${t.toFixed(2).padStart(6)} ${p[2].padEnd(7)} удар ${got.toFixed(3)} ожид ${exp.toFixed(3)} Δ ${d.toFixed(0)} мс${fl}`); });
console.log(`событий ${G.length}, вне ±50 мс: ${bad}, макс |Δ| ${worst.toFixed(0)} мс`);
fs.writeFileSync('.tmp/verify_solo.txt', `событий ${G.length}, вне ±50 мс: ${bad}, макс |Δ| ${worst.toFixed(0)} мс\n`);
