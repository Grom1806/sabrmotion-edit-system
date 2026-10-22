// node tools/gaps.js — вставляет паузы-«вдохи» между битами (слова и длительности в gaps.json):
// режет .tmp/voice.wav между словами, сдвигает .tmp/words.json
const fs = require('fs'), { execFileSync } = require('child_process');
const W = JSON.parse(fs.readFileSync('.tmp/words.json', 'utf8'));
const GAP = JSON.parse(fs.readFileSync('gaps.json', 'utf8')).gaps || {};
const cuts = []; W.forEach((x, i) => { const k = x.w.normalize('NFD').replace(/\u0301/g, '').normalize('NFC'); if (GAP[k] && W[i + 1]) cuts.push({ at: +((x.e + W[i + 1].t) / 2).toFixed(3), g: GAP[k], i }); });
if (!cuts.length) { console.log('пауз нет (gaps.json пуст)'); process.exit(0); }
let sh = 0; const out = W.map((x, i) => { const y = { ...x, t: +(x.t + sh).toFixed(3), e: +(x.e + sh).toFixed(3) }; const c = cuts.find(c => c.i === i); if (c) sh += c.g; return y; });
let f = '', prev = 0; cuts.forEach((c, k) => { f += `[0:a]atrim=${prev}:${c.at},asetpts=PTS-STARTPTS[a${k}];aevalsrc=0:d=${c.g}:s=48000[z${k}];`; prev = c.at; });
f += `[0:a]atrim=start=${prev},asetpts=PTS-STARTPTS[a${cuts.length}];` + cuts.map((_, k) => `[a${k}][z${k}]`).join('') + `[a${cuts.length}]concat=n=${cuts.length * 2 + 1}:v=0:a=1[o]`;
fs.copyFileSync('.tmp/voice.wav', '.tmp/voice_raw.wav');
execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', '.tmp/voice_raw.wav', '-filter_complex', f, '-map', '[o]', '-c:a', 'pcm_s24le', '.tmp/voice.wav']);
fs.writeFileSync('.tmp/words.json', JSON.stringify(out));
console.log('пауз', cuts.length, 'сдвиг', sh.toFixed(2), 'последнее слово', out[out.length - 1].e);
