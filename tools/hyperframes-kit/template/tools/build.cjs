// node tools/build.cjs <name> [--take take2 --tempo 1.1] [--draft] [--skip-render]
// Полный прогон системы «без AE»: (words → gaps →) inject → dump → mix → verify_solo → check → render → master/light → QA → лист.
const fs = require('fs'), { spawnSync } = require('child_process');
const a = process.argv.slice(2), name = a[0] && !a[0].startsWith('--') ? a[0] : 'reel', opt = k => { const i = a.indexOf('--' + k); return i >= 0 ? (a[i + 1] && !a[i + 1].startsWith('--') ? a[i + 1] : true) : null; };
const HF = ['--yes', 'hyperframes@0.8.140'];
const run = (cmd, args, must = true) => { console.log('\n▶', cmd, args.join(' ')); const r = spawnSync(cmd, args, { stdio: 'inherit', shell: process.platform === 'win32' }); if (must && r.status !== 0) { console.error('✖ шаг упал:', cmd, args.join(' ')); process.exit(1); } return r.status; };
fs.mkdirSync('.tmp', { recursive: true }); fs.mkdirSync('out', { recursive: true });
if (opt('take')) { run('node', ['tools/words.js', opt('take'), opt('tempo') || '1.0']); run('node', ['tools/gaps.js']); }
if (fs.existsSync('.tmp/words.json')) run('node', ['tools/inject.js']);
run('node', ['tools/dump.js']);
run('node', ['tools/mix.js']);
run('node', ['tools/verify_solo.cjs'], false);
run('npx', [...HF, 'check', '.'], false);
if (opt('skip-render')) process.exit(0);
const draft = !!opt('draft');
run('npx', [...HF, 'render', '.', '-o', '.tmp/render.mp4', '--quality', draft ? 'draft' : 'delivery', ...(draft ? [] : ['--crf', '8'])]);
const enc = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart'];
const src = ['-i', '.tmp/render.mp4', '-i', '.tmp/audio.wav', '-map', '0:v', '-map', '1:a', '-shortest'];
if (draft) { run('ffmpeg', ['-v', 'error', '-y', ...src, ...enc, '-crf', '23', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '192k', `out/${name}_draft.mp4`]); process.exit(0); }
run('ffmpeg', ['-v', 'error', '-y', ...src, ...enc, '-crf', '14', '-preset', 'slow', '-c:a', 'aac', '-b:a', '320k', `out/${name}_master.mp4`]);
run('ffmpeg', ['-v', 'error', '-y', ...src, ...enc, '-crf', '18', '-preset', 'slow', '-c:a', 'aac', '-b:a', '256k', `out/${name}_1080.mp4`]);
run('ffmpeg', ['-v', 'error', '-y', '-i', `out/${name}_master.mp4`, '-vf', `fps=12/${JSON.parse(fs.readFileSync('.tmp/stats.json')).END},scale=270:480,tile=6x2`, '-frames:v', '1', `out/${name}_sheet.jpg`]);
process.exit(run('node', ['tools/qa.cjs', name], false));
