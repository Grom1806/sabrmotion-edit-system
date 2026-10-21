# «Путь аль-Бухари» — документальный моушен на ночной карте. python3 render.py [out.mp4] [t0] [t1]
import sys, json, math, re, subprocess, numpy as np, cv2
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from docu import *

FPS = 30
WORDS = json.load(open(f'{D}/words.json'))
def norm(w): return re.sub(r'[^\wё-]', '', w.lower().replace('́', ''))
def cue(word, n=1, end=False):
    k = 0
    for w in WORDS:
        if norm(w['w']).startswith(word):
            k += 1
            if k == n: return w['e'] if end else w['t']
    raise KeyError(word)
T_END = WORDS[-1]['e'] + 1.6

NEVER = 1e9
C = dict(
    hook=0.0, kniga=cue('книгу'), buh=cue('бухары'), y810=cue('корана'), s16=cue('шестнадцать'), hajj=cue('хадж'),
    mecca=cue('мекка'), medina=cue('медина'), basra=cue('басра'), kufa=cue('куфа'), baghdad=cue('багдад'),
    egypt=cue('египет'), sham=cue('шам'), rode=NEVER, peredat=NEVER,
    chain=cue('проверял') - 0.25, cep=cue('проверял'), prophet=cue('пророка'), prov=cue('пророка'), zveno=cue('приветствует', end=True),
    k600=cue('шестисот'), k7=cue('семи'), y16=cue('сахих') - 0.15,
    died=NEVER, khart=NEVER, y870=NEVER, sahih=cue('сахих'), world=cue('читают'),
    t1100=cue('тысячи'), outro=cue('историй') - 0.35, end=T_END)
C['y16e'] = C['y16'] + 0.3

ROUTE = ['bukhara', 'mecca', 'medina', 'basra', 'kufa', 'baghdad', 'egypt', 'sham']
RLAB = {'bukhara': ('Бухара', 'l'), 'mecca': ('Мекка', 'r'), 'medina': ('Медина', 'l'), 'basra': ('Басра', 'l'), 'kufa': ('Куфа', 'r'),
        'baghdad': ('Багдад', 'r'), 'egypt': ('Египет', 'r'), 'sham': ('Шам', 'l')}
SEGS = [bez(geo(*CITY[a]), geo(*CITY[b]), (0.12 if a == 'bukhara' else (-0.2 if b == 'egypt' else 0.18)), 120) for a, b in zip(ROUTE[:-1], ROUTE[1:])]
ARRIVE = [C['mecca'], C['medina'], C['basra'], C['kufa'], C['baghdad'], C['egypt'], C['sham']]
LEAVE = [C['hajj'] - 0.2] + [a + 0.05 for a in ARRIVE[:-1]]

# ---------- камера: ключи (t, lon, lat, z) ----------
KEYS = [
    (0.0, 63.0, 40.9, 0.50), (C['buh'], 63.4, 41.1, 0.60), (C['s16'], 63.9, 40.4, 0.70),
    (C['hajj'] + 0.2, 52.0, 31.0, 0.27), (C['mecca'] + 0.3, 41.5, 23.5, 0.36), (C['medina'] + 0.2, 41.8, 25.5, 0.34),
    (C['basra'] + 0.2, 43.2, 28.4, 0.29), (C['baghdad'] + 0.3, 41.0, 29.6, 0.25), (C['sham'] + 0.3, 40.0, 29.2, 0.24),
    (C['chain'] + 0.6, 44.4, 32.0, 0.9), (C['k600'] - 0.3, 44.4, 32.0, 0.95), (C['y16'], 46.0, 33.0, 0.6),
    (C['sahih'] + 0.6, 50.0, 31.5, 0.3), (C['world'] + 0.6, 52.0, 31.0, 0.22), (C['end'], 52.0, 31.0, 0.21),
]
def camera(t):
    for (ta, *a), (tb, *b) in zip(KEYS[:-1], KEYS[1:]):
        if ta <= t <= tb:
            u = ease_in_out((t - ta) / max(tb - ta, 1e-6))
            pa, pb = geo(a[0], a[1]), geo(b[0], b[1])
            z = math.exp(math.log(a[2]) * (1 - u) + math.log(b[2]) * u)
            # «прыжок»: на дальних перелётах камера чуть отъезжает в середине
            dist = np.linalg.norm(pb - pa) * min(a[2], b[2]) / W
            z *= 1 - min(dist, 1.6) * 0.22 * math.sin(math.pi * u)
            c = pa * (1 - u) + pb * u
            return Cam(c[0], c[1], z)
    k = KEYS[-1]; return cam_at(k[1], k[2], k[3])

