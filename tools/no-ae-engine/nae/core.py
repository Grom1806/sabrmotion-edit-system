# Ядро движка «монтаж без After Effects»: кривые, камера, композиция, растр текста/форм.
# Всё считается во float32 RGB 0..1, кадр 1080×1920 по умолчанию. Нормы vault: motion-v3 (кривые 40–55 %,
# bounce со снапом 0.7 с), sharpness-guard (в покое масштаб ровно 1, блюр 0, целые пиксели, без зерна).
import math, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

FPS = 30
W, H = 1080, 1920

# ---------- время и кривые ----------
def clamp(x, a=0.0, b=1.0): return a if x < a else (b if x > b else x)
def prog(t, t0, t1): return clamp((t - t0) / max(1e-9, t1 - t0))
def lerp(a, b, u): return a + (b - a) * u

@functools.lru_cache(maxsize=None)
def bezier(x1, y1, x2, y2):
    """cubic-bezier как в CSS/AE (influence → x1 и 1−x2). Возвращает f(u)->v."""
    def bx(s): return 3 * x1 * s * (1 - s) ** 2 + 3 * x2 * s * s * (1 - s) + s ** 3
    def by(s): return 3 * y1 * s * (1 - s) ** 2 + 3 * y2 * s * s * (1 - s) + s ** 3
    def dbx(s): return 3 * x1 * (1 - s) ** 2 + 6 * (x2 - x1) * s * (1 - s) + 3 * (1 - x2) * s * s
    def f(u):
        if u <= 0: return 0.0
        if u >= 1: return 1.0
        s = u
        for _ in range(8):
            d = dbx(s)
            if abs(d) < 1e-6: break
            s = clamp(s - (bx(s) - u) / d)
        lo, hi = 0.0, 1.0
        for _ in range(20):  # страховка бисекцией
            if abs(bx(s) - u) < 1e-6: break
            if bx(s) < u: lo = s
            else: hi = s
            s = (lo + hi) / 2
        return by(s)
    return f

# Базовая кривая (измерено по рефам профи 2026-10-21: влияние 40–55 %, пик ≈2× средней)
EASE = bezier(0.5, 0.1, 0.4, 0.9)
# Камера: резко уходит из ключа (1–5 %), долго досаживается (35–80 %)
EASE_CAM = bezier(0.05, 0.0, 0.35, 1.0)
# Спокойный проезд 50/50
EASE_SOFT = bezier(0.5, 0.0, 0.5, 1.0)
# Акцент (expo-out) — только для отдельных ударов, не по умолчанию
EASE_ACCENT = bezier(0.16, 1.0, 0.3, 1.0)
EASE_IN = bezier(0.5, 0.0, 0.9, 0.6)

def bounce(t_after, amp=0.08, freq=2.5, decay=6.0):
    """Затухающее колебание после ключа (доля). Снап на 0.7 с — ровно 0, иначе «вечные 99.9 %» = мыло."""
    if t_after <= 0 or t_after >= 0.7: return 0.0
    return amp * math.sin(freq * t_after * 2 * math.pi) / math.exp(decay * t_after)

def pop_scale(t, t0, dur=0.4, amp=0.08):
    """0 → 100 % с одним мягким перелётом героя; после t0+dur+0.7 ровно 1.0."""
    if t < t0: return 0.0
    u = prog(t, t0, t0 + dur)
    if u < 1: return EASE_ACCENT(u)
    return 1.0 + bounce(t - t0 - dur, amp)

def kf(t, keys, ease=EASE):
    """Ключи [(t, v), ...] (v — число или кортеж). Между ключами — кривая ease."""
    if t <= keys[0][0]: return keys[0][1]
    for (ta, va), (tb, vb) in zip(keys[:-1], keys[1:]):
        if t <= tb:
            u = ease(prog(t, ta, tb))
            if isinstance(va, tuple): return tuple(lerp(a, b, u) for a, b in zip(va, vb))
            return lerp(va, vb, u)
    return keys[-1][1]

