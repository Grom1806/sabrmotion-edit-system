# Слои движка: Text (буквы/слова), Counter, Box (расширение из точки/линии/угла, рост контейнера),
# Picture (фото без апскейла, blur-rise, Ken Burns до ровных 100 %), Path (линия рисуется), Clip (видео).
# Каждый слой сам регистрирует свои SFX-события (sfx-expressive: буква = тик, объект = свой звук)
# и свои «окна чтения» (reading-time) — микшер и QA берут их отсюда, а не «на глаз».
import math, subprocess
import numpy as np, cv2
from .core import *

def ev(t, kind, layer, db=None, **kw):
    e = dict(t=round(max(t, 0.0), 4), kind=kind, layer=layer)
    if db is not None: e['db'] = db
    e.update(kw); return e

class Layer:
    world = True      # False = экранный слой (не двигается камерой: субтитры, логотип)
    z = 0
    def __init__(s, name, t_in, t_out=None):
        s.name, s.t_in, s.t_out = name, t_in, t_out
    def alive(s, t): return t >= s.t_in - 1e-6 and (s.t_out is None or t <= s.t_out + s.out_dur() + 1e-6)
    def out_dur(s): return 0.0
    def draw(s, dst, t, cam): pass
    def events(s): return []
    def holds(s): return []            # [(текст, слов, t_полностью_видно, t_уход, тип)]
    def issues(s): return []           # нарушения резкости (апскейл и т.п.)
    def motion(s, t): return 0.0       # px/кадр — для motion blur
    def reveal(s): return None         # (t0, t1) окно проявления — для QA конфликтов

