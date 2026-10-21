# Движок «документальный моушен на ночной карте» (Ummah Link, 2026-10-21)
# Карта: NASA Black Marble 2016 + Blue Marble topo-bathy (public domain), lon 25..75E, lat 50..15N, 240 px/град.
import json, math, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
D = __file__.rsplit('/', 1)[0]
LON0, LAT0, PPD = 25.0, 52.0, 240.0
FONT = f'{D}/fonts/Montserrat.ttf'
FONT_AR = f'{D}/fonts/Amiri-Bold.ttf'
GOLD = np.array([226, 196, 95], np.float32) / 255      # #E2C45F
GOLD2 = np.array([212, 175, 55], np.float32) / 255     # #D4AF37
CREAM = np.array([253, 247, 232], np.float32) / 255    # #FDF7E8
GREEN = np.array([23, 63, 41], np.float32) / 255       # #173F29
LEAF = np.array([107, 175, 118], np.float32) / 255     # #6BAF76
WHITE = np.array([1, 1, 1], np.float32)

def geo(lon, lat):
    return np.array([(lon - LON0) * PPD, (LAT0 - lat) * PPD], np.float64)

CITY = {
    'bukhara': (64.42, 39.77), 'mecca': (39.83, 21.42), 'medina': (39.61, 24.47), 'basra': (47.78, 30.51),
    'kufa': (44.40, 32.03), 'baghdad': (44.37, 33.31), 'egypt': (31.24, 30.04), 'sham': (36.29, 33.51),
    'nishapur': (58.80, 36.21), 'samarkand': (66.97, 39.65), 'khartank': (66.86, 39.78),
}

