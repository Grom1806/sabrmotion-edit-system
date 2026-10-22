// node tools/qa.cjs <name> — проверка перед показом (как ae_sharp_preflight + sharpcheck + аудиты SFX/чтения).
// Без «PASS» ролик пользователю не показываем. Отчёт: out/<name>_QA.md
const fs = require('fs'), path = require('path'), { spawnSync } = require('child_process');
const name = process.argv[2] || 'reel';
const st = JSON.parse(fs.readFileSync('.tmp/stats.json', 'utf8')), ev = JSON.parse(fs.readFileSync('.tmp/sfx_events.json', 'utf8'));
const voice = fs.existsSync('.tmp/voice.wav'), refTempo = !!process.env.REF_TEMPO;
const R = []; let fails = 0;
const row = (k, ok, msg) => { if (!ok) fails++; R.push(`| ${k} | ${ok ? 'ok' : '**FAIL**'} | ${msg} |`); };
// 1. предупреждения композиции: зерно/шум, масштаб в покое ≠ 1
row('Без зерна, масштаб в покое = 100 %', !(st.warn || []).length, (st.warn || []).join('; ') || 'нет слоёв grain/noise, все конечные масштабы ровно 1');
// 2. время чтения (reading-time.md): без голоса 0.6 + 0.2/слово (+0.3 числа/UI, +0.6 CTA)
const norm = r => 0.6 + 0.2 * r.words + (['number', 'ui'].includes(r.kind) ? 0.3 : 0) + (r.kind === 'cta' ? 0.6 : 0);
const rt = ['| надпись | слов | норма, с | видна, с | ок |', '|---|---|---|---|---|']; let bad = 0;
(st.reveal || []).forEach(r => { if (r.kind === 'caption' || r.kind === 'service') return;
  const vis = (r.out ?? st.END) - r.t1, need = norm(r), ok = vis + 1e-6 >= need || voice || refTempo; if (!ok) bad++;
  rt.push(`| ${r.text.slice(0, 40)} | ${r.words} | ${need.toFixed(1)} | ${vis.toFixed(2)} | ${ok ? 'да' : 'НЕТ'} |`); });
fs.mkdirSync('out', { recursive: true }); fs.writeFileSync(`out/${name}_reading_time.md`, rt.join('\n') + '\n');
row('Время чтения', bad === 0, bad ? `${bad} надписей уходят раньше нормы (out/${name}_reading_time.md)` : 'все надписи держатся по норме' + (voice || refTempo ? ' (голос/темп референса)' : ''));
// 3. буква = тик (sfx-expressive)
const mism = Object.entries(st.letters || {}).filter(([, v]) => v.sfx && v.letters !== v.ticks).map(([k, v]) => `${k}: букв ${v.letters}, тиков ${v.ticks}`);
row('Буква = тик', !mism.length, mism.join('; ') || 'в каждой побуквенной надписи тиков = букв');
// 4. звуки без события: каждый S() должен назвать слой
const orphan = ev.filter(e => !e[3]).map(e => `${e[0]} ${e[1]}`);
row('Нет звуков без события', !orphan.length, orphan.length ? 'без слоя: ' + orphan.slice(0, 6).join(', ') : `${ev.length} SFX, все привязаны к элементам`);
// 5. нет «каши»: 5+ громких (не тики) в окне 0.25 с
const loud = ev.filter(e => !/^tick/.test(e[1]) && e[2] > -12).map(e => e[0]).sort((a, b) => a - b);
const burst = loud.filter((a, i) => loud.slice(i).filter(b => b - a < 0.25).length >= 5);
row('Нет звуковой каши', !burst.length, burst.length ? 'окна: ' + burst.slice(0, 5).join(', ') : 'нет окон 0.25 с с ≥5 акцентами');
// 6. проявление не прерывается уходом
const conf = (st.reveal || []).filter(r => r.out != null && r.out < r.t1 - 1e-6).map(r => r.id);
row('Проявление не прерывается', !conf.length, conf.join(', ') || 'нет');
// 7. синхрон SFX (verify_solo ±50 мс)
if (fs.existsSync('.tmp/verify_solo.txt')) { const v = fs.readFileSync('.tmp/verify_solo.txt', 'utf8').trim().split('\n').pop(); const m = v.match(/вне ±50 мс: (\d+)/);
  row('Синхрон SFX ±50 мс', m && +m[1] === 0, v); }
// 8. резкость экспорта: кадры near-lossless рендера (эталон) vs master/light ≥ 0.9; кадры покоя не мягче 60 % медианы
const ref = '.tmp/render.mp4', master = `out/${name}_master.mp4`, light = `out/${name}_1080.mp4`;
if (fs.existsSync(ref) && fs.existsSync(master)) {
  const dir = '.tmp/qa_frames'; fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const ts = (st.reveal || []).map(r => r.t1 + 0.25).filter(t => t < st.END - 0.1).slice(0, 12);
  ts.forEach(t => spawnSync('ffmpeg', ['-v', 'error', '-y', '-ss', t.toFixed(3), '-i', ref, '-frames:v', '1', `${dir}/${name}_${t.toFixed(2)}.png`]));
  const py = process.platform === 'win32' ? 'python' : 'python3';
  const r = spawnSync(py, [path.join(__dirname, 'sharpcheck.py'), '--frames', dir, '--video', master, '--video', light], { encoding: 'utf8' });
  fs.writeFileSync(`out/${name}_sharpcheck.txt`, r.stdout + r.stderr);
  row('Резкость (sharpcheck)', r.status === 0, (r.stdout.trim().split('\n').pop() || r.stderr.slice(-200)) + ` — кадров ${ts.length}`);
  // 9. громкость мастера
  const e = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', master, '-af', 'ebur128=peak=true', '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const s = e.slice(e.lastIndexOf('Summary:')), I = +s.split('I:')[1].split('LUFS')[0], TP = +s.split('Peak:')[1].split('dBFS')[0];
  row('Громкость −14 LUFS, TP ≤ −1', Math.abs(I + 14) <= 1 && TP <= -1, `I ${I} LUFS, TP ${TP} dBTP`);
  // 10. первый кадр не пустой
  const f0 = spawnSync('ffmpeg', ['-v', 'error', '-i', master, '-frames:v', '1', '-vf', 'signalstats,metadata=print:key=lavfi.signalstats.YDIF:file=-,metadata=print:key=lavfi.signalstats.YMAX:file=-', '-f', 'null', '-'], { encoding: 'utf8' }).stdout;
  const ymax = +((f0.match(/YMAX=(\d+)/) || [])[1] || 0);
  row('Первый кадр не пустой', ymax > 40, `YMAX кадра 0 = ${ymax}`);
}
const rep = [`# QA ${name} (HyperFrames, без AE)`, '', `Итог: **${fails ? `FAIL (${fails})` : 'PASS'}**`, '', `END ${st.END} с · событий/с ${st.perSec} · SFX ${ev.length}`, '',
  '| проверка | статус | детали |', '|---|---|---|', ...R].join('\n');
fs.writeFileSync(`out/${name}_QA.md`, rep + '\n'); console.log(rep); process.exitCode = fails ? 2 : 0;
