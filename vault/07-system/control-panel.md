---
title: Пульт монтажа — бриф кнопками перед каждым роликом
type: workflow
tags: [workflow, system-v3, questions, rule]
summary: Артефакт «Пульт монтажа» (https://claude.ai/artifact/9KKFp4QoCgF5JJLVcrLSA3) — пользователь выбирает тип, есть ли исходное видео (и какое, где лежит), сценарий, бренд, направление D0–D6, уровень, живой монтаж, анимации, переходы, субтитры, инфографику, звук, цвет, грейд, лицо, формат, длину, показы; Claude читает сохранённый бриф через ArtifactData
updated: 2026-10-22
source: пользователь 2026-10-19 («сделай красивую нормальную систему монтажей, в которой можно выбирать и полностью контролировать монтаж и стили вопросами»)
---
# Пульт монтажа

Ссылка: https://claude.ai/artifact/9KKFp4QoCgF5JJLVcrLSA3. Исходник лежит в скретчпаде треда «Сбор знаний», копия — `vault/_tools/pult-montazha.html`.

## Как читать бриф
- Последний бриф лежит в ArtifactData, artifact `https://claude.ai/artifact/9KKFp4QoCgF5JJLVcrLSA3`, документ `state/current`.
  - Поля: `choices` (объект: id вопроса → значение или массив), `note`, `summary`, `createdAt`.
  - История хранится в коллекции `briefs`.
- Значение `__auto` или отсутствие ключа означает «реши сам»: берём рекомендованное и свежую комбинацию, не повторяя 2 прошлых ролика ([[ask-before-edit]]).
- Если `createdAt` старше последнего ролика или пользователь не говорил «бриф готов», уточнить, что бриф относится к этому ролику.
- Пользователь может вставить текст брифа в чат (кнопка «Скопировать»). Тогда этот текст главнее документа.

## Вопросы (id → значения)
Отмеченные в вопросах о приёмах (recipes, entrances, transitions, pro…) — пожелания, а не квота; неотмеченное берём только к месту ([[techniques-by-situation]]).
| id | значения |
|---|---|
| type | talking, voice, demo, beforeafter, promo, islamic |
| source | talking, broll, screen, photos, audio, none (multi; **обязателен для каждого ролика**, с 2026-10-20) |
| srcwhere | текст: папка на ПК / ссылка / «скину в тред»; показывается, если есть исходник |
| srcstate | onetake, takes, precut, phone, camera; только если есть видео |
| orient | vert, horiz, mixed; только если есть видео (горизонталь кадрируем, не растягиваем, см. проверку SAR) |
| build | motion, infog, library, 3d, ai, ui, map (документальный моушен на карте, [[docu-map-motion]]); если исходника нет / только голос / только фото |
| script | ready, theses, frommedia, write |
| brand | sabrmotion, perset, ummah, none |
| direction | D0–D6, до 2 |
| blogstyle | A журнальный, B неоновый капс, C диорамы, D кино-слово; до 2; для говорящей головы ([[ref-blog-beforeafter-2026-10-20]]) |
| textlevels | u1–u5 = уровни У1–У5 из [[talking-head-pro-guide]] (2–3 на ролик, ротация) |
| techmode | situ (по ситуации, рекоменд.), mine (только отмеченные), clean (почти без приёмов), rich (побольше, но к месту) — с 2026-10-21, [[techniques-by-situation]] |
| repeat | fresh (хук / главный переход / текстовый приём / финал не как в 2–3 прошлых роликах, рекоменд.), series (серия, общий стиль), part (1–2 узнаваемые вещи) |
| pro | T1, T3, T4, T5, T6, T7, angles, vtext, scale, card — приёмы «дорого» из [[pro-advanced-editing]]; отмеченные = точно берём, остальные только если подходят ([[pro-baseline]]); если есть видео |
| recipes | R1,R3–R11,R13,R14 из [[ref-blog-beforeafter-2026-10-20]]; Y1–Y5,Y7–Y10 и ST (стаккато) из [[ref-blog-shot-by-shot-2026-10-20]] |
| broll | reshoot, photos, stock, 3d, ai — источники перебивок; перед монтажом шот-лист «слово → кадр → источник» |
| fonts | fA Segoe+Georgia Italic, fB Montserrat ExtraBold+Georgia Italic, fC Segoe, brand |
| engine | ae (всё в AE, видимый таймлайн), code (без AE: HyperFrames-кит или Python nae, [[no-ae-pipeline]]), both (ключевые сцены в AE, остальное кодом; рекоменд.) — с 2026-10-22. Если выбрано ae, а AE занят (AE_LOCK) или не отвечает — сказать пользователю и собирать кодом |
| blender | hero (3D-герой через весь ролик), accents (1–2 вставки, рекоменд.), intro (3D в хуке/финале), no (без 3D) — с 2026-10-22; Blender MCP на RTX 5080, рендер вставляется в AE или в код |
| tier | min, std, power, ultra |
| live | cuts, framings, jl, broll, behind, pointing, split, rehook ([[live-editing-v3]]); для talking/beforeafter или source=talking |
| entrances | expand, grow, blurrise, bounce, stagger, chars, bento, mask, corner, counter, draw, rig ([[motion-v3]], [[animation-techniques-2026-10-19]]) |
| transitions | morph, cut, square, grid, wipe, match, whip, defocus, vtext (сквозь букву), push, mix |
| captions | phrases, wordswitch (по слову, шрифт меняется каждые 0.25–0.4 с), hero (слово-герой на груди), neon2 (две строки, вторая светится), kinetic, word, accents, none |
| infographics | max, mid, low |
| sound | sfx_many, sfx_few, sfx_human (жесты/смена плана/наезд), sfx_material (бумага/стекло/стол), nasheed (тихий нашид на фоне; старое значение ambience читать как nasheed), silence, voice_own, voice_clone |
| color | main, B1, B2, B3, B10, B11, light ([[color-palettes-research]]) |
| grade | L1, L2, L3, L4, L9 (для живой съёмки: type talking/beforeafter/demo или source с видео) |
| face | 100, 70, 40, 0 |
| format | v, h, s, p |
| length | 15, 30, 60, 90 |
| finale | loop (затемнение + знак бренда, последнее слово тает), textlogo, loopstart |
| proof | frames, animatic, direct |

На пульте закреплены постоянные правила: без музыки, без звуков природы, оригинальный фон, всё появляется с анимацией, никого не критикуем; камера разрешена плавно ([[camera-allowed]]); лицо по центру кадра, грейд не темнит исходник, картинка под слово, а не под тему (уроки теста блога 2026-10-20, [[talking-head-anti-ai]]).

Пресет «Блог как у профи» (2026-10-20): стиль A, У1–У3, R3/R4/R5/Y1/Y7, досъёмка + 3D, субтитры wordswitch, SFX человека и материала, шрифты fA, финал-луп.

## Исходное видео (с 2026-10-20)
Пользователь: «при каждом новом монтаже нужно сделать пульт с выбором стилей, есть ли исходное видео и другое». Вопрос `source` задаётся для **каждого** ролика сразу после типа. Если на пульте его нет, это первая карточка `ask_decision`.
- Есть видео → спросить, где лежит (`srcwhere`), что за съёмка (`srcstate`) и как снято (`orient`); перед монтажом проверить SAR/поворот.
- Нет видео или только голос/фото → спросить, из чего собирать картинку (`build`), и собрать карту арсенала ([[use-everything]]).
- `script` уточняет, есть ли текст или писать с нуля.

## Если пользователь не заполнил пульт
Вопросы задаются кнопками по [[ask-before-edit]], в том же наборе и порядке. Ссылку на пульт даём в первом сообщении.