# ---------- элементы ----------
def city_point(dst, cam, key, label=None, r=9, size=44, side='r', a=1.0, pulse=None, eyebrow=None, lab_a=None):
    if a <= 0: return dst
    p = cam.to_screen(geo(*CITY[key]))[0]
    lay = np.zeros_like(dst)
    disc(lay, p, r * back_out(a), GOLD * 1.1 * min(a * 2, 1))
    if pulse is not None:
        ring(lay, p, r + 8 + 46 * pulse, GOLD * (1 - pulse) * 0.85 * min(a * 2, 1), 2)
    dst = glow_add(dst, lay, (3, 10, 26), (0.9, 0.55, 0.3))
    disc(dst, p, r * 0.45 * back_out(a), WHITE * min(a * 2, 1) + dst[int(np.clip(p[1], 0, H - 1)), int(np.clip(p[0], 0, W - 1))] * 0)
    la = a if lab_a is None else lab_a
    if label and la > 0:
        t = text_rgba(label, size, 700, WHITE)
        dx = (r + 20 + 16 * (1 - ease_out(la))) * (1 if side == 'r' else -1)
        x = p[0] + dx; an = 'lm' if side == 'r' else 'rm'
        dst = shadow(dst, t, x, p[1], an, alpha=la, blur=10, k=0.8)
        dst = place(dst, t, x, p[1], an, alpha=ease_out(la))
        if eyebrow:
            e = text_rgba(eyebrow, 22, 600, GOLD, track=0.18)
            dst = place(dst, e, x, p[1] - size * 0.72, 'lb' if side == 'r' else 'rb', alpha=ease_out(la))
    return dst

_TC = {}
def T(txt, size, wght=700, color=WHITE, track=0.0, maxw=None):
    k = (txt, size, wght, tuple(np.round(color, 3)), track, maxw)
    if k not in _TC:
        r = text_saw(txt, size, wght, color) if 'ﷺ' in txt else text_rgba(txt, size, wght, color, track)
        if maxw and r.shape[1] > maxw:
            r = cv2.resize(r, None, fx=maxw / r.shape[1], fy=maxw / r.shape[1], interpolation=cv2.INTER_AREA)
        _TC[k] = r
    return _TC[k]

def gold_grad(r):
    r = r.copy(); g = np.linspace(1.15, 0.78, r.shape[0])[:, None, None]; r[..., :3] = np.clip(r[..., :3] * g, 0, 1); return r

def pop_word(dst, rgba, x, y, anchor, t, t_in, t_out=None, rise=26, blur_in=True, sh=True):
    """вход: подъём + проявление (крупное — с коротким блюром ≤8 px, мелкое — без блюра); выход — уходит вверх и гаснет"""
    a = ease_out(seg(t, t_in, t_in + 0.32))
    if t_out is not None:
        a *= 1 - ease_in_out(seg(t, t_out, t_out + 0.28))
    if a <= 0.001: return dst
    yy = y + rise * (1 - ease_out(seg(t, t_in, t_in + 0.4)))
    if t_out is not None: yy -= 30 * ease_in_out(seg(t, t_out, t_out + 0.28))
    r = rgba
    big = rgba.shape[0] > 90
    if blur_in and big:
        b = 8 * (1 - ease_out(seg(t, t_in, t_in + 0.22)))
        if b > 0.4:
            r = rgba.copy(); r[..., 3] = cv2.GaussianBlur(np.pad(rgba[..., 3], 12), (0, 0), b)[12:-12, 12:-12]
    if sh: dst = shadow(dst, r, x, yy, anchor, alpha=a, blur=22 if big else 10, k=0.7)
    return place(dst, r, x, yy, anchor, alpha=a)

