---
title: Монтаж без After Effects — тот же монтаж, только кодом
type: system
tags: [system, system-v3, pipeline, hyperframes, gsap, remotion, ffmpeg, python, no-ae, rule]
summary: Если AE нет на компьютере, занят другим тредом (AE_LOCK) или не отвечает — ролик собирается кодом с теми же свойствами графики и теми же нормами: HyperFrames-кит (HTML + GSAP, основной) или Python-движок nae (документальный моушен, композит по маске). Таблица «свойство AE → код», пайплайн tts → words → inject → dump → mix → verify_solo → check → render → QA, скиллы, грабли
updated: 2026-10-22
source: пользователь 2026-10-22 («если нет After Effects… через HyperFrames… всё, чему научились в монтажах… графика с теми же свойствами, как в After Effects, только монтаж через код»); рабочие ролики до AE (plan-2-mosque, be-honest, «Шкала должника», perset reel02, showcase3d); тест кита 2026-10-22 (QA PASS)
---
# Монтаж без After Effects

**Правило.** Ролик не ждёт AE. Если After Effects не установлен, занят другим тредом (`claude-edit\ae\AE_LOCK.json`) или не отвечает, ролик собирается **кодом** — с той же графикой (кривые, bounce, побуквенные входы, маски, камера, тени), теми же нормами vault и той же проверкой. Пользователю одной строкой: «AE занят/нет — собираю кодом (HyperFrames)». Это не «запасной сорт»: до AE так были сделаны одобренные ролики («Шкала должника» v3, Ummah Link план 2 «Сайт для мечети», be-honest, PERSET reel02).

Всё остальное в [[SYSTEM]] не меняется: Пульт вопросов, бриф с «миром ролика», 3 стиль-фрейма, плотность, звук, QA, урок в `04-lessons/reels/`.

## Чем собирать

| Ситуация | Движок | Где лежит |
|---|---|---|
| Моушен-графика, типографика, UI-истории, инфографика, промо, субтитры, говорящая голова с плашками (по умолчанию) | **HyperFrames-кит**: HTML + GSAP, одна временная шкала, `lib/sabr.js` | репо `tools/hyperframes-kit/template/`, ПК `claude-edit\tools\hyperframes-kit\template\` |
| Документальный моушен на карте, длинные проезды камеры с настоящим motion blur, фото-коллажи, кадр из пикселей (numpy/OpenCV) | **Python-движок nae** (слои Text/Counter/Box/Picture/Path/Clip, камера, авто-SFX, QA) | репо `tools/no-ae-engine/` |
| Текст за/у/из-за головы, трекинг лица, маска человека, ракурсы из одной 4K-камеры | движок профи-техник (MediaPipe + RVM) → графику поверх делаем в HyperFrames или nae | `tools/pro-techniques-engine` ([[pro-advanced-editing]]) |
| Длинные data-driven ролики на React, массовые вариации | Remotion (скиллы `remotion-*`, `OpenMontage\remotion-composer`) | ПК `Desktop\subhan\OpenMontage` |
| 3D-объект, свет | Blender MCP → рендер PNG/видео → слой в HyperFrames (`<video>`/`<img>`) | [[tools-catalog]] |

Выбор пишем в бриф строкой «Движок: HyperFrames / nae / …».

## Пайплайн HyperFrames-кита (как в рабочих роликах до AE)

```
copy tools\hyperframes-kit\template  →  reels\<дата>_<слаг>\
node tools/tts.js fv3LKrS09h3gGy4GZW1e .tmp/vo/take1 script.txt eleven_v4 0.35   # голос пользователя + тайминги по символам
node tools/build.cjs <слаг> --take take1 --tempo 1.05
```
`build.cjs` делает по порядку: **words** (слова + обработка голоса по [[voice-processing]]: HPF, EQ, де-эссер, компрессор, без de-reverb) → **gaps** (паузы-вдохи из `gaps.json`) → **inject** (слова и END в `index.html`) → **dump** (headless Chrome выполняет таймлайн, выгружает `sfx-dump` и `stats-dump`) → **mix** (SFX по якорям: начало или пик звука на событии; −14 LUFS, TP −2.5 запас под AAC) → **verify_solo** (каждый SFX отдельно, удар ±50 мс от события) → **hyperframes check** (lint, раскладка, контраст WCAG) → **render** (`--quality delivery --crf 8`, эталон) → мастер CRF 14 + light 1080×1920 CRF 18 (BT.709, faststart) → контакт-лист → **qa.cjs**.

Без голоса: просто `node tools/build.cjs <слаг>`. Черновик: `--draft` (быстро, без QA). Живой «таймлайн» для пользователя и для правок: `npx hyperframes@0.8.140 preview` (студия со скраббером) + скриншот, сцены в `index.html` подписаны блоками `// ═══ 1 · хук ═══`, времена — объект ключей (`T1, T2…`) из слов озвучки.

