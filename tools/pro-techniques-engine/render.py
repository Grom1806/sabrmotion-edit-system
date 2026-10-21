# Demo «сложный монтаж»: ракурсы из 4K, текст за головой, подписи по трекингу головы,
# b-roll с текстом, переходы (whip / defocus / push / video-in-text / card-morph / slide),
# инфографика «шкала долга», SFX из событий анимации (каждое событие сам регистрирует свой звук).
import subprocess, json, sys, math, random, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = sys.argv[1] if len(sys.argv) > 1 else '.'
ONLY = None  # для стиль-фреймов: список номеров кадров
if len(sys.argv) > 2: ONLY = [int(x) for x in sys.argv[2].split(',')]
OW, OH = 1080, 1920
FPS = 30000 / 1001
T_END = 24.82
NF = int(T_END * FPS)

# ---------- палитра SABRMOTION ----------
WHITE = (244/255, 244/255, 241/255); RED = (242/255, 40/255, 59/255)
ASH = (140/255, 140/255, 148/255); BLACK = (11/255, 11/255, 12/255); STEEL = (42/255, 42/255, 48/255)
GRAPH = (22/255, 22/255, 26/255)

from functools import lru_cache
@lru_cache(maxsize=None)
def font(name, size, var=None):
    f = ImageFont.truetype(f'{D}/fonts/{name}', max(1, int(round(size))))
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f
SERIF = 'PlayfairDisplay-Italic.ttf'; SANS = 'Onest.ttf'; WIDE = 'Unbounded.ttf'

# ---------- easing ----------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def prog(t, t0, t1): return clamp((t - t0) / max(1e-6, t1 - t0))
def e_outexpo(x): return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def e_inexpo(x): return 0 if x <= 0 else 2 ** (10 * x - 10)
def e_inout(x): return 4*x**3 if x < .5 else 1 - (-2*x + 2)**3 / 2
def e_outback(x, s=1.7): x -= 1; return 1 + (s + 1) * x**3 + s * x**2
def e_outcubic(x): return 1 - (1 - x)**3
def lerp(a, b, x): return a + (b - a) * x

# ---------- SFX регистр (ключ -> событие), дубликаты от сабсэмплов схлопываются ----------
SFX = {}
def sfx(key, t, f, db, pan=0., pitch=0., align='start'):
    if key not in SFX: SFX[key] = dict(t=round(t * FPS) / FPS, f=f, db=db, pan=pan, pitch=pitch, align=align, key=key)

# ---------- трекинг лица (1080p -> 4K) ----------
tr = json.load(open(f'{D}/face_track.json'))['frames']
def arr(k, i=None):
    return np.array([(f[k] if i is None else f[k][i]) * (1 if k in ('roll', 'yaw', 'ear') else 2) for f in tr], float)
RAW = dict(ptop=arr('ptop'), lft=arr('lft'), cx=arr('cx'), cy=arr('cy'), w=arr('w'), h=arr('h'), roll=arr('roll'), top=arr('top', 1), chin=arr('chin', 1), ey=arr('eyes', 1))
def gsmooth(a, s):
    if s <= 0: return a.copy()
    r = int(3 * s); k = np.exp(-np.arange(-r, r + 1)**2 / (2 * s * s)); k /= k.sum()
    return np.convolve(np.pad(a, r, mode='edge'), k, 'valid')
FS = {k: gsmooth(v, 2.5) for k, v in RAW.items()}    # для подписей (быстро, без дрожи)
FH = {k: gsmooth(v, 14) for k, v in RAW.items()}     # для камеры (тяжело)
FL = {k: gsmooth(v, 7) for k, v in RAW.items()}      # для «ленивых» элементов (коробка выноски)
def fget(S, k, t):
    x = clamp(t * FPS, 0, len(tr) - 1); i = int(x); j = min(i + 1, len(tr) - 1); a = x - i
    return S[k][i] * (1 - a) + S[k][j] * a

# ---------- матрицы камеры ----------
def T(x, y): return np.array([[1, 0, x], [0, 1, y], [0, 0, 1.]])
def Sc(s): return np.array([[s, 0, 0], [0, s, 0], [0, 0, 1.]])
def Rz(d):
    r = math.radians(d); c, s = math.cos(r), math.sin(r); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.]])
def Yaw(d, px=OW/2, py=OH/2, f=1700.):
    r = math.radians(d); K = np.array([[f, 0, px], [0, f, py], [0, 0, 1.]])
    R = np.array([[math.cos(r), 0, math.sin(r)], [0, 1, 0], [-math.sin(r), 0, math.cos(r)]])
    return K @ R @ np.linalg.inv(K)
def cam(t, z, fx_out, fy_out, rot=0., yaw=0.):
    """кадр: лицо (тяжело сглаженное) стоит в точке fx_out,fy_out; z=1 -> высота кропа 2160"""
    s = z * OH / 2160.
    fx, fy = fget(FH, 'cx', t), fget(FH, 'cy', t)
    M = T(fx_out, fy_out) @ Rz(rot) @ Sc(s) @ T(-fx, -fy)
    if yaw: M = Yaw(yaw, fx_out, fy_out) @ M
    return M
def mp(M, x, y):
    v = M @ np.array([x, y, 1.]); return v[0] / v[2], v[1] / v[2]

# ---------- кадры исходника ----------
class Src:
    def __init__(s):
        s.v = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f'{D}/src.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        s.m = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f'{D}/matte.mkv', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
        s.i = -1; s.f = None; s.a = None
    def get(s, i):
        while s.i < i:
            b = s.v.stdout.read(3840 * 2160 * 3); m = s.m.stdout.read(1920 * 1080)
            if len(b) < 3840 * 2160 * 3: break
            s.f = np.frombuffer(b, np.uint8).reshape(2160, 3840, 3)
            s.a = np.frombuffer(m, np.uint8).reshape(1080, 1920)
            s.i += 1
        return s.f, s.a
SRC = Src()
CUR = {}

