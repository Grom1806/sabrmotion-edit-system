// node tools/sfxgen.js <name> <seconds> "<prompt>" → assets/sfx/<name>.wav (ElevenLabs sound generation)
const fs = require('fs'), { execFileSync } = require('child_process'); const { api } = require('./el.js');
const [name, dur, prompt] = process.argv.slice(2);
(async () => {
  const r = await api('/v1/sound-generation', { method: 'POST', body: JSON.stringify({ text: prompt, duration_seconds: +dur, prompt_influence: 0.6 }) });
  fs.writeFileSync(`.tmp/${name}.mp3`, Buffer.from(await r.arrayBuffer()));
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', `.tmp/${name}.mp3`, '-ar', '48000', `assets/sfx/${name}.wav`]); console.log('ok', name);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