Стиль-фреймы (этап 4): `node tools/build.cjs <слаг> --draft`, затем кадры `ffmpeg -ss <t> -i out/<слаг>_draft.mp4 -frames:v 1` по одному на хук/середину/финал; или `npx hyperframes render --format png-sequence` на короткий кусок. Для nae: `python -m nae.run project.py --out out --frames 1.2,6.0,12.5`.

## Свойство AE → то же самое кодом

| В After Effects | HyperFrames + GSAP (`lib/sabr.js`) | Python nae |
|---|---|---|
| Ключи + Easy Ease 40–55 % ([[motion-curves-measured-2026-10-21]]) | `ease: "sabr"` = cubic-bezier(.5,.1,.4,.9) (CustomEase) | `EASE` |
| Камера: выход 1–5 %, вход 35–80 % | `ease: "sabrCam"` = (.05,0,.35,1); `cam(t, {x,y,scale}, d)` двигает `#world` | `CamTrack`, `EASE_CAM` |
| Акцент expo-out | `"sabrHit"` | `EASE_ACCENT` |
| Выражение bounce со снапом 0.7 с | `pop()` — `back.out(1.4)`, кончается ровно на 1 | `pop_scale()`, `bounce()` со снапом |
| Text Animator по буквам: opacity + offset + blur | `letters(el, t)`: буква за буквой, blur ≤ 8 px только у заголовков ≥ 60 px, ноль к середине входа, **тик на каждую букву** | `Text(mode='letters')` |
| Range Selector по словам (мелкий текст) | `words(el, t)`: opacity + y 7 px, без блюра, тихий тик на слово; `times` из слов озвучки | `Text(mode='words', times=…)` |
| Source Text + слайдер-счётчик | `counter(el, a, b, t, d)`: tabular-nums, удар в конце | `Counter` (цифры фиксированной ширины) |
| Shape Rectangle Size 0 → w,h (расширение из точки) | `grow(el, t, {hero})` | `Box(enter='point')` |
| Линия → блок | `lineToBlock(el, t)` | `Box(enter='line')` |
| Раскрытие из угла | `transform-origin: 0 0` + `grow` | `Box(enter='corner')` |
| Контейнер растёт за контентом | `tl.to(card, {height})` на каждый новый пункт | `Box(keys=[(t,x,y,w,h),…])` |
| Trim Paths | `strokeDasharray/strokeDashoffset` по `getTotalLength()` | `Path` |
| Track matte / Alpha matte | CSS `mask-image`, `clip-path`, `overflow:hidden` | альфа-маски numpy |
| Маска-шторка | `clip-path: inset(0 100% 0 0)` → `inset(0 0 0 0)` | `Picture(enter='wipe')` |
| Прекомп | `<div>`-группа или под-композиция `data-composition-src` | функция-сцена / свой `Comp` |
| Null + parent | общий контейнер, дети наследуют transform | `world=True` слои под камерой |
| 3D-слой, перспектива, наклон | `perspective` + `rotateX/Y`, `transform-style: preserve-3d`; сложное 3D — Three.js в композиции или Blender | плоскость `Yaw` в движке профи-техник |
| Motion blur 180° | нативного нет: короткие быстрые проезды с `sabrCam`, крупные быстрые движения — рендерить в nae | сабсэмплы в окне затвора 180° (`Comp.frame`) |
| Gaussian Blur (вход/расфокус) | `filter: blur()` только на входе, в покое `blur(0px)` | `cv2.GaussianBlur` только во входе |
| Расфокус-переход вместо реза | `defocus(from, to, tc)` с перекрытием (без пустого кадра) | `Defocus(tc)` |
| Glow / Drop Shadow | `box-shadow`, `text-shadow`, `drop-shadow` (glow только на входе) | `soft_shadow` |
| Blending modes | `mix-blend-mode` (не работает внутри родителя с transform/filter — см. грабли) | `screen()`, `over()` |
| Time Remap / заморозка | `video.playbackRate`, отдельный `tl` с `timeScale` | индекс кадра `Clip` |
| Маркеры композиции | `E(t)` → `stats-dump` (события/с, дыры > 1.6 с) | `events.json` |
| Lumetri / грейд | грейд видео ffmpeg на подготовке ([[color-playbook]]), графика — точные HEX бренда | `Clip(grade='eq=…,curves=…')` |
| Rotobrush, трекер | RVM-маска и MediaPipe из движка профи-техник → ключи x/y | то же |
| `saveFrameToPng`, aerender | `hyperframes render` (mp4/png-sequence), `--crf 8` эталон | `--frames`, `nae.run` |
| `ae_sharp_preflight.jsx` | `finish()`: зерно/шум = FAIL, конечный scale ≠ 1 = FAIL | `issues()` (апскейл фото), покой без блюра |
| `sharpcheck.py` | `qa.cjs` → `tools/sharpcheck.py` (эталон CRF 8 vs master/light ≥ 0.9) | `qa.py` (кадр рендера vs видео ≥ 0.9) |