# ---------- карта с пирамидой ----------
_PYR = None
def pyr():
    global _PYR
    if _PYR is None:
        Image.MAX_IMAGE_PIXELS = None
        m = cv2.cvtColor(cv2.imread(f'{D}/map_full.png', cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        _PYR = [m]
        for _ in range(4):
            m = cv2.resize(m, (m.shape[1] // 2, m.shape[0] // 2), interpolation=cv2.INTER_AREA)
            _PYR.append(m)
    return _PYR

class Cam:
    def __init__(s, cx, cy, z, rot=0.0):
        s.c = np.array([cx, cy], np.float64); s.z = z; s.rot = rot
    def M(s):
        a = math.radians(s.rot); ca, sa = math.cos(a) * s.z, math.sin(a) * s.z
        # экран = R*z*(X - c) + центр
        return np.array([[ca, -sa, W / 2 - (ca * s.c[0] - sa * s.c[1])],
                         [sa, ca, H / 2 - (sa * s.c[0] + ca * s.c[1])]], np.float64)
    def to_screen(s, P):
        P = np.atleast_2d(P); M = s.M()
        return P @ M[:, :2].T + M[:, 2]

def cam_at(lon, lat, z, rot=0.0):
    p = geo(lon, lat); return Cam(p[0], p[1], z, rot)

def lerp_cam(a, b, t):
    # зум интерполируем в лог-пространстве, центр — с учётом зума (без «вылета»)
    z = math.exp(math.log(a.z) * (1 - t) + math.log(b.z) * t)
    c = a.c * (1 - t) + b.c * t
    return Cam(c[0], c[1], z, a.rot * (1 - t) + b.rot * t)

def render_map(cam, blur=0.0, bright=1.0):
    P = pyr(); lvl = 0
    while lvl < len(P) - 1 and cam.z * (2 ** (lvl + 1)) <= 1.0:
        lvl += 1
    s = 2 ** lvl
    c2 = Cam(cam.c[0] / s, cam.c[1] / s, cam.z * s, cam.rot)
    img = cv2.warpAffine(P[lvl], c2.M(), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(4, 4, 4))
    img = img.astype(np.float32) / 255 * bright
    if blur > 0.3:
        img = cv2.GaussianBlur(img, (0, 0), blur)
    return img

# ---------- цвет / постобработка ----------
_VIG = None
def vignette(img, k=0.55):
    global _VIG
    if _VIG is None:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
        _VIG = np.clip(1 - np.clip(r - 0.35, 0, 1) ** 1.6, 0, 1)
    return img * (1 - k + k * _VIG[..., None])

def screen(a, b):
    return 1 - (1 - a) * (1 - np.clip(b, 0, 1))

def over(dst, rgba):
    a = rgba[..., 3:4]
    return dst * (1 - a) + rgba[..., :3] * a

def glow_add(dst, layer_rgb, sigmas=(4, 14, 36), gains=(0.9, 0.6, 0.35)):
    g = np.zeros_like(layer_rgb)
    for s, k in zip(sigmas, gains):
        g += cv2.GaussianBlur(layer_rgb, (0, 0), s) * k
    return screen(dst, g + layer_rgb)

# ---------- линии ----------
def bez(p0, p1, bend=0.18, n=80):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0; nrm = np.array([-d[1], d[0]])
    c = (p0 + p1) / 2 + nrm * bend
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1

def trim(pts, a, b=None):
    """часть ломаной от доли a до b (по длине)"""
    if b is None: a, b = 0.0, a
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); L = np.concatenate([[0], np.cumsum(seg)])
    tot = L[-1]
    if tot <= 0 or b <= a: return pts[:1]
    la, lb = a * tot, b * tot
    out = [np.array([np.interp(la, L, pts[:, 0]), np.interp(la, L, pts[:, 1])])]
    out += [p for p, l in zip(pts, L) if la < l < lb]
    out.append(np.array([np.interp(lb, L, pts[:, 0]), np.interp(lb, L, pts[:, 1])]))
    return np.array(out)

def polyline(layer, pts, color, width, dash=None, offset=0.0):
    S = 4  # субпиксельная точность cv2
    if dash is None:
        cv2.polylines(layer, [np.round(pts * S).astype(np.int32)], False, tuple(map(float, color)), width, cv2.LINE_AA, shift=2)
        return
    on, off = dash
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); L = np.concatenate([[0], np.cumsum(seg)])
    pos = -(offset % (on + off))
    while pos < L[-1]:
        a, b = max(pos, 0), min(pos + on, L[-1])
        if b > a:
            sub = trim(pts, a / L[-1], b / L[-1])
            cv2.polylines(layer, [np.round(sub * S).astype(np.int32)], False, tuple(map(float, color)), width, cv2.LINE_AA, shift=2)
        pos += on + off

def disc(layer, p, r, color):
    S = 4
    cv2.circle(layer, tuple(np.round(np.asarray(p) * S).astype(int)), int(round(r * S)), tuple(map(float, color)), -1, cv2.LINE_AA, shift=2)

def ring(layer, p, r, color, w):
    S = 4
    cv2.circle(layer, tuple(np.round(np.asarray(p) * S).astype(int)), int(round(r * S)), tuple(map(float, color)), w, cv2.LINE_AA, shift=2)

_GJ = None
def country(name):
    global _GJ
    if _GJ is None:
        _GJ = json.load(open(f'{D}/dl/ne50.geojson'))
    for f in _GJ['features']:
        if f['properties']['NAME'] == name:
            g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            rings = [np.array([geo(x, y) for x, y in poly[0]]) for poly in polys]
            return max(rings, key=len)
    raise KeyError(name)

# ---------- текст ----------
_FC = {}
def font(size, wght=700, ar=False):
    k = (size, wght, ar)
    if k not in _FC:
        if ar:
            _FC[k] = ImageFont.truetype(FONT_AR, size)
        else:
            f = ImageFont.truetype(FONT, size)
            try: f.set_variation_by_axes([wght])
            except Exception: pass
            _FC[k] = f
    return _FC[k]

def text_rgba(txt, size, wght=700, color=WHITE, track=0.0, ar=False):
    f = font(size, wght, ar)
    if ar:
        bb = f.getbbox(txt, direction='rtl', language='ar')
    else:
        bb = f.getbbox(txt)
    w = int(bb[2] - bb[0] + abs(track) * size * len(txt) + size * 0.4); h = int(size * 1.6)
    im = Image.new('L', (max(w, 2), h), 0); d = ImageDraw.Draw(im)
    if ar:
        d.text((size * 0.2 - bb[0], size * 0.25 - bb[1] * 0 + 0), txt, font=f, fill=255, direction='rtl', language='ar')
    elif track == 0:
        d.text((size * 0.2 - bb[0], size * 0.3), txt, font=f, fill=255)
    else:
        x = size * 0.2
        for ch in txt:
            d.text((x, size * 0.3), ch, font=f, fill=255); x += f.getlength(ch) + track * size
    a = np.asarray(im).astype(np.float32) / 255
    ys, xs = np.nonzero(a > 0.002)
    if len(xs):
        a = a[max(ys.min() - 2, 0):ys.max() + 3, max(xs.min() - 2, 0):xs.max() + 3]
    rgba = np.zeros(a.shape + (4,), np.float32); rgba[..., :3] = color; rgba[..., 3] = a
    return rgba

def place(dst, rgba, x, y, anchor='lt', alpha=1.0, scale=1.0):
    if scale != 1.0:
        rgba = cv2.resize(rgba, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR if scale > 1 else cv2.INTER_AREA)
    h, w = rgba.shape[:2]
    ax = {'l': 0, 'c': 0.5, 'r': 1}[anchor[0]]; ay = {'t': 0, 'm': 0.5, 'b': 1}[anchor[1]]
    x0, y0 = int(round(x - w * ax)), int(round(y - h * ay))
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if xb <= xa or yb <= ya: return dst
    src = rgba[ya - y0:yb - y0, xa - x0:xb - x0]
    a = src[..., 3:4] * alpha
    dst[ya:yb, xa:xb] = dst[ya:yb, xa:xb] * (1 - a) + src[..., :3] * a
    return dst

def shadow(dst, rgba, x, y, anchor='lt', alpha=1.0, blur=18, k=0.6, scale=1.0):
    if scale != 1.0:
        rgba = cv2.resize(rgba, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR if scale > 1 else cv2.INTER_AREA)
    pad = int(blur * 3); a = np.pad(rgba[..., 3], pad)
    a = cv2.GaussianBlur(a, (0, 0), blur) * k * alpha
    sh = np.zeros(a.shape + (4,), np.float32); sh[..., 3] = a
    h, w = rgba.shape[:2]
    ax = {'l': 0, 'c': 0.5, 'r': 1}[anchor[0]]; ay = {'t': 0, 'm': 0.5, 'b': 1}[anchor[1]]
    return place(dst, sh, x - w * ax - pad, y - h * ay - pad + blur * 0.4, 'lt')

# ---------- плашки ----------
def rrect_mask(w, h, r):
    m = np.zeros((h * 4, w * 4), np.uint8)
    r4 = r * 4
    cv2.rectangle(m, (r4, 0), (w * 4 - r4, h * 4), 255, -1); cv2.rectangle(m, (0, r4), (w * 4, h * 4 - r4), 255, -1)
    for cx, cy in ((r4, r4), (w * 4 - r4, r4), (r4, h * 4 - r4), (w * 4 - r4, h * 4 - r4)):
        cv2.circle(m, (cx, cy), r4, 255, -1, cv2.LINE_AA)
    return cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255

def glass(dst, x, y, w, h, r=28, alpha=1.0, tint=0.10, border=0.38, gold_border=False):
    """стеклянная плашка: размытый фон + светлая заливка + тонкая обводка"""
    x, y, w, h = int(x), int(y), int(w), int(h)
    xa, ya, xb, yb = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if xb <= xa or yb <= ya: return dst
    m = rrect_mask(w, h, r)[ya - y:yb - y, xa - x:xb - x][..., None] * alpha
    reg = dst[max(ya - 40, 0):min(yb + 40, H), max(xa - 40, 0):min(xb + 40, W)]
    bl = cv2.GaussianBlur(reg, (0, 0), 16)
    oy, ox = ya - max(ya - 40, 0), xa - max(xa - 40, 0)
    bl = bl[oy:oy + (yb - ya), ox:ox + (xb - xa)]
    fill = bl * (1 - tint) + tint
    dst[ya:yb, xa:xb] = dst[ya:yb, xa:xb] * (1 - m) + fill * m
    # обводка
    outer = rrect_mask(w, h, r); inner = np.pad(rrect_mask(w - 4, h - 4, max(r - 2, 1)), 2)
    edge = np.clip(outer - inner, 0, 1)[ya - y:yb - y, xa - x:xb - x][..., None] * alpha * border
    col = GOLD if gold_border else WHITE
    dst[ya:yb, xa:xb] = dst[ya:yb, xa:xb] * (1 - edge) + col * edge
    return dst

def pill(dst, x, y, w, h, color, alpha=1.0):
    x, y, w, h = int(x), int(y), int(w), int(h)
    m = rrect_mask(w, h, h // 2)
    rgba = np.zeros((h, w, 4), np.float32); rgba[..., :3] = color; rgba[..., 3] = m
    return place(dst, rgba, x, y, 'lt', alpha)

# ---------- кривые ----------
def clamp01(t): return max(0.0, min(1.0, t))
def ease_out(t): t = clamp01(t); return 1 - (1 - t) ** 3
def ease_in_out(t): t = clamp01(t); return 3 * t * t - 2 * t * t * t
def ease_expo(t):
    t = clamp01(t)
    return 0.5 * (2 ** (20 * t - 10)) if t < 0.5 else 1 - 0.5 * 2 ** (-20 * t + 10) if t < 1 else 1.0
def back_out(t, s=1.4):
    t = clamp01(t) - 1; return 1 + (s + 1) * t ** 3 + s * t ** 2
def seg(t, a, b): return clamp01((t - a) / (b - a)) if b > a else float(t >= a)

def text_saw(txt, size, wght=700, color=WHITE):
    """текст с ﷺ: кириллица Montserrat + знак Amiri"""
    if 'ﷺ' not in txt: return text_rgba(txt, size, wght, color)
    a = text_rgba(txt.replace('ﷺ', '').rstrip(), size, wght, color)
    b = text_rgba('ﷺ', int(size * 1.15), 700, color, ar=True)
    h = max(a.shape[0], b.shape[0]); gap = int(size * 0.25)
    out = np.zeros((h, a.shape[1] + gap + b.shape[1], 4), np.float32)
    out[h - a.shape[0]:, :a.shape[1]] = a
    yb = max(0, h - a.shape[0] - int(size * 0.05))
    bb = b[:min(b.shape[0], h - yb)]
    out[yb:yb + bb.shape[0], a.shape[1] + gap:] = np.maximum(out[yb:yb + bb.shape[0], a.shape[1] + gap:], bb)
    return out

def top_shade(img, h=900, k=0.65):
    g = np.clip(1 - np.arange(H) / h, 0, 1) ** 1.4 * k
    return img * (1 - g[:, None, None])
