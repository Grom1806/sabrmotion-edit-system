// node tools/words.js take2 1.1 → .tmp/voice.wav (темп ×1.1) + .tmp/words.json [{w,t,e,line}]
const fs = require('fs'); const { execFileSync } = require('child_process');
const [take = 'take2', tempo = '1.1'] = process.argv.slice(2), K = +tempo;
const a = JSON.parse(fs.readFileSync(`.tmp/vo/${take}.json`)).alignment;
const ch = a.characters, s = a.character_start_times_seconds, e = a.character_end_times_seconds;
const words = []; let cur = null, inTag = false, line = 0;
for (let i = 0; i < ch.length; i++) {
  const c = ch[i];
  if (c === '[') { inTag = true; continue; } if (inTag) { if (c === ']') inTag = false; continue; }
  if (c === '\n') { line++; }
  if (/\s/.test(c)) { if (cur) { words.push(cur); cur = null; } continue; }
  if (!cur) cur = { w: '', t: s[i], e: e[i], line };
  cur.w += c; cur.e = e[i];
}
if (cur) words.push(cur);
words.forEach(w => { w.t = +(w.t / K).toFixed(3); w.e = +(w.e / K).toFixed(3); });
fs.writeFileSync('.tmp/words.json', JSON.stringify(words));
execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', `.tmp/vo/${take}.mp3`, '-af', `atempo=${K},aresample=48000,highpass=f=80,equalizer=f=260:t=q:w=1:g=-2.5,equalizer=f=3400:t=q:w=1.2:g=3,highshelf=f=9000:g=2,deesser=i=0.35,acompressor=threshold=-20dB:ratio=2.6:attack=8:release=120:makeup=2`, '-ac', '1', '-c:a', 'pcm_s24le', '.tmp/voice.wav']);
console.log(words.map(w => `${w.line}:${w.w}@${w.t}`).join(' '));
