# Композиция: фон, слои, камера, переходы, motion blur (сабсэмплы, затвор 180°), события звука.
import math
import numpy as np, cv2
from .core import *
from .layers import Layer, ev

class Defocus:
    """Расфокус-переход вместо реза (ref-ui-card): сцена уходит в blur+zoom, новая приходит из blur+zoom.
    tc — момент склейки (старые слои кончаются, новые начинаются), dur 0.3–0.5 с."""
    def __init__(s, tc, dur=0.4, blur=22, zoom=0.06, name=None):
        s.tc, s.dur, s.blur, s.zoom = tc, dur, blur, zoom
        s.name = name or f'Переход расфокус {tc:.2f}'
    def active(s, t): return abs(t - s.tc) < s.dur / 2
    def apply(s, img, t):
        if not s.active(t): return img
        u = 1 - abs(t - s.tc) / (s.dur / 2)           # 0 → 1 (на склейке) → 0
        k = math.sin(u * math.pi / 2)
        b = s.blur * k
        if b > 0.3: img = cv2.GaussianBlur(img, (0, 0), b)
        z = 1 + s.zoom * k
        M = cv2.getRotationMatrix2D((img.shape[1] / 2, img.shape[0] / 2), 0, z)
        return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    def events(s):
        return [ev(s.tc, 'whoosh', s.name, -22, align='peak')]

class Comp:
    def __init__(s, dur, bg='#0B0B0C', w=W, h=H, fps=FPS, cam=None, bg2=None, name='comp'):
        s.dur, s.w, s.h, s.fps, s.name = dur, w, h, fps, name
        s.bg = hexc(bg) if isinstance(bg, str) else np.asarray(bg, np.float32)
        s.bg2 = (hexc(bg2) if isinstance(bg2, str) else bg2)    # вертикальный градиент без шума (no grain)
        s.cam = cam or STATIC
        s.layers, s.post, s.extra_events = [], [], []
        s.mb_threshold = 2.5        # px/кадр, с какой скорости включать motion blur
        s.mb_max = 12               # макс. сабсэмплов
        s._bgimg = None

    def add(s, *ls):
        for l in ls:
            (s.post if isinstance(l, Defocus) else s.layers).append(l)
        return ls[0] if len(ls) == 1 else ls

    def sfx(s, t, kind, name, db=-22, **kw):
        """Ручное событие, привязанное к видимому событию name (например, клик курсора)."""
        s.extra_events.append(ev(t, kind, name, db, **kw))

    def background(s):
        if s._bgimg is None:
            img = np.empty((s.h, s.w, 3), np.float32); img[:] = s.bg
            if s.bg2 is not None:
                v = np.linspace(0, 1, s.h, dtype=np.float32)[:, None, None]
                img[:] = s.bg * (1 - v) + s.bg2 * v
            s._bgimg = img
        return s._bgimg.copy()

    def _raw(s, t):
        cam = s.cam(t)
        img = s.background()
        for l in sorted(s.layers, key=lambda l: l.z):
            if l.alive(t): l.draw(img, t, cam if l.world else Cam())
        for p in s.post: img = p.apply(img, t)
        return img

    def speed(s, t):
        sp = s.cam.speed(t)
        for l in s.layers:
            if l.alive(t): sp = max(sp, l.motion(t) + (s.cam.speed(t) if l.world else 0))
        return sp

    def frame(s, n, mb=True):
        """Кадр n (float32 RGB). Motion blur: при движении быстрее порога — среднее сабсэмплов
        в окне затвора 180° (±¼ кадра), в покое — один чистый кадр (резкость)."""
        t = n / s.fps
        sp = s.speed(t) if mb else 0
        if sp < s.mb_threshold: return s._raw(t)
        k = int(min(s.mb_max, max(3, math.ceil(sp / 4))))
        acc = np.zeros((s.h, s.w, 3), np.float32)
        for i in range(k):
            acc += s._raw(t + ((i + 0.5) / k - 0.5) * 0.5 / s.fps)
        return acc / k

    def frame8(s, n):
        return (np.clip(s.frame(n), 0, 1) * 255 + 0.5).astype(np.uint8)

    def nframes(s): return int(round(s.dur * s.fps))

    # ---------- события звука ----------
    def cam_peaks(s, thr=14.0):
        sp = [(n / s.fps, s.cam.speed(n / s.fps)) for n in range(s.nframes())]
        return [(t, v) for (_, a), (t, v), (_, b) in zip(sp, sp[1:], sp[2:]) if v > thr and v >= a and v > b]

    def events(s):
        out = []
        for l in s.layers: out += l.events()
        for p in s.post: out += p.events()
        for t, v in s.cam_peaks():
            # вжух пиком в кадр пика скорости камеры, сила по скорости (sfx-expressive, docu-map)
            out.append(ev(t, 'whoosh_big' if v > 45 else 'whoosh', f'Камера {t:.2f}', -20 if v > 45 else -24,
                          align='peak', speed=round(v, 1)))
        out += s.extra_events
        return sorted(out, key=lambda e: e['t'])

    def holds(s):
        out = []
        for l in s.layers:
            for h in l.holds(): out.append((l.name,) + h)
        return out

    def issues(s):
        out = []
        for l in s.layers: out += l.issues()
        return out
