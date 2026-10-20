---
title: Цвет: палитры и киношный грейд (ресерч)
type: research
tags: [research, color, grade, palette, ffmpeg]
summary: 12 палитр с hex для рилсов (тренды 2025-26, кино, инди-стили) + 9 «луков» цветокора с ffmpeg-цепочками; карта применения к PERSET/Sabrmotion/без бренда; ротация, чтобы цвет не повторялся
updated: 2026-10-18
source: веб-ресерч 2026-10-18 (Pantone, WGSN/Coloro, Gridfiti, Eggradients, Melies, Beverly Boy, PremiumBeat, Digital Production, Fujifilm, Analog.cafe, StudioBinder, SVGator); ссылки внизу
---
# Цвет: палитры и киношный грейд

Пользователь (2026-10-18): «очень однообразные цвета, цветокоррекции, стили». Заметка = меню цвета. **По умолчанию остаются основные цвета**; новую палитру (раздел B) или лук грейда (раздел C) берём только если пользователь выбрал это в вопросе 5 из [[ask-before-edit]] (уточнение пользователя 2026-10-18: «главные цвета пусть остаются, не каждое видео новое, пусть каждый раз спрашивает»). Фон спикера не меняем, только грейд ([[keep-original-background]]). Палитры из учебника референсов: [[uchebnik-refs-2026-10-18]] (раздел 2–3).

**Что проверено, а что наше.** Hex, помеченные *(источник)*, взяты из источников. Палитры с пометкой *(наша сборка)* я собрал сам на основе описанного тренда: это не «палитра компании X».

## A. Принципы, на которых держится «дорогой» цвет
1. **Ограничение = вкус.** Ровно 2 оттенка в сплит-тоне, больше не усиливает эффект (Melies). Teal-orange только на ключевые моменты и с приглушённой насыщенностью; лук строить по теням/середине/светам отдельно, а не одним LUT-ом (Beverly Boy).
2. **Альтернативы teal-orange** (Melies, Beverly Boy): золото на бирюзе, маджента на зелёном, сталь на янтаре; teal сдвигать в циан, orange в янтарь/золото; аналоговые и сплит-комплементарные схемы.
3. **Проверка в ч/б**: если кадр не читается в ч/б, цвет его не спасёт (Beverly Boy).
4. **Кожа на кроссовере.** Точка перехода тени/света в середине, а кожа сидит именно там; проверять лицо после каждого шага (Melies).
5. **Color script** (Pixar, StudioBinder): цвет меняется по эмоциональной дуге. Для рилса: хук, проблема, решение, CTA = 2–3 «цветовых состояния» одного лука, а не один цвет на весь ролик.
6. **60-30-10** (общая практика дизайна): 60 % фон, 30 % вторичный, 10 % акцент. В референсах тоже **один акцент на ролик** ([[refs-2026-10-18-overview]]).
7. **Пленочные текстуры только чуть-чуть.** Халация и диффузия «как соль в супе», убрать уже нельзя (Digital Production). Халация физически красно-оранжевая, почти никогда не синяя. Ставить в конец цепочки.

## B. Палитры для графики (hex)

### Тренды 2025–2026
**B1. Cloud Dancer Editorial** — Pantone 2026 = PANTONE 11-4201 Cloud Dancer, «воздушный белый», **#F0EEE9** *(источник: Pantone через Galerie, Office-Watch)*. Редакционный минимал: фон #F0EEE9, текст #1A1A1A, линии #BDB8AE, один акцент (кобальт #2F4BFF или красный #E0301E) *(наша сборка)*. Огромная типографика, много воздуха.

**B2. Mocha Cream** — Pantone 2025 Mocha Mousse **#A47864** *(источник)*. + крем #F3E9DC, эспрессо #3B2A22, шалфей #8F9E7E, сливочное масло #F2D98D *(наша сборка)*. Тёплые нейтрали вместо холодных серых; коричневый как «новый чёрный» для текста (CustomStickers).

