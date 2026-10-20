---
title: "Библиотека анимаций: 50–70 плавных приёмов профессионалов (рецепты AE)"
type: research
tags: [research, motion, animation, easing, after-effects, system-v3]
summary: 64 приёма анимации (входы/выходы, вторичное движение, переходы без движения кадра, инфографика/UI, текст, Apple-стиль) с рецептами на штатных средствах AE 2026 — ключи, кадры при 30 fps, % влияния в Graph Editor, выражения; топ-10 для старта и принципы профи с цифрами.
updated: 2026-10-19
source: Adobe AE Help (Text Animators, Animation Presets, Expressions), Motion Array blog (expressions, shape transitions), Tuts+ (inertial bounce), mtmograph (bounce vs overshoot), AEJuice (elastic), PremiumBeat (per-letter), Ben Marriott via lesterbanks (shape morph), Creative Bloq / Noble Desktop (liquid), Adobe blog + IBM Design (принципы анимации), Apple WWDC23 «Animate with springs», easings.net, Material 3 motion, гайды по short-form (async, hera.video)
---

# Библиотека анимаций: 64 плавных приёма (рецепты для After Effects 2026, только штатные эффекты)

> Для кого: монтаж коротких вертикальных роликов 1080×1920, 30 fps. Только штатные эффекты AE, без плагинов.
> Пожелания автора: **всё плавно**, **ничего не появляется сразу**, **блоки и квадраты часто раскрываются**, **красивый bounce**, **стиль Apple**, **много анимации**.
> **Нельзя:** двигать весь кадр (удары, зум, тряска), музыка. Все переходы ниже сделаны слоями ПОВЕРХ кадра или масками. Сам кадр стоит на месте.

---

## 0. Базовый набор: кривые, длительности, выражения (их используют все рецепты)

### 0.1 Пресеты кривых в Graph Editor (F9 → Ctrl/Cmd+Shift+K, «Keyframe Velocity»)

В рецептах ниже кривые называются по этим кодам. Влияние (influence) указано так: «исходящее у ключа 1 / входящее у ключа 2».

| Код | Название | Влияние | Ощущение | Аналог cubic-bezier |
|---|---|---|---|---|
| **E-OUT** | Expo Out (главная «Apple-кривая» для входа) | 0–10% / **90–100%** | резкий старт и очень длинное мягкое торможение | ≈ (0.16, 1, 0.3, 1) |
| **Q-OUT** | Quint/Cubic Out (мягче) | 15% / 75% | быстро, без «рывка» | ≈ (0.22, 1, 0.36, 1) |
| **E-IN** | Expo In (выход) | **90%** / 0–10% | медленный старт, улёт с разгоном | ≈ (0.7, 0, 0.84, 0) |
| **S-IO** | Smooth In-Out (перемещение внутри кадра) | 75–85% / 75–85% | «шёлковый», симметричный | ≈ (0.65, 0, 0.35, 1) |
| **SNAP** | Snappy (UI-переключатели) | 33% / 85% | короткий и отзывчивый | ≈ (0.2, 0, 0, 1) |
| **LIN** | Linear | — | только для дрейфа, вращения и loop | — |

Правила:
- **Никогда не оставляйте линейный вход.** Минимум F9 (Easy Ease = 33/33), но лучше настроить вручную.
- В **Speed Graph** у входа пик скорости в начале и длинный «хвост» к нулю. У выхода наоборот.
- Если двигаются X и Y, включите **Separate Dimensions**, тогда кривые настраиваются по каждой оси отдельно. Так получаются «дуги» (arcs).
- Для Scale и Rotation смотрите Value Graph: overshoot рисуется третьим ключом (см. 0.3).

### 0.2 Длительности при 30 fps (ориентир)

| Что | Кадры | Секунды |
|---|---|---|
| Микро (иконка, точка, toggle) | 6–9 | 0.2–0.3 |
| Малый элемент, слово | 9–15 | 0.3–0.5 |
| Блок или карточка раскрывается | 15–24 | 0.5–0.8 |
| Переход сцены (wipe, block) | 18–30 | 0.6–1.0 |
| Большой «hero» reveal в стиле Apple | 30–45 | 1.0–1.5 |
| Stagger между элементами | 2–4 | — |
| Stagger между буквами | 1–2 (или через Text Animator) | — |
| Выход по сравнению со входом | на 20–30% короче | — |

(Material 3: short 50–200 мс, medium 250–400 мс, long 450–600 мс, extra-long 700–1000 мс. У Apple пружины с duration около 0.5 с и bounce 0.15 для лёгкого отскока.)

### 0.3 Ключевые выражения (Alt/Option+клик по секундомеру)

**A. Inertial Bounce / Overshoot** (классика Дэна Эбберта: после последнего ключа значение «пролетает» дальше и затухает). Работает на Position, Scale, Rotation, Opacity и Path-параметрах прямоугольника.
```js
amp = .05; freq = 3.0; decay = 6.0;   // amp: сила, freq: колебаний в секунду, decay: скорость затухания
n = 0;
if (numKeys > 0) { n = nearestKey(time).index; if (key(n).time > time) n--; }
t = (n == 0) ? 0 : time - key(n).time;
if (n > 0 && t < 1) {
  v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
  value + v * amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t);
} else value;
```
Настройки: Apple-мягко amp .03 / freq 2.5 / decay 7. «Сочный» bounce amp .06 / freq 3.5 / decay 5. Резиновый amp .09 / freq 4 / decay 4.
**Важно:** inertia берёт скорость в последнем ключе. Поэтому ставьте у последнего ключа **входящее влияние 0–30%**: без скорости отскока не будет. С E-OUT на 100% отскок пропадает, так и задумано.

**B. Elastic «от точки» без ключей** (для появления слоя, начиная с inPoint):
```js
freq = 3; decay = 5; d = framesToTime(2);  // небольшая задержка
t = Math.max(0, time - inPoint - d);
s = 100 * (1 - Math.cos(freq * t * 2 * Math.PI) / Math.exp(decay * t));
[s, s]
```

