"""sharpcheck.py — вторая защита от «мыла»: сравнивает резкость кадров AE (эталон) с кадрами готового видео.

Использование (на ПК):
  python sharpcheck.py --frames <папка с PNG из AE saveFrameToPng, имена вида NAME_<сек>.png или NAME_f<кадр>.png> --video master.mp4 [--video light.mp4]
  python sharpcheck.py --frames <папка PNG>            # только абсолютная проверка стиль-фреймов

Метрика: Tenengrad (средний квадрат градиента Собеля) по самым детальным 10 % тайлов кадра —
так меряется резкость текста и краёв, а не пустого фона.
FAIL, если кадр видео < 90 % резкости кадра AE (виноват экспорт/кодек),
или если стиль-фрейм заметно мягче своих соседей (< 60 % медианы — виноваты слои: размытие, апскейл, шум поверх).
Нужно: numpy, Pillow, ffmpeg в PATH.
"""
import argparse, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image

def sharp(path):
    g = np.asarray(Image.open(path).convert("L"), dtype=np.float32)
    gx = np.zeros_like(g); gy = np.zeros_like(g)
    gx[1:-1, 1:-1] = (g[:-2, 2:] + 2 * g[1:-1, 2:] + g[2:, 2:]) - (g[:-2, :-2] + 2 * g[1:-1, :-2] + g[2:, :-2])
    gy[1:-1, 1:-1] = (g[2:, :-2] + 2 * g[2:, 1:-1] + g[2:, 2:]) - (g[:-2, :-2] + 2 * g[:-2, 1:-1] + g[:-2, 2:])
    e = gx * gx + gy * gy
    h, w = e.shape; t = 64
    tiles = [e[y:y + t, x:x + t].mean() for y in range(0, h - t + 1, t) for x in range(0, w - t + 1, t)]
    tiles.sort(reverse=True)
    top = tiles[:max(1, len(tiles) // 10)]
    return float(np.mean(top)), (w, h)

def frame_time(name, fps):
    m = re.search(r"_f(\d+)\.png$", name)
    if m: return int(m.group(1)) / fps
    m = re.search(r"_(\d+(?:\.\d+)?)s?\.png$", name)
    return float(m.group(1)) if m else None

def grab(video, t, size, tmp):
    out = os.path.join(tmp, "v_%.3f.png" % t)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % t, "-i", video, "-frames:v", "1",
                    "-vf", "scale=%d:%d:flags=neighbor" % size, out], check=True)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", required=True)
    ap.add_argument("--video", action="append", default=[])
    ap.add_argument("--fps", type=float, default=30.0)
    a = ap.parse_args()
    pngs = sorted(f for f in os.listdir(a.frames) if f.lower().endswith(".png") and not f.startswith("_"))
    if not pngs: sys.exit("нет PNG в " + a.frames)
    res = {f: sharp(os.path.join(a.frames, f)) for f in pngs}
    med = float(np.median([v[0] for v in res.values()]))
    fails = 0
    print("Кадр".ljust(40), "резкость", "отн. медианы")
    for f, (s, size) in res.items():
        rel = s / med if med else 0
        flag = "FAIL мягче соседей — проверить слои" if rel < 0.6 else ""
        if size not in [(1080, 1920), (1920, 1080)]: flag += " WARN размер %dx%d" % size
        if flag.startswith("FAIL"): fails += 1
        print(f.ljust(40), "%9.0f" % s, "%6.2f" % rel, flag)
    with tempfile.TemporaryDirectory() as tmp:
        for v in a.video:
            print("\nВидео:", v)
            for f, (s, size) in res.items():
                t = frame_time(f, a.fps)
                if t is None: continue
                vs, _ = sharp(grab(v, t, size, tmp))
                r = vs / s if s else 0
                flag = "FAIL экспорт мылит (CRF/битрейт/масштаб)" if r < 0.9 else "ok"
                if r < 0.9: fails += 1
                print("  %-38s %5.2f  %s" % (f, r, flag))
    print("\nИТОГ:", "FAIL — не показывать пользователю" if fails else "резкость в норме")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
