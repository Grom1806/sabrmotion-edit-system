---
title: Практики моушна и монтажа — что делают руками (ресерч 2026-10-19)
type: research
tags: [research, practitioners, motion, anti-ai, system-v2]
summary: 30+ студий и авторов (BUCK, ManvsMachine, Golden Wolf, Giant Ant, Ordinary Folk, Oddfellows, Animade, Studio Dumbar, DIA, Koto, DixonBaxi, Tendril, Gunner, Elastic, Kurzgesagt, Vox, Johnny Harris, Ben Marriott, Jake in Motion, Ariel Costa, Winston Hacking, Nicolas Ménard…): 18 ручных техник со штатными настройками AE, 10 признаков ИИ → как у людей, 4 направления. Скриншоты в refs/2026-10-19-practitioners
updated: 2026-10-19
source: Chrome на ПК (скриншоты сайтов студий, Behance-поиск) + облачный веб-ресерч practitioners-web-2026-10-19 (полная версия с 30 авторами и ссылками)
---
# Практики: как делают живой моушн

Повод: пользователь 2026-10-19 — «иишный дизайн всё ещё… научись у монтажёров и моушн-дизайнеров, их техники полностью». Свод аудита наших роликов: [[audit-2026-10-19-ai-tells]]. Полный список 30 авторов со ссылками: [[practitioners-web-2026-10-19]] (облачный ресерч).

## Что видно на работах (скриншоты в `refs/2026-10-19-practitioners/`)
| Автор / студия | Ссылка | Приёмы (видно на скриншотах и в работах) | Как повторить штатным AE |
|---|---|---|---|
| Golden Wolf | goldenwolf.tv | реальная съёмка спортсмена + растр/полутон + нарисованные от руки кольца и линии поверх (draw-over) | CC Ball Action / Threshold на дубле, Multiply; Shape + Trim Paths + Wiggle Paths на двойках |
| ManvsMachine | mvsm.com | фото-кадр + мультяшный персонаж/коллаж, кислотные плоские цвета, крупный гротеск | вырезка (маска) + плоские Solid-подложки, Hold-ключи |
| BUCK | buck.co/work | «Firebrand»: кислотный жёлто-зелёный, огромный конденс-набор + каракули-смайлы, работа на двойках | Text + Shape-дудлы, posterizeTime(12), Wiggle Paths |
| Giant Ant | giantant.ca | плоская насыщенная заливка + тушевая линия, сюрреалистичные сцены, мало градиентов | Shape с Stroke Taper, Roughen Edges, 2–3 цвета |
| Studio Dumbar / DEPT | studiodumbar.com | генеративная кинетическая типографика: полосы, ритм, жёлтый на чёрном/белом | Repeater + Expressions от звука (Convert Audio to Keyframes) |
| Koto | koto.studio | хроматический свет-объект, бренд-системы | только акцентом (у нас без неона) |
| Ordinary Folk, Oddfellows, Animade | ordinaryfolk.co, oddfellows.tv, animade.tv | персонажная 2D, гэги, тайминг с висом и antic, смаз-кадры | Speed Graph 95/10, antic 3 к, смаз-кадр 1 к вместо motion blur |
| Vox / Johnny Harris | vox.com/videos, youtube @johnnyharris | стол исследователя: скан документов, маркер, стикерная обводка вырезок, карта, камера по столу | Minimax + Fill для обводки, Solid Multiply маркер, 2.5D камера |
| Behance «mixed media collage» | behance.net (поиск) | «The City That Captured a King» — арабский плакат, бумага, печать; «US Open» — полутон-вырезка спортсмена | см. техники 3, 6, 13 |
| Ben Marriott, Jake in Motion | YouTube | туториалы: бумажный край с «кипением», shape-анимация на двойках, ручной тайминг | техники 1, 4, 8 |
| Kurzgesagt | kurzgesagt.org | плоский вектор, строгая палитра, всё дышит, параллакс | (уже в S08) |