**B3. Midnight Teal** — WGSN+Coloro: цвет 2026 «Transformative Teal», смесь тёмно-синего и водно-зелёного *(источник; официальный hex в открытом доступе не нашёл)*. Сборка: фон #0B1F24, teal #1F6F6B, циан-акцент #5FE3D0, янтарь #F2B354, текст #EAF2EF *(наша сборка)*. Тренд «deep teal + тёплый нейтрал + янтарный микро-акцент» (CustomStickers).

**B4. Acid Dark** — тренд «тёмный режим + неоновые акценты» (SVGator 2025). Фон #0D0D0D, лайм #C6FF00, белый #F5F5F0, серый #8A8A8A *(наша сборка)*. Для техно/AI-тем, кинетическая типографика.

**B5. Dusty Rose + Moss** — «взрослый розовый» (CustomStickers): пыльная роза #D8A7A0, мох #5E6B47, сливочный #F6EBD3, какао #3A2A24 *(наша сборка по описанию)*.

### Инди / арт-направления
**B6. Synthwave Sunset** *(источник: Gridfiti)*: #461E52 · #DD517F · #E68E36 · #556DC8 · #7998EE. Фон добавить тёмный #120A1F. Градиент заката снизу вверх #E68E36 → #DD517F → #461E52, сетка-горизонт #7998EE.

**B7. Outrun** *(источник: Gridfiti)*: #362FBB · #712275 · #F97698 · #FFB845. Для цифр-героев и «ретро-будущего».

**B8. Vaporwave** *(источник: Gridfiti)*: #A653F5 · #8F8CF2 · #65B8BF · #F96CFF · #FA92FB. Только графика и фоны-плашки, на кожу не лить.

**B9. Grand Budapest** *(источник: Eggradients)*: #390C1E · #C41311 · #C6645F · #854D65. + светлый #F3D9D3 *(наша)*. Симметрия, кадр в рамке, кукольная плоскость.

**B10. Moonrise Khaki** *(источник: Eggradients, Moonrise Kingdom)*: #BFB17C · #6A4021 · #D88A3B · #849585. Землистый, тёплый, для «историй» и лайфстайла.

**B11. Darjeeling Saffron** *(источник: Eggradients)*: #E27505 · #9C1425 · #827B82 · #3B3332 · #CDC1BD. Насыщенный шафран на дымчатом сером.

**B12. Neon Noir** (настроение Blade Runner 2049: холодный неон города против тёплого оранжевого, серые для одиночества; Pixflow) *(наша сборка)*: фон #07080F, циан #19D3FF, маджента #FF2E88, дымный оранж #E8743B, туман #9AA3AD.

Палитры из того же источника, если нужен ещё запас: 80s #FF68A8 · #64CFF7 · #F7E752 · #CA7CD8 · #3968CB; Lofi #674AB3 · #A348A6 · #9F63C4 · #9075D8 · #CEA2D7; Plant #2D4030 · #49684C · #5D7F61 · #6B8E6E · #97B299 *(Gridfiti)*.

## C. Луки цветокора спикера (ffmpeg)
Порядок как в [[color-playbook]]: сначала нормализация источника и баланс белого, потом лук, текстуры последними. Грейдить только видео спикера; графика не грейдится. Цифры стартовые, подбирать по signalstats и контакт-листу ([[qa-frame-by-frame]]).