TYPE_DT = 0.042
def chronicle(dst, txt, sub, t, t_in, t_out):
    if t < t_in or t > t_out + 0.4: return dst
    p = ease_out(seg(t, t_in, t_in + 0.35)); q = 1 - ease_in_out(seg(t, t_out, t_out + 0.35))
    h = 118; y = H - 300; w = int(W * p)
    if w < 2 or q <= 0: return dst
    bar = np.zeros((h, W, 4), np.float32); bar[..., :3] = CREAM; bar[:, :w, 3] = 0.94 * q
    dst = place(dst, bar, 0, y, 'lt')
    gl = np.zeros((4, W, 4), np.float32); gl[..., :3] = GOLD2; gl[:, :w, 3] = q; dst = place(dst, gl, 0, y, 'lt')
    # печатная машинка: символы по 0.028 с
    n = int(max(0, t - t_in - 0.15) / TYPE_DT)
    s1 = txt[:n]; s2 = sub[:max(0, n - len(txt))]
    if s1: dst = place(dst, T(s1, 34, 700, GREEN), 64, y + 22, 'lt', alpha=q)
    if s2: dst = place(dst, T(s2, 26, 500, GREEN * 1.6), 64, y + 70, 'lt', alpha=q)
    return dst

def route_path(t):
    """растущий маршрут: список отрезков до текущей доли"""
    parts = []; head = None
    for i, sg in enumerate(SEGS):
        u = ease_in_out(seg(t, LEAVE[i], ARRIVE[i]))
        if u <= 0: break
        parts.append(trim(sg, 0, u) if u < 1 else sg)
        if u < 1: head = parts[-1][-1]; break
    return parts, head

def book_img(w=520, h=720):
    im = np.zeros((h, w, 4), np.float32)
    im[..., :3] = GREEN * 0.9; im[..., 3] = rrect_mask(w, h, 18)
    # корешок и рамки
    im[:, :34, :3] *= 0.6
    for m, th in ((40, 3), (58, 1)):
        lay = np.zeros((h, w), np.uint8); cv2.rectangle(lay, (m + 20, m), (w - m, h - m), 255, th, cv2.LINE_AA)
        a = lay.astype(np.float32)[..., None] / 255; im[..., :3] = im[..., :3] * (1 - a) + GOLD2 * a
    t1 = text_rgba('صحيح البخاري', 92, 700, GOLD, ar=True)
    t2 = text_rgba('САХИХ АЛЬ-БУХАРИ', 26, 700, GOLD, track=0.16)
    for r, y in ((t1, 250), (t2, 430)):
        x0 = (w + 20 - r.shape[1]) // 2; a = r[..., 3:4]
        im[y:y + r.shape[0], x0:x0 + r.shape[1], :3] = im[y:y + r.shape[0], x0:x0 + r.shape[1], :3] * (1 - a) + r[..., :3] * a
    # ромб-орнамент
    lay = np.zeros((h, w), np.uint8); cx, cy = (w + 20) // 2, 560
    pts = np.array([[cx, cy - 34], [cx + 34, cy], [cx, cy + 34], [cx - 34, cy]]); cv2.polylines(lay, [pts], True, 255, 2, cv2.LINE_AA)
    cv2.polylines(lay, [np.array([[cx, cy - 18], [cx + 18, cy], [cx, cy + 18], [cx - 18, cy]])], True, 255, 2, cv2.LINE_AA)
    a = lay.astype(np.float32)[..., None] / 255; im[..., :3] = im[..., :3] * (1 - a) + GOLD2 * a
    return im
