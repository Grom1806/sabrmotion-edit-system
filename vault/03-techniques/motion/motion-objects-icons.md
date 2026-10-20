---
title: A. Объекты и иконки
type: technique
tags: [technique, motion, graphics]
summary: 1. Icon pop — иконка scale 0→1.15→1 (back.out(2.5), 0.35 с) + rotate −12°→0 + тень. SFX - pop/bubble.
updated: 2026-10-13
source: style/motion_library.md
---
# A. Объекты и иконки

1. **Icon pop** — иконка scale 0→1.15→1 (back.out(2.5), 0.35 с) + rotate −12°→0 + тень. SFX: pop/bubble.
2. **Icon morph** — одна иконка перетекает в другую (SVG path morph через flubber/MorphSVG-аналог или crossfade с scale-squash 0.15 с). Пример: кошелёк → пустой кошелёк → дыра. SFX: swoosh short.
3. **Объект-персонаж** — иконка «живёт»: дыхание scale 1↔1.03 (2 с, sine), покачивание rotate ±3°, моргание/тряска на ударных словах. Ничего не замирает.
4. **Стикер-штамп** — падает с scale 1.6→1, rotate −8°, микротряска кадра 4 px 0.15 с, «пыль» 6 частиц. SFX: stamp thump + sub.
5. **3D-наклон карточки** — perspective 1200px, rotateY 18°→0, rotateX 6°→0, тень смещается обратно, блик (linear-gradient) пробегает по поверхности 0.6 с. SFX: card swipe.
6. **Стопка карточек / уведомлений** — новые падают сверху стопкой (offset 14 px, scale 0.96 за каждую), смахиваются вбок с blur. SFX: notification ding → swipe.
7. **Cel-spin логотипа/монеты** — 3–5 копий со сдвигом 2–3 кадра, scale 95/90/85 %, opacity 80→60 %. SFX: coin spin.

См. также: [[motion-catalog]], [[motion-tiers]] (что разрешено на уровне), [[variety]].
