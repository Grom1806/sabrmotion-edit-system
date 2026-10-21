# голос (уже обработан words.js: EQ, де-эссер, компрессор; без de-reverb) + SFX → −14 LUFS
import json, subprocess, numpy as np, sys
SR = 48000; SFX = '/mnt/user-data/uploads/claude-edit/assets/sfx'; T_END = float(sys.argv[1])
def load(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
voice = load('voice_proc.wav'); N = int(T_END * SR)
mix = np.zeros((N, 2), np.float32); mix[:min(N, len(voice))] += voice[:N] * 10 ** (-1 / 20)
env = np.abs(voice[:N, 0]); k = int(.05 * SR); env = np.convolve(env, np.ones(k) / k, 'same'); env = np.pad(env, (0, max(0, N - len(env))))
duck = 1 - 0.35 * np.clip(env / (env.max() * .25), 0, 1)
rows = []; cache = {}
for e in json.load(open('sfx_events30.json')):
    if e['f'] not in cache: cache[e['f']] = load(f"{SFX}/{e['f']}")
    x = cache[e['f']]
    if abs(e['pitch']) > .01:
        r = 2 ** (e['pitch'] / 12); idx = np.arange(0, len(x) - 1, r)
        x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32)
    if e.get('dur'):
        m = int(e['dur'] * SR); x = x[:m].copy(); fo = min(int(.12 * SR), len(x)); x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    off = 0
    if e['align'] == 'peak':
        a = np.abs(x).mean(1); off = int(np.argmax(np.convolve(a, np.ones(480) / 480, 'same')))
    g = 10 ** (e['db'] / 20); pan = e['pan']
    y = x.copy(); y[:, 0] *= g * np.sqrt((1 - pan) / 2) * 1.414; y[:, 1] *= g * np.sqrt((1 + pan) / 2) * 1.414
    s0 = int(e['t'] * SR) - off; a0, b0 = max(0, s0), min(N, s0 + len(y))
    if b0 <= a0: continue
    mix[a0:b0] += y[a0 - s0:b0 - s0] * duck[a0:b0, None]; rows.append(e)
fo = int(0.4 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_f32le', 'mix_raw.wav'], input=mix.tobytes(), check=True)
# двухпроходная нормализация в −14 LUFS
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', 'mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
j = json.loads(r.stderr[r.stderr.rindex('{'):])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'mix_raw.wav', '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
                '-ar', str(SR), '-c:a', 'pcm_s16le', 'mix30.wav'], check=True)
with open('sfx_audit30.tsv', 'w') as f:
    f.write('время_с\tкадр\tсобытие\tфайл\tдБ\n')
    for e in rows: f.write(f"{e['t']:.3f}\t{round(e['t'] * 30)}\t{e['key']}\t{e['f']}\t{e['db']}\n")
print('sfx', len(rows))