# ---------------- ТЕКСТ ----------------
class Text(Layer):
    """Надпись. mode='letters' — побуквенно (заголовки ≥60 px: blur ≤8 px только на входе, тик на букву);
    mode='words' — по словам, opacity + y 6–8 px, резко с первого кадра (мелкий текст, без блюра).
    times — явные моменты появления слов (субтитры по words.json)."""
    def __init__(s, name, text, x, y, size, t_in, t_out=None, font='Inter-Bold', color='#FFFFFF',
                 anchor='l', mode='auto', stagger=None, unit_dur=None, rise=None, times=None,
                 kind='body', line_h=1.18, sfx=True, tick_db=None, out_dur=None, world=True, z=10, wobble=0.0):
        super().__init__(name, t_in, t_out)
        s.text, s.x, s.y, s.size, s.font = text, x, y, size, font
        s.color = hexc(color) if isinstance(color, str) else np.asarray(color, np.float32)
        s.anchor, s.kind, s.line_h, s.sfx, s.world, s.z, s.wobble = anchor, kind, line_h, sfx, world, z, wobble
        s.mode = mode if mode != 'auto' else ('letters' if size >= 60 else 'words')
        letters = s.mode == 'letters'
        s.stagger = stagger if stagger is not None else (0.035 if letters else 0.06)
        s.unit_dur = unit_dur if unit_dur is not None else (0.2 if letters else 0.2)
        s.rise = rise if rise is not None else (14 if letters else 7)
        s.blur = 8.0 if (letters and size >= 60) else 0.0          # sharpness-guard: мелкий текст без блюра
        s.tick_db = tick_db if tick_db is not None else (-24 if letters else -27)
        s._out = out_dur if out_dur is not None else 0.22
        s.lines = text.split('\n')
        # единицы: (строка, i0, i1) — буквы или слова
        s.units = []
        for li, ln in enumerate(s.lines):
            if letters:
                s.units += [(li, i, i + 1) for i, ch in enumerate(ln) if ch.strip()]
            else:
                i = 0
                for wd in ln.split(' '):
                    if wd: s.units.append((li, i, i + len(wd)))
                    i += len(wd) + 1
        if times is not None:
            assert len(times) == len(s.units), f'{name}: {len(times)} времён на {len(s.units)} слов'
            s.t_units = list(times)
        else:
            s.t_units = [t_in + k * s.stagger for k in range(len(s.units))]
        s.t_full = s.t_units[-1] + s.unit_dur if s.units else t_in
        s.unit_of = {}
        for k, (li, a, b) in enumerate(s.units):
            for i in range(a, b): s.unit_of[(li, i)] = k

    def out_dur(s): return s._out
    def reveal(s): return (s.t_in, s.t_full)

    def _op(s, k, t):
        u = prog(t, s.t_units[k], s.t_units[k] + s.unit_dur)
        op = EASE(u)
        if s.t_out is not None and t > s.t_out:
            op *= 1 - EASE(prog(t, s.t_out, s.t_out + s._out))
        return op, u

    def draw(s, dst, t, cam):
        if not s.alive(t) or not s.units: return
        z = cam.z
        sz = s.size * z
        lh = s.size * s.line_h
        for li, ln in enumerate(s.lines):
            xs, wd, asc, desc = layout(ln, s.font, sz)
            wx = s.x - {'l': 0, 'c': 0.5, 'r': 1}[s.anchor] * (wd / z)
            for i, ch in enumerate(ln):
                k = s.unit_of.get((li, i))
                if k is None: continue
                op, u = s._op(k, t)
                if op <= 0.002: continue
                dy = s.rise * (1 - EASE(u))
                if s.t_out is not None and t > s.t_out: dy -= s.rise * 0.5 * EASE(prog(t, s.t_out, s.t_out + s._out))
                if s.wobble: dy += s.wobble * math.sin(2 * math.pi * (t * 0.35 + k * 0.07))
                px, py = cam.pt(wx, s.y + li * lh + dy) if s.world else (wx, s.y + li * lh + dy)
                px += xs[i]
                x0, y0 = int(math.floor(px)), int(math.floor(py))
                fx, fy = round((px - x0) * 4) / 4, round((py - y0) * 4) / 4
                a, ox, oy = glyph(ch, s.font, qsize(sz), fx, fy)
                b = s.blur * max(0.0, 1 - op / 0.5)            # блюр уходит к 50 % непрозрачности
                if b > 0.25:
                    p = int(b * 3) + 1
                    a = cv2.GaussianBlur(np.pad(a, p), (0, 0), b); x0 -= p; y0 -= p
                over(dst, s.color, a * op, x0 - ox, y0 - oy)

    def events(s):
        if not s.sfx: return []
        out = []
        for k, (li, a, b) in enumerate(s.units):
            unit = s.lines[li][a:b]
            # тик в кадр, где единица впервые видна; одна буква = один тик, слово = один тихий тик
            out.append(ev(s.t_units[k] + 1 / FPS, 'tick', s.name, s.tick_db, unit=unit,
                          pitch=((k * 7) % 3 - 1) * 0.5, pan=round(-0.3 + 0.6 * (k / max(1, len(s.units) - 1)), 2)))
        return out

    def holds(s):
        words = len(s.text.split())
        return [(s.text.replace('\n', ' '), words, s.t_full, s.t_out, s.kind)]

    def letters(s): return sum(1 for ln in s.lines for ch in ln if ch.strip())

# ---------------- СЧЁТЧИК ----------------
def fmt_int(n): return f'{int(round(n)):,}'.replace(',', ' ')