## Нормы vault, встроенные в код (не вспоминать — они срабатывают сами)
- **Резкость** ([[sharpness-guard]]): текст всегда живой (DOM или растр в нужном кегле, без масштабирования картинки текста); мелкий текст без блюра; в покое масштаб ровно 1; апскейл фото — FAIL; **зерно и шум запрещены** — слой `grain/noise` валит QA (в старых роликах был `#grain` — больше не ставим); light 1080×1920 CRF 18, не 720p.
- **Звук** ([[sfx-expressive]], [[sound-v2]]): каждый `S(t, вид, дБ, слой)` привязан к элементу; буква = тик (QA сверяет число букв и тиков); вжух пиком на пике скорости камеры и на склейке; под голосом тики −6 дБ, остальное −3 дБ; окна 0.25 с с ≥ 5 акцентами = FAIL; без музыки ([[no-music]]), фон под голосом — только тихий нашид ([[ambience-library]]); −14 LUFS, TP ≤ −1.
- **Время чтения** ([[reading-time]]): `finish()` прокручивает таймлайн и находит, когда надпись реально пропала (ушла, сменилась сцена, увезла камера, расфокус); без голоса 0.6 + 0.2/слово (+0.3 числа, +0.6 CTA); с голосом — по фразе; с референсом — `REF_TEMPO=1`, сокращаем текст, а не тянем время.
- **Анимация** ([[motion-v3]]): ничего не появляется без входа, выходы быстрее входов, bounce только у героев, расширение блоков — `grow`/`lineToBlock`.
- **Первый кадр не пустой**, проявление надписи не прерывается уходом, контраст WCAG (`hyperframes check`), поля ≥ 60 px.
- Камера и ракурсы разрешены ([[camera-allowed]]), плавно; приёмы — по ситуации ([[techniques-by-situation]]).