def plate(t, M):
    """кадр головы через камеру M + маска человека в тех же координатах. Фон -0.5 стопы, низ уходит в чёрный."""
    f, a = CUR['f'], CUR['a']
    img = cv2.warpPerspective(f, M, (OW, OH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32) / 255
    Ma = M @ Sc(2.)
    mt = cv2.warpPerspective(a, Ma, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32) / 255
    mt = np.clip((mt - 0.04) / 0.92, 0, 1)
    img *= (0.66 + 0.34 * mt)[..., None]
    # низ кадра: исходник кончается -> мягкий уход в чёрный (и зона интерфейса Reels)
    _, yb = mp(M, fget(FH, 'cx', t), 2160)
    ys = np.arange(OH, dtype=np.float32)
    fade = np.clip((yb - 20 - ys) / 340., 0, 1); fade = fade * fade * (3 - 2 * fade)
    img *= fade[:, None, None]; mt *= fade[:, None]
    # верх: за пределами исходника (replicate) чуть темнее
    _, yt = mp(M, fget(FH, 'cx', t), 0)
    if yt > 0:
        top = np.clip((ys - yt + 160) / 160., 0, 1) * 0.35 + 0.65
        img *= top[:, None, None]
    return img, mt

# ---------- b-roll ----------
BR = {}
def broll_img(name):
    if name not in BR: BR[name] = np.asarray(Image.open(f'{D}/img/{name}').convert('RGB')).astype(np.float32) / 255
    return BR[name]
def broll(name, t, t0, t1, z0, z1, cxr, cyr, r0=0., r1=0., dark=0.82):
    im = broll_img(name); h, w = im.shape[:2]
    p = e_inout(prog(t, t0, t1))
    s = max(OW / w, OH / h) * lerp(z0, z1, p)
    M = T(OW / 2, OH / 2) @ Rz(lerp(r0, r1, p)) @ Sc(s) @ T(-cxr * w, -cyr * h)
    out = cv2.warpAffine(im, M[:2], (OW, OH), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
    vig = 1 - 0.35 * (((xx - OW / 2) / OW) ** 2 + ((yy - OH / 2) / OH) ** 2) * 2.2
    return out * (dark * vig)[..., None], M

# ---------- текст ----------
_tc = {}
def text_rgba(txt, fname, size, color, var=None, track=0):
    key = (txt, fname, round(size, 1), color, var, track)
    if key in _tc: return _tc[key]
    f = font(fname, size, var)
    asc, desc = f.getmetrics()
    wdt = int(sum(f.getlength(c) for c in txt) + track * len(txt)) + int(size)
    im = Image.new('L', (wdt, asc + desc + int(size * .3)), 0); d = ImageDraw.Draw(im)
    x = size * .15
    if track:
        for c in txt: d.text((x, size * .1), c, font=f, fill=255); x += f.getlength(c) + track
    else: d.text((x, size * .1), txt, font=f, fill=255)
    a = np.asarray(im).astype(np.float32) / 255
    ys, xs = np.nonzero(a > 0.002)
    if len(xs) == 0: r = (np.zeros((1, 1, 4), np.float32), 0, 0, 0)
    else:
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        a = a[y0:y1, x0:x1]
        rgba = np.dstack([a * color[0], a * color[1], a * color[2], a])
        # (rgba, ox, oy, baseline_from_top): ox,oy смещение от «пера» до bbox
        r = (rgba, x0 - size * .15, y0 - size * .1, asc - (y0 - size * .1))
    _tc[key] = r; return r

def over(dst, rgba, x, y, op=1.):
    """premultiplied RGBA поверх dst в точке (x,y) — левый верх, субпиксель через сдвиг"""
    if op <= 0.001: return
    h, w = rgba.shape[:2]
    fx, fy = x - math.floor(x), y - math.floor(y)
    if fx > .01 or fy > .01:
        Mt = np.float32([[1, 0, fx], [0, 1, fy]])
        rgba = cv2.warpAffine(rgba, Mt, (w + 1, h + 1), flags=cv2.INTER_LINEAR)
        h, w = rgba.shape[:2]
    x, y = math.floor(x), math.floor(y)
    X0, Y0, X1, Y1 = max(0, x), max(0, y), min(OW, x + w), min(OH, y + h)
    if X0 >= X1 or Y0 >= Y1: return
    s = rgba[Y0 - y:Y1 - y, X0 - x:X1 - x] * op
    d = dst[Y0:Y1, X0:X1]
    d[:] = s[..., :3] + d * (1 - s[..., 3:4])

def xform(rgba, scale=1., rot=0.):
    h, w = rgba.shape[:2]
    if abs(scale - 1) < 1e-3 and abs(rot) < 1e-3: return rgba, 0, 0
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -rot, scale)
    c, s = abs(M[0, 0]), abs(M[0, 1]); nw, nh = int(w * c + h * s) + 2, int(w * s + h * c) + 2
    M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
    return cv2.warpAffine(rgba, M, (nw, nh), flags=cv2.INTER_CUBIC if scale > 1 else cv2.INTER_AREA), (nw - w) / 2, (nh - h) / 2

def put_text(dst, txt, fname, size, color, x, y, anchor='l', op=1., scale=1., rot=0., var=None, track=0):
    """x,y = точка базовой линии; anchor l/c/r"""
    rgba, ox, oy, base = text_rgba(txt, fname, size, color, var, track)
    w = rgba.shape[1]
    ax = {'l': 0, 'c': w / 2, 'r': w}[anchor]
    bx, by = x - ax, y - base
    if scale != 1 or rot:
        r2, dx, dy = xform(rgba, scale, rot)
        cx, cy = bx + w / 2, by + rgba.shape[0] / 2
        over(dst, r2, cx - r2.shape[1] / 2, cy - r2.shape[0] / 2, op); return w
    over(dst, rgba, bx, by, op); return w

def letters_layout(txt, fname, size, var=None):
    f = font(fname, size, var); pos = []; x = 0
    for i, c in enumerate(txt):
        pos.append(f.getlength(txt[:i])); x = f.getlength(txt)
    return pos, x

def typed(dst, key, txt, fname, size, color, x, y, t, t0, t1, anchor='l', var=None, tick_db=-24, op=1., rise=10, tick_pan=0.):
    """печать по буквам: ОДНА буква = ОДИН тик, в кадр появления буквы. Мелкий текст: только opacity + y, без blur."""
    pos, W = letters_layout(txt, fname, size, var)
    ax = {'l': 0, 'c': W / 2, 'r': W}[anchor]
    idx = [i for i, c in enumerate(txt) if c.strip()]
    n = len(idx)
    for k, i in enumerate(idx):
        ti = t0 + (t1 - t0) * (k / max(1, n - 1)) if n > 1 else t0
        ti = round(ti * FPS) / FPS
        sfx(f'{key}_ch{k}', ti, 'tick/el_tick_soft.wav', tick_db, pan=tick_pan, pitch=random.Random(sum(map(ord, key)) * 31 + k).uniform(-1, 1))
        p = prog(t, ti, ti + 2.5 / FPS)
        if p <= 0: continue
        put_text(dst, txt[i], fname, size, color, x - ax + pos[i], y + rise * (1 - e_outcubic(p)), op=op * p, var=var)
    return W

def rrect_mask(w, h, r, ss=2):
    im = Image.new('L', (int(w * ss), int(h * ss)), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255)
    return np.asarray(im.resize((int(w), int(h)), Image.LANCZOS)).astype(np.float32) / 255

def shadow(dst, mask, x, y, blur=40, op=.45, dy=18):
    h, w = mask.shape; pad = int(blur * 2)
    m = np.zeros((h + 2 * pad, w + 2 * pad), np.float32); m[pad:pad + h, pad:pad + w] = mask
    m = cv2.GaussianBlur(m, (0, 0), blur / 2)
    over(dst, np.dstack([m * 0, m * 0, m * 0, m]), x - pad, y - pad + dy, op)

def dot(dst, x, y, r, color, op=1.):
    if r <= 0.3: return
    s = int(r * 2 + 4); yy, xx = np.mgrid[0:s, 0:s].astype(np.float32)
    a = np.clip(r + .5 - np.hypot(xx - s / 2, yy - s / 2), 0, 1)
    over(dst, np.dstack([a * color[0], a * color[1], a * color[2], a]), x - s / 2, y - s / 2, op)

def line(dst, x0, y0, x1, y1, wdt, color, op=1.):
    L = math.hypot(x1 - x0, y1 - y0)
    if L < .5: return
    pad = int(wdt + 3); X0, Y0 = int(min(x0, x1)) - pad, int(min(y0, y1)) - pad
    Wd, Hd = int(abs(x1 - x0)) + 2 * pad + 2, int(abs(y1 - y0)) + 2 * pad + 2
    yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float32); xx += X0; yy += Y0
    dx, dy = (x1 - x0) / L, (y1 - y0) / L
    u = np.clip((xx - x0) * dx + (yy - y0) * dy, 0, L)
    d = np.hypot(xx - (x0 + u * dx), yy - (y0 + u * dy))
    a = np.clip(wdt / 2 + .5 - d, 0, 1)
    over(dst, np.dstack([a * color[0], a * color[1], a * color[2], a]), X0, Y0, op)