| # | Лук | На что похоже | Когда |
|---|---|---|---|
| L1 | Clean Apple | нейтраль, мягкий контраст, чистая кожа | продукт, Apple-стиль |
| L2 | Сплит «золото/бирюза» | вместо банального teal-orange | эксперт, бизнес |
| L3 | Portra warm | тёплый, пастельные света, чуть синие тени (Analog.cafe) | лайфстайл, истории |
| L4 | Eterna muted | приглушённая насыщенность, плоская мягкая градация (Fujifilm) | серьёзная тема, кино |
| L5 | Bleach bypass | жёсткий S-контраст, насыщенность ~15–20 из 50 в Resolve, сила 0.5–0.7 (PremiumBeat) | «проблема», драма |
| L6 | Duotone | карта градиента в 2 цвета (Spotify-стиль) | вставки, хук, пауза |
| L7 | Mono + 1 цвет | ч/б, живой только один цвет | акцент-слово, ключевая фраза |
| L8 | Neon split | тени в фиолет/маджента, света тёплые (как Before/After из учебника) | техно, AI, ночь |
| L9 | Print-film | плотные тени, тёплые мягкие света, «плёночная» печать 2383 | премиум, финал |

**L1 Clean Apple:** `eq=contrast=1.03:saturation=1.02,curves=master='0/0.01 0.5/0.51 1/0.97',unsharp=5:5:0.3`

**L2 золото/бирюза (сплит-тон):** `colorbalance=rs=-0.03:gs=0.01:bs=0.04:rh=0.04:gh=0.02:bh=-0.04:pl=1,eq=saturation=0.95,selectivecolor=reds='0 0.02 0.03 0'` — тени в бирюзу, света в золото, `pl=1` держит яркость, selectivecolor возвращает кожу.

**L3 Portra warm:** `curves=master='0/0.04 0.3/0.30 0.7/0.74 1/0.95',colorbalance=bs=0.03:rh=0.03:gh=0.015,eq=saturation=0.92,vibrance=0.12` — поднятые чёрные, мягкие света, сине-холодные тени (у Portra так и есть).

**L4 Eterna muted:** `eq=contrast=0.96:saturation=0.78,curves=master='0/0.03 0.5/0.5 1/0.96',colorbalance=gm=-0.01:bh=0.01`

**L5 Bleach bypass:** `split[a][b];[b]hue=s=0[g];[a][g]blend=all_mode=overlay:all_opacity=0.6,eq=saturation=0.65:contrast=1.08` — ч/б копия в режиме overlay поверх цвета, сила через opacity.

**L6 Duotone:** обесцветить и отобразить яркость в 2 цвета через curves (0 = тёмный цвет, 1 = светлый, значения = hex/255). Пример PERSET ночной navy #0E1A2B → блик золота #E6C68C: `format=gray,format=rgb24,curves=r='0/0.055 1/0.902':g='0/0.102 1/0.776':b='0/0.169 1/0.549'`. Только на вставки и паузы, не на весь ролик.

**L7 Mono + 1 цвет:** в ffmpeg нет квалификатора; делать в HyperFrames/AE: ч/б слой спикера + цветная графика акцентом, либо в AE (Leave Color / Hue-Sat по ключу). Резервно: `hue=s=0` на спикера и цветной только графика.

**L8 Neon split:** `colorbalance=rs=0.03:gs=-0.03:bs=0.06:rh=0.04:gh=0.01:bh=-0.03,eq=contrast=1.06:saturation=1.0,vignette=PI/4.5`

**L9 Print-film:** `curves=master='0/0 0.15/0.10 0.5/0.50 0.85/0.88 1/0.95',colorbalance=rs=0.01:bs=0.02:rh=0.03:bh=-0.02,eq=saturation=0.9` — плотные тени, скруглённые света. Если есть настоящий LUT 2383, ставить его в конец цепочки (Lowepost).

### Текстуры (добавлять к любому луку, слабее, чем хочется)
- **Зерно:** `noise=alls=4:allf=t` (2–6, на 1080x1920 после масштабирования).
- **Халация** (красно-оранжевое свечение вокруг светов): `split[a][b];[b]curves=all='0/0 0.8/0 1/1',gblur=sigma=14,colorchannelmixer=rr=1:gg=0.35:bb=0.08[h];[a][h]blend=all_mode=screen:all_opacity=0.2`
- **Диффузия (Pro-Mist):** `split[a][b];[b]gblur=sigma=20[s];[a][s]blend=all_mode=screen:all_opacity=0.12`
- **Виньетка:** `vignette=PI/5` (мягко) … `PI/4` (заметно). Фон графики всегда с градиентом или виньеткой, не плоский.