## Скиллы, которые уже стоят на ПК (ставили 2026-10-13, [[tools-catalog]])
- HyperFrames (21): `hyperframes-animation`, `motion-graphics`, `talking-head-recut`, `embedded-captions` (35 стилей, субтитры за спиной), `faceless-explainer`, `product-launch-video`, `/media-use`, `/hyperframes-audio`.
- `video-editing` (nopefallacy, вертикальный рилс на HyperFrames с верификацией), `short-form-video`, `beat-sync-editing`.
- iart-ai (17 пакетов): `kinetic-typography`, `animated-infographic`, `chart-animation`, `diagram-animation`, `logo-animation`, `lower-thirds`, `svg-animation`, `isometric-animation`, `text-message-animation`.
- Remotion (12): `remotion-*`, `remotion-captions`, `video-talkcraft`; OpenMontage (`remotion-composer`).
- ffmpeg-master (`ffmpeg-color`, `ffmpeg-kinetic`, `ffmpeg-effects`, `transitions-effects`, `animation-timing-reference`), `video-shotcraft` (2.5D-камера по скриншотам), `manim`.
- Арт-дирекция: `motion-art-direction`, `animation-principles`, `color-motion`, `brand-motion-guidelines`.
Скилл даёт приёмы и разметку; нормы (кривые, звук, резкость, без зерна, без музыки, без капса с цветным словом) — из этого файла и `01-rules`, они главнее скилла.

## Грабли (из роликов до AE и теста 2026-10-22)
- `tl.set` на позиции 0 не рисует кадр 0 → видимость/стартовые значения через `S0()` (в ките уже так).
- `hyperframes check` требует строку `window.__timelines["main"] = tl` прямо в `index.html` (иначе `missing_timeline_registry`).
- Элементы, которые камера увозит за кадр, помечать `data-layout-allow-overflow` на контейнере `#world`.
- `mix-blend-mode: screen` у видео внутри родителя с transform/filter не работает → рендерить 3D на цвете фона и гасить края `mask-image`.
- Прозрачная заливка у контурного текста → `text_not_painted` в check: дать еле видимую заливку.
- `inject.js` обязан писать `{w,t,e,line}`: без `e` все события «на конец слова» молча пропадают.
- ffmpeg 6 не знает `-/filter_complex` → `mix.js` сам переключается на `-filter_complex_script`.
- AAC поднимает true peak до +3 дБ на острых тиках → микс в TP −2.5, QA меряет уже mp4.
- Chrome для `dump.js`: env `CHROME`, `.tmp/chrome_path.txt` или стандартный путь; на ПК — Chrome из Program Files.
- Пустой кадр на расфокус-склейке: новая сцена должна иметь контент с момента `tc − d/4` (QA ловит пустой кадр только на 0-м кадре — смотреть контакт-лист).
- Крупный файл на ПК (> 25 МБ) — gzip + split ([[pro-advanced-editing]]).

## Проверка кита (2026-10-22)
Тестовый ролик SABRMOTION 12.4 с (линия → карточка, буквы с тиками, проезд камеры, счётчик 100 %, расфокус, пилюли, финал-точка): `hyperframes check` 0 ошибок, 48/48 контраст; QA PASS — синхрон SFX макс. 5 мс, резкость master/light ≥ 0.9 эталона, −14.1 LUFS / TP −2.4, все надписи по норме чтения. QA сам поймал и заставил исправить: надпись уходила раньше нормы, пустой кадр на склейке, TP −0.5 после AAC. nae: 9 с за 34 с на 4 ядрах, QA PASS (поймал пустой первый кадр).

См. [[SYSTEM]], [[ae-pipeline]], [[pipeline-gotchas]], [[tools-catalog]], [[pro-advanced-editing]], [[docu-map-motion]].
