# Микшер: голос (уже обработан по voice-processing — без de-reverb) + SFX из events.json → −14 LUFS, TP ≤ −1.
# Звук по типу события берётся из библиотеки claude-edit\assets\sfx (карта sfx_map.json);
# если библиотеки нет (облако, тест) — синтезирует нетональную заглушку и пишет это в отчёт.
import json, os, subprocess, math
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))

def load(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()

# ---------- нетональные заглушки (только если нет библиотеки) ----------
def _noise(n, seed): return np.random.default_rng(seed).standard_normal(n).astype(np.float32)
def _bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)
def _norm(x): return x / (np.abs(x).max() + 1e-9) * 0.9
def synth(kind, seed=0):
    if kind == 'tick':
        n = int(0.025 * SR); x = _bp(_noise(n, seed), 2500, 9000) * np.exp(-np.arange(n) / (0.003 * SR))
    elif kind in ('pop', 'click'):
        n = int(0.06 * SR); x = _bp(_noise(n, seed), 600, 4000) * np.exp(-np.arange(n) / (0.008 * SR))
    elif kind in ('card', 'swish', 'grow'):
        n = int(0.18 * SR); e = np.sin(np.linspace(0, np.pi, n)) ** 2
        x = _bp(_noise(n, seed), 800, 6000) * e
    elif kind == 'stroke':
        n = int(0.4 * SR); x = _bp(_noise(n, seed), 1500, 7000) * (0.4 + 0.6 * np.abs(np.sin(np.linspace(0, 9, n))))
    elif kind in ('whoosh', 'whoosh_big'):
        n = int((0.6 if kind == 'whoosh_big' else 0.4) * SR); e = np.exp(-((np.linspace(-1, 1, n)) ** 2) * 6)
        x = _bp(_noise(n, seed), 300, 5000) * e
    elif kind == 'impact':
        n = int(0.35 * SR); x = _bp(_noise(n, seed), 40, 400) * np.exp(-np.arange(n) / (0.06 * SR))
    elif kind == 'counter':
        n = int(1.2 * SR); x = np.zeros(n, np.float32)
        for i, t in enumerate(np.cumsum(np.linspace(0.03, 0.09, 24))):
            a = int(t * SR)
            if a + 600 < n: x[a:a + 600] += _bp(_noise(600, seed + i), 2500, 8000) * np.exp(-np.arange(600) / 90)
    else:
        n = int(0.1 * SR); x = _bp(_noise(n, seed), 500, 5000) * np.exp(-np.arange(n) / (0.02 * SR))
    x = _norm(x); return np.stack([x, x], 1)

def mix(events, out_wav, dur, voice=None, sfx_root=None, sfx_map=None, audit=None, voice_db=-1.0, duck=0.35):
    sfx_map = sfx_map or json.load(open(os.path.join(HERE, '..', 'sfx_map.json')))
    N = int(dur * SR); buf = np.zeros((N, 2), np.float32)
    env = np.zeros(N, np.float32)
    if voice:
        v = load(voice)[:N]; buf[:len(v)] += v * 10 ** (voice_db / 20)
        a = np.abs(v[:, 0]); k = int(0.05 * SR); a = np.convolve(a, np.ones(k) / k, 'same')
        env[:len(a)] = a / (a.max() * 0.25 + 1e-9)
    ducking = 1 - duck * np.clip(env, 0, 1)                   # сайдчейн: SFX тише под голосом
    cache, rows, synth_used = {}, [], set()
    for i, e in enumerate(events):
        kind = e['kind']; spec = sfx_map.get(kind, sfx_map.get('default'))
        files = spec['files']; f = files[i % len(files)] if spec.get('rotate') else files[0]
        path = os.path.join(sfx_root, f) if sfx_root else None
        key = path if path and os.path.exists(path) else f'synth:{kind}'
        if key not in cache:
            cache[key] = load(path) if key == path else synth(kind, len(cache))
            if key.startswith('synth'): synth_used.add(kind)
        x = cache[key]
        if abs(e.get('pitch', 0)) > 0.01:
            r = 2 ** (e['pitch'] / 12); idx = np.arange(0, len(x) - 1, r)
            x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32)
        if e.get('dur'):
            m = max(int(e['dur'] * SR), 1); x = x[:m].copy(); fo = min(int(0.1 * SR), len(x)); x[-fo:] *= np.linspace(1, 0, fo)[:, None]
        off = 0
        if e.get('align', spec.get('align')) == 'peak':
            a = np.abs(x).mean(1); off = int(np.argmax(np.convolve(a, np.ones(480) / 480, 'same')))
        db = e.get('db', spec.get('db', -22)) + (-6 if kind == 'tick' and voice else (-3 if voice else 0))
        g = 10 ** (db / 20); pan = e.get('pan', 0.0)
        y = x * g; y[:, 0] *= math.sqrt((1 - pan) / 2) * 1.414; y[:, 1] *= math.sqrt((1 + pan) / 2) * 1.414
        s0 = int(round(e['t'] * SR)) - off; a0, b0 = max(0, s0), min(N, s0 + len(y))
        if b0 <= a0: continue
        buf[a0:b0] += y[a0 - s0:b0 - s0] * ducking[a0:b0, None]
        rows.append((e, key, db, off / SR))
    fo = int(0.3 * SR); buf[-fo:] *= np.linspace(1, 0, fo)[:, None]
    raw = out_wav + '.raw.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_f32le', raw],
                   input=buf.tobytes(), check=True)
    loudnorm(raw, out_wav); os.remove(raw)
    if audit:
        with open(audit, 'w') as fh:
            fh.write('время_с\tкадр\tсобытие\tслой\tтип\tфайл\tдБ\n')
            for e, key, db, off in rows:
                fh.write(f"{e['t']:.3f}\t{round(e['t'] * 30)}\t{e.get('unit', '')}\t{e['layer']}\t{e['kind']}\t{key}\t{db}\n")
    return dict(n=len(rows), synth=sorted(synth_used))

def loudnorm(src, dst, I=-14, TP=-1.5):
    """Двухпроходный loudnorm (как в мастерах Бухари/демо): точнее однопроходного."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', f'loudnorm=I={I}:TP={TP}:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rindex('{'):])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af',
                    f"loudnorm=I={I}:TP={TP}:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
                    f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
                    '-ar', str(SR), '-c:a', 'pcm_s16le', dst], check=True)
