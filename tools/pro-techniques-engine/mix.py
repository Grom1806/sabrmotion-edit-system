# Звук: голос (без de-reverb; HPF, ясность, компрессия, де-эссер, -14 LUFS) + SFX из sfx_events.json
import json, subprocess, numpy as np, sys
D = sys.argv[1]; SR = 48000; T_END = 24.82
import os
# папка SFX: 2-й аргумент или SFX_DIR, по умолчанию assets\sfx рядом с проектом
SFXDIR = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('SFX_DIR', os.path.join(D, 'assets', 'sfx'))
def load(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True)
    if r.returncode or not r.stdout: sys.exit(f'не прочитан звук: {path}\n{r.stderr.decode(errors="replace")}')
    b = r.stdout
    return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-t', str(T_END), '-i', f'{D}/src.mp4', '-vn', '-af',
                'highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2.5,'
                'acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,deesser=i=0.35,'
                'loudnorm=I=-15:TP=-2:LRA=9,afade=t=out:st=24.55:d=0.25',
                '-ar', str(SR), '-ac', '2', f'{D}/voice.wav'], check=True)
voice = load(f'{D}/voice.wav')
N = int(T_END * SR); mix = np.zeros((N, 2), np.float32); mix[:len(voice)] += voice[:N]
# огибающая голоса для сайдчейна SFX (−4 дБ под речью)
env = np.abs(voice[:N, 0]); k = int(.05 * SR)
env = np.convolve(env, np.ones(k) / k, 'same'); env = np.pad(env, (0, N - len(env)))
duck = 1 - 0.37 * np.clip(env / (env.max() * .25), 0, 1)
ev = json.load(open(f'{D}/sfx_events.json')); cache = {}; rows = []
for e in ev:
    if e['f'] not in cache: cache[e['f']] = load(f"{SFXDIR}/{e['f']}")
    x = cache[e['f']]
    if abs(e['pitch']) > .01:   # ±полутон: ресемплинг
        r = 2 ** (e['pitch'] / 12); idx = np.arange(0, len(x) - 1, r)
        x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32)
    off = 0
    if e['align'] == 'peak':    # пик звука ровно в кадр события
        a = np.abs(x).mean(1); off = int(np.argmax(np.convolve(a, np.ones(480) / 480, 'same')))
    g = 10 ** (e['db'] / 20); pan = e['pan']
    gl, gr = g * np.sqrt((1 - pan) / 2) * 1.414, g * np.sqrt((1 + pan) / 2) * 1.414
    s0 = int(e['t'] * SR) - off
    y = x.copy(); y[:, 0] *= gl; y[:, 1] *= gr
    a0, b0 = max(0, s0), min(N, s0 + len(y))
    if b0 <= a0: continue
    seg = y[a0 - s0:b0 - s0] * duck[a0:b0, None]
    mix[a0:b0] += seg
    rows.append((e['t'], e['key'], e['f'], e['db']))
peak = np.abs(mix).max()
if peak > .89: mix *= .89 / peak
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_s16le', f'{D}/mix.wav'], input=mix.tobytes(), check=True)
with open(f'{D}/sfx_audit.tsv', 'w') as f:
    f.write('время_с\tкадр\tсобытие\tфайл\tдБ\n')
    for t, k, fn, db in rows: f.write(f'{t:.3f}\t{round(t * 30000 / 1001)}\t{k}\t{fn}\t{db}\n')
print('sfx', len(rows), 'peak', peak)