class Counter(Text):
    """Число-герой: счёт от a до b (ease), цифры фиксированной ширины (не прыгают), удар в конце."""
    def __init__(s, name, a, b, x, y, size, t_in, dur=1.2, t_out=None, fmt=fmt_int, suffix='', **kw):
        s.a, s.b, s.dur, s.fmt, s.suffix = a, b, dur, fmt, suffix
        super().__init__(name, fmt(b) + suffix, x, y, size, t_in, t_out, mode='words', rise=10, unit_dur=0.25, kind='number', **kw)
        s.t_full = t_in + dur
    def reveal(s): return (s.t_in, s.t_in + s.dur)
    def draw(s, dst, t, cam):
        if not s.alive(t): return
        v = lerp(s.a, s.b, EASE_ACCENT(prog(t, s.t_in, s.t_in + s.dur)))
        txt = s.fmt(v) + s.suffix
        sz = s.size * cam.z
        op = EASE(prog(t, s.t_in, s.t_in + s.unit_dur))
        if s.t_out is not None and t > s.t_out: op *= 1 - EASE(prog(t, s.t_out, s.t_out + s._out))
        if op <= 0.002: return
        f = font(s.font, qsize(sz))
        dw = max(f.getlength(d) for d in '0123456789')
        adv = [dw if ch.isdigit() else f.getlength(ch) for ch in txt]
        total = sum(adv) / cam.z
        wx = s.x - {'l': 0, 'c': 0.5, 'r': 1}[s.anchor] * total
        sc = pop_scale(t, s.t_in + s.dur - 0.02, 0.18, 0.05) if t >= s.t_in + s.dur - 0.02 else 1.0
        px, py = cam.pt(wx, s.y + s.rise * (1 - EASE(prog(t, s.t_in, s.t_in + s.unit_dur)))) if s.world else (wx, s.y)
        x = px
        for ch, w_ in zip(txt, adv):
            cx = x + (w_ - f.getlength(ch)) / 2
            x0 = int(math.floor(cx)); fx = round((cx - x0) * 4) / 4
            a, ox, oy = glyph(ch, s.font, qsize(sz * (sc if sc > 0 else 1)), fx)
            over(dst, s.color, a * op, x0 - ox, int(round(py)) - oy)
            x += w_
    def events(s):
        if not s.sfx: return []
        return [ev(s.t_in, 'counter', s.name, -24, dur=s.dur),
                ev(s.t_in + s.dur, 'impact', s.name, -16)]

