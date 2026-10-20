---
title: E. Текст и типографика
type: technique
tags: [technique, motion, text, subtitles]
summary: 27. Kinetic word slam — одно слово на весь экран, буквы с stagger 0.03 с, y 60→0, scale 1.4→1, blur 10→0. SFX - hit на слово.
updated: 2026-10-13
source: style/motion_library.md
---
# E. Текст и типографика

27. **Kinetic word slam** — одно слово на весь экран, буквы с stagger 0.03 с, y 60→0, scale 1.4→1, blur 10→0. SFX: hit на слово.
28. **Scramble/decode** — текст «расшифровывается» из случайных символов (0.5 с). Для чисел и заголовков. SFX: digital ticks.
29. **Highlighter/underline** — маркер прорисовывается под словом (scaleX 0→1, 0.3 с). SFX: marker squeak.
30. **Счётчик-слот** — размытые числа крутятся → приземление с bounce. SFX: ratchet ticks → ding.
31. **Text behind subject** — крупное слово стоит ЗА головой спикера (нужна маска/вырез спикера: rembg/robust-video-matting). Очень «дорогой» эффект.
32. **Pill-лейблы** — капсулы «до 10 000 ₽», «×7», «пропущенных 16» прилетают с разных сторон и прилипают к объекту.

См. также: [[motion-catalog]], [[motion-tiers]] (что разрешено на уровне), [[variety]].
