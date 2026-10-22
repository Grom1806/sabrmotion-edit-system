// node tools/dump.js — headless Chrome выполняет таймлайн и отдаёт #sfx-dump и #stats-dump
// → .tmp/sfx_events.json, .tmp/stats.json. Chrome: env CHROME, .tmp/chrome_path.txt или стандартные пути.
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
fs.mkdirSync('.tmp', { recursive: true });
const cands = [process.env.CHROME, fs.existsSync('.tmp/chrome_path.txt') && fs.readFileSync('.tmp/chrome_path.txt', 'utf8').trim().replace(/^\/c\//, 'C:/'),
  'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/opt/pw-browsers/chromium', '/usr/bin/chromium', '/usr/bin/google-chrome'].filter(Boolean);
let ch = cands.find(p => fs.existsSync(p) && fs.statSync(p).isFile());
if (!ch) for (const p of cands) if (fs.existsSync(p) && fs.statSync(p).isDirectory()) {   // папка playwright
  const f = require('child_process').execSync(`find ${p} -type f \\( -name chrome -o -name headless_shell \\) | head -1`).toString().trim(); if (f) { ch = f; break; } }
if (!ch) throw new Error('не найден Chrome: задай env CHROME или .tmp/chrome_path.txt');
const url = 'file:///' + path.resolve('index.html').split(path.sep).join('/').replace(/^\//, '');
const s = execFileSync(ch, ['--headless', '--no-sandbox', '--allow-file-access-from-files', '--virtual-time-budget=10000', '--dump-dom', url],
  { encoding: 'utf8', maxBuffer: 1 << 26, stdio: ['ignore', 'pipe', 'ignore'] });
const g = id => s.split(`id="${id}">`)[1].split('</script>')[0];
fs.writeFileSync('.tmp/sfx_events.json', g('sfx-dump')); fs.writeFileSync('.tmp/stats.json', g('stats-dump'));
const ev = JSON.parse(g('sfx-dump')), st = JSON.parse(g('stats-dump')), k = {}; ev.forEach(e => k[e[1]] = (k[e[1]] || 0) + 1);
fs.writeFileSync('.tmp/timing.json', JSON.stringify({ END: st.END }));   // END из композиции (inject.js его уже вписал)
console.log('END', st.END, '| событий/с', st.perSec, '| SFX', ev.length, JSON.stringify(k)); (st.warn || []).forEach(w => console.log('ВНИМАНИЕ:', w));