**C. Squash & Stretch с сохранением объёма** (Scale; работает в паре с ключами Position):
```js
maxDev = 12; spd = 25; decay = 4;
t = time - inPoint;
x = 100 + maxDev * Math.sin(spd * t) / Math.exp(decay * t);
y = 100 * 100 / x;      // объём сохраняется
[x, y]
```

**D. Delay по индексу** (stagger для копий слоя: анимируйте только «ведущий» слой и дублируйте):
```js
leader = thisComp.layer("LEAD");
delay = framesToTime(3) * (index - leader.index);
leader.transform.position.valueAtTime(time - delay)   // так же для scale, rotation, opacity
```
Вариант со сдвигом позиции: `leader.transform.position.valueAtTime(time - delay) + [0, 140*(index-leader.index)]`.

**E. Wiggle только по одной оси, медленный дрейф:**
```js
w = wiggle(0.6, 18); [value[0], w[1]]       // плавный «float» по Y
```
Плавный wiggle без дрожи: частота 0.3–1, амплитуда 5–30 px.

**F. Loop:** `loopOut("pingpong")` для дыхания и пульса, `loopOut("cycle")` для вращения и бегущей ленты, `loopOut("continue")` для продолжения движения.

**G. «Дыхание» синусом:** `s = 100 + 2*Math.sin(time*2*Math.PI/3); [s,s]` (±2% за 3 с).

**H. Счётчик:** на Source Text: `n = Math.round(effect("Slider Control")("Slider")); (""+n).replace(/\B(?=(\d{3})+(?!\d))/g, " ")`.

