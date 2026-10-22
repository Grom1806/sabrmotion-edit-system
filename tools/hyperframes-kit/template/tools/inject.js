// node tools/inject.js — вставляет .tmp/words.json в index.html, ставит END (последнее слово + 1.4 с), пишет .tmp/timing.json
const fs = require('fs');
const raw = JSON.parse(fs.readFileSync('.tmp/words.json', 'utf8')), W = raw.map(({ w, t, e, line }) => ({ w, t, e, line }));
const END = Math.round((raw[raw.length - 1].e + 0.72) * 10) / 10;
const f = 'index.html'; let s = fs.readFileSync(f, 'utf8');
s = s.replace(/(\/\/ <words>[^\n]*\n)[\s\S]*?(\n\s*\/\/ <\/words>)/, `$1      var WORDS = ${JSON.stringify(W)};$2`)
  .replace(/\/\*END\*\/[\d.]+\/\*\/END\*\//, `/*END*/${END}/*/END*/`)
  .replace(/(data-composition-id="main"[^>]*data-duration=")[\d.]+"/, `$1${END}"`);
fs.writeFileSync(f, s); fs.writeFileSync('.tmp/timing.json', JSON.stringify({ END }));
console.log('words', W.length, 'END', END);