# ---------- инфографика: шкала долга (сквозной объект) ----------
SC_X0, SC_X1, SC_Y = 92, 988, 318
TICKS = [0, 10, 30, 50, 100, 200]
def sc_x(v): return SC_X0 + (SC_X1 - SC_X0) * math.sqrt(v / 200.)
FILLS = [(6.23, 10), (8.82, 30), (12.11, 50), (16.00, 100), (19.91, 200)]
def scale_value(t):
    v = 0.
    for k, (tt, val) in enumerate(FILLS):
        prev = FILLS[k - 1][1] if k else 0
        v = lerp(prev, val, e_outexpo(prog(t, tt, tt + .55))) if t >= tt else v
        sfx(f'fill{k}', tt, 'swipe/el_swipe_ui.wav', -21, pan=lerp(-.6, .6, math.sqrt(val / 200)))
    return v
def draw_scale(dst, t):
    if t < 4.70: return
    col = 1 - e_inout(prog(t, 23.96, 24.40))         # схлопывание в точку в финале
    cx = (SC_X0 + SC_X1) / 2
    def cxp(x): return lerp(cx, x, col)
    p = e_outexpo(prog(t, 4.70, 5.15))
    sfx('sc_line', 4.70, 'whoosh/mixkit_tech_slide.wav', -22, pan=-.2)
    x1 = lerp(SC_X0, SC_X1, p)
    line(dst, cxp(SC_X0), SC_Y, cxp(x1), SC_Y, 3, STEEL, 1)
    put_text(dst, 'ДОЛГ, ₽', SANS, 22, ASH, cxp(SC_X0), SC_Y - 30, var='Medium', op=prog(t, 4.75, 4.95) * col, track=2)
    for k, v in enumerate(TICKS):
        tk = 4.80 + k * .07
        if v: sfx(f'sc_tick{k}', tk, 'tick/kenney_tick_002.wav', -18, pan=lerp(-.7, .7, k / 5))
        q = e_outback(prog(t, tk, tk + .2))
        if q <= 0: continue
        x = cxp(sc_x(v))
        line(dst, x, SC_Y - 7 * q, x, SC_Y + 7 * q, 2, ASH, col)
        if v: put_text(dst, f'{v}к', 'JetBrainsMono.ttf' if False else SANS, 20, ASH, x, SC_Y + 36, anchor='c', op=prog(t, tk, tk + .15) * col, var='Medium')
    v = scale_value(t)
    if v > 0.05:
        xv = cxp(sc_x(v))
        line(dst, cxp(SC_X0), SC_Y, xv, SC_Y, 6, RED, 1)
        dot(dst, xv, SC_Y, 9 * max(col, .0001) if col > .01 else 0, RED)
    if t >= 23.96:   # финальная красная точка
        r = 9 + 5 * e_outback(prog(t, 24.38, 24.52)) * (1 - prog(t, 24.62, 24.74))
        sfx('end_click', 24.40, 'tick/kenney_ui_click3.wav', -12)
        if col < .05: dot(dst, cx, SC_Y, r, RED, 1 - prog(t, 24.66, 24.76))