Источники: Motion Array «6 common AE expressions» (https://blog.motionarray.com/learn/after-effects/6-common-after-effects-expressions-you-should-be-using/), Tuts+ «Inertial bounce» (https://photography.tutsplus.com/tutorials/how-to-animate-inertial-bounce-expressions-in-after-effects--cms-41469), mtmograph «Bounce vs Overshoot» (https://mtmograph.com/blogs/tools/the-bounce-and-overshoot-animation-trick-every-motion-designer-should-know), AEJuice «Elastic motion» (https://aejuice.com/blog/how-to-create-elastic-springy-motion-in-after-effects).

### 0.4 Универсальная «плавная обвязка» любого входа
Почти каждый вход в библиотеке собирается из трёх слоёв свойств:
1. **Основное движение** (scale, path, position): 12–24 кадра, E-OUT.
2. **Opacity 0→100** за первые 40–50% этого времени (6–9 кадров), Q-OUT. Так «ничего не появляется сразу».
3. **Размытие на старте:** Fast Box Blur (Iterations 3, Repeat Edge Pixels) 20→0 за те же кадры, либо Motion Blur слоя (Shutter 180°, в Composition Settings Samples 16 / Adaptive 128).

---

## 1. Входы и выходы элементов

### 1. Раскрытие блока из точки (Point → Block Expand) ★ТОП
- **Видно:** в кадре появляется точка, вытягивается в линию, линия раскрывается в плашку со скруглением, затем проявляется контент.
- **Когда:** подложка под заголовок, карточка факта, плашка цены. Главный «фирменный» вход под запрос «расширение квадратов».
- **Рецепт:** Shape Layer → Rectangle. Свойство **Size** (отвяжите пропорции).
  - Кадры 0–8: Size [0,0] → [W,8] (линия), Q-OUT. Roundness = 4.
  - Кадры 6–22: Size [W,8] → [W,H], E-OUT. Roundness 4 → 32 (через пресет).
  - На Size выражение A (amp .04, freq 3, decay 7) даёт мягкий «вдох» в конце.
  - Контент (текст) прекомпозируйте и используйте плашку как **Alpha Matte**. Контент въезжает Position Y +40→0 с 10-го кадра, E-OUT, 14 кадров.
- **Источник:** Motion Array «Shape transitions» (https://blog.motionarray.com/learn/after-effects/shape-transitions-after-effects/).

### 2. Раскрытие из угла (Corner Grow) ★ТОП
- **Видно:** блок растёт из левого верхнего угла по диагонали, как раскрывающаяся карточка iOS.
- **Когда:** второй и третий блоки в серии; при split-screen.
- **Рецепт:** Rectangle; Anchor Point слоя поставьте в угол (Pan Behind, Y). У Rectangle Path задайте **Position = Size/2** выражением `[content("Rectangle 1").content("Rectangle Path 1").size[0]/2, …[1]/2]`, чтобы рост шёл из угла. Size [0,0]→[W,H], 18 кадров, E-OUT, плюс inertia amp .03. Opacity 0→100 за 5 кадров.
- **Источник:** Adobe Help, Shape layers (https://helpx.adobe.com/after-effects/using/shape-attributes-paint-operations-path.html).

### 3. Раскрытие из линии по центру (Center-Line Split Open)
- **Видно:** по центру проходит тонкая горизонтальная линия, затем блок «распахивается» вверх и вниз.
- **Рецепт:** Size.y 2→H за 16 кадров, E-OUT, после того как Size.x 0→W прошёл за 10 кадров (Q-OUT). Края линии рисуются через Trim Paths у Stroke (End 50→100 и Start 50→0 одновременно).
- **Когда:** разделители глав, «ящик», который открывается.

### 4. Маска-reveal (Mask / Matte Reveal)
- **Видно:** объект «выезжает» из-под невидимой границы.
- **Рецепт:** над объектом прямоугольная фигура-маска как **Alpha Matte** (в AE 2026 выбирается колонкой Track Matte прямо на слое). Объект Position Y +100% высоты → 0, 15 кадров, E-OUT. Маска стоит на месте. Выход зеркальный, E-IN, 10 кадров.
- **Когда:** строки текста, логотипы, фото в рамке.
- **Источник:** Adobe Help, Track Mattes (https://helpx.adobe.com/after-effects/using/alpha-channels-masks-mattes.html).

### 5. Stagger-каскад элементов (Staggered Cascade) ★ТОП
- **Видно:** 3–8 карточек или иконок входят по очереди «волной».
- **Рецепт:** настройте вход у одного слоя (Scale 80→100, Opacity 0→100, Position Y +60→0, 15 кадров, E-OUT). Дублируйте и сдвигайте на **3 кадра** (выделите слои → Animation → Keyframe Assistant → **Sequence Layers** с overlap, либо выражение D). Порядок: от главного к второстепенному, сверху вниз или по диагонали.
- **Совет:** stagger на 2 кадра ощущается как «волна», на 4–5 как «перечисление».

### 6. Pop с overshoot (Scale Pop + Overshoot) ★ТОП
- **Видно:** элемент вырастает до 108% и мягко оседает на 100%. Классический «красивый bounce».
- **Рецепт (ключами):** Scale 0 → **108** (кадр 9, Q-OUT) → **97** (кадр 14) → 100 (кадр 19), S-IO 60/60 на средних ключах. Opacity 0→100 за 5 кадров.
- **Рецепт (выражением):** Scale 0→100 за 10 кадров, ключ 2 с входящим влиянием 20%, плюс выражение A (amp .06 / freq 3.5 / decay 6).
- **Когда:** иконки, эмодзи, стикеры, значки «NEW», цифры.

### 7. Elastic-вход (Elastic Spring In)
- **Видно:** упругая пружина с 2–3 затухающими колебаниями.
- **Рецепт:** выражение B на Scale (freq 2.5–3.5, decay 4–6) без ключей. Для позиции используйте A с amp .08 / decay 4.
- **Когда:** игровые и детские темы, «весёлые» акценты. Не больше 1–2 раз за ролик, иначе дёшево.
- **Источник:** AEJuice (https://aejuice.com/blog/how-to-create-elastic-springy-motion-in-after-effects).

### 8. Squash & Stretch при приземлении
- **Видно:** круг или плашка падает, сплющивается и отпружинивает, объём сохраняется.
- **Рецепт:** Position Y: падение 12 кадров (E-IN), в точке касания Scale [115,85] на 2 кадра, затем [95,105] → [100,100] за 8 кадров. Либо выражение C. Anchor Point внизу слоя.
- **Источник:** Motion Array (Squash & Stretch expression).

### 9. Инерция и follow-through (Inertia / Follow-Through)
- **Видно:** плашка останавливается, а её «хвосты» (текст внутри, тень, иконка) доезжают на 2–4 кадра позже с лёгким перелётом.
- **Рецепт:** контент внутри плашки получает те же ключи, но позже на 2–3 кадра (выражение D с leader = плашка). На Position контента выражение A, amp .04.
- **Когда:** везде, где есть «контейнер + содержимое». Сильно добавляет «живости».

### 10. Морфинг формы (Shape Morph)
- **Видно:** круг перетекает в скруглённый прямоугольник, затем в карточку.
- **Рецепт (простой, штатный):** Rectangle: Size [80,80] → [W,H] и Roundness 40 → 24, 20 кадров, E-OUT. Круг получается из квадрата с Roundness = половина стороны.
- **Рецепт (сложный):** Path-ключи двух разных форм. Скопируйте Path формы B в ключ формы A, выставьте одинаковое число вершин и First Vertex (Ben Marriott: «примитивы + двигаем точки»).
- **Источник:** Ben Marriott, «Morph between any two shapes» (https://lesterbanks.com/2019/08/how-to-morph-between-any-two-shapes-in-after-effects/).

### 11. Прорисовка контура (Path Draw / Trim Paths)
- **Видно:** обводка рисуется по линии, затем заполняется цветом.
- **Рецепт:** Stroke и Add → **Trim Paths**: End 0→100, 20 кадров, E-OUT. Затем Fill Opacity 0→100, 8 кадров. Для «змейки» анимируйте Start с отставанием на 6 кадров. Line Cap = Round.
- **Когда:** иконки, стрелки, подчёркивания, карты, маршруты.

### 12. Жидкий блоб (Liquid / Blob)
- **Видно:** капля «наливается», края колышутся, капли сливаются.
- **Рецепт:** 2–3 круга-фигуры в одной прекомпозиции. Adjustment Layer: **Fast Box Blur 30** + **Levels** (Alpha: Input Black 110, Input White 140) или **Simple Choker**. Получается «metaball»: круги слипаются как жидкость. Размер кругов анимируйте с overshoot, Position с wiggle(0.5,20).
- **Когда:** фоновые акценты, «капля» под иконку, весёлые переходы.
- **Источник:** Noble Desktop, Liquid fill (https://blog.nobledesktop.com/learn/after-effects/liquid-fill-effect-after-effects); Creative Bloq (https://creativebloq.com/after-effects/create-liquid-transitions-10059836).

### 13. 3D-переворот карточки (3D Card Flip)
- **Видно:** карточка поворачивается по Y и показывает обратную сторону.
- **Рецепт:** 3D-слой (куб). Y Rotation 0→180, 20 кадров, S-IO 80/80. Обратная сторона: второй слой с Y Rotation +180 и **Material Options → Accepts Lights off**; видимость сторон через выражение `opacity: (Math.abs(transform.yRotation%360) < 90) ? 100 : 0`. Камера одна (2-Node), Zoom 2000+ для мягкой перспективы. Камера статична, двигается только карточка.
- **Когда:** «до/после», вопрос→ответ.

### 14. Слайд с размытием в движении (Slide + Motion Blur)
- **Видно:** элемент влетает сбоку со смазом, тормозит и становится резким.
- **Рецепт:** Position X +600→0, 14 кадров, E-OUT. Включите Motion Blur (переключатель слоя и композиции), Shutter Angle 180–270. Без MB: **Directional Blur** (90°) 40→0 по тем же ключам.

### 15. Рост от якоря (Scale From Anchor)
- **Видно:** полоска или карточка растёт от своего края, а не от центра.
- **Рецепт:** Pan Behind (Y): Anchor на левый край. Scale X 0→100 (отвязать пропорции), 15 кадров, E-OUT, плюс inertia amp .03. Подходит под «расширение блоков».

### 16. Раскол на полосы (Split / Slice Reveal) ★ТОП
- **Видно:** изображение собирается из 5–8 вертикальных полос, которые въезжают по очереди.
- **Рецепт:** прекомпозиция с картинкой. Внутри 6 дубликатов, у каждого прямоугольная маска шириной 1/6 кадра. Каждая полоса Position Y ±1920→0, 18 кадров, E-OUT, stagger 2 кадра (выражение D). Полосы попеременно сверху и снизу.
- **Когда:** смена фото, обложка главы.

### 17. Печатная машинка (Typewriter)
- **Видно:** буквы появляются по одной, мигает курсор.
- **Рецепт:** Effects & Presets → *Animation Presets → Text → Animate In → Typewriter*. Либо Text → Animate → Opacity 0, Range Selector Start 0→100, Shape **Square**. Скорость 1–2 кадра на символ. Курсор: слой «|» с Opacity `Math.round(time*2)%2*100`.
- **Плавная версия:** Shape **Ramp Up**, Ease Low 50 (буквы «проявляются», а не щёлкают).
- **Источник:** Adobe Help, Animation presets (https://helpx.adobe.com/after-effects/using/animation-presets.html).

### 18. Декодирование, scramble (Scramble / Decode)
- **Видно:** буквы перебирают случайные символы и «защёлкиваются» в слово.
- **Рецепт:** Text Animator → **Character Offset** = 15, Character Range: Preserve Case & Digits. Range Selector: Advanced → **Randomize Order On**, Shape Ramp Up. Offset ключами 0→100%, 20 кадров, E-OUT. Добавьте в тот же аниматор Opacity 0 и Fill Color акцент для «ещё не собранных» букв.
- **Когда:** технологичные, крипто- и «секретные» темы, цифры.

### 19. Растягивание по ширине (Width Stretch Reveal)
- **Видно:** слово «растягивается» из узкого в нормальное с размытием.
- **Рецепт:** Text Animator: Scale [30,100] + Tracking −20 + Blur 20, Range Selector Offset −100→100, Shape Ramp Up, Ease High 50 / Low 100, 20 кадров.

### 20. Выход «в точку» (Collapse to Point)
- **Видно:** зеркало №1: блок схлопывается в линию, потом в точку и исчезает.
- **Рецепт:** ключи №1 в обратном порядке, E-IN, на 30% короче (12–15 кадров). Контент уходит первым (overlap: контент начинает за 4 кадра до плашки).

### 21. Растворение с размытием и подъёмом (Blur-Up Fade Out)
- **Видно:** элемент мягко «улетучивается» вверх.
- **Рецепт:** Position Y 0→−40, Opacity 100→0, Fast Box Blur 0→15, 10–12 кадров, E-IN. Универсальный «никогда не обрывать» выход.

---

## 2. Вторичное движение (кадр живой, но стоит на месте)

### 22. Медленный дрейф (Drift)
- **Видно:** элементы еле заметно плывут.
- **Рецепт:** Position: два ключа, ±20–40 px за всю длительность плана, LIN или S-IO 50/50. Либо `value + [0, -time*8]` (8 px/с вверх).
- **Важно:** дрейфуют элементы и плашки, кадр нет.

### 23. Дыхание (Breathe)
- Scale `s = 100 + 1.5*Math.sin(time*2*Math.PI/3); [s,s]`. Также тень: Drop Shadow Softness 30±5. Для «живых» кнопок и CTA.

### 24. Парение (Float)
- `w = wiggle(0.5, 12); [value[0], w[1]]` на Position плюс `wiggle(0.4, 2)` на Rotation. Стикеры и 3D-иконки «висят в воздухе».

### 25. Параллакс внутри композиции (In-Frame Parallax)
- **Видно:** слои разной «глубины» дрейфуют с разной скоростью, задний план стоит.
- **Рецепт:** Null «DRIFT» с Position X 0→−60 за план (LIN). Слои: Position = `value + thisComp.layer("DRIFT").transform.position * k`, где k = 0.2 (дальний), 0.5, 1.0 (ближний). Сам футаж-фон не двигаем, двигаем только графику поверх.

### 26. Мягкий wiggle с затуханием (Settling Wiggle)
- `amp = 20*Math.exp(-3*(time-inPoint)); wiggle(2, amp)`. Элемент «подрагивает» после появления и успокаивается.

### 27. Задержка и наложение (Delay / Overlap)
- Каждое свойство стартует со сдвигом: Position (0 к.), Scale (+2), Opacity (+0, короче), Rotation (+3). Контент позже контейнера на 2–4 кадра. Делается сдвигом ключей или `valueAtTime(time - framesToTime(3))`.

### 28. Вращение-орбита (Orbit / Spin Loop)
- Rotation `time*20` (20°/с), или Rotation 0→360 + `loopOut("cycle")`. Декоративные кольца, звёзды, «бейдж».

### 29. Бегущая лента (Marquee Loop)
- Текст-лента дважды подряд, Position X 0→−ширина_ленты, LIN, `loopOut("cycle")`. Скорость 60–120 px/с.

### 30. Пульс-волна (Ripple Ping)
- Ellipse со Stroke: Scale 0→300, Stroke Opacity 100→0, 24 кадра, E-OUT, `loopOut("cycle")` с паузой (ключи растянуты до 45 кадров). 2–3 копии со сдвигом 8 кадров. «Точка на карте», «live».

### 31. Блик-перелив по плашке (Shimmer Loop)
- Слой-градиент (белый 30% → прозрачный), поворот 20°, как Alpha Matte по форме плашки. Position X −W→+W за 20 кадров, E-IN-OUT, повтор каждые 60 кадров.

---

## 3. Переходы между сценами (кадр стоит, двигаются слои поверх или маски)

### 32. Шторка-фигура (Shape Wipe) ★ТОП
- **Видно:** цветная плашка проезжает через экран, закрывает сцену A и открывает B.
- **Рецепт:** Solid или прямоугольник цвета бренда. Position Y: снизу за кадр → центр (кадры 0–10, E-IN 70%) → вверх за кадр (кадры 10–22, E-OUT). Склейка A/B на кадре 10–11 под плашкой. 2–3 плашки разных цветов со stagger 3 кадра дают «многослойную» шторку.
- **Источник:** Motion Array (https://blog.motionarray.com/learn/after-effects/shape-transitions-after-effects/).

### 33. Блок разрастается на весь экран (Block Grow to Full Frame) ★ТОП
- **Видно:** карточка из сцены A раскрывается до размеров всего экрана и становится фоном сцены B, как открытие приложения на iPhone.
- **Рецепт:** Rectangle Size [W,H] → [1080+40,1920+40], Roundness 32→0, Position к центру, 20–24 кадра, S-IO 70/90. Сцена B прекомпозирована, её Track Matte = этот прямоугольник. Внутри B контент начинает вход с кадра 12. Не камера и не зум кадра: растёт только плашка-маска.

### 34. Match cut по форме (Shape Match Cut)
- **Видно:** круг в A (кнопка, мяч, зрачок) в одном и том же месте становится кругом в B.
- **Рецепт:** совместите объекты по позиции и размеру. На стыке 4–6 кадров кросс-фейда только внутри маски-круга (маска с Feather 20). Сопровождайте вторичной фигурой-кольцом (Ripple, №30).

### 35. Iris (круг раскрывается)
- Маска-эллипс на сцене B: Mask Expansion −600→1200 или Size эллипса 0→2400, 18 кадров, E-OUT, Mask Feather 0→40. Центр на объекте внимания.

### 36. Сетка-переход (Grid Split / Tiles) ★ТОП
- **Видно:** экран разбивается на сетку 3×5 квадратов, они по очереди переворачиваются или «заливаются», и открывается сцена B.
- **Рецепт:** Shape Layer: Rectangle 360×384 плюс **Repeater** ×3 (Offset X 360), второй Repeater ×5 (Offset Y 384). Анимация: у Repeater 1 → Transform: Scale 0→100 и Rectangle Size 0→full с E-OUT. Для stagger используйте **Offset** у Repeater (ключи 3→0) либо 15 отдельных квадратов с выражением D (delay 1–2 кадра, порядок по диагонали). Квадраты служат Alpha Matte для сцены B.
- **Источник:** Motion Array (Repeater-переходы), Adobe Help Repeater.

### 37. Маска-переход по форме объекта (Object Mask Transition)
- Объект из A (силуэт, текст) масштабируется (только он), и через его форму видна B: B получает Alpha Matte = объект. Scale 100→3000, 20 кадров, E-IN-OUT 90/60. Двигается объект-маска, не кадр.

### 38. Жидкий переход (Liquid Transition)
- **Видно:** «вода или краска» заливает экран волнистым краем.
- **Рецепт:** Solid + маска-прямоугольник снизу вверх (Mask Path ключи, 20 кадров, E-OUT). Эффекты: **Turbulent Displace** (Amount 60, Size 120, Evolution `time*200`) и **Wave Warp** (Wave Height 30, Width 300). Тот же слой как Alpha Matte для B. 2 цветных слоя со stagger 4 кадра дают «двухцветную волну».
- **Источник:** Noble Desktop (Wave Warp + matte), Creative Bloq.

### 39. Чернильное растекание (Ink Bleed)
- Fractal Noise (Contrast 300, Brightness ключ −100→+100, 24 кадра, E-OUT) → **Levels** → используйте как Luma Matte для B. Плюс Fast Box Blur 4 на матте для мягкого края. Только штатные эффекты.

### 40. Стеклянная шторка (Glass Wipe)
- **Видно:** матовая «стеклянная» панель проезжает. Под ней всё размыто, после неё видна сцена B.
- **Рецепт:** Adjustment Layer в форме прямоугольника (рисуйте маску на adjustment) с **Fast Box Blur 40** + Brightness & Contrast +10, по краю Stroke 1 px белый 30%. Маска едет снизу вверх 20 кадров, S-IO. Склейка A/B в момент, когда панель покрыла центр.

### 41. Полосы-жалюзи (Venetian Bars)
- 6–8 горизонтальных плашек: Scale X 0→100 от левого края (якорь), 12 кадров, E-OUT, stagger 2 кадра. Затем уходят Scale X 100→0 от правого края. Пауза-склейка между ними. Штатный пресет-аналог: *Transitions → Venetian Blinds* (грубее).

### 42. Растворение через размытие (Blur Dissolve)
- A: Fast Box Blur 0→30 и Opacity 100→0 за 10 кадров; B: Blur 30→0 и Opacity 0→100, наложение 6 кадров. Самый «тихий» Apple-переход.

### 43. Карточный стек-переход (Card Stack Swap)
- Сцена A сжимается **как карточка** внутри кадра (прекомпозиция A: Scale 100→92, Roundness маски 0→40, темнеет на 30%), а сцена B въезжает поверх снизу как новая карточка (Position Y 1920→0, 20 кадров, E-OUT). Кадр-основа (фон) стоит. Этот пункт пограничный: используйте, только если «сжатие сцены-карточки» не считается движением кадра. Иначе B просто наезжает поверх A.

---

## 4. Инфографика и UI

### 44. Рост столбцов (Bar Grow) ★ТОП
- **Видно:** столбцы вырастают от оси по очереди с лёгким overshoot, цифры «докручиваются».
- **Рецепт:** Rectangle, Anchor внизу (Pan Behind). Scale Y 0→100, 18 кадров, E-OUT + inertia amp .04. Stagger 3 кадра (выражение D). Цифра над столбцом: Position = верх столбца (`thisComp.layer("bar1").toComp([0,-h])` или проще: parent к столбцу и обратная компенсация масштаба).

### 45. Счётчик (Number Counter)
- Text → Expression Controls → **Slider Control**; ключи 0→1250, 30–45 кадров, **E-OUT** (цифры бегут быстро и плавно тормозят). Source Text: выражение H. Без «дрожания» ширины: моноширинный шрифт или Paragraph выравнивание по правому краю.

### 46. Прорисовка графика (Line Chart Draw)
- Линия Pen-tool, Trim Paths End 0→100, 30 кадров, S-IO 60/90. Точка-маркер едет по пути: скопируйте Path → вставьте в Position точки (ключи станут roving), подгоните под те же кадры. Под линией градиентная заливка: маска едет слева направо за линией с отставанием 4 кадра.

### 47. Круговая диаграмма / кольцо прогресса (Donut Fill)
- Ellipse только со Stroke (толщина 40, Round Cap) → Trim Paths End 0→72 (72%), 30 кадров, E-OUT. Offset −90°, чтобы начиналось сверху. В центре счётчик №45 синхронно.

### 48. Переключатель (Toggle Switch)
- Капсула + кружок. Кружок Position X сдвигается на (W−H), **8 кадров, SNAP** + inertia amp .03. Цвет капсулы (Fill) серый → зелёный за 6 кадров. Кружок на середине пути Scale X 115% (растягивается, squash).

### 49. Перестановка списка (List Reorder)
- Элементы списка меняются местами: Position Y по дугам (Separate Dimensions; X уходит на +20 и обратно, S-IO), 16 кадров. Поднятый элемент Scale 104% + Drop Shadow Distance 4→16, «поднят пальцем».

### 50. Стопка карточек (Card Stack)
- 3–4 карточки: каждая следующая Scale −5% и Position Y −30 px, Opacity −15%. Вход stagger 4 кадра снизу, E-OUT. Свайп верхней: Position X → +1200, Rotation 0→12°, 14 кадров, E-IN, остальные «подтягиваются» вперёд с задержкой 2 кадра (S-IO).

### 51. Аккордеон (Accordion Expand)
- Плашка Size.y 120→480, 16 кадров, E-OUT. Блоки ниже съезжают синхронно (parent к null или expression `[value[0], value[1] + (size.y - 120)]`). Содержимое внутри: Mask reveal (№4) с задержкой 4 кадра. Стрелка Rotation 0→180, 12 кадров.

### 52. Сборка bento-сетки (Bento Grid Build) ★ТОП
- **Видно:** экран собирается из скруглённых блоков разного размера (как в Apple-презентациях): блоки раскрываются из точек и углов по очереди, потом в них проявляется контент.
- **Рецепт:** 5–7 Rectangle (Roundness 28, зазор 24 px). Каждый: приём №1 или №2 (Size от 0, 18 кадров, E-OUT, inertia amp .03). Порядок по диагонали от главного блока, stagger 3–4 кадра. Контент каждого блока +6 кадров к своему блоку (follow-through). Фон блоков: белый или #F5F5F7 и тень Softness 40, Opacity 10%.

### 53. Уведомление / баннер (Notification Drop)
- Плашка сверху: Position Y −200→120, 14 кадров, E-OUT + inertia (amp .04), Scale 95→100. Через 2 с уход вверх, E-IN, 10 кадров. Иконка внутри Pop (№6) с задержкой 4 кадра.

### 54. Прогресс-бар (Progress Fill)
- Rectangle Anchor слева, Scale X 0→100, 40 кадров, S-IO 40/90, с паузами «загрузки» (ключи 30%→55%→100%). Сверху Shimmer (№31).

---

## 5. Текст

### 55. Побуквенный stagger с размытием (Per-Character Blur Stagger) ★ТОП
- **Видно:** буквы проявляются по очереди: из размытия, снизу вверх, с прозрачностью.
- **Рецепт:** Text → Animate → **Position** [0,40] + Add Property **Opacity 0** + **Blur 12**. Range Selector → Advanced: Based On **Characters**, Shape **Ramp Up**, **Ease High 50, Ease Low 100**. Offset −100 → 100, ключи на 0 и 20 кадров (для слова из 6–10 букв), E-OUT. Хотите случайный порядок: Randomize Order On.
- **Источник:** PremiumBeat (https://www.premiumbeat.com/blog/animate-individual-letters-in-after-effects/), Adobe Help: Text animators (https://helpx.adobe.com/after-effects/using/animating-text.html).

### 56. Построчный reveal из-под маски (Line Mask Reveal)
- Каждая строка своим слоем (или Based On Lines) с Track Matte-прямоугольником по высоте строки. Position Y +100%→0, 15 кадров, E-OUT, stagger 4 кадра на строку. Самый «журнальный» и чистый вход.

### 57. Маркер-выделение (Highlight Sweep)
- Плашка-маркер под словом: Anchor слева, Scale X 0→100, 10 кадров, E-OUT, цвет акцента 60–80% Opacity, **Blending Mode Multiply** (или под текстом). Цвет слова меняется вслед: Text Animator Fill Color, Range Offset синхронно со шторкой.

### 58. Подчёркивание рисуется (Underline Draw)
- Линия со Stroke 6 px, Round Cap: Trim Paths End 0→100, 12 кадров, E-OUT. Для «живого» вида ведите линию слегка изогнутой Pen-tool. Выход: Start 0→100, E-IN (уходит в ту же сторону).

### 59. Смена слова с переворотом (Word Swap Flip)
- **Видно:** «быстро → дёшево → красиво»: слово переворачивается по X как табло.
- **Рецепт:** слова отдельными 3D-слоями внутри маски строки. Старое: X Rotation 0→90 и Position Y 0→−30, Opacity 100→0, 8 кадров, E-IN. Новое: X Rotation −90→0, Position Y +30→0, 10 кадров, E-OUT + inertia amp .03, старт на 4-м кадре (overlap). Цикл через 30–45 кадров.
- **Плавная 2D-версия:** Track Matte строки + Position Y (старое вверх, новое снизу) + Blur 8→0.

### 60. 3D-вращение текста по буквам (3D Per-Character Rotation)
- Text → Animate → Enable **Per-character 3D**; добавьте Rotation X −90 + Opacity 0. Range Selector Ramp Up, Offset −100→100, 20 кадров, E-OUT. Anchor Point Grouping = Character, Grouping Alignment Y −50%, чтобы буквы вращались «на петле» снизу.

### 61. Текст по траектории (Text on Path)
- Нарисуйте маску на текстовом слое → Text → Path Options → Path = Mask 1. Анимируйте **First Margin** от −ширины до 0, 24 кадра, E-OUT. Для бейджа по кругу используйте `loopOut` и First Margin LIN.

### 62. Кинетическая типографика (Kinetic Type Layout)
- **Видно:** фраза строится словами: каждое слово входит своим приёмом (масштаб, маска, слайд), и они «складываются» в плотный блок.
- **Рецепт:** по одному слою на слово или фразу из 1–3 слов. Ключевое слово крупно, Pop (№6). Служебные слова мельче, Line Mask (№56). Stagger 4–6 кадров по ритму речи (ставьте ключи по пикам голосовой дорожки). При появлении нового слова предыдущие **сдвигаются, освобождая место** (Position, 10 кадров, S-IO). Двигается текстовый блок, не кадр.
- **Short-form практика:** субтитры по 1–3 слова, «pop» только на ключевых словах; CTA держится дольше; текст не прижимать к нижнему и правому краю (интерфейс площадки). Источник: async (https://async.com/blog/how-to-edit-instagram-reels/), hera.video (https://hera.video/blog/motion-graphics-for-youtube-shorts-and-reels).

---

## 6. Приёмы в стиле Apple

### 63. Blur-in + Expo (Apple Blur Rise) ★ТОП
- **Видно:** заголовок проявляется из сильного размытия, чуть поднимаясь и уменьшаясь до 100%. Очень медленный «хвост».
- **Рецепт:** Scale 108→100, Position Y +30→0, Opacity 0→100 (первые 12 кадров), **Fast Box Blur 40→0** (или Gaussian Blur 60→0), длительность **30–36 кадров, E-OUT 0/95**. Без bounce: Apple-вход садится мягко. Цвет текста #1D1D1F на белом или белый на чёрном, шрифт SF Pro / Inter, Semibold, трекинг −1…−2%.
- **Источник:** Apple WWDC23 «Animate with springs» (https://developer.apple.com/videos/play/wwdc2023/10158/); Skillshare «Apple UI motion graphics in AE» (https://www.skillshare.com/en/classes/master-viral-apple-ui-motion-graphics-in-adobe-after-effects/945257092).

### 64. Product reveal со светом и глубиной (Product Reveal + Light Sweep + Depth Stack)
- **Видно:** объект (телефон, скрин, упаковка) поднимается из темноты, по нему проходит блик. Сзади мягко проявляются «слои глубины»: размытые карточки на разных расстояниях.
- **Рецепт:**
  - **Объект:** Position Y +200→0, Scale 92→100, 40 кадров, E-OUT 0/95. Opacity 0→100 за 15 кадров. Тень (Drop Shadow, Softness 80, Opacity 25→40%) растёт вместе с ним.
  - **Light sweep:** слой-градиент (белый → прозрачный, полоса 15% ширины, поворот 25°), Blending Mode **Add/Screen** 40%, Track Matte = объект. Position X слева направо 24 кадра, S-IO, старт на 20-м кадре (после посадки).
  - **Depth stacking:** 2–3 карточки позади: дальняя Scale 80% + Fast Box Blur 20 + Opacity 50%, средняя 90% / Blur 8 / 75%. Входят на 4 и 8 кадров позже объекта с меньшей амплитудой (параллакс-коэффициенты 0.3 и 0.6). Всё в 2D, камера не нужна.
  - **Свет фона:** Radial Gradient (эффект Gradient Ramp, Radial) под объектом, Opacity 0→60, 30 кадров.
- **Когда:** показ продукта, приложения, результата «после».

---

## ⭐ ТОП-10 «самых эффектных и плавных» для старта

| # | Приём | Почему начать с него |
|---|---|---|
| 1 | **№1 Раскрытие блока из точки** | прямо закрывает запрос «расширение квадратов»; основа плашек |
| 2 | **№33 Блок разрастается на весь экран** | переход в стиле iOS без движения кадра |
| 3 | **№63 Apple Blur Rise** | самый «дорогой» вход для заголовков |
| 4 | **№6 Pop с overshoot** | «красивый bounce» в одну минуту (ключи или выражение A) |
| 5 | **№55 Побуквенный blur-stagger** | любой текст сразу выглядит профессионально |
| 6 | **№52 Сборка bento-сетки** | Apple-презентация плюс много раскрывающихся блоков |
| 7 | **№5 Stagger-каскад** | «много анимации везде» без хаоса |
| 8 | **№36 Сетка-переход** | эффектный переход квадратами |
| 9 | **№44 Рост столбцов + №45 счётчик** | цифры и факты оживают |
| 10 | **№32 Shape Wipe (многослойная шторка)** | быстрый, чистый, брендовый переход |

Запасные к ним: №2 (угол), №16 (раскол на полосы), №59 (смена слова), №64 (product reveal).

---

## 7. Принципы профессионалов (коротко и с цифрами)

### 12 принципов анимации применительно к моушн-дизайну
1. **Squash & Stretch:** плашки и точки сплющиваются на 10–15% при ударе и растягиваются в полёте; объём сохраняется (x·y = const). Для UI достаточно 3–8%.
2. **Anticipation (подготовка):** перед вылетом элемент отходит назад на 5–10% хода или Scale 100→95 за 4–6 кадров. Перед большим переходом мелкий «вдох» на 3–5 кадров.
3. **Staging (постановка):** в каждый момент один главный акцент. Остальное ждёт или притушено (Opacity 40–60%, Blur 4–8). IBM: «направляйте внимание последовательностью, без конкурирующих действий».
4. **Straight-ahead vs Pose-to-pose:** в AE почти всегда pose-to-pose: ключевые позы, затем кривые. Straight-ahead используется для «живых» блобов (wiggle/noise).
5. **Follow-through & Overlap:** части останавливаются не одновременно. Контент позже контейнера на 2–4 кадра, свойства разнесены на 1–3 кадра (№9, №27).
6. **Slow in / Slow out (easing):** единственный принцип, который применяется **всегда** (Issara Willenskomer, Adobe). Вход E-OUT, выход E-IN, перемещение S-IO. Линейное только для loop.
7. **Arcs (дуги):** перемещение по диагонали ведите по дуге: Separate Dimensions с разными кривыми X (Q-OUT) и Y (E-OUT).
8. **Secondary action:** дыхание, блик, дрейф и пульс (раздел 2) поддерживают главное действие, но в 3–5 раз тише по амплитуде.
9. **Timing:** малые объекты 6–12 кадров, средние 12–20, крупные 20–40 (при 30 fps). Чем больше и «тяжелее» объект, тем дольше. Выход на 20–30% короче входа.
10. **Exaggeration:** overshoot 5–10% для UI, 15–25% для игривого стиля. Apple почти без overshoot (≤3%).
11. **Solid drawing → консистентность:** одна сетка, единые радиусы скругления (например 24/32 px), единая система кривых (раздел 0.1) на весь ролик.
12. **Appeal:** читабельность важнее эффекта. Текст должен простоять неподвижно минимум 1.5–2 с (≈ 3–4 слова в секунду чтения).
13. *Бонус: Transform (морфинг):* «новый» принцип UI-моушна по Willenskomer: объекты меняют форму во времени (№10, №33).

### Тайминг и спейсинг
- **Тайминг** = сколько кадров, **спейсинг** = как распределено движение между кадрами (то есть кривая). Одинаковые 15 кадров с E-OUT и с LIN выглядят как два разных мира.
- Ритм ролика: вход 15–20 кадров → удержание 30–60 → выход 10–12. Новая визуальная информация каждые ≈1–2 с, но не обрывать ничего резко.
- Не меньше **6 кадров** на любое появление: так соблюдается «ничего не появляется сразу».

### Overlap и offset
- Stagger **2 кадра** = волна, **3–4** = каскад, **5–6** = перечисление по одному.
- Offset по направлению: элементы входят в порядке чтения (сверху вниз, слева направо) или от центра внимания наружу.
- В Graph Editor: сдвиньте ключи разных свойств на 1–3 кадра, не обязательно ставить новые.

### Иерархия
- 3 уровня: **Hero** (самый долгий и эффектный вход, 24–36 кадров), **Supporting** (15–20 кадров, проще), **Detail** (8–12 кадров, только fade + сдвиг 20 px).
- Чем важнее элемент, тем раньше он входит и тем больше амплитуда. Мелкое входит после главного.

### Anticipation и «ожидание» в переходах
- За 4–6 кадров до перехода элементы сцены A начинают уходить (E-IN). Сам переход стартует до того, как всё исчезло (overlap 3–5 кадров), иначе ощущается «дыра».

### Мини-чеклист «плавно, как у профи»
1. Ни одного линейного ключа на входах и выходах.
2. Ни одного появления короче 6 кадров; у всего есть opacity- или blur-подъём.
3. Контейнер и контент разнесены на 2–4 кадра.
4. Включён Motion Blur (Shutter 180°) на всём, что быстро двигается.
5. Overshoot только там, где нужен характер; в Apple-сценах E-OUT без отскока.
6. Кадр-основа не двигается (нет зума, тряски, «ударов»); анимация только у слоёв.
7. Единые радиусы, цвета и кривые на весь ролик.

---

## Источники
- Adobe AE Help, анимация текста и Text Animators: https://helpx.adobe.com/after-effects/using/animating-text.html
- Adobe AE Help, Animation Presets: https://helpx.adobe.com/after-effects/using/animation-presets.html
- Adobe Help, примеры текстовой анимации: https://helpx.adobe.com/ph_en/after-effects/desktop/animating-text/text-animation-examples/examples-resources-text-animation.html
- Motion Array, распространённые выражения AE: https://blog.motionarray.com/learn/after-effects/6-common-after-effects-expressions-you-should-be-using/
- Motion Array, Shape transitions: https://blog.motionarray.com/learn/after-effects/shape-transitions-after-effects/
- Envato Tuts+, Inertial bounce: https://photography.tutsplus.com/tutorials/how-to-animate-inertial-bounce-expressions-in-after-effects--cms-41469
- mtmograph, Bounce vs Overshoot: https://mtmograph.com/blogs/tools/the-bounce-and-overshoot-animation-trick-every-motion-designer-should-know
- AEJuice, Elastic motion: https://aejuice.com/blog/how-to-create-elastic-springy-motion-in-after-effects
- PremiumBeat, анимация отдельных букв: https://www.premiumbeat.com/blog/animate-individual-letters-in-after-effects/
- Ben Marriott, морфинг форм (через Lester Banks): https://lesterbanks.com/2019/08/how-to-morph-between-any-two-shapes-in-after-effects/
- Creative Bloq, жидкие переходы: https://creativebloq.com/after-effects/create-liquid-transitions-10059836
- Noble Desktop, Liquid fill: https://blog.nobledesktop.com/learn/after-effects/liquid-fill-effect-after-effects
- Adobe Blog, «Redesigning the 12 Principles for Motion Design» (Issara Willenskomer): https://blog.adobe.com/en/publish/2016/11/08/redesigning-the-12-principles-of-animation-for-motion-design
- IBM Design Language, классические принципы: https://www.ibm.com/design/language/animation/classic-principles
- Apple WWDC23, «Animate with springs»: https://developer.apple.com/videos/play/wwdc2023/10158/
- Skillshare, Apple UI motion в AE: https://www.skillshare.com/en/classes/master-viral-apple-ui-motion-graphics-in-adobe-after-effects/945257092
- easings.net (справочник кривых): https://easings.net/ ; Material 3 motion: https://m3.material.io/styles/motion/easing-and-duration
- Short-form: async, монтаж Reels: https://async.com/blog/how-to-edit-instagram-reels/ ; hera.video: https://hera.video/blog/motion-graphics-for-youtube-shorts-and-reels

*Примечание:* значения cubic-bezier в 0.1 — стандартные аппроксимации (easings.net / cubic-bezier.com). Перевод в % влияния AE приблизительный, доводите на глаз в Speed Graph. Числа Apple (duration ≈0.5 с, bounce 0.15) взяты из сессии WWDC23 и вторичных разборов.
