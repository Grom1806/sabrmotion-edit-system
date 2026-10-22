// node tools/tts.js <voice_id> <out_base> <text_file|-> [model] [stability]
// Пишет out_base.mp3 и out_base.json (alignment по символам). Ключ не выводится.
const fs = require('fs');
const { api } = require('./el.js');
const [vid, outb, tf, model = 'eleven_v4', stab = '0.35', pubOwner] = process.argv.slice(2);
const text = fs.readFileSync(tf, 'utf8').trim();
(async () => {
  const body = { text, model_id: model, voice_settings: { stability: +stab, similarity_boost: 0.8 } , language_code: 'ru' };
  const r = await api(`/v1/text-to-speech/${vid}/with-timestamps?output_format=mp3_44100_128`, { method: 'POST', body: JSON.stringify(body) });
  const j = await r.json();
  fs.writeFileSync(outb + '.mp3', Buffer.from(j.audio_base64, 'base64'));
  delete j.audio_base64; fs.writeFileSync(outb + '.json', JSON.stringify(j));
  console.log('ok', outb, r.headers.get('character-cost') || '');
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