def fit(txt, fname, size, var, maxw):
    w = font(fname, size, var).getlength(txt)
    return size if w <= maxw else max(24, size * maxw / w)
def fmt(n): return f'{int(round(n)):,}'.replace(',', ' ')

# ---------- «гуи-морф» текста (Ben Marriott: сильный blur + порог альфы) ----------
def word_mask(txt, fname, size, W, H, var=None):
    rgba, ox, oy, base = text_rgba(txt, fname, size, (1, 1, 1), var)
    m = np.zeros((H, W), np.float32); h, w = rgba.shape[:2]
    x, y = (W - w) // 2, (H - h) // 2 + int(size * .05)
    m[y:y + h, x:x + w] = rgba[..., 3][:H - y, :W - x]
    return m
def gooey(mA, mB, m):
    k = math.sin(math.pi * m); sig = 1 + 22 * k
    a = cv2.GaussianBlur(mA, (0, 0), sig) * (1 - m) + cv2.GaussianBlur(mB, (0, 0), sig) * m if k > .02 else (mA * (1 - m) + mB * m)
    th = np.clip((a - .5) * 8 + .5, 0, 1)
    return a * (1 - k) + th * k

# ================= СЦЕНЫ =================
def s1(t, pan=0.):   # ХУК: «журнальная обложка» — слово за головой, медленный наезд, параллакс
    z = lerp(.84, .885, e_inout(prog(t, 0, 4.4)))
    M = cam(t, z, 540 - pan, 1135)
    sfx('s1_push', 0.05, 'whoosh/mixkit_air_woosh.wav', -27)
    img, mt = plate(t, M)
    back = img.copy()
    # надзаголовок
    sz = 212 * (1 + .45 * (z - .84))  # текст «глубже» человека: масштабируется слабее (параллакс)
    W, H = 1080, 420
    _, ytop = mp(M, fget(FH, 'cx', t), fget(FL, 'ptop', t))   # верх волос по маске
    yb = min(640, ytop + 38)
    if t >= 1.0:
        if t < 3.80:   # «список» — буквы поднимаются из-под маски (каждая буква = тик)
            txt = 'список'; pos, Wt = letters_layout(txt, SERIF, sz, 'Black Italic')
            for i, c in enumerate(txt):
                ti = 1.01 + i * .055
                sfx(f's1_l{i}', ti, 'tick/kenney_ui_click3.wav', -21, pan=lerp(-.5, .5, i / 5))
                p = e_outexpo(prog(t, ti, ti + .45))
                if p <= 0: continue
                layer = np.zeros_like(back)
                put_text(layer, c, SERIF, sz, WHITE, 540 - pan * .85 - Wt / 2 + pos[i], yb + 120 * (1 - p), var='Black Italic')
                layer[int(yb + 40):] = 0           # маска-«пол»: буква выезжает из-под линии
                over_full(back, layer)
        else:          # морф «список» -> «должник» (blur + порог), красный градиент
            m = e_inout(prog(t, 3.80, 4.18))
            sfx('s1_morph', 3.80, 'whoosh/mixkit_light_pop_whoosh.wav', -15)
            sfx('s1_morph_sub', 4.10, 'sub/el_sub_hit_1.wav', -15)
            mA = word_mask('список', SERIF, sz, W, H, 'Black Italic'); mB = word_mask('должник', SERIF, sz, W, H, 'Black Italic')
            a = gooey(mA, mB, m)
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            g = np.clip((xx - 250) / 600, 0, 1) * m       # белый -> красный по слову (1 градиентное слово на ролик)
            col = np.dstack([lerp(WHITE[0], RED[0], g), lerp(WHITE[1], RED[1], g), lerp(WHITE[2], RED[2], g)])
            y0 = int(yb - H / 2 - sz * .3)
            over(back, np.dstack([col * a[..., None], a]), -pan * .85, y0)
    # человек поверх слова
    out = back * (1 - mt[..., None]) + img * mt[..., None]
    if t >= .4:
        op = prog(t, .4, .8) * (1 - prog(t, 4.25, 4.4))
        put_text(out, 'РУБРИКА  ·  КЛАССИФИКАТОР ДОЛЖНИКОВ', SANS, 23, ASH, 540, 300, anchor='c', op=op, var='Medium', track=3)
        sfx('s1_kicker', .4, 'ui/el_ui_click_soft.wav', -22)
    return out

def over_full(dst, layer):
    a = np.clip(layer.max(axis=2, keepdims=True) / max(WHITE), 0, 1)
    dst[:] = layer + dst * (1 - a)

def s2_cam(t, pan=0.): return cam(t, .62, 735 + pan, 1000)
def s2(t, pan=0.):   # ОБЩИЙ план, подпись привязана к голове (трек + 40 % наклона), счётчик, шкала
    M = s2_cam(t, pan); img, mt = plate(t, M)
    out = img
    fx, fy = fget(FS, 'cx', t), fget(FS, 'ey', t)
    fw = fget(FS, 'w', t); roll = fget(FS, 'roll', t)
    ax, ay = mp(M, fget(FL, 'lft', t) - 30, fy)   # край человека по маске
    ax -= 26
    rot = .4 * roll
    exit_ = e_inexpo(prog(t, 7.22, 7.41))
    ax -= 120 * exit_; opx = 1 - exit_
    # №1
    q = e_outback(prog(t, 4.70, 4.95))
    sfx('s2_n1', 4.70, 'notification/mixkit_dry_pop.wav', -12, pan=-.4)
    layer = np.zeros_like(out)
    if q > 0:
        dot(layer, ax - 34, ay - 92, 34 * q, RED)
        put_text(layer, '1', SANS, 40 * q, WHITE, ax - 34, ay - 78, anchor='c', var='Bold')
    ax = max(ax, 60 + font(SERIF, 52, 'Italic').getlength('«до зарплаты»'))
    typed(layer, 's2_lbl', '«до зарплаты»', SERIF, 52, WHITE, ax, ay, t, 5.08, 5.74, anchor='r', var='Italic', tick_pan=-.4)
    if t >= 6.23:
        p = e_outexpo(prog(t, 6.23, 6.85))
        sfx('s2_roll', 6.23, 'tick/el_counter_roll.wav', -19, pan=-.4)
        sfx('s2_coin', 6.85, 'money/el_coin_single.wav', -16, pan=-.4)
        put_text(layer, f'до {fmt(10000 * p)} ₽', SANS, 40, RED, ax, ay + 62 + 8 * (1 - prog(t, 6.23, 6.33)), anchor='r', var='SemiBold', op=prog(t, 6.23, 6.33))
    if abs(rot) > .05 or opx < 1:
        # поворот всей группы вокруг якоря (40 % от наклона головы)
        Mr = cv2.getRotationMatrix2D((ax, ay), -rot, 1.)
        layer = cv2.warpAffine(layer, Mr, (OW, OH), flags=cv2.INTER_LINEAR)
    over_full(out, layer * opx)
    return out

