#!/usr/bin/env python3
"""Чистка дублей, запинок и пауз по словам whisper.

Вход: words.json [{w,s,e,p}] (faster-whisper word_timestamps) + wav 16 кГц моно.
Выход: segs.json [[a,b],...] — что оставить; cut_report.md — каждый рез с причиной.

Правила (vault/03-techniques/clean-cut-pro.md):
  1. Дубль: фраза, начало которой повторяется в одной из следующих фраз (окно 15 с),
     режется целиком — оставляем ПОСЛЕДНИЙ дубль.
  2. Повтор подряд («в историю в историю») — убираем первое вхождение.
  3. Слова-паразиты (э, эм, ну, короче, типа, как бы, это самое) — если стоят отдельно.
  4. Обрывки: слово с p<0.35 и длиной <0.18 с перед паузой — в отчёт «проверить ушами».
  5. Паузы > --gap сжимаются до --gap (по умолчанию 0.12 с); --keep t:dur оставляет
     смысловую паузу (после панчлайна).
  6. Точку реза двигаем к минимуму громкости ±40 мс; поля: до слова 0.05, после 0.07 с.
"""
import argparse, json, re, wave
from difflib import SequenceMatcher
import numpy as np

FILLERS = {"э", "ээ", "эээ", "эм", "мм", "ммм", "ну", "короче", "типа", "вот", "значит"}
FILLER_BIGRAMS = {("как", "бы"), ("это", "самое"), ("так", "сказать")}

def norm(w):
    return re.sub(r"[^\w]", "", w.lower().replace("ё", "е"))