BOOK = None

def persp(rgba, ang, cx, cy, scale=1.0):
    """поворот плоскости вокруг вертикальной оси (ang, град), центр на экране"""
    global _PC
    h, w = rgba.shape[:2]; f = 1600.0; a = math.radians(ang)
    corners = np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]]) * scale
    out = []
    for x, y in corners:
        X, Z = x * math.cos(a), x * math.sin(a); k = f / (f + Z); out.append([cx + X * k, cy + y * k])
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(out))
    return cv2.warpPerspective(rgba, M, (W, H), flags=cv2.INTER_LINEAR)

# ---------- точки «600 000 → 7 000» ----------
rng = np.random.default_rng(7)
NDOT = 600
DOTS = np.c_[rng.uniform(90, W - 90, NDOT), rng.uniform(640, 1500, NDOT)]
KEEP = rng.choice(NDOT, 7, replace=False)

# ---------- кадр ----------
def frame(t, cam_override=None):
    cam = cam_override or camera(t)
    # глубина: в сцене цепочки и чисел карта уходит в расфокус и темнеет
    dof = 10 * ease_in_out(seg(t, C['chain'] - 0.2, C['chain'] + 0.5)) * (1 - ease_in_out(seg(t, C['y16'] + 0.2, C['y16e'] + 0.4)))
    dim = 1 - 0.45 * dof / 10
    img = render_map(cam, blur=dof, bright=dim)
    img = top_shade(img, 950, 0.55)

    # Узбекистан неоном (Бухара → хадж)
    a_uz = seg(t, C['buh'] - 0.1, C['buh'] + 1.2); f_uz = 1 - seg(t, C['hajj'], C['hajj'] + 0.6)
    a_uz2 = seg(t, C['died'] + 0.3, C['died'] + 1.6) * (1 - seg(t, C['sahih'], C['sahih'] + 0.6))
    if (a_uz > 0 and f_uz > 0) or a_uz2 > 0:
        uz = cam.to_screen(country('Uzbekistan')); lay = np.zeros_like(img)
        polyline(lay, trim(uz, 0, ease_in_out(max(a_uz * (f_uz > 0), a_uz2))), WHITE * 0.95 * max(f_uz * (a_uz > 0), a_uz2), 3)
        # пока висит хук — контур не лезет в зону текста
        hk = 1 - ease_in_out(seg(t, C['s16'] - 0.3, C['s16'] + 0.2))
        if hk > 0:
            yy = np.arange(H, dtype=np.float32)
            band = np.clip(1 - np.abs(yy - 600) / 380, 0, 1)[:, None, None] ** 0.5
            lay *= 1 - 0.9 * hk * band
        img = glow_add(img, lay, (3, 9, 24), (0.7, 0.45, 0.25))

    # маршрут
    parts, head = route_path(t)
    fade_r = 1 - 0.75 * ease_in_out(seg(t, C['chain'] - 0.3, C['chain'] + 0.4)) + 0.75 * ease_in_out(seg(t, C['y16e'], C['y16e'] + 0.8))
    if parts and fade_r > 0:
        lay = np.zeros_like(img)
        for p in parts: polyline(lay, cam.to_screen(p), GOLD * fade_r, 4)
        # пунктир впереди (куда ещё поедет) — течёт
        if C['hajj'] < t < C['sham']:
            nxt = [SEGS[i] for i in range(len(SEGS)) if seg(t, LEAVE[i], ARRIVE[i]) < 1]
            for sg in nxt[:2]: polyline(lay, cam.to_screen(sg), GOLD * 0.28, 2, dash=(10, 12), offset=t * 40)
        img = glow_add(img, lay, (3, 10, 28), (0.8, 0.5, 0.3))
        if head is not None:
            hl = np.zeros_like(img); disc(hl, cam.to_screen(head)[0], 9, WHITE); img = glow_add(img, hl, (6, 18, 40), (1.0, 0.7, 0.4))

    # точки городов
    vis_c = 1 - ease_in_out(seg(t, C['chain'] - 0.3, C['chain'] + 0.3)) + ease_in_out(seg(t, C['y16e'], C['y16e'] + 0.6))
    vis_c = min(vis_c, 1 - ease_in_out(seg(t, C['sahih'] - 0.1, C['sahih'] + 0.5)))
    for i, key in enumerate(ROUTE):
        t_on = C['buh'] if key == 'bukhara' else ARRIVE[i - 1]
        a = seg(t, t_on - 0.05, t_on + 0.35) * vis_c
        if a <= 0: continue
        lab, side = RLAB[key]
        lab_a = a * (1 - seg(t, C['peredat'] + 1.0, C['peredat'] + 1.5)) if key != 'bukhara' else a * (1 - seg(t, C['hajj'] + 0.6, C['hajj'] + 1.0))
        pul = ((t - t_on) * 0.9) % 1 if t > t_on else 0
        img = city_point(img, cam, key, lab, r=9 if key == 'bukhara' else 7, size=58 if key == 'bukhara' else 40, side=side,
                         a=a, pulse=pul, eyebrow='МАВЕРАННАХР' if key == 'bukhara' else None, lab_a=lab_a)
    # Самарканд и Хартанг (финал)
    a_k = seg(t, C['khart'] - 0.1, C['khart'] + 0.4) * (1 - seg(t, C['sahih'] - 0.1, C['sahih'] + 0.4))
    if a_k > 0:
        img = city_point(img, cam, 'samarkand', 'Самарканд', r=6, size=34, side='r', a=a_k, pulse=None)
        img = city_point(img, cam, 'khartank', 'Хартанг', r=9, size=52, side='l', a=a_k, pulse=((t - C['khart']) * 0.8) % 1)

    # ---- тексты по битам ----
    # хук
    if t < C['s16'] + 0.3:
        to = C['s16'] - 0.3
        img = pop_word(img, T('Как подросток из Бухары собрал', 44, 500), W / 2, 400, 'cb', t, 0.15, to)
        img = pop_word(img, gold_grad(T('КНИГУ', 250, 900, GOLD)), W / 2, 430, 'ct', t, C['kniga'] - 0.05, to)
        img = pop_word(img, T('которую называют самой достоверной', 38, 500, CREAM), W / 2, 720, 'ct', t, C['kniga'] + 0.45, to)
        img = pop_word(img, T('после Корана', 38, 500, CREAM), W / 2, 770, 'ct', t, C['kniga'] + 0.75, to)
    img = chronicle(img, 'Бухара — 810 год (194 г. х.)', 'Родился аль-Бухари', t, C['kniga'] + 0.9, C['s16'] - 0.3)
    img = chronicle(img, 'В 16 лет — хадж в Мекку', 'и годы в поиске хадисов', t, C['hajj'], C['basra'])
    # «он ехал туда, где жил хотя бы один ПЕРЕДАТЧИК»
    if C['rode'] - 0.3 < t < C['chain'] + 0.4:
        to = C['chain'] - 0.25
        img = pop_word(img, T('Он ехал туда, где жил', 46, 500), 80, 250, 'lt', t, C['rode'], to)
        img = pop_word(img, T('хотя бы один', 104, 800), 80, 320, 'lt', t, C['rode'] + 0.55, to)
        img = pop_word(img, gold_grad(T('ПЕРЕДАТЧИК', 132, 900, GOLD, maxw=900)), 80, 440, 'lt', t, C['peredat'] - 0.04, to)

    # цепочка передатчиков
    a_ch = seg(t, C['chain'] + 0.1, C['chain'] + 0.6) * (1 - ease_in_out(seg(t, C['k600'] - 0.5, C['k600'] - 0.1)))
    if a_ch > 0:
        img = chain_scene(img, t, a_ch)

    # 600 000 → 7 000
    if C['k600'] - 0.4 < t < C['y16'] + 0.2:
        img = numbers_scene(img, t)
    # 16 лет
    img = chronicle(img, 'Хартанг — 870 год (256 г. х.)', 'Рядом с Самаркандом', t, C['khart'] - 0.1, C['sahih'] - 0.4)
    # книга и мир
    if t > C['sahih'] - 0.4:
        img = book_scene(img, t, cam)
    return img