def s3(t):   # B-ROLL + текст «на днях закину», привязанный к плоскости снимка, ценник-штамп
    img, M = broll('money_08_v3490.jpg', t, 7.2, 10.6, 1.02, 1.12, .52, .48, -1.2, .6, dark=.78)
    def P(x, y): return mp(M, x, y)
    h, w = broll_img('money_08_v3490.jpg').shape[:2]
    s = M[0, 0] / math.cos(math.radians(0)) if True else 1
    sc = math.hypot(M[0, 0], M[1, 0]) / (max(OW / w, OH / h))     # масштаб Кен Бёрнса
    for k, (word, tw, yy) in enumerate([('на днях', 7.45, 1260), ('закину', 7.75, 1395)]):
        sfx(f's3_w{k}', tw, 'whoosh/mixkit_small_sweep.wav', -19, pan=-.3, pitch=k)
        p = e_outexpo(prog(t, tw, tw + .4))
        if p <= 0: continue
        x0, y0 = P(.27 * w, (.40 + (yy - 1260) / OH) * h)
        layer = np.zeros_like(img)
        put_text(layer, word, SERIF, 128 * sc, WHITE, x0, y0 + 60 * (1 - p), var='Italic')
        layer[int(y0 + 34 * sc):] = 0                 # вырастает из-под линии
        a = layer.max(axis=2)
        sh = cv2.GaussianBlur(a, (0, 0), 26)
        img *= (1 - .75 * np.clip(sh * 1.6, 0, 1))[..., None]
        over_full(img, layer)
    if t >= 8.82:   # ценник-штамп «10–30 тыс ₽», прибит к купюрам
        p = prog(t, 8.82, 9.0); q = lerp(1.35, 1., e_outback(p, 2.2))
        sfx('s3_stamp', 8.82, 'stamp/el_stamp_thump.wav', -10, pan=.3)
        x0, y0 = P(.66 * w, .27 * h)
        tag = np.zeros((130, 400, 4), np.float32); m = rrect_mask(400, 130, 22)
        tag[..., 0] = m * RED[0]; tag[..., 1] = m * RED[1]; tag[..., 2] = m * RED[2]; tag[..., 3] = m
        tmp = np.zeros((130, 400, 3), np.float32)
        put_text(tmp, '10–30 тыс ₽', SANS, 50, WHITE, 200, 85, anchor='c', var='Bold')
        tag[..., :3] = tag[..., :3] * (1 - tmp.max(2, keepdims=True) / max(WHITE)) + tmp
        r2, _, _ = xform(tag, q * sc, -7)
        shadow(img, r2[..., 3], x0 - r2.shape[1] / 2, y0 - r2.shape[0] / 2, 30, .5 * min(1, p * 3), 14)
        over(img, r2, x0 - r2.shape[1] / 2, y0 - r2.shape[0] / 2, min(1, p * 4))
    return img

def s4_cam(t): return cam(t, .80, 380, 1020)
def s4(t):   # КРУПНЫЙ план + выноска: точка на виске (трек), коробка «ленивая», линия тянется
    M = s4_cam(t); img, mt = plate(t, M); out = img
    fx, fy, fw = fget(FS, 'cx', t), fget(FS, 'ey', t), fget(FS, 'w', t)
    axp, ayp = mp(M, fx + fw * .5, fy - fw * .28)
    lx, ly, lw = fget(FL, 'cx', t), fget(FL, 'ey', t), fget(FL, 'w', t)
    bxp, byp = mp(M, lx + lw * .5, ly - lw * .28)
    bx, by = min(bxp + 110, 1080 - 56 - font(SERIF, 60, 'Italic').getlength('я помню')), max(470, byp - 200)
    ret = e_inexpo(prog(t, 13.45, 13.70))
    sfx('s4_dot', 10.62, 'notification/mixkit_bubble_pop.wav', -15, pan=.3)
    sfx('s4_line', 10.66, 'whoosh/mixkit_light_pop_whoosh.wav', -20, pan=.4)
    sfx('s4_ret', 13.45, 'whoosh/mixkit_short_sweep.wav', -22, pan=.2)
    q = e_outback(prog(t, 10.62, 10.80)) * (1 - ret)
    dot(out, axp, ayp, 9 * q, RED); dot(out, axp, ayp, 4 * q, WHITE)
    p = e_outexpo(prog(t, 10.66, 10.95)) * (1 - ret)
    ex, ey = lerp(axp, bx, p), lerp(ayp, by + 20, p)
    if p > 0.01:
        line(out, axp, ayp, ex, ey, 2.5, WHITE, .95)
        line(out, ex, ey, ex + 170 * p, ey, 2.5, WHITE, .95)
    if t < 13.62:
        op = 1 - prog(t, 13.40, 13.55)
        typed(out, 's4_t1', 'брат,', SERIF, 60, WHITE, bx, by - 80, t, 10.62, 10.84, var='Italic', op=op, tick_pan=.4)
        typed(out, 's4_t2', 'я помню', SERIF, 60, WHITE, bx, by - 6, t, 10.86, 11.31, var='Italic', op=op, tick_pan=.4)
        if t >= 12.11:
            sfx('s4_amt', 12.11, 'ui/kenney_drop_001.wav', -15, pan=.4)
            put_text(out, '30–50 тыс ₽', SANS, 38, RED, bx, by + 74 + 8 * (1 - prog(t, 12.11, 12.25)), var='SemiBold', op=prog(t, 12.11, 12.25) * op)
    return out