# ---------------- ПЛАШКА / КАРТОЧКА ----------------
class Box(Layer):
    """Скруглённый блок. enter: 'point' (из точки), 'line' (линия → блок), 'corner' (из угла), 'fade'.
    keys: [(t, x, y, w, h)] — контейнер растёт/едет за контентом (ref-ui-card «контейнер растёт с объектом»).
    hero=True — мягкий перелёт с одним колебанием (только герои)."""
    def __init__(s, name, x, y, w, h, t_in, t_out=None, color='#FFFFFF', radius=28, enter='point', dur=0.45,
                 hero=False, shadow=True, keys=None, sfx=True, sound=None, z=0, world=True, op=1.0, out='shrink'):
        super().__init__(name, t_in, t_out)
        s.x, s.y, s.w, s.h = x, y, w, h
        s.color = hexc(color) if isinstance(color, str) else np.asarray(color, np.float32)
        s.radius, s.enter, s.dur, s.hero, s.shadow, s.sfx, s.sound, s.z, s.world, s.op, s.outm = \
            radius, enter, dur, hero, shadow, sfx, sound, z, world, op, out
        s.keys = sorted(keys) if keys else [(t_in, x, y, w, h)]
    def out_dur(s): return 0.3
    def geom(s, t):
        k = [(a[0], a[1:]) for a in s.keys]
        x, y, w, h = kf(t, k) if len(k) > 1 else k[0][1]
        u = prog(t, s.t_in, s.t_in + s.dur)
        cx, cy = x + w / 2, y + h / 2
        if s.enter == 'point':
            sc = pop_scale(t, s.t_in, s.dur, 0.06) if s.hero else EASE(u)
            w, h = w * sc, h * sc
        elif s.enter == 'line':
            u1, u2 = EASE(prog(u, 0, 0.45)), EASE(prog(u, 0.45, 1))
            hh = 4 + (h - 4) * u2
            w, h = w * u1, hh
        elif s.enter == 'corner':
            sc = pop_scale(t, s.t_in, s.dur, 0.06) if s.hero else EASE(u)
            w, h = w * sc, h * sc; cx, cy = x + w / 2, y + h / 2
        op = s.op * (EASE(prog(u, 0, 0.35)) if s.enter in ('point', 'corner', 'line') else EASE(u))
        if s.t_out is not None and t > s.t_out:
            v = EASE_IN(prog(t, s.t_out, s.t_out + 0.3))
            if s.outm == 'shrink': w, h = w * (1 - 0.4 * v), h * (1 - 0.4 * v)
            op *= 1 - v
        return cx, cy, w, h, op
    def draw(s, dst, t, cam):
        if not s.alive(t) or t < s.t_in: return
        cx, cy, w, h, op = s.geom(t)
        if w < 0.5 or h < 0.5 or op <= 0.002: return
        z = cam.z if s.world else 1.0
        sx, sy = cam.pt(cx, cy) if s.world else (cx, cy)
        w, h = w * z, h * z
        x0f, y0f = sx - w / 2, sy - h / 2
        x0, y0 = int(math.floor(x0f)), int(math.floor(y0f))
        a = rrect_alpha(w, h, s.radius * z * min(1, w / max(s.w * z, 1e-6) * 1.5), 2, (x0f - x0, y0f - y0))
        if s.shadow: soft_shadow(dst, a * op, x0 - 2, y0 - 2, blur=34 * z, op=0.28, dy=14 * z)
        over(dst, s.color, a * op, x0 - 2, y0 - 2)
    def motion(s, t):
        a, b = s.geom(t), s.geom(t + 1 / FPS)
        return math.hypot(b[0] - a[0], b[1] - a[1]) + abs(b[2] - a[2]) / 2 + abs(b[3] - a[3]) / 2
    def events(s):
        if not s.sfx: return []
        big = s.w * s.h > 300 * 300
        out = []
        if s.enter == 'line':
            out.append(ev(s.t_in, 'stroke', s.name, -26))
            out.append(ev(s.t_in + s.dur * 0.45, 'card' if big else 'pop', s.name, -22))
        elif s.enter != 'none':
            out.append(ev(s.t_in, s.sound or ('card' if big else 'pop'), s.name, -20 if s.hero else -23))
        for (ta, *a), (tb, *b) in zip(s.keys[:-1], s.keys[1:]):
            if a != b: out.append(ev(ta, 'grow', s.name, -24, dur=tb - ta))
        return out