CHAIN = [('Пророк Мухаммад ﷺ', ''), ('Умар ибн аль-Хаттаб', 'сподвижник'), ('Алкама ибн Ваккас', 'Медина'),
         ('Мухаммад ибн Ибрахим ат-Тейми', 'Медина'), ('Яхья ибн Саид аль-Ансари', 'Медина'),
         ('Суфьян ибн Уйейна', 'Мекка'), ('аль-Хумайди', 'Мекка'), ('аль-Бухари', 'Бухара')]
def chain_scene(img, t, a):
    # строим снизу вверх: аль-Бухари → … → Пророк ﷺ; камера едет вверх по цепочке
    n = len(CHAIN); step = 168
    t0, t1 = C['cep'], C['prophet'] + 0.4
    u = ease_in_out(seg(t, t0 - 0.2, t1))
    scroll = (1 - u) * 520 - 40              # сначала видим низ цепочки
    cps = [(W / 2 + (150 if i % 2 else -150), 330 + i * step + 46 + scroll) for i in range(n)]
    snake = np.concatenate([bez(np.array(cps[i + 1]), np.array(cps[i]), (0.55 if i % 2 == 0 else -0.55), 60) for i in range(n - 1)][::-1])
    lay = np.zeros_like(img)
    polyline(lay, trim(snake, 0, ease_in_out(seg(t, t0, t1))), GOLD * a, 4)
    img = glow_add(img, lay, (3, 10, 26), (0.85, 0.5, 0.3))
    for j in range(n):
        i = n - 1 - j                          # порядок появления: снизу вверх
        ti = t0 - 0.35 + (t1 - t0) * j / (n - 1)
        b = ease_out(seg(t, ti, ti + 0.3)) * a
        if b <= 0: continue
        cx, cy = cps[i]; name, sub = CHAIN[i]
        tt = T(name, 34 if i else 38, 700, GOLD if i == 0 else WHITE)
        w = max(tt.shape[1] + 80, 360); h = 92 if sub else 80
        yy = cy + 18 * (1 - b)
        img = glass(img, cx - w / 2, yy - h / 2, w, h, r=24, alpha=b, tint=0.12, gold_border=(i in (0, n - 1)))
        img = place(img, tt, cx, yy - (12 if sub else 0), 'cm', alpha=b)
        if sub: img = place(img, T(sub, 22, 500, CREAM * 0.85), cx, yy + 22, 'cm', alpha=b)
    # «проверял каждое звено»: кольцо-лупа проходит по звеньям сверху вниз
    v = seg(t, C['prov'], C['zveno'] + 0.4)
    if 0 < v < 1:
        k = v * (n - 1); i0 = int(k); fr = k - i0
        p = np.array(cps[i0]) * (1 - fr) + np.array(cps[min(i0 + 1, n - 1)]) * fr
        lay = np.zeros_like(img); ring(lay, p, 120, GOLD * 0.9, 3); img = glow_add(img, lay, (4, 12), (0.8, 0.4))
    img = pop_word(img, T('Хадис № 1: восемь звеньев до Пророка ﷺ', 30, 600, CREAM), W / 2, 205, 'cm', t, C['cep'], C['k600'] - 0.5, rise=12)
    return img