def sim(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words"); ap.add_argument("wav")
    ap.add_argument("--start", type=float, default=None, help="обрезать всё до (плохой старт)")
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--gap", type=float, default=0.12)
    ap.add_argument("--keep", action="append", default=[], help="t:dur — сохранить паузу")
    ap.add_argument("--thr", type=float, default=None, help="порог речи, дБFS (авто)")
    ap.add_argument("--window", type=float, default=15.0)
    ap.add_argument("--out", default="segs.json"); ap.add_argument("--report", default="cut_report.md")
    a = ap.parse_args()

    W = json.load(open(a.words))
    for w in W: w["n"] = norm(w["w"])
    W = [w for w in W if w["n"]]
    if a.start is not None: W = [w for w in W if w["s"] >= a.start - 0.01]
    if a.end is not None: W = [w for w in W if w["e"] <= a.end + 0.01]
    drop, why = set(), {}

    # 0. громкость с шагом 5 мс (границы слов whisper без зазоров — паузы ищем по звуку)
    with wave.open(a.wav) as f:
        sr = f.getframerate(); x = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32)
    hop = sr // 200  # 5 мс
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-9)
    db = 20 * np.log10(rms / 32768 + 1e-9)
    live = db[db > -120]  # цифровую тишину не считаем
    thr = a.thr if a.thr is not None else max(np.percentile(live, 10) + 12, -46)

    # 1. дубли: если 3 слова подряд повторяются дальше (окно --window) и кусок между ними
    #    похож на начало следующего варианта — это брошенный дубль, режем его, оставляем последний
    i = 0
    while i < len(W) - 3:
        tri = [W[k]["n"] for k in range(i, i + 3)]
        best = None
        for j in range(i + 3, len(W) - 2):
            if W[j]["s"] - W[i]["s"] > a.window: break
            if [W[k]["n"] for k in range(j, j + 3)] == tri:
                L = j - i
                if sim([W[k]["n"] for k in range(i, j)], [W[k]["n"] for k in range(j, min(len(W), j + L))]) >= 0.5:
                    best = j
        if best is not None:
            for k in range(i, best): drop.add(k); why[k] = f"дубль → оставлен вариант с {W[best]['s']:.2f}"
            i = best
        else: i += 1

    # 2. повтор n-граммы подряд (запинка)
    for n in (4, 3, 2, 1):
        for i in range(len(W) - 2 * n + 1):
            if any(k in drop for k in range(i, i + 2 * n)): continue
            if [W[k]["n"] for k in range(i, i + n)] == [W[k]["n"] for k in range(i + n, i + 2 * n)]:
                if n == 1 and W[i]["n"] in {"да", "нет", "очень"}: continue  # «нет, нет» бывает намеренно
                for k in range(i, i + n): drop.add(k); why[k] = "повтор подряд"

    # 3. паразиты
    for i, w in enumerate(W):
        if i in drop: continue
        nb = (W[i]["n"], W[i + 1]["n"]) if i + 1 < len(W) else None
        gap_l = w["s"] - W[i - 1]["e"] if i else 1
        gap_r = W[i + 1]["s"] - w["e"] if i + 1 < len(W) else 1
        if w["n"] in FILLERS and (gap_l > 0.15 or gap_r > 0.15) and w["n"] not in {"вот", "значит"}:
            drop.add(i); why[i] = "паразит"
        if nb in FILLER_BIGRAMS:
            drop |= {i, i + 1}; why[i] = why[i + 1] = "паразит"

    # 4. подозрительные обрывки — только в отчёт
    suspect = [w for i, w in enumerate(W) if i not in drop and w.get("p", 1) < 0.35 and w["e"] - w["s"] < 0.18]

    # 5. маска «оставить» с шагом 5 мс: оставленные слова минус длинные паузы
    keepp = [(float(v.split(":")[0]), float(v.split(":")[1])) for v in a.keep]
    n = len(db); m = np.zeros(n, bool)
    kept = [w for i, w in enumerate(W) if i not in drop]
    for i, w in enumerate(W):
        if i not in drop: m[int(w["s"] * 200):int(w["e"] * 200) + 1] = True
    for i, w in enumerate(W):  # вырезанное: границу двигаем в самую тихую точку ±40 мс
        if i in drop:
            lo, hi = int(w["s"] * 200), int(w["e"] * 200)
            m[lo:hi + 1] = False
    sil = db < thr
    i = 0
    while i < n:
        if m[i] and sil[i]:
            j = i
            while j < n and m[j] and sil[j]: j += 1
            dur = (j - i) / 200
            want = next((d for t, d in keepp if i / 200 - .3 <= t <= j / 200 + .3), a.gap)
            if dur > want + 0.04:
                h = int(want / 2 * 200)
                m[i + h:j - h] = False
            i = j
        else: i += 1
    segs, i = [], 0
    while i < n:
        if m[i]:
            j = i
            while j < n and m[j]: j += 1
            segs.append([round(i / 200, 3), round(j / 200, 3)]); i = j
        else: i += 1
    segs = [sg for sg in segs if sg[1] - sg[0] >= 0.06]
    json.dump(segs, open(a.out, "w"))

    # отчёт
    L = ["# Отчёт чистки", "", f"Сегментов: {len(segs)}, длительность {sum(b-a_ for a_,b in segs):.2f} с", "",
         "| время | вырезано | причина |", "|---|---|---|"]
    i = 0
    while i < len(W):
        if i in drop:
            j = i
            while j + 1 < len(W) and j + 1 in drop and why[j + 1] == why[i]: j += 1
            L.append(f"| {W[i]['s']:.2f}–{W[j]['e']:.2f} | {' '.join(W[k]['w'] for k in range(i, j+1))} | {why[i]} |")
            i = j + 1
        else: i += 1
    if suspect:
        L += ["", "## Проверить ушами (обрывки, низкая уверенность)"] + [f"- {w['s']:.2f} «{w['w']}» p={w.get('p',0):.2f}" for w in suspect]
    L += ["", "## Резы, которым нужно прикрытие (вырезано > 0.8 с — голова может прыгнуть)"]
    for (a0, b0), (a1, b1) in zip(segs, segs[1:]):
        if a1 - b0 > 0.8: L.append(f"- рез {b0:.2f}→{a1:.2f} (вырезано {a1-b0:.2f} с): смена крупности 100↔112 %, перебивка или графика на весь экран")
    L += ["", "Итог: " + " ".join(w["w"] for w in kept)]
    open(a.report, "w").write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