# ---------------- ФОТО ----------------
class Picture(Layer):
    """Фото в рамке x,y,w,h (cover). Апскейл запрещён: если фото меньше рамки — issue (sharpness-guard).
    enter: 'rise' (blur 12→0 + y 40→0 + opacity, для крупных объектов), 'wipe' (шторка слева), 'fade'.
    kb — Ken Burns: масштаб kb→1.0 за kb_dur и ровно 1.0 в покое."""
    def __init__(s, name, path, x, y, w, h, t_in, t_out=None, radius=24, enter='rise', dur=0.5,
                 kb=1.0, kb_dur=None, shadow=True, sfx=True, z=0, world=True, focus=(0.5, 0.5)):
        super().__init__(name, t_in, t_out)
        im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if im is None: raise FileNotFoundError(path)
        if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        s.alpha = im[..., 3].astype(np.float32) / 255 if im.shape[2] == 4 else None
        s.img = cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2RGB).astype(np.float32) / 255
        s.path, s.x, s.y, s.w, s.h = path, x, y, w, h
        s.radius, s.enter, s.dur, s.kb, s.shadow, s.sfx, s.z, s.world, s.focus = radius, enter, dur, kb, shadow, sfx, z, world, focus
        s.kb_dur = kb_dur if kb_dur is not None else dur + 1.2
        ih, iw = s.img.shape[:2]
        s.base = max(w / iw, h / ih)
    def out_dur(s): return 0.3
    def issues(s):
        if s.base > 1.0001:
            return [f'{s.name}: апскейл фото {s.base * 100:.0f} % ({s.img.shape[1]}×{s.img.shape[0]} в рамку {s.w}×{s.h}) — нужен исходник крупнее']
        return []
    def kbs(s, t): return kf(t, [(s.t_in, s.kb), (s.t_in + s.kb_dur, 1.0)], EASE_SOFT) if s.kb != 1.0 else 1.0
    def draw(s, dst, t, cam):
        if not s.alive(t) or t < s.t_in: return
        u = prog(t, s.t_in, s.t_in + s.dur); e = EASE(u)
        op = e if s.enter in ('rise', 'fade') else 1.0
        dy = 40 * (1 - e) if s.enter == 'rise' else 0
        blur = 12 * (1 - e) if s.enter == 'rise' else 0
        if s.t_out is not None and t > s.t_out:
            v = EASE_IN(prog(t, s.t_out, s.t_out + 0.3)); op *= 1 - v; dy -= 30 * v
        if op <= 0.002: return
        z = cam.z if s.world else 1.0
        sx, sy = cam.pt(s.x, s.y + dy) if s.world else (s.x, s.y + dy)
        W_, H_ = s.w * z, s.h * z
        sc = s.base * s.kbs(t) * z                    # пикселей экрана на пиксель исходника
        ih, iw = s.img.shape[:2]
        cw, ch = W_ / sc, H_ / sc
        fx, fy = s.focus
        cx = clamp(iw * fx, cw / 2, iw - cw / 2); cy = clamp(ih * fy, ch / 2, ih - ch / 2)
        x0, y0 = int(math.floor(sx)), int(math.floor(sy))
        ow, oh = int(round(W_)), int(round(H_))
        if ow < 2 or oh < 2: return
        if abs(sc - 1.0) < 1e-6 and abs(sx - x0) < 1e-6:
            xa, ya = int(round(cx - cw / 2)), int(round(cy - ch / 2))
            patch = s.img[ya:ya + oh, xa:xa + ow]
        else:
            M = np.float32([[sc, 0, -(cx - cw / 2) * sc + (sx - x0)], [0, sc, -(cy - ch / 2) * sc + (sy - y0)]])
            src = s.img
            if sc < 0.5:  # сильное уменьшение: сначала INTER_AREA, чтобы не было муара
                k = 0.5 / sc
                src = cv2.resize(s.img, None, fx=1 / k, fy=1 / k, interpolation=cv2.INTER_AREA)
                M = np.float32([[sc * k, 0, M[0, 2]], [0, sc * k, M[1, 2]]])
            patch = cv2.warpAffine(src, M, (ow, oh), flags=cv2.INTER_CUBIC if sc > 1 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        a = rrect_alpha(ow, oh, s.radius * z, 0)[:patch.shape[0], :patch.shape[1]]
        if s.enter == 'wipe':
            a = a * (np.arange(a.shape[1])[None, :] < EASE(u) * a.shape[1])
        if blur > 0.3:
            patch = cv2.GaussianBlur(patch, (0, 0), blur)
        if s.shadow: soft_shadow(dst, a * op, x0, y0, blur=40 * z, op=0.3, dy=18 * z)
        over(dst, np.clip(patch, 0, 1), a * op, x0, y0)
    def motion(s, t):
        return 40 * abs(EASE(prog(t + 1 / FPS, s.t_in, s.t_in + s.dur)) - EASE(prog(t, s.t_in, s.t_in + s.dur)))
    def events(s):
        return [ev(s.t_in, 'swish', s.name, -24)] if s.sfx else []

# ---------------- ЛИНИЯ (рисуется) ----------------
class Path(Layer):
    """Ломаная/кривая рисуется от 0 до 100 % за dur (trim path). pts — мировые координаты."""
    def __init__(s, name, pts, t_in, dur=0.6, t_out=None, color='#FFFFFF', width=6, sfx=True, z=5, world=True):
        super().__init__(name, t_in, t_out)
        s.pts = np.asarray(pts, np.float64); s.dur, s.width, s.sfx, s.z, s.world = dur, width, sfx, z, world
        s.color = hexc(color) if isinstance(color, str) else np.asarray(color, np.float32)
        seg = np.linalg.norm(np.diff(s.pts, axis=0), axis=1); s.L = np.concatenate([[0], np.cumsum(seg)])
    def out_dur(s): return 0.25
    def draw(s, dst, t, cam):
        if not s.alive(t) or t < s.t_in: return
        u = EASE(prog(t, s.t_in, s.t_in + s.dur)); op = 1.0
        if s.t_out is not None and t > s.t_out: op = 1 - EASE(prog(t, s.t_out, s.t_out + 0.25))
        lb = u * s.L[-1]
        keep = [p for p, l in zip(s.pts, s.L) if l < lb]
        end = np.array([np.interp(lb, s.L, s.pts[:, 0]), np.interp(lb, s.L, s.pts[:, 1])])
        pts = np.array(keep + [end])
        if len(pts) < 2: return
        if s.world: pts = np.array([cam.pt(*p) for p in pts])
        m = np.zeros(dst.shape[:2], np.float32)
        cv2.polylines(m, [np.round(pts * 16).astype(np.int32)], False, 1.0, max(1, int(round(s.width * (cam.z if s.world else 1)))), cv2.LINE_AA, shift=4)
        over(dst, s.color, m * op, 0, 0)
    def events(s):
        return [ev(s.t_in, 'stroke', s.name, -26, dur=s.dur)] if s.sfx else []

# ---------------- ВИДЕО ----------------
class Clip(Layer):
    """Видео-исходник в рамке (cover), декод ffmpeg последовательно. grade — строка фильтров ffmpeg
    (грейд из color-playbook), применяется при декоде. Фон оригинальный (keep-original-background)."""
    def __init__(s, name, path, x, y, w, h, t_in, t_out, src_in=0.0, grade='', z=-5, world=True, sfx=False):
        super().__init__(name, t_in, t_out)
        s.path, s.x, s.y, s.w, s.h, s.src_in, s.grade, s.z, s.world, s.sfx = path, x, y, w, h, src_in, grade, z, world, sfx
        s._p = None; s._next = None; s._last = None
    def _open(s, n):
        if s._p: s._p.kill()
        vf = f'fps={FPS},scale={s.w}:{s.h}:force_original_aspect_ratio=increase:flags=lanczos,crop={s.w}:{s.h}'
        if s.grade: vf += ',' + s.grade
        s._p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{s.src_in + n / FPS:.4f}', '-i', s.path, '-vf', vf,
                                 '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        s._next = n
    def frame(s, n):
        if s._last is not None and s._last[0] == n: return s._last[1]
        if s._p is None or s._next != n: s._open(n)
        buf = s._p.stdout.read(s.w * s.h * 3)
        if len(buf) < s.w * s.h * 3:
            return s._last[1] if s._last else np.zeros((s.h, s.w, 3), np.float32)
        f = np.frombuffer(buf, np.uint8).reshape(s.h, s.w, 3).astype(np.float32) / 255
        s._next = n + 1; s._last = (n, f); return f
    def draw(s, dst, t, cam):
        if not (s.t_in <= t < s.t_out): return
        f = s.frame(int(round((t - s.t_in) * FPS)))
        if s.world and not cam.at_rest or (s.world and (cam.cx, cam.cy) != (W / 2, H / 2)):
            sx, sy = cam.pt(s.x, s.y)
            M = np.float32([[cam.z, 0, sx], [0, cam.z, sy]])
            m = cv2.warpAffine(np.ones(f.shape[:2], np.float32), M, (dst.shape[1], dst.shape[0]))
            g = cv2.warpAffine(f, M, (dst.shape[1], dst.shape[0]), flags=cv2.INTER_CUBIC)
            dst[:] = dst * (1 - m[..., None]) + g * m[..., None]
        else:
            over(dst, f, np.ones(f.shape[:2], np.float32), int(s.x), int(s.y))
