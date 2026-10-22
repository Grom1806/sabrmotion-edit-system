// node tools/mix.js — голос (.tmp/voice.wav, если есть) + SFX из .tmp/sfx_events.json (без музыки) → .tmp/audio.wav (−14 LUFS, TP −1.8)
// Карта звуков — sfx_map.json (папка библиотеки: env SABR_SFX или "root"). Каждый звук ставится по ЯКОРЮ:
// o — начало звука, p — пик (вжухи/удары пиком на событии). Для облачного теста без библиотеки: SABR_SYNTH=1 (шумовые заглушки).
const fs = require('fs'), { spawnSync } = require('child_process');
const { END } = JSON.parse(fs.readFileSync('.tmp/timing.json', 'utf8'));
const ev = JSON.parse(fs.readFileSync('.tmp/sfx_events.json', 'utf8'));
const CFG = JSON.parse(fs.readFileSync('sfx_map.json', 'utf8')), L = process.env.SABR_SFX || CFG.root;
const ff = a => { const r = spawnSync('ffmpeg', ['-hide_banner', '-nostats', ...a], { encoding: 'utf8', maxBuffer: 1 << 26 }); if (r.status !== 0) throw new Error(r.stderr.slice(-3000)); return r.stderr; };
const SYN = { tick: 'anoisesrc=d=0.03:c=white,highpass=f=2500,afade=t=out:d=0.02', tickS: 'anoisesrc=d=0.03:c=white,highpass=f=3500,afade=t=out:d=0.02',
  whoosh: 'anoisesrc=d=0.5:c=pink,bandpass=f=1500:w=1200,afade=t=in:d=0.2,afade=t=out:st=0.25:d=0.25', whooshBig: 'anoisesrc=d=0.8:c=pink,bandpass=f=900:w=900,afade=t=in:d=0.35,afade=t=out:st=0.4:d=0.4',
  impact: 'anoisesrc=d=0.4:c=brown,lowpass=f=300,afade=t=out:d=0.38', roll: 'anoisesrc=d=1.1:c=white,highpass=f=3000,tremolo=f=22:d=0.9,afade=t=out:st=0.9:d=0.2' };
const synth = k => { fs.mkdirSync('.tmp/synth', { recursive: true }); const f = `.tmp/synth/${k}.wav`;
  if (!fs.existsSync(f)) ff(['-y', '-f', 'lavfi', '-i', (SYN[k] || 'anoisesrc=d=0.12:c=pink,bandpass=f=1800:w=1500,afade=t=out:d=0.1') + ',lowpass=f=12000,afade=t=in:d=0.003', '-ar', '48000', f]); return f; };