# ---------- цвет ----------
def hexc(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255

# ---------- камера ----------
class Cam:
    """2D-камера: центр (cx, cy) в координатах мира и зум z. Мир = экран при cx=W/2, cy=H/2, z=1."""
    def __init__(s, cx=W / 2, cy=H / 2, z=1.0):
        s.cx, s.cy, s.z = cx, cy, z
    def pt(s, x, y):
        return (x - s.cx) * s.z + W / 2, (y - s.cy) * s.z + H / 2
    @property
    def at_rest(s):
        return abs(s.z - 1.0) < 1e-9

class CamTrack:
    """Ключи камеры [(t, cx, cy, z)]. Проезды между «станциями»; на станции зум ровно 1.0 (резкость)."""
    def __init__(s, keys, ease=EASE_CAM):
        s.keys = sorted(keys); s.ease = ease
    def __call__(s, t):
        k = s.keys
        if t <= k[0][0]: return Cam(*k[0][1:])
        for a, b in zip(k[:-1], k[1:]):
            if t <= b[0]:
                u = s.ease(prog(t, a[0], b[0]))
                z = math.exp(lerp(math.log(a[3]), math.log(b[3]), u))
                return Cam(lerp(a[1], b[1], u), lerp(a[2], b[2], u), z)
        return Cam(*k[-1][1:])
    def moves(s):
        """Интервалы движения (t0, t1) — для вжухов и QA конфликтов с проявлением текста."""
        return [(a[0], b[0]) for a, b in zip(s.keys[:-1], s.keys[1:]) if a[1:] != b[1:]]
    def speed(s, t, dt=1 / FPS):
        a, b = s(t), s(t + dt)
        return math.hypot(b.cx - a.cx, b.cy - a.cy) * b.z + abs(math.log(b.z / a.z)) * 900

STATIC = CamTrack([(0, W / 2, H / 2, 1.0)])

# ---------- шрифты и растр текста ----------
FONT_DIRS = ['fonts', '/usr/share/fonts/opentype/inter', 'C:/Windows/Fonts']
FONTS = {  # имя → файл; переопределяется проектом (шрифты бренда из claude-edit\branding\...)
    'Inter-Bold': '/usr/share/fonts/opentype/inter/Inter-Bold.otf',
    'Inter-SemiBold': '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf',
    'Inter-Medium': '/usr/share/fonts/opentype/inter/Inter-Medium.otf',
    'Inter-Regular': '/usr/share/fonts/opentype/inter/Inter-Regular.otf',
    'InterDisplay-Bold': '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf',
    'InterDisplay-SemiBold': '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf',
}

@functools.lru_cache(maxsize=256)
def font(name, size_q):
    """name — ключ FONTS или путь; «Имя:800» — вес вариативного шрифта (Unbounded, Manrope)."""
    base, _, wght = name.partition(':')
    f = ImageFont.truetype(FONTS.get(base, base), size_q / 4)
    if wght:
        try: f.set_variation_by_axes([float(wght)])
        except Exception: pass
    return f

def qsize(px):
    """Кегль квантуется до 0.25 px: при проезде камеры текст РАСТЕРИЗУЕТСЯ заново в нужном размере,
    а не масштабируется картинкой (главная причина «мыла» в AE — запечённый текст)."""
    return max(4, int(round(px * 4)))

@functools.lru_cache(maxsize=4096)
def glyph(ch, name, size_q, fx=0.0, fy=0.0):
    """Маска одного символа (альфа float32) + целые поля (ox, oy). fx/fy — дробный сдвиг (шаг 0.25 px)
    для субпиксельной раскладки: буква растеризуется сразу в нужной позиции, без пересэмплинга."""
    f = font(name, size_q); size = size_q / 4
    asc, desc = f.getmetrics()
    pad = int(math.ceil(size * 0.3)) + 1
    w = int(math.ceil(f.getlength(ch))) + 2 * pad; h = asc + desc + 2 * pad
    im = Image.new('L', (w, h), 0)
    ImageDraw.Draw(im).text((pad + fx, pad + fy), ch, font=f, fill=255)
    return np.asarray(im, np.float32) / 255, pad, pad

def layout(text, name, size):
    """x-смещения символов (с кернингом через длину префикса), ширина, метрики строки."""
    f = font(name, qsize(size))
    xs = [f.getlength(text[:i]) for i in range(len(text))]
    asc, desc = f.getmetrics()
    return xs, f.getlength(text), asc, desc

def over(dst, rgb, a, x0, y0):
    """Альфа-композит патча (rgb: цвет (3,) или массив HxWx3; a: HxW) в точку (x0, y0) — целые пиксели."""
    h, w = a.shape
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + w, dst.shape[1]), min(y0 + h, dst.shape[0])
    if xb <= xa or yb <= ya: return
    aa = a[ya - y0:yb - y0, xa - x0:xb - x0][..., None]
    src = rgb if np.ndim(rgb) == 1 else rgb[ya - y0:yb - y0, xa - x0:xb - x0]
    dst[ya:yb, xa:xb] = dst[ya:yb, xa:xb] * (1 - aa) + src * aa

# ---------- формы (SDF — точный антиалиас при любом дробном размере) ----------
def rrect_alpha(w, h, r, pad=2, frac=(0.0, 0.0)):
    """Альфа скруглённого прямоугольника w×h (дробные ок) в патче с полями pad. frac — дробная позиция."""
    W_, H_ = int(math.ceil(w + frac[0])) + 2 * pad, int(math.ceil(h + frac[1])) + 2 * pad
    y, x = np.mgrid[0:H_, 0:W_].astype(np.float32)
    cx, cy = pad + frac[0] + w / 2, pad + frac[1] + h / 2
    r = min(r, w / 2, h / 2)
    qx = np.abs(x + 0.5 - cx) - (w / 2 - r); qy = np.abs(y + 0.5 - cy) - (h / 2 - r)
    d = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r
    return np.clip(0.5 - d, 0, 1)

def disc_alpha(r, pad=2, frac=(0.0, 0.0)):
    return rrect_alpha(2 * r, 2 * r, r, pad, frac)

def soft_shadow(dst, a, x0, y0, blur=36, op=0.35, dy=16, color=(0, 0, 0)):
    p = int(blur * 2)
    big = np.pad(a, p)
    sh = cv2.GaussianBlur(big, (0, 0), blur / 2) * op
    over(dst, np.array(color, np.float32), sh, int(x0 - p), int(round(y0 - p + dy)))