def numbers_scene(img, t):
    a_in = ease_out(seg(t, C['k600'] - 0.3, C['k600'] + 0.2)); a_out = 1 - ease_in_out(seg(t, C['y16'] - 0.2, C['y16'] + 0.15))
    a = a_in * a_out
    if a <= 0: return img
    # счётчик
    u = ease_out(seg(t, C['k600'] - 0.1, C['k600'] + 1.1)); val = int(round(600000 * u / 1000.0)) * 1000
    s = f'{val:,}'.replace(',', ' ')
    gone = ease_in_out(seg(t, C['k7'] - 0.6, C['k7'] + 0.3))
    img = place(img, gold_grad(T(s, 170, 900, GOLD)), W / 2, 330, 'ct', alpha=a * (1 - gone))
    img = place(img, T('передач собрал', 44, 600), W / 2, 540, 'ct', alpha=a * (1 - gone))
    # точки: 600 огней, на «семи тысяч» гаснут все, кроме 7
    lay = np.zeros_like(img)
    nshow = int(NDOT * u)
    for i in range(nshow):
        keep = i in KEEP
        al = a * (1 if keep else 1 - gone)
        if al <= 0.01: continue
        p = DOTS[i]
        if keep:
            tgt = np.array([W / 2, 1180 - list(KEEP).index(i) * 46]); p = p * (1 - gone) + tgt * gone
        disc(lay, p, (5 if keep else 3) * (1 + gone * keep * 1.4), GOLD * al)
    img = glow_add(img, lay, (3, 9), (0.8, 0.4))
    if gone > 0:
        img = pop_word(img, gold_grad(T('≈ 7 000', 170, 900, GOLD)), W / 2, 330, 'ct', t, C['k7'] - 0.05, C['y16'] - 0.2)
        img = pop_word(img, T('вошло в книгу', 44, 600), W / 2, 540, 'ct', t, C['k7'] + 0.25, C['y16'] - 0.2)
    return img