def s5_cam(t): return cam(t, lerp(.64, .68, e_inout(prog(t, 14.2, 17.8))), 790, 1000, rot=lerp(0, -1.4, e_inout(prog(t, 14.2, 17.8))))
def s5(t):   # слова выходят ИЗ-ЗА головы (окклюзия маской) и уходят обратно
    M = s5_cam(t); img, mt = plate(t, M)
    back = img.copy()
    fx, fy, fw = fget(FS, 'cx', t), fget(FS, 'ey', t), fget(FS, 'w', t)
    cxh, cyh = mp(M, fx, fy)
    lx, _ = mp(M, fget(FL, 'lft', t) - 50, fy)   # край ЧЕЛОВЕКА по маске (с волосами/ухом), не по точкам лица
    for k, (word, tw, dy) in enumerate([('всё', 14.68, -40), ('будет', 15.28, 70)]):
        sfx(f's5_w{k}', tw, 'whoosh/mixkit_fast_swoosh.wav', -17, pan=-.5, pitch=-k * 2)
        p = e_outexpo(prog(t, tw, tw + .55)) * (1 - e_inexpo(prog(t, 17.35 + k * .05, 17.70)))
        if p <= 0: continue
        lx2 = lx - 20
        x = lerp(cxh, lx2, p)
        put_text(back, word, SERIF, fit('будет', SERIF, 92, 'Italic', lx - 80), WHITE, x, cyh + dy, anchor='r', var='Italic')
    sfx('s5_back', 17.35, 'whoosh/mixkit_short_sweep.wav', -21, pan=-.3)
    out = back * (1 - mt[..., None]) + img * mt[..., None]
    if 16.0 <= t < 17.6:
        sfx('s5_amt', 16.0, 'money/el_coin_single.wav', -17, pan=-.4)
        op = prog(t, 16.0, 16.14) * (1 - prog(t, 17.35, 17.55))
        put_text(out, '50–100 тыс ₽', SANS, 38, RED, lx - 20, cyh + 150 + 8 * (1 - prog(t, 16.0, 16.14)), anchor='r', var='SemiBold', op=op)
    return out

def s6(t):   # B-ROLL телефон + чат-пузырь растёт под текст, «печатает…», число-герой
    img, M = broll('smartphone_10_h4096.jpg', t, 17.5, 21.4, 1.0, 1.07, .53, .52, .8, -.4, dark=.66)
    if t >= 18.10:
        txt = 'как раз хотел тебе написать…'
        f = font(SANS, 46, 'Medium'); full = f.getlength(txt)
        idx = [i for i, c in enumerate(txt) if c.strip()]
        # контейнер растёт вместе с текстом
        nshow = sum(1 for k, i in enumerate(idx) if t >= 18.12 + (19.10 - 18.12) * k / (len(idx) - 1))
        lastc = idx[nshow - 1] if nshow else 0
        cw = f.getlength(txt[:lastc + 1]) if nshow else 0
        bw = max(120, 72 + cw)
        pin = e_outback(prog(t, 18.08, 18.30))
        sfx('s6_bub', 18.08, 'notification/el_msg_pop.wav', -14, pan=.2)
        x0, y0, bh = 70, 560, 104
        m = rrect_mask(bw, bh, 40)
        bub = np.dstack([m * WHITE[0], m * WHITE[1], m * WHITE[2], m])
        r2, _, _ = xform(bub, max(.01, pin))
        shadow(img, r2[..., 3], x0 + (bw - r2.shape[1]) / 2, y0 + (bh - r2.shape[0]) / 2, 30, .45, 12)
        over(img, r2, x0 + (bw - r2.shape[1]) / 2, y0 + (bh - r2.shape[0]) / 2)
        typed(img, 's6_typ', txt, SANS, 46, BLACK, x0 + 36, y0 + 68, t, 18.12, 19.10, var='Medium', tick_db=-27, rise=6, tick_pan=.2)
        if t >= 19.30:   # «печатает…»
            ph = (t - 19.30) * 3
            put_text(img, 'печатает', SANS, 34, WHITE, x0 + 14, y0 + bh + 52, var='Medium', op=prog(t, 19.3, 19.45))
            for k in range(3):
                a = .35 + .65 * max(0, math.sin((ph - k * .25) * math.pi))
                dot(img, x0 + 178 + k * 16, y0 + bh + 42, 4, WHITE, a * prog(t, 19.3, 19.45))
    if t >= 19.91:   # число-герой
        p = e_outexpo(prog(t, 19.91, 20.55))
        sfx('s6_roll', 19.91, 'tick/el_counter_roll.wav', -16)
        sfx('s6_land', 20.50, 'sub/el_sub_hit_1.wav', -15)
        op = prog(t, 19.91, 20.05)
        put_text(img, 'было 100 тыс — стало', SANS, 38, WHITE, 540, 1120, anchor='c', var='Medium', op=op)
        put_text(img, f'{fmt(lerp(100000, 200000, p))} ₽', WIDE, 128, RED, 540, 1290 + 14 * (1 - op), anchor='c', var='Bold', op=op)
    return img

def s7_cam(t):
    pp = e_inout(prog(t, 21.0, 24.6))
    return cam(t, lerp(.70, .74, pp), 735, 1000, yaw=lerp(-7, -2, pp))
