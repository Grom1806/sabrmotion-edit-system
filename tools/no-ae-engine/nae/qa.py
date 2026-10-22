# Автопроверка перед показом (аналог ae_sharp_preflight.jsx + sharpcheck.py + аудиты SFX/чтения):
# без «PASS» ролик пользователю не показываем (sharpness-guard, qa-frame-by-frame, sfx-expressive, reading-time).
import json, subprocess, math, os
import numpy as np, cv2
from .core import W, H, FPS
from .layers import Text, Counter

def sharp(img8):
    g = cv2.cvtColor(img8, cv2.COLOR_RGB2GRAY).astype(np.float32)
    gx, gy = cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)
    return float(np.mean((gx * gx + gy * gy) / 255.0 / 16))

def video_frame(path, t, w=W, h=H):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.4f}', '-i', path, '-frames:v', '1', '-vf', f'scale={w}:{h}:flags=lanczos',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8)[:w * h * 3].reshape(h, w, 3)

def loudness(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    tail = r[r.rindex('Summary:'):]
    I = float(tail.split('I:')[1].split('LUFS')[0]); TP = float(tail.split('Peak:')[1].split('dBFS')[0])
    return I, TP

def norm_read(words, kind):
    """reading-time.md: без голоса 0.6 + 0.2/слово (+0.3 числа/UI, +0.6 CTA)."""
    return 0.6 + 0.2 * words + (0.3 if kind in ('number', 'ui') else 0) + (0.6 if kind == 'cta' else 0)

def rest_times(comp):
    """Моменты покоя для проверки резкости: надпись полностью видна, камера стоит, motion blur не нужен."""
    out = []
    for l in comp.layers:
        if isinstance(l, Text):
            t = l.t_full + 0.25
            end = l.t_out if l.t_out is not None else comp.dur
            while t < end - 0.05 and comp.speed(t) >= comp.mb_threshold: t += 0.1
            if t < end - 0.05 and not any(p.active(t) for p in comp.post): out.append(round(t * FPS) / FPS)
    return sorted(set(out))[:12]

def run(comp, outdir, master, light, mix_wav=None, events=None, voice=False, ref_tempo=False):
    os.makedirs(f'{outdir}/qa', exist_ok=True)
    R, fails = [], 0
    def row(sec, ok, msg):
        nonlocal fails
        fails += 0 if ok else 1; R.append(f"| {sec} | {'ok' if ok else '**FAIL**'} | {msg} |")
    # 1. апскейл и прочие проблемы слоёв (аналог preflight)
    iss = comp.issues(); row('Слои: апскейл/растр', not iss, '; '.join(iss) or 'нет апскейла растров')
    # 2. резкость: кадр рендера vs кадр видео (≥ 0.9 — иначе виноват экспорт), кадры покоя без блюра
    ts = rest_times(comp); worst = (9, None)
    sheet = []
    for t in ts:
        ref = comp.frame8(int(round(t * FPS)))
        cv2.imwrite(f'{outdir}/qa/ref_{t:05.2f}.png', cv2.cvtColor(ref, cv2.COLOR_RGB2BGR))
        sr = sharp(ref)
        for name, p in (('master', master), ('light', light)):
            if p and os.path.exists(p):
                r = sharp(video_frame(p, t + 0.5 / FPS)) / max(sr, 1e-6)
                if r < worst[0]: worst = (r, f'{name} @ {t:.2f} с')
        sheet.append(sr)
    if ts:
        row('Резкость экспорта (sharpcheck)', worst[0] >= 0.9, f'мин. отношение видео/рендер {worst[0]:.2f} ({worst[1]}), кадров {len(ts)}')
        med = float(np.median(sheet)); soft = [f'{t:.2f}' for t, v in zip(ts, sheet) if v < 0.6 * med]
        row('Резкость кадров покоя', not soft, ('мягче 60 % медианы: ' + ', '.join(soft)) if soft else f'медиана {med:.2f}, все ≥ 60 %')
    # 3. нет зерна/мерцания: два соседних кадра покоя почти идентичны
    noise = []
    for t in ts[:6]:
        n = int(round(t * FPS))
        if comp.speed(t) < 0.01 and comp.speed(t + 1 / FPS) < 0.01:
            a = video_frame(master, (n + 0.5) / FPS).astype(np.float32); b = video_frame(master, (n + 1.5) / FPS).astype(np.float32)
            noise.append(float(np.abs(a - b).mean()))
    if noise: row('Без зерна/шума (кадр к кадру в покое)', max(noise) < 0.8, f'средняя разница {max(noise):.2f} уровня из 255')
    # 4. время чтения
    rt = ['| надпись | слов | норма, с | видна, с | ок |', '|---|---|---|---|---|']; bad = 0
    byname = {l.name: l for l in comp.layers}
    def gone(l, t_full, t_out):
        # момент, когда надпись реально пропала: уход (t_out) или камера увезла её за кадр
        end = t_out if t_out is not None else comp.dur
        if not l.world: return end
        for n in range(int(t_full * FPS) + 1, int(end * FPS)):
            cam = comp.cam(n / FPS); x, y = cam.pt(l.x, l.y)
            if y < -l.size or y > H or x < -200 or x > W + 200: return n / FPS
        return end
    for name, txt, words, t_full, t_out, kind in comp.holds():
        if kind in ('service', 'caption'): continue
        vis = gone(byname[name], t_full, t_out) - t_full
        need = norm_read(words, kind); ok = vis + 1e-6 >= need or voice or ref_tempo
        bad += 0 if ok else 1
        rt.append(f'| {txt[:40]} | {words} | {need:.1f} | {vis:.2f} | {"да" if ok else "НЕТ"} |')
    open(f'{outdir}/qa/reading_time.md', 'w').write('\n'.join(rt) + '\n')
    row('Время чтения', bad == 0, f'{bad} надписей уходят раньше нормы' if bad else 'все надписи держатся по норме' + (' (голос/темп референса — норма по фразе)' if voice or ref_tempo else ''))
    # 5. буква = тик
    events = events if events is not None else comp.events()
    mism = []
    for l in comp.layers:
        if type(l) is Text and l.mode == 'letters' and l.sfx:
            n = sum(1 for e in events if e['layer'] == l.name and e['kind'] == 'tick')
            if n != l.letters(): mism.append(f'{l.name}: букв {l.letters()}, тиков {n}')
    row('Буква = тик', not mism, '; '.join(mism) or 'в каждой побуквенной надписи тиков = букв')
    # 6. нет звуков без события
    names = {l.name: l for l in comp.layers}
    orphan = []
    for e in events:
        l = names.get(e['layer'])
        if l is None:
            if not (e['layer'].startswith('Камера') or e['layer'].startswith('Переход') or any(getattr(p, 'name', '') == e['layer'] for p in comp.post)):
                orphan.append(f"{e['t']:.2f} {e['layer']}")
        elif not l.alive(e['t']) and not l.alive(e['t'] + 1 / FPS):
            orphan.append(f"{e['t']:.2f} {e['layer']} (слоя нет в кадре)")
    row('Нет звуков без события', not orphan, '; '.join(orphan[:6]) or f'{len(events)} событий, все привязаны к видимым слоям')
    # 7. нет «каши»: окна 0.25 с с ≥5 громкими (не тики) звуками
    loud = sorted(e['t'] for e in events if e['kind'] != 'tick' and e.get('db', -22) > -26)
    burst = [f'{a:.2f}' for i, a in enumerate(loud) if sum(1 for b in loud[i:] if b - a < 0.25) >= 5]
    row('Нет звуковой каши', not burst, ('окна: ' + ', '.join(burst[:5])) if burst else 'нет окон 0.25 с с ≥5 акцентами')
    # 8. текст не уходит/камера не едет, пока надпись проявляется
    conf = []
    moves = comp.cam.moves()
    for l in comp.layers:
        r = l.reveal()
        if not r: continue
        if l.t_out is not None and l.t_out < r[1] - 1e-6: conf.append(f'{l.name}: уходит до полного проявления')
        for a, b in moves:
            if r[0] + 0.05 < a < r[1] - 0.05 and l.world: conf.append(f'{l.name}: камера стартует {a:.2f} во время проявления')
    open(f'{outdir}/qa/reveal_conflicts.txt', 'w').write('\n'.join(conf) or 'нет')
    row('Проявление не прерывается', not conf, '; '.join(conf[:4]) or 'нет')
    # 9. поля: надписи в покое не ближе 60 px к краю
    edge = []
    for l in comp.layers:
        if isinstance(l, Text) and not isinstance(l, Counter):
            from .core import layout
            wd = max(layout(ln, l.font, l.size)[1] for ln in l.lines)
            x0 = l.x - {'l': 0, 'c': 0.5, 'r': 1}[l.anchor] * wd
            cam = comp.cam(l.t_full + 0.3) if l.world else None
            if cam: (sx0, _), (sx1, _) = cam.pt(x0, l.y), cam.pt(x0 + wd, l.y)
            else: sx0, sx1 = x0, x0 + wd
            if sx0 < 60 - 1 or sx1 > W - 60 + 1: edge.append(f'{l.name} ({sx0:.0f}…{sx1:.0f})')
    row('Поля ≥ 60 px', not edge, '; '.join(edge[:4]) or 'все надписи в полях')
    # 10. первый кадр не пустой
    f0 = comp.frame8(0)
    row('Первый кадр не пустой', float(f0.std()) > 2.0 or any(l.alive(0) for l in comp.layers if not isinstance(l, Text)),
        f'std {f0.std():.1f}')
    # 11. громкость
    if mix_wav and os.path.exists(mix_wav):
        I, TP = loudness(master if master else mix_wav)
        row('Громкость −14 LUFS, TP ≤ −1', abs(I + 14) <= 1.0 and TP <= -1.0, f'I {I:.1f} LUFS, TP {TP:.1f} dBTP')
    rep = ['# QA движка без AE', '', f'Итог: **{"PASS" if fails == 0 else f"FAIL ({fails})"}**', '',
           '| проверка | статус | детали |', '|---|---|---|'] + R
    open(f'{outdir}/qa/report.md', 'w').write('\n'.join(rep) + '\n')
    return fails == 0, '\n'.join(rep)