def years_scene(img, t):
    a = ease_out(seg(t, C['y16'] - 0.2, C['y16'] + 0.2)) * (1 - ease_in_out(seg(t, C['died'] - 0.2, C['died'] + 0.25)))
    if a <= 0: return img
    x0, x1, y = 120, W - 120, 900
    p = ease_in_out(seg(t, C['y16'], C['y16e'] + 0.3))
    lay = np.zeros_like(img)
    polyline(lay, np.array([[x0, y], [x0 + (x1 - x0) * p, y]], float), GOLD * a, 4)
    for k in range(16):
        x = x0 + (x1 - x0) * k / 15
        on = p * 15 >= k - 0.01
        disc(lay, (x, y), 9 if on else 5, GOLD * a * (1 if on else 0.35))
    img = glow_add(img, lay, (3, 10, 24), (0.8, 0.5, 0.3))
    n = min(16, int(p * 15 + 1.001))
    img = place(img, gold_grad(T(f'{n}', 260, 900, GOLD)), W / 2, 520, 'ct', alpha=a)
    img = place(img, T('лет работы над книгой', 46, 600), W / 2, 960, 'ct', alpha=a)
    return img

def book_scene(img, t, cam):
    global BOOK
    if BOOK is None: BOOK = book_img()
    a = ease_out(seg(t, C['sahih'] - 0.2, C['sahih'] + 0.5)) * (1 - ease_in_out(seg(t, C['end'] - 0.9, C['end'] - 0.3)))
    if a <= 0: return img
    # дуги по миру от Бухары
    w = ease_in_out(seg(t, C['world'] - 0.2, C['t1100'] + 0.6))
    if w > 0:
        src = geo(*CITY['bukhara']); lay = np.zeros_like(img)
        for k, ang in enumerate(np.linspace(-170, 170, 11)):
            dst = src + 9000 * np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
            arc = cam.to_screen(bez(src, dst, 0.2, 80))
            polyline(lay, trim(arc, 0, ease_out(seg(w, k * 0.04, k * 0.04 + 0.6))), GOLD * 0.8 * a, 3)
        img = glow_add(img, lay, (3, 10, 26), (0.8, 0.5, 0.3))
    ang = 28 * (1 - ease_out(seg(t, C['sahih'] - 0.2, C['sahih'] + 1.2))) - 4 * seg(t, C['sahih'] + 1.2, C['end'])
    sc = (0.86 + 0.06 * seg(t, C['sahih'], C['end'])) * (0.92 + 0.08 * ease_out(seg(t, C['sahih'] - 0.2, C['sahih'] + 0.6)))
    shadow_l = np.zeros((H, W, 4), np.float32)
    bk = persp(BOOK, ang, W / 2, 900, sc)
    sh = cv2.GaussianBlur(bk[..., 3], (0, 0), 30) * 0.7 * a
    img = img * (1 - sh[..., None])
    img = img * (1 - bk[..., 3:4] * a) + bk[..., :3] * bk[..., 3:4] * a
    img = pop_word(img, T('читают больше', 46, 600), W / 2, 1360, 'ct', t, C['world'] - 0.1, C['outro'] - 0.3)
    img = pop_word(img, gold_grad(T('1100 лет', 130, 900, GOLD)), W / 2, 1430, 'ct', t, C['t1100'] - 0.05, C['outro'] - 0.3)
    # финал: вордмарк
    if t > C['outro'] - 0.2:
        wm = text_rgba('Ummah Link', 96, 400, CREAM); wm = wm  # Pacifico ниже
        f = ImageFont.truetype(f'{D}/fonts/Pacifico.ttf', 104)
        im = Image.new('L', (900, 220), 0); ImageDraw.Draw(im).text((30, 10), 'Ummah Link', font=f, fill=255)
        al = np.asarray(im).astype(np.float32) / 255; ys, xs = np.nonzero(al > 0.01); al = al[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        wm = np.zeros(al.shape + (4,), np.float32); wm[..., :3] = CREAM; wm[..., 3] = al
        img = pop_word(img, T('Больше историй — в', 40, 500, CREAM), W / 2, 1380, 'ct', t, C['outro'], None, rise=14)
        img = pop_word(img, wm, W / 2, 1440, 'ct', t, C['outro'] + 0.5, None)
    return img

def finish(img, t):
    img = vignette(img, 0.6)
    # общий fade in/out
    k = ease_out(seg(t, 0, 0.35)) * (1 - ease_in_out(seg(t, C['end'] - 0.5, C['end'])))
    return (np.clip(img * k, 0, 1) * 255).astype(np.uint8)

def cam_speed(t):
    a, b = camera(t), camera(t + 1 / FPS)
    p = np.array([[W / 2, H / 2], [0, 0], [W, H]], float)
    pa = np.linalg.inv(np.vstack([a.M(), [0, 0, 1]])) @ np.c_[p, np.ones(3)].T
    sb = b.to_screen(pa[:2].T)
    return float(np.max(np.linalg.norm(sb - p, axis=1)))

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else f'{D}/out.mp4'
    t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    t1 = float(sys.argv[3]) if len(sys.argv) > 3 else C['end']
    print({k: round(v, 2) for k, v in C.items()})
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    n0, n1 = int(t0 * FPS), int(t1 * FPS)
    for n in range(n0, n1):
        t = n / FPS
        sp = cam_speed(t)
        if sp > 6:   # motion blur 180°: сабсэмплы затвора только по камере
            k = min(7, 2 + int(sp / 10)); acc = None
            for j in range(k):
                tj = t + (j / (k - 1) - 0.5) * 0.5 / FPS
                f = frame(tj, camera(tj)) if j != k // 2 else frame(t)
                acc = f if acc is None else acc + f
            img = acc / k
        else:
            img = frame(t)
        pr.stdin.write(finish(img, t).tobytes())
        if n % 60 == 0: print(f'{t:.1f}s sp={sp:.1f}', flush=True)
    pr.stdin.close(); pr.wait()