def s7(t):   # «3D-ракурс»: плоскость кадра повёрнута (yaw), текст в своей плоскости, зачёркивание
    M = s7_cam(t); img, mt = plate(t, M); out = img
    sfx('s7_air', 21.40, 'whoosh/mixkit_air_woosh.wav', -28, pan=-.3)
    fx, fy, fw = fget(FS, 'cx', t), fget(FS, 'ey', t), fget(FS, 'w', t)
    lx, ly = mp(M, fget(FL, 'lft', t) - 50, fy)
    lx = max(lx, 100 + font(SERIF, 92, 'Italic').getlength('деньги') + 24)
    col = 1 - e_inout(prog(t, 23.96, 24.40))
    layer = np.zeros_like(out)
    for k, (word, tw, dy) in enumerate([('деньги', 21.42, -70), ('есть,', 21.80, 30)]):
        sfx(f's7_w{k}', tw, 'paper/mixkit_paper_slide.wav' if k == 0 else 'whoosh/mixkit_small_sweep.wav', -20, pan=-.4)
        p = e_outexpo(prog(t, tw, tw + .45))
        if p <= 0: continue
        L = np.zeros_like(out)
        put_text(L, word, SERIF, 92, WHITE, lx - 24, ly + dy + 70 * (1 - p), anchor='r', var='Italic')
        L[int(ly + dy + 28):] = 0
        over_full(layer, L)
    f = font(SERIF, 92, 'Italic'); we = f.getlength('есть,')
    if t >= 23.30:
        p = e_outexpo(prog(t, 23.30, 23.52))
        sfx('s7_strike', 23.30, 'paper/mixkit_paper_slice.wav' if False else 'whoosh/mixkit_light_pop_whoosh.wav', -14, pan=-.4)
        xs = lx - 24 - we
        line(layer, xs - 10, ly + 8, lerp(xs - 10, lx - 14, p), ly + 2, 7, RED)
        typed(layer, 's7_nem', 'не у меня', SERIF, 84, RED, lx - 24, ly + 140, t, 23.32, 23.96, anchor='r', var='Italic', tick_pan=-.4)
    # общая «перспектива» текста: своя плоскость, поворачивается слабее плиты (параллакс глубины)
    pp = e_inout(prog(t, 21.0, 24.6))
    H = Yaw(lerp(-3, -1, pp), lx - 200, ly)
    layer = cv2.warpPerspective(layer, H, (OW, OH), flags=cv2.INTER_LINEAR)
    if col < 1:   # схлопывание текста к красной точке
        Ms = cv2.getAffineTransform(np.float32([[0, 0], [OW, 0], [0, OH]]), np.float32([[lerp(540, 0, col), lerp(SC_Y, 0, col)], [lerp(540, OW, col), lerp(SC_Y, 0, col)], [lerp(540, 0, col), lerp(SC_Y, OH, col)]]))
        layer = cv2.warpAffine(layer, Ms, (OW, OH), flags=cv2.INTER_AREA) * col
        sfx('s7_suck', 23.96, 'whoosh/el_whoosh_short.wav', -16)
    over_full(out, layer)
    fade = prog(t, 24.52, 24.74)
    return out * (1 - fade)

# ================= ПЕРЕХОДЫ =================
def whip(t):   # 4.40–4.70: панорама вправо по 4K-кадру + обрыв в новый ракурс (motion blur сабсэмплами)
    sfx('t1_whip', 4.55, 'whoosh/mixkit_fast_swoosh.wav', -11, pan=.5, align='peak')
    if t < 4.55:
        p = e_inexpo(prog(t, 4.40, 4.55))
        return s1(t, pan=1500 * p)
    p = e_outexpo(prog(t, 4.55, 4.75))
    return s2(t, pan=1400 * (1 - p))
def s1_bg_only(t, M):
    img, mt = plate(t, M); return img

def defocus(t):   # 7.21–7.61: лицо уходит в blur+zoom, b-roll приходит из blur+zoom (без «пакетных» переходов)
    sfx('t2_whoosh', 7.41, 'whoosh/el_whoosh_short.wav', -14, align='peak')
    sfx('t2_jcut', 7.24, 'paper/mixkit_paper_slide.wav', -17, pan=.2)
    if t < 7.41:
        p = e_inexpo(prog(t, 7.21, 7.41)); img = s2(t)
        z = 1 + .14 * p
        img = cv2.warpAffine(img, cv2.getRotationMatrix2D((540, 900), 0, z)[:2] if False else cv2.getRotationMatrix2D((540, 900), 0, z), (OW, OH), flags=cv2.INTER_LINEAR)
        return cv2.GaussianBlur(img, (0, 0), .1 + 16 * p)
    p = 1 - e_outexpo(prog(t, 7.41, 7.66)); img = s3(t)
    img = cv2.warpAffine(img, cv2.getRotationMatrix2D((540, 900), 0, 1 + .14 * p), (OW, OH), flags=cv2.INTER_LINEAR)
    return cv2.GaussianBlur(img, (0, 0), .1 + 16 * p) if p > .01 else img

def push_up(t):   # 10.24–10.56: b-roll уезжает вверх, голова въезжает снизу (шкала стоит на месте)
    sfx('t3_push', 10.40, 'whoosh/mixkit_short_sweep.wav', -12, align='peak')
    p = e_inout(prog(t, 10.24, 10.56))
    a = s3(t); b = s4(t); out = np.zeros_like(a)
    dy = int(round(OH * p))
    out[:OH - dy] = a[dy:]; out[OH - dy:] = b[:dy] if dy else out[OH:]
    return out

PASS_TXT = ('НЕ', 'ПЕРЕЖИВАЙ')
_vt = {}
def vt_mask():
    if 'm' in _vt: return _vt['m']
    m = np.zeros((OH, OW), np.float32); tmp = np.zeros((OH, OW, 3), np.float32)
    put_text(tmp, PASS_TXT[0], WIDE, 230, (1, 1, 1), 540, 880, anchor='c', var='Black')
    put_text(tmp, PASS_TXT[1], WIDE, 112, (1, 1, 1), 540, 1090, anchor='c', var='Black')
    m = tmp[..., 0]
    dist = cv2.distanceTransform((m > .5).astype(np.uint8), cv2.DIST_L2, 5)
    dist[:, :] *= 1; yx = np.unravel_index(np.argmax(dist[700:900]), dist[700:900].shape)
    _vt['m'] = m; _vt['c'] = (yx[1], yx[0] + 700); return m
