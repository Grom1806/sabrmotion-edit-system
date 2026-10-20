---
title: C. Виртуальная камера
type: technique
tags: [technique, motion, camera]
summary: 14. Slow push-in постоянно (scale 1→1.06 за сцену) — даже на статике.
updated: 2026-10-13
source: style/motion_library.md
---
# C. Виртуальная камера

14. **Slow push-in** постоянно (scale 1→1.06 за сцену) — даже на статике.
15. **Smash zoom / punch-in** на ударном слове: scale 1→1.25 за 0.12 с + zoom-blur. SFX: impact/whoosh-in.
16. **Infinite zoom** — камера влетает в объект (в экран телефона, в цифру «0», в глаз), внутри следующая сцена. SFX: long whoosh.
17. **Камера едет по «доске»** — все сцены лежат на большом холсте 3×3, переходы = пролёт камеры (pan + небольшой zoom out/in, ease power3.inOut 0.6 с, motion blur). Даёт ощущение единого мира. SFX: swoosh.
18. **3D-облёт** — rotateY сцены ±10° с медленным дрейфом, параллакс 3 планов (фон 60 %, середина 100 %, передний 140 % скорости).
19. **Camera shake** на ударах: 3–6 px, 0.15–0.25 с, затухающий. Не чаще раза в 3 с.

См. также: [[motion-catalog]], [[motion-tiers]] (что разрешено на уровне), [[variety]].
