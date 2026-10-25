#!/usr/bin/env python3
"""Corner pin для HTML/CSS: прямоугольник w×h → 4 точки в кадре → строка matrix3d(...).

Точки по часовой: левый верх, правый верх, правый низ, левый низ (пиксели кадра 1080×1920).
  python3 cornerpin.py 600 200  120,300 700,340 690,560 110,520
Для движущейся плоскости: --track points.json ([[t, [[x,y]x4]], ...]) → JSON [[t, "matrix3d(...)"], ...]
"""
import json, sys
import numpy as np

def homography(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    h = np.linalg.solve(np.array(A, float), np.array(b, float))
    return np.append(h, 1).reshape(3, 3)

def matrix3d(w, h, pts):
    H = homography([(0, 0), (w, 0), (w, h), (0, h)], pts)
    H = H / H[2, 2]
    m = [H[0, 0], H[1, 0], 0, H[2, 0], H[0, 1], H[1, 1], 0, H[2, 1], 0, 0, 1, 0, H[0, 2], H[1, 2], 0, H[2, 2]]
    return "matrix3d(" + ",".join(f"{v:.8g}" for v in m) + ")"

if __name__ == "__main__":
    a = sys.argv[1:]
    w, h = float(a[0]), float(a[1])
    if a[2] == "--track":
        print(json.dumps([[t, matrix3d(w, h, p)] for t, p in json.load(open(a[3]))]))
    else:
        print(matrix3d(w, h, [tuple(map(float, s.split(","))) for s in a[2:6]]))