## 18 ручных техник (стоковый AE, 1080×1920, 24 fps, графика на двойках)
1. Бумажная вырезка с «кипящим» краем: Wiggle Paths Size 3–6, Detail 8–15, Temporal Phase `posterizeTime(8); time*360`; Drop Shadow Softness 0, Distance 8–14, 135°, 60–80 %.
2. Живое зерно: Add Grain (Kodak 5218) 0.6–1.0 / Fractal Noise Contrast 400 Scale 3–5 `posterizeTime(12)` как Luma Matte; Roughen Edges Border 20–60.
3. Вырезка со стикерным краем: дубликат ниже, Minimax Maximum 10–16 → Fill #F4EFE6, тень Softness 0–4, Roughen 2; появление за 2–3 кадра Hold-ключами.
4. Коллаж-риг на двойках: части фото слоями, Parent, только Hold-ключи, позы через 2–4 кадра, `wiggle(4,1.5)` + posterizeTime(8).
5. Draw-over: Trim Paths 0→100 за 6–10 кадров Linear + Wiggle Paths 1.5 + Taper; обводка «не до конца».
6. Полутон: CC Ball Action (Grid 6–10) поверх Threshold, Multiply на бумагу.
7. Stop-motion: Posterize Time 8 + wiggle(8,2) + Turbulent Displace 6/40.
8. Тайминг с висом: Speed Graph Out 85–95 %, In 5–15 %; antic 3 кадра; смаз-кадр Scale 140 % на 1 кадр.
9. Перелёт с затуханием (выражение inertial bounce), разные freq 2.5–4 и задержки.
10. Маркер по документу: Solid #F7E35A Multiply, маска слева направо 8–12 кадров, Roughen 3, наклон 1–2°.
11. Машинопись: Text Animator Opacity + Range Start Linear, Hold по слогам, ±1.5 px дрожь.
12. Кинетическая типографика: букву резать маской, Tracking 0→200 за 4 к, Scale 100→160 % за 2 к на ударном слоге, текст выходит за край, 180–320 px.
13. Ризограф: 2–3 краски Multiply, приводка 2–4 px wiggle posterize 12, недопечатка через Fractal Noise.
14. Палитра против глянца: глухие цвета, Levels Output 12–18 / 235–242.
15. Плёнка: gate weave `posterizeTime(24)` ±1.2 px, Exposure ±0.04, виньетка 25 %.
16. Ксерокс: B&W → Threshold 120–150 → Roughen → Multiply, Threshold дрожит.
17. Ручная камера 2.5D: One-Node Camera wiggle(1.2,12) + наезд Z 3–5 %.
18. Физические склейки: hard/smash cut, whip-pan, перекрытие рукой, кадр-вспышка 2 кадра, своя фоли на каждую.

## 10 признаков ИИ → как делает человек
1 blur+scale+fade у всего → появление за 1–3 кадра Hold-ключами, разные входы. 2 Easy Ease 33/33 одной длины → 95/10, висы, antic. 3 всё по центру → асимметрия, текст режется краем, сетка. 4 стеклянные скруглённые карточки, мягкая тень → бумага, резкий край, тень Softness 0, стикерная обводка, скотч. 5 гладкие градиенты → зерно, Roughen, сканы. 6 60/30 fps гладко → 24 fps, двойки, gate weave. 7 моно-капс лейблы → крупный выразительный набор, рукопись, машинопись. 8 чёрный+неон → глухие цвета, бумажный белый, 2–3 краски. 9 диссолвы и морфы → жёсткие склейки, match cut. 10 «вжух» на всё → фоли, пауза. Бонус: показывать следы процесса — рука, стол, реальный телефон.

## Направления (из ресерча)
1. **Редакционный коллаж / стол исследователя** (Vox, Johnny Harris, Ariel Costa, Winston Hacking).
2. **Ризо-плакат / кинетическая типографика** (DIA, Studio Dumbar, Nicolas Ménard, ManvsMachine, BUCK).
3. **Рисованное поверх жизни** (Golden Wolf, BUCK, Animade, Ordinary Folk, Casey Neistat).
4. **Тактильный предметный документ** — медленный, только акцентом (Giant Ant, Allen Laseter, Cleo Abram).

Instagram/Pinterest без входа показывают только стену логина — русскоязычных Reels-монтажёров с ручным стилем там найти не удалось; нужен вход пользователя или Telegram-каналы.

См. [[audit-2026-10-19-ai-tells]], [[styles-pro]], [[SYSTEM]].