const an = {}; const analyze = (f, tr) => an[f + tr] || (an[f + tr] = (() => { const r = spawnSync('ffmpeg', ['-v', 'error', ...(tr ? ['-t', String(tr)] : []), '-i', f, '-ac', '1', '-ar', '8000', '-f', 'f32le', '-'], { maxBuffer: 1 << 26 }); const b = r.stdout, n = b.length / 4, x = new Float32Array(b.buffer, b.byteOffset, n), w = 40, env = []; for (let i = 0; i + w <= n; i += w) { let q = 0; for (let j = 0; j < w; j++) q += x[i + j] * x[i + j]; env.push(Math.sqrt(q / w)); } const pk = Math.max(...env), th = pk * Math.pow(10, -25 / 20); return { o: env.findIndex(v => v >= th) * w / 8000, p: env.indexOf(pk) * w / 8000 }; })());
const hasVoice = fs.existsSync('.tmp/voice.wav');
const inputs = hasVoice ? ['-i', '.tmp/voice.wav'] : ['-f', 'lavfi', '-t', String(END), '-i', 'anullsrc=r=48000:cl=stereo'];
const idx = {}, cnt = {}, parts = [], log = [], synthUsed = new Set();
ev.forEach(([t, k, g, layer], i) => {
  const m = CFG.map[k]; if (!m) throw new Error('нет звука для вида ' + k + ' (sfx_map.json)');
  let f = L + m.f[(cnt[k] = (cnt[k] || 0) + 1) % m.f.length] + '.wav';
  if (!fs.existsSync(f)) { if (process.env.SABR_SYNTH) { f = synth(k); synthUsed.add(k); } else throw new Error('нет файла ' + f); }
  if (!(f in idx)) { idx[f] = Object.keys(idx).length + 1; inputs.push('-i', f); }
  const TR = m.trim, tr = TR ? `atrim=0:${TR},afade=t=out:st=${(TR - 0.15).toFixed(2)}:d=0.15,` : '';
  const [mode, off] = m.anch || ['o', 0], a = analyze(f, TR)[mode], raw = t + off - a, st = Math.max(0, raw), pre = raw < 0 ? `atrim=start=${(-raw).toFixed(3)},asetpts=PTS-STARTPTS,` : '';
  log.push(`${t.toFixed(2).padStart(6)} ${k.padEnd(7)} → старт ${st.toFixed(3)} (якорь ${mode}${off ? '+' + off : ''}, в файле ${a.toFixed(3)}) ${f.split('/').pop()} [${layer || ''}]`);
  // под голосом SFX тише (reading-time/sound-v2): тики −6 дБ, остальное −3 дБ
  const duck = hasVoice ? (/^tick/.test(k) ? -6 : -3) : 0;
  parts.push(`[${idx[f]}:a]${pre}${tr}aformat=sample_rates=48000:channel_layouts=stereo,volume=${g - 3 + duck}dB,adelay=${Math.round(st * 1000)}:all=1[s${i}]`);
});
parts.push(`[0:a]aformat=sample_rates=48000:channel_layouts=stereo,${hasVoice ? 'loudnorm=I=-15:TP=-2:LRA=9,' : ''}apad=whole_dur=${END}[v]`);
parts.push(`${ev.map((_, i) => `[s${i}]`).join('')}amix=inputs=${ev.length}:duration=longest:normalize=0[sfx0]`, `[sfx0]asplit=2[sfx][sfxo]`);
parts.push(`[v][sfx]amix=inputs=2:duration=longest:normalize=0,atrim=0:${END}[mx]`);
fs.writeFileSync('.tmp/mix_graph.txt', parts.join(';\n'));
fs.writeFileSync('.tmp/mix_inputs.json', JSON.stringify(inputs));
fs.writeFileSync('.tmp/mix_files.json', JSON.stringify(['voice', ...Object.keys(idx)]));
const outs = ['-map', '[mx]', '-c:a', 'pcm_s24le', '.tmp/mix_raw.wav', '-map', '[sfxo]', '-c:a', 'pcm_s24le', '.tmp/sfx_only.wav'];
try { ff(['-y', ...inputs, '-/filter_complex', '.tmp/mix_graph.txt', ...outs]); }                 // ffmpeg 7+
catch (e) { if (!/Unrecognized option|Option not found/.test(e.message)) throw e; ff(['-y', ...inputs, '-filter_complex_script', '.tmp/mix_graph.txt', ...outs]); }   // ffmpeg 6
const js = s => JSON.parse(s.match(/\{[^{}]*"input_i"[^{}]*\}/)[0]), pre = 'lowpass=f=17500,alimiter=limit=0.6:attack=2:release=60:level=false,';
const j1 = js(ff(['-i', '.tmp/mix_raw.wav', '-af', `${pre}loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json`, '-f', 'null', '-']));
const ln = `loudnorm=I=-14:TP=-2.5:LRA=11:measured_I=${j1.input_i}:measured_TP=${j1.input_tp}:measured_LRA=${j1.input_lra}:measured_thresh=${j1.input_thresh}:offset=${j1.target_offset}:linear=true:print_format=json`;
const j2 = js(ff(['-y', '-i', '.tmp/mix_raw.wav', '-af', `${pre}${ln},aresample=48000`, '-c:a', 'pcm_s24le', '.tmp/audio.wav']));
fs.writeFileSync('.tmp/sfx_placement.txt', log.join('\n'));
fs.writeFileSync('.tmp/sfx_audit.tsv', 'время_с\tкадр\tвид\tслой\tдБ\n' + ev.map(([t, k, g, l]) => `${t}\t${Math.round(t * 30)}\t${k}\t${l || ''}\t${g}`).join('\n') + '\n');
console.log(`${ev.length} SFX (${(ev.length / END).toFixed(2)}/с); мастер I=${j2.output_i} TP=${j2.output_tp} (${j2.normalization_type})` + (synthUsed.size ? ` | ЗАГЛУШКИ: ${[...synthUsed]}` : ''));
