# text-in-space — corner pin для текста на стене/экране/столе

```
python3 cornerpin.py <w> <h> x0,y0 x1,y1 x2,y2 x3,y3     # → matrix3d(...) для CSS
python3 cornerpin.py <w> <h> --track points.json         # → [[t, "matrix3d(...)"], ...]
```
Точки: левый верх, правый верх, правый низ, левый низ. Методика: vault/03-techniques/text-in-space.md.