def video_in_text(t):   # 13.76–14.48: видео внутри букв -> пролёт сквозь букву в новый ракурс
    sfx('t4_hit', 13.76, 'sub/el_sub_hit_2.wav', -11)
    sfx('t4_zoom', 14.12, 'impact/mixkit_quick_zoom.wav', -13)
    sfx('t4_land', 14.46, 'sub/el_boom_big.wav', -19)
    m = vt_mask(); cx, cy = _vt['c']
    plate_img = s5(t)
    if t < 14.14:
        p = e_outexpo(prog(t, 13.76, 13.95)); z = lerp(.92, 1., p); op = p
    else:
        z = lerp(1., 26., e_inexpo(prog(t, 14.14, 14.48))); op = 1
    M = cv2.getRotationMatrix2D((float(cx), float(cy)), 0, z)
    mm = cv2.warpAffine(m, M, (OW, OH), flags=cv2.INTER_LINEAR) * op
    bg = np.empty_like(plate_img); bg[:] = BLACK
    edge = np.clip(cv2.dilate(mm, np.ones((5, 5), np.uint8)) - mm, 0, 1) * .55 * (1 - prog(t, 14.14, 14.30))
    out = plate_img * mm[..., None] * 1.25 + bg * (1 - mm[..., None])
    return out * (1 - edge[..., None]) + edge[..., None] * np.array(WHITE, np.float32)

def card_morph(t):   # 17.50–18.42: карточка b-roll въезжает с 3D-наклоном и раскрывается на весь экран
    sfx('t5_card', 17.52, 'money/el_card_slide.wav', -14, pan=-.5)
    sfx('t5_open', 18.20, 'whoosh/el_whoosh_short.wav', -14, align='peak')
    base = s5(t) if t < 18.42 else None
    full = s6(t)
    pin = e_outexpo(prog(t, 17.50, 17.90)); op = e_inout(prog(t, 18.08, 18.42))
    x0, y0, w0, h0 = lerp(-360, 70, pin), 1180, 330, 470
    x, y, w, h = lerp(x0, 0, op), lerp(y0, 0, op), lerp(w0, OW, op), lerp(h0, OH, op)
    r = lerp(34, 0, op)
    # содержимое карточки — полный кадр b-roll, вписанный по центру
    sc = max(w / OW, h / OH); cw, ch = int(OW * sc) + 1, int(OH * sc) + 1
    small = cv2.resize(full, (cw, ch), interpolation=cv2.INTER_AREA)
    ox, oy = (cw - int(w)) // 2, (ch - int(h)) // 2
    card = small[oy:oy + int(h), ox:ox + int(w)]
    msk = rrect_mask(card.shape[1], card.shape[0], r) if r > .5 else np.ones(card.shape[:2], np.float32)
    rgba = np.dstack([card * msk[..., None], msk])
    if op < .999:
        Hh = Yaw(lerp(16, 6, pin) * (1 - op), rgba.shape[1] / 2, rgba.shape[0] / 2, 900)
        rgba = cv2.warpPerspective(rgba, Hh, (rgba.shape[1], rgba.shape[0]), flags=cv2.INTER_LINEAR)
    out = base.copy() if base is not None else full.copy()
    shadow(out, rgba[..., 3], x, y, 36, .55 * (1 - op), 20)
    over(out, rgba, x, y)
    return out

def slide_left(t):   # 21.20–21.44: b-roll уходит влево, голова въезжает справа
    sfx('t6_slide', 21.32, 'whoosh/mixkit_fast_swoosh.wav', -12, pan=-.5, align='peak')
    p = e_inout(prog(t, 21.20, 21.44))
    a = s6(t); b = s7(t); dx = int(round(OW * p)); out = np.empty_like(a)
    out[:, :OW - dx] = a[:, dx:]; out[:, OW - dx:] = b[:, :dx] if dx else out[:, OW:]
    return out

# ================= ТАЙМЛАЙН =================
TL = [  # (t0, t1, функция, motion blur сабсэмплов)
    (0.00, 4.40, s1, 1), (4.40, 4.75, whip, 7), (4.75, 7.21, s2, 1), (7.21, 7.66, defocus, 1),
    (7.66, 10.24, s3, 1), (10.24, 10.56, push_up, 7), (10.56, 13.76, s4, 1), (13.76, 14.48, video_in_text, 1),
    (14.48, 17.50, s5, 1), (17.50, 18.42, card_morph, 3), (18.42, 21.20, s6, 1), (21.20, 21.44, slide_left, 7),
    (21.44, 99, s7, 1)]

def frame(i):
    t = i / FPS
    for t0, t1, fn, ns in TL:
        if t0 <= t < t1: break
    if ns > 1:   # затвор 180°: сабсэмплы внутри половины кадра
        acc = None
        for k in range(ns):
            ts = t + (k / (ns - 1) - .5) * .5 / FPS
            img = fn(min(max(ts, t0), t1 - 1e-4))
            acc = img if acc is None else acc + img
        img = acc / ns
    else: img = fn(t)
    draw_scale(img, t)
    return img

if __name__ == '__main__':
    random.seed(7)
    frames = ONLY if ONLY else range(NF)
    if ONLY:
        for i in ONLY:
            SRC.get(i); CUR['f'], CUR['a'] = SRC.f, SRC.a
            Image.fromarray((np.clip(frame(i), 0, 1) * 255 + .5).astype(np.uint8)).save(f'{D}/sf/f{i:04d}.png')
        sys.exit()
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}', '-r', '30000/1001', '-i', '-',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', f'{D}/video_noaudio.mp4'], stdin=subprocess.PIPE)
    import time; t0 = time.time()
    for i in range(NF):
        SRC.get(i); CUR['f'], CUR['a'] = SRC.f, SRC.a
        enc.stdin.write((np.clip(frame(i), 0, 1) * 255 + .5).astype(np.uint8).tobytes())
        if i % 60 == 0: print(i, round(time.time() - t0), flush=True)
    enc.stdin.close(); enc.wait()
    json.dump(sorted(SFX.values(), key=lambda e: e['t']), open(f'{D}/sfx_events.json', 'w'), ensure_ascii=False, indent=0)
    print('frames', NF, 'sfx', len(SFX))
