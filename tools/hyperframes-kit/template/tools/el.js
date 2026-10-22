// ElevenLabs helper: ключ читается из toolkit/.env и никуда не выводится.
const fs = require('fs');
const KEY = fs.readFileSync('C:/Users/subhan/Desktop/subhan/claude-code-video-toolkit/.env', 'utf8').match(/^ELEVENLABS_API_KEY=(.*)$/m)[1].trim().replace(/^["']|["']$/g, '');
const api = async (path, opt = {}) => {
  const r = await fetch('https://api.elevenlabs.io' + path, { ...opt, headers: { 'xi-api-key': KEY, 'Content-Type': 'application/json', ...(opt.headers || {}) } });
  if (!r.ok) throw new Error(r.status + ' ' + (await r.text()).slice(0, 500));
  return r;
};
module.exports = { api };