## D. Применение по брендам
**PERSET** (navy #1A2636, золото #C39953, лого и шрифты фиксированы, см. [[perset]]). Варианты по ролику ([[perset-voice-tone]]):
- **Белый Cloud Dancer**: фон #F0EEE9 или чистый #FFFFFF вместо крема, navy-текст, золото только линиями, грейд L1.
- **Ночной PERSET**: фон #0E1A2B с радиальным свечением #1A2636, светящийся золотой градиент #E6C68C → #C39953 на ключевых цифрах, грейд L9.
- **Тёплый Mocha**: крем #F3E9DC + мокко #A47864 как третий цвет, грейд L3.
- **Duotone-пауза**: navy→золото L6 на одной вставке за ролик.

**SABRMOTION** (чёрный #0B0B0C, красный #F2283B, зелёный #20DD78; [[sabrmotion]], [[apple-style-signature]]). Палитру бренда не трогаем, меняем грейд и роль цвета:
- проблема в L5 bleach bypass + красный акцент; решение переходит в L1 и зелёный (color script).
- L7 ч/б спикер + красное слово.
- L8 неон-сплит для AI/техно тем.

**Без бренда**: любая палитра B1–B12, по теме: техно = B4/B12, лайфстайл = B2/B10, ретро/хайп = B6/B7, эстетика = B9/B11, премиум = B1/B3.

## E. Как выбирать
Перед монтажом спросить (вопрос 5 в [[ask-before-edit]]): «основные цвета или новая палитра?» и предложить 2–3 варианта из этой заметки, один рекомендовать. Нет ответа → основные цвета. Принудительной ротации нет. Выбранную пару «палитра + лук» записать в заметку рилса ([[self-learning]]).

## Источники
- Pantone 2026 Cloud Dancer: https://galeriemagazine.com/pantone-announces-cloud-dancer-color-of-the-year-2026/ , hex: https://office-watch.com/2025/pantone-2026-color-cloud-dancer-office/
- Pantone 2025 Mocha Mousse hex: https://office-watch.com/2024/pantone-2025-color-mocha-mousse-word-excel-powerpoint-designe/
- WGSN Transformative Teal: https://www.wgsn.com/en/blogs/colour-year-2026-transformative-teal
- Тренды палитр 2026: https://customstickers.com/community/blog/color-trends-for-2026-palettes-designers-will-actually-use
- Synthwave/Vaporwave/80s: https://gridfiti.com/aesthetic-color-palettes/
- Wes Anderson hex: https://eggradients.com/blog/wes-anderson-color-palettes
- Сплит-тон: https://melies.co/cinematic-techniques/color/split-tone
- Teal-orange со вкусом: https://beverlyboy.com/film-technology/stylized-palettes-teal-orange-done-tastefully-by-constraint/
- Bleach bypass: https://www.premiumbeat.com/blog/color-grading-bleach-bypass-look-in-davinci-resolve/
- Халация и диффузия: https://digitalproduction.com/2024/01/30/halation-and-diffusion-on-the-hunt-for-the-ultimate-film-look/
- Fujifilm Eterna: https://www.fujifilm-x.com/en-au/products/film-simulation/eterna/
- Portra 400: https://www.analog.cafe/r/kodak-portra-400-film-review-teli
- Print-film 2383: https://lowepost.com/insider/insights/print-film-emulation-workflow-r76/page/2/
- Color script: https://www.studiobinder.com/blog/what-is-a-color-script-definition/
- Villeneuve цвет: https://pixflow.net/blog/how-denis-villeneuve-uses-color-palettes-to-elevate-storytelling-in-film/
- Тренды 2025: https://www.svgator.com/blog/graphic-design-trends-2025/

См. также: [[color-playbook]], [[motion-texture-color]], [[brand-moves-table]], [[no-music]].
