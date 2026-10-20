---
title: practitioners-web-2026-10-19
type: research
tags: [research, motion, editing, anti-ai, practitioners, reels, after-effects]
summary: 30 реальных монтажёров, моушн-студий и авторов туториалов с «ручной» эстетикой, их техники и как повторить в стоковом AE + Python/ffmpeg/Blender; 18 рецептов, 10 признаков «ИИ-шаблона», 4 стилевых направления для вертикальных talking-head/продуктовых Reels без музыки
updated: 2026-10-19
source: веб-ресерч (WebSearch/WebFetch) — Motionographer, Stash, It's Nice That, Creative Bloq, Videobolt, Motion Array, Lesterbanks, Skwigly, Video Consortium, RNDR newsletter, Artlist, Musicbed, Typeroom, Sostav
---

# Реальные практики: у кого учиться уходить от «ИИ-чистого» моушена

**Контекст.** Вертикальные Reels 9:16, говорящая голова + закадр про продукт/технологии, русскоязычная аудитория, основатель исламского приложения, **без музыки** (только голос, SFX, фоли). Текущие монтажи собираются ИИ-агентами в After Effects / коде и выглядят как Apple-кейноут: скруглённые карточки UI, blur-in и scale-in, всё по центру, мягкие градиенты, моно-капс подписи, глянцевый минимализм.

**Главный вывод исследования.** В 2026 индустрия сама отталкивается от этого вида. Creative Bloq называет «anti-AI crafting» трендом года и цитирует Graham Sykes (Landor): ручная фактура как «противоядие» от гиперглянцевого языка ИИ ([Creative Bloq](https://creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026)). Videobolt в обзоре моушн-трендов 2026 выделяет те же пункты: рисованные кадры с неровными линиями, аналоговое зерно и пыль, рваная бумага со **сниженной частотой кадров**, модульные редакционные сетки ([Videobolt](https://blog.videobolt.net/post/top-motion-graphics-trends-2026)). Golden Wolf формулирует свою позицию как «raw, irreverent, unapologetically unpolished»: ИИ у них используется только для версий и мудбордов, а не для готового кадра ([Motionographer](https://motionographer.com/2025/05/12/studio-stories-12-years-of-golden-wolf/)).

Условные обозначения: **[ист.]** — техника подтверждена источником по ссылке; **[набл.]** — описание по общеизвестным работам, источник не проверен в этой сессии; **[рецепт]** — моя реконструкция для стокового AE, это не слова самого автора.

---

## Часть 1. Практики (30)

### A. Монтажёры и создатели short-form и YouTube-эксплейнеров

**1. Cleo Abram / «Huge If True»: аниматор Whitney Theis, монтажёр Joan Educate**
- Ссылки: youtube.com/@CleoAbram · интервью [Video Consortium](https://videoconsortium.org/mag/episode-8-cleo-abram) · разбор [RNDR](https://rndr.beehiiv.com/p/rndr-firstever-edition)
- Техники [ист.]: Cleo сознательно ушла от «серого, чёрного и одного неона» техно-шоу к тёмно-коричневым, зелёным и синим фонам, ориентир — solarpunk. Сценарий строится вокруг одного ключевого визуала: схемы, архивного кадра или демонстрации. В графике есть текстурированные цветные подложки, лёгкий stop-motion-джиттер на аудио-волне, текст, разложенный по струнам нарисованной гитары, и пазлы, которые притягиваются как магниты: у каждого своя скорость и небольшой перелёт.
- Как повторить: палитра без чёрного и неона (см. рецепт 14). Джиттер через Posterize Time 12 на слое волны (Audio Spectrum). Текст по пути через Text > Path Options. Пазлы — разные задержки плюс overshoot-выражение (рецепт 9).

**2. Johnny Harris (бывший Vox)**
- Ссылки: youtube.com/@johnnyharris · [aescripts: How Johnny Harris makes maps](https://aescripts.com/learn/how-johnny-harris-makes-maps/)
- Техники [ист.]: карты в AE (GEOlayers — сторонний плагин), смешанные с документальной съёмкой. [набл.]: бумажные и ретро-карты, маркер и красная линия, вырезанные фото со сдвинутыми тенями, «рабочий стол» с распечатками, камера ездит по физическому коллажу.
- Как повторить без плагина: экспорт карты из Natural Earth / OSM в SVG или PNG через Python (geopandas + matplotlib), затем в AE: Multiply-текстура бумаги, Trim Paths на маршруте, Roughen Edges на границах, 3D-камера с лёгким wiggle.

**3. Vox (команда видео, школа Johnny Harris, Joss Fong, Sam Ellis)**
- Ссылки: youtube.com/@Vox
- Техники [набл.]: вырезанные из фото фигуры с белой обводкой, полутона, газетная бумага, подсвеченные маркером строки документов, архив в рамке с зерном. RNDR отмечает Johnny Harris и Sam Ellis как бывших Vox с похожим дизайн-подходом [ист.].
- Как повторить: рецепты 3 (стикер-вырез), 6 (полутон), 10 (маркер по документу).

**4. Ali Abdaal (команда монтажа)**
- Ссылки: youtube.com/@aliabdaal · [RNDR: 5 visuals](https://rndr.beehiiv.com/p/5-visuals-next-video)
- Техники [ист.]: в интро линия текстового подчёркивания превращается в линейный график в следующей сцене (match-morph), затем переход в A-roll. Анимированные главы и оглавление.
- Ценность для нас: это **морф-переход по форме**, а не blur-in. Сама эстетика у Abdaal довольно чистая, поэтому брать стоит приём, а не вид.

**5. Hayden Hillier-Smith (монтажёр Logan Paul и др.)**
- Ссылки: [Musicbed: Masterminding Viral Edits](https://www.musicbed.com/articles/?p=7556)
- Техники [ист.]: «проактивный» монтаж: монтажёр заранее решает, чем станет материал, а не идёт за исходниками. Принцип «2+2» Эндрю Стэнтона: дать зрителю детали и не проговаривать вывод. Сдержанность в серьёзных моментах: убрать джамп-каты, замедлить ритм, чтобы возврат к динамике ощущался заслуженным.
- Для нас (без музыки): эмоцию задают тишина и SFX. Переключение «плотно, потом тихо, потом плотно» работает и без трека.

**6. Casey Neistat**
- Ссылки: youtube.com/@casey · [Artlist: разбор](https://artlist.io/blog/editing-storytelling-techniques-casey-neistat/)
- Техники [ист.]: обрыв фразы на полуслове со склейкой в новую сцену; одна мысль, разнесённая по нескольким локациям; ассоциативные вставки; ускоренный монтаж-прогресс; наезд к лицу в камере; переходы в камере (поставил камеру, поднял, шлепок по объективу). [набл.]: рукописные титры, маркер на бумаге, снятые на камеру.
- Как повторить: снимать переходы физически. Титры писать от руки маркером на бумаге и снимать на телефон (или сканировать), ключ через Extract или Linear Color Key.

**7. Rickie Ho (RNDR, бывший монтажёр Humphrey Yang)**
- Ссылки: [rndr.beehiiv.com](https://rndr.beehiiv.com/p/rndr-firstever-edition)
- Ценность: еженедельные разборы конкретных визуалов YouTube-эксплейнеров. Пример [ист.]: «аудио-волна с гранж-деталями: бейджи с именами, текстурированные обороты фото, зерно, машинописный шрифт и анимация печати».
- Как повторить: рецепт 11 (машинопись) и рецепт 2 (зерно).

**8. Sam Ellis (Search Party, бывший Vox)** [набл.]
- Ссылки: youtube.com/@SearchPartyTV (проверить)
- Техники: документальный ретро-коллаж, архивные плёнки, графика на «бумажной» подложке, плотная сценарная работа над визуалом. RNDR ставит его в одну линию с Abram и Harris [ист.].

### B. Студии моушн-дизайна

**9. BUCK**: buck.co
- [набл.] Рисованная 2D-анимация кадр за кадром, на двойках, с вариацией толщины линии, плюс 3D, стилизованный под 2D. Creative Bloq цитирует Simon Chong (BUCK) о персонажах и маскотах внутри брендовых сред [ист.].
- Повторить: Blender Grease Pencil, анимация на 2s (12 fps внутри 24), экспорт PNG-секвенции в AE.

**10. Oddfellows**: oddfellows.tv
- [ист., Motion Array] Иллюстративный вид и сильная история; Junebugs и работы для Nest. [набл.] Насыщенная, но не неоновая палитра, зернистые градиенты (stipple), мягкий squash & stretch.
- Повторить: зерно внутри заливки (рецепт 2b), а не гладкий градиент.

**11. ManvsMachine** (теперь в WPP/Landor): manvsmachine.co.uk
- [ист., Stash] Фильм для Canva/Affinity: 3D, 2D, кинетическая типографика и рисованная иллюстрация в одной непрерывной цепочке. Стиль объекта меняется на лету: пиксельный стул, плюшевый, деревянный. Реальный UI с курсором и выделением вплетён в сюжет.
- Ценность для нас: **один объект в разных техниках** как механизм переходов. UI показан как инструмент в руке, а не как стеклянная карточка.

**12. Ordinary Folk** (Jorge R. Canedo Estrada): ordinaryfolk.co
- [ист.] Манифест School of Motion, короткий фильм «Nightdrive», проект «Mainframe» ([Stash](https://www.stashmedia.tv/ordinary-folk-rescues-mainframe-motion-project-from-the-bin-of-destiny/), [SoM podcast](https://schoolofmotion.com/podcast/ordinary-folk-interview)). [набл.] Плоские формы с очень выразительным таймингом: резкие старты, длинные «висы», смазы (smear frames).
- Повторить: рецепт 8 (тайминг с висом и смазом).

**13. Giant Ant** (Ванкувер, Jay Grandin): giantant.ca
- [ист., Motion Array] Смешение эпох: для Slack — оммаж мультфильмам 1940-х с cartoon-shaded 3D. Практические рукотворные декорации и стилизованная камера (Visa). Трейлеры DOXA: «один кадр, один объект, сплошной фон», медленный темп и звуковой дизайн до раскрытия.
- Ценность для нас: формат DOXA идеален для продуктового Reels без музыки: предмет в руке на однотонном фоне, фоли, раскрытие.

**14. Golden Wolf** (Лондон / Нью-Йорк): goldenwolf.tv
- [ист.] 2D + 3D + аналоговое, ностальгия, поп-культура, сюрреализм, рисованные эскизы и физические реквизиты; draw-over поверх рендера.
- Повторить: дорисовка поверх кадра (рецепт 5) и аналоговые реквизиты.

**15. Gunner** (Детройт, куплена Duolingo): gunner.work
- [ист.] Студия перешла к Duolingo ([Cartoon Brew](https://cartoonbrew.com/studios/duolingo-acquires-gunner-animation-studio-221889.html)); ранее «Remembering Gravity» ([Motionographer](https://motionographer.com/2016/02/24/remembering-gravity-the-animated-story-of-an-astronaut-coming-home)). [набл.] Живая характерная анимация, cel-shading, резкие позы.

**16. Animade** (Лондон): animade.tv
- [ист., Motionographer] «Почти пещерный» рисунок персонажей, «тёмная землистая» атмосфера в духе восточноевропейской анимации. Короткие гэги на 15 секунд в стиле Looney Tunes. Простые джамп-каты оказались понятнее склеенных переходов.
- Ценность для нас: **жёсткая склейка лучше, чем ещё один плавный переход**.

**17. Tendril** (Торонто): tendril.ca
- [ист.] Студия брендинга и моушна, графический язык для Deserve и VIZIO (Abduzeedo). [набл.] Скорее 3D-премиум, поэтому как анти-референс для глянца брать осторожно. Полезна системностью моушн-языка бренда.

**18. DIA Studio** (Нью-Йорк, Mitch Paone, Meg Donohoe): dia.tv
- [ист., It's Nice That] Движение — это и есть содержание. Шрифт в айдентике A-Trak «никогда не останавливается, всегда переход». Десятки вариантов за несколько часов. Типографика как механика, «как теория музыки»: пропорция и негативное пространство.
- Повторить: рецепт 12 (кинетическая типографика с физикой и разрезанием букв).

**19. Studio Dumbar / DEPT®** (Роттердам): studiodumbar.com
- [ист., Typeroom] Для Amsterdam Sinfonietta написали код, превращающий музыку в паттерны из акронима «AS». North Sea Jazz — кинетическая типографика на шрифтах Gravity и Monument Grotesk (Dinamo). Цвет передаёт настроение.
- Для нас: типографический паттерн из имени приложения, который генерирует **голос** (амплитуда речи через Python), а не музыка.

**20. Studio Moross** (Aries Moross): studiomoross.com
- [ист., MOO] Яркий цвет, рукописная и плакатная типографика, концертные визуалы. [набл.] Плоские плашки, рисованные шрифты, ритмичная смена цвета.

**21. Hornet** (Нью-Йорк, представительство режиссёров): hornet.com
- [ист.] Ростер включает Ariel Costa ([Stash](https://www.stashmedia.tv/ariel-costa-aka-blinkmybrain-joins-hornet-directing-roster)). Полезен как витрина режиссёров mixed media.

**22. SILA SVETA (Москва) и Nord Collective** (русскоязычный пласт)
- [ист., Sostav] Арт-директор SILA SVETA Артур Кондрашенков — работа «PURE» для Pause Fest, отмечена Behance. Владимир Томин — сооснователь Nord Collective, судья по моушну.
- Честно о пробеле: русскоязычных Reels-монтажёров с узнаваемым «ручным» стилем через веб-поиск найти не удалось, выдача забита фрилансом и курсами. Искать вручную в Instagram и Telegram по хэштегам #коллажнаяанимация и #motiondesign_ru.

### C. Отдельные моушн-дизайнеры и аниматоры

**23. Ariel Costa / Blink My Brain**: blinkmybrain.tv
- [ист., Motionographer] Коллаж «старой школы плюс новой»: «ригги сделаны, суставы сломаны, всё движется вместе», то есть вырезанные фото-части с нарочито ломаными шарнирами. Подложки с фактурой, жирная типографика, громкий цвет. Есть бесплатный AE-проект «Bang Bang».
- Повторить: рецепт 4 (коллаж-риг из вырезанных фото, Puppet Pin, на 2s).

**24. Allen Laseter**: allenlaseter.com
- [ист., Motionographer «Step by Step»] Фейковое 3D: стилизованная перспектива целиком в After Effects. [набл.] Бумажные фактуры, приглушённая «книжная» палитра, ровный медленный ритм. Подписан на Jelly London ([LBB](https://lbbonline.com/news/jelly-london-signs-allen-laseter-and-hattie-newman)).
- Повторить: перспективные шейпы плюс Multiply-фактура бумаги и Posterize Time.

**25. Winston Hacking**: winstonhacking.substack.com
- [ист.] Около десяти лет ручной коллажной анимации: клипы для Flying Lotus, Run the Jewels, Animal Collective; D&AD Wood Pencil, Clio Gold. Метод: бумага, вырезанная руками, stop-motion и найденная плёнка с минимумом цифры. Ошибки **сознательно оставляет в работе**.
- Повторить: печать кадров, вырезание ножницами, съёмка на телефон с рук, затем обратно в монтаж. Или цифровой суррогат (рецепт 4 + 7).

**26. Nicolas Ménard**: nicolasmenard.com
- [ист., Skwigly] Шесть лет графдизайна и шелкографии. Правило «трёх красок»: наложение трёх цветов даёт дополнительные оттенки, как в трафаретной печати.
- Повторить: рецепт 13 (ризограф / трафарет, 2–3 краски, Multiply, сдвиг приводки).

**27. Felix Colgrave**: [Wikipedia](https://en.wikipedia.org/wiki/Felix_Colgrave)
- [набл.] Сюрреалистичная покадровая анимация, кислотная, но цельная палитра, плотный дизайн звука, органические «живые» формы. Интервью Pictoplasma «Animation is sensory» [ист. заголовок].
- Для нас: в основном звуко-визуальная синхронность. Каждое движение получает свой звук.

### D. Авторы туториалов и разборов (методика)

**28. Ben Marriott** (Сидней): benmarriott.com · youtube.com/@BenMarriott · [Textures in AE](https://benmarriott.gumroad.com/l/DOFSr)
- [ист., Lesterbanks] Вид бумажной вырезки и stop-motion в стоковом AE: Shape Layer, оператор **Wiggle Paths** с выражением и posterize time (край меняется как новая вырезка в каждом кадре), низкая частота обновления, wiggle позиции и поворота. Отдельный урок: зерно через маску, матт и **Roughen Edges**, «быстрее и гибче» его старого метода.
- Это ядро рецептов 1, 2, 7.

**29. Jake Bartlett / Jake in Motion**: youtube.com/@JakeInMotion · [Skillshare: Texturing in AE](https://www.skillshare.com/en/classes/texturing-in-adobe-after-effects/1333636165)
- [ист.] Курс по текстурированию в AE. [набл.] Стоковые методы: Fractal Noise, Turbulent Displace, CC Composite, track matte с текстурой, грязные тени.

**30. School of Motion**: schoolofmotion.com
- [ист.] Подкасты со студиями (Ordinary Folk и др.), обзоры текстурных инструментов. Полезен как библиотека интервью о процессе.

Дополнительно для просмотра (не проверено в этой сессии): Kurzgesagt — это как раз чистый вектор, анти-пример; LEMMiNO — минимализм с сильной типографикой и звуком.

---

## Часть 2. 18 «ручных» техник с рецептами (стоковый AE, без плагинов)

Общие базовые настройки: композиция **1080×1920, 24 fps** (не 30 и не 60: 24 сразу даёт «киношную» дискретность). Анимационные элементы на **двойках**: Posterize Time 12 fps или выражение `posterizeTime(12)`. Для stop-motion — 8 fps.

1. **Бумажная вырезка с «кипящим» краем** (Ben Marriott) [рецепт]
   Shape Layer, Add, **Wiggle Paths**: Size 3–6, Detail 8–15, Points Corner, Wiggles/Second 0. На Temporal Phase выражение `posterizeTime(8); time*360`. Под фигурой тень: Drop Shadow Softness 0, Distance 8–14, Direction 135°, Opacity 60–80%, цвет — тёмный оттенок фона, не чёрный.

2. **Зерно, которое «живёт»**
   (a) На Adjustment Layer: **Add Grain**, Preset Kodak 5218, Intensity 0.6–1.0, Size 1.2–1.6, затем **Noise** 3–5% (Use Color Noise off). Режим Overlay, Opacity 40–70%.
   (b) Зерно внутри заливки (Oddfellows/stipple): Solid → **Fractal Noise** (Contrast 400, Brightness −30, Scale 3–5, Evolution `time*1000`, posterizeTime(12)) → используется как Luma Matte для второго цвета. Получается стохастический градиент из точек вместо гладкого.
   (c) Roughen Edges (Ben Marriott): Edge Type Roughen, Border 20–60, Scale 3–8, Evolution `posterizeTime(12); time*400` на маске тени.
   Альтернатива в ffmpeg: `-vf noise=alls=10:allf=t+u`.

3. **Вырезанное фото с белым «стикерным» краем** (Vox, Johnny Harris)
   Человека или объект вырезать **Roto Brush 3** → Freeze. Дубликат ниже: **Minimax** (Operation Maximum, Radius 10–16, Channel Alpha) → **Fill** белым, слегка тёплый #F4EFE6. Ещё ниже Drop Shadow Softness 0–4, Distance 10. Добавить **Roughen Edges** Border 2 на белую обводку, чтобы край не был векторно ровным. Анимация: появление **за 2–3 кадра** (Hold-ключи), без blur-in.

4. **Коллаж-риг на 2s** (Ariel Costa, Winston Hacking)
   Фото разрезать на части (голова, рука, предмет) отдельными слоями, якоря в суставах, Parent. Ключи только позами, все ключи **Toggle Hold Keyframe**, позы через 2–4 кадра. Сверху `wiggle(4,1.5)` на Rotation с posterizeTime(8): «дрожь руки аниматора».

5. **Draw-over / рукописные пометки поверх видео** (Golden Wolf, Casey Neistat)
   Лучший вариант — нарисовать на iPad в Procreate или Rough Animator (экспорт PNG-секвенции 12 fps) или маркером на бумаге со сканом. В AE: Shape-штрих + **Trim Paths** End 0→100% за 6–10 кадров с ключами Linear, + Wiggle Paths Size 1.5, posterizeTime(12). Ширина линии меняется через Taper (Stroke > Taper). Круг вокруг слова рисуется «не до конца» и с перехлёстом.

6. **Полутон / газетная печать**
   Без плагинов: слой фото → **CC Ball Action** (Grid Spacing 6–10, Ball Size 100–140, Twist 0) поверх Threshold-версии; или в Python: PIL, сетка кругов с радиусом по яркости, экспорт PNG. Затем Multiply на бумажную текстуру, Levels с белым ~235, чтобы не было чистого белого.

7. **Stop-motion из любой анимации**
   На прекомпозицию: **Posterize Time** 8 fps + на Position `wiggle(8,2)` с posterizeTime(8) (сдвиг «руки») + Turbulent Displace (Amount 6, Size 40, Evolution `posterizeTime(8); time*600`) — «кадр перекладки». Звук: щелчки и бумажный шелест на каждом шаге.

8. **Тайминг «с висом»** (Ordinary Folk, DIA): вместо Easy Ease 33/33
   Graph Editor, Speed Graph: Out influence 85–95%, In influence 5–15%. Объект резко срывается и долго «доезжает», или наоборот. Для сильного акцента — ключ «antic»: 3 кадра назад на 5–10% от движения, потом бросок за 4–6 кадров, затем **hold 8–20 кадров неподвижно**. Смаз-кадр: 1 кадр растянутой копии (Scale 140% по оси движения, Opacity 100%), никакого Motion Blur.

9. **Перелёт с затуханием** (пазлы Cleo Abram): выражение на Position/Scale
   ```
   n=numKeys; if(n>0){t=time-key(n).time; if(t>0&&t<1){v=velocityAtTime(key(n).time-.01); amp=.06; freq=3; decay=6; value+v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);}else value}else value
   ```
   У разных объектов разные `freq` (2.5–4) и задержки (2–5 кадров), чтобы не было синхронного «шаблона».

10. **Маркер по реальному документу** (Vox): скан или фото документа/скрина Multiply на бумагу; Solid жёлтый #F7E35A в режиме **Multiply**, маска-прямоугольник, ключи Mask Path слева направо за 8–12 кадров, края маски Roughen Edges Border 3. Слегка кривая линия, на 1–2° выше строки.

11. **Машинопись и мерцание шрифта**: Text Animator → Opacity 0 + Range Selector Start 0→100 (Based On Characters, ключи Linear), Hold-ключи по слогам речи. Добавить Animator → Position Y с Wiggly Selector (Max/Min ±1.5 px, Wiggles 6/s, posterize через Temporal Phase) — «неровная литера». Шрифты: моноширинные с характером (Courier Prime, IBM Plex Mono в немного «грязном» виде) или гротески с засечками — но **не капс-моно-лейблы** везде.

12. **Кинетическая типографика по DIA/Dumbar**: слово — это объект. Разрезать букву маской на 2–3 части и разводить их; растягивать трекинг (Tracking 0→200 за 4 кадра); менять кегль строки на ударном слоге (Scale 100→160% за 2 кадра, Hold 6, обратно). Текст **выходит за кадр** и обрезается краем 9:16. Шрифт крупный: 180–320 px по высоте кадра 1920, 2–4 слова на экране.

13. **Ризограф / трафаретная печать** (Nicolas Ménard): 2–3 «краски» (например, тёплый красный #E5452E, синий #2E4CB0, жёлто-охристый #E8B23A на бумаге #EFE8DA). Каждый цветовой слой в режиме **Multiply**, у каждого свой сдвиг на 2–4 px (приводка): `wiggle(2,1.5)` с posterizeTime(12). На слой Fractal Noise как Luma Matte для «недопечатки».

14. **Палитра против глянца** (Cleo Abram, Animade): фон не #000 и не градиент, а глухой цвет: тёмная хвоя #1F3A2E, коричневый #3B2A20, чернила #1E2433, бумага #EFE8DA. Один акцент, тёплый (томат, охра, изумруд). Levels на всё видео: Output Black 12–18, Output White 235–242, иначе «цифровая» белизна.

15. **Плёночный кадр: gate weave, мерцание, виньетка**: Adjustment Layer: Transform → Position `posterizeTime(24); [value[0]+random(-1.2,1.2), value[1]+random(-1.5,1.5)]`, Scale 102%. Exposure `posterizeTime(24); random(-0.04,0.04)` (флики). Виньетка: эллипс-маска Feather 600, Black Solid Multiply 25%. В ffmpeg: `crop=iw-8:ih-8:4+3*random(1):4+3*random(2),scale=1080:1920,vignette=PI/5,noise=alls=8:allf=t`.

16. **Фотокопия / ксерокс**: Black & White → Levels (жёсткий) → **Threshold** 120–150 → Roughen Edges Border 1–2 → Multiply на бумагу. Цикличный «переснимок»: каждые 3 кадра чуть менять Threshold (`posterizeTime(8); 135+random(-8,8)`).

17. **Ручная камера по графике (2.5D)**: AE-камера One-Node, Position: `wiggle(1.2, 12)` + на Z медленный наезд 3–5%. Графика — слои на разной Z-глубине (параллакс). Это заменяет «центрированный статичный» кадр.

18. **Монтаж «физическими» склейками вместо плавных переходов** (Animade, Neistat): hard cut на согласной, smash cut, J/L-cut голоса, whip-pan **снятый в камере**, перекрытие рукой, «кадр-вспышка» 2 кадра цветной плашки. Каждой склейке — свой звук: бумага, щелчок, «вжух» от рук, шаг. Музыки нет, поэтому фоли и есть ритм.

**Blender (бесплатно)**: Grease Pencil для покадровой дорисовки поверх импортированного видео (Video Editing / Reference). На F-кривых модификатор **Stepped Interpolation** (Step Size 2), чтобы 3D двигался «на двойках». Freestyle-контуры с Noise-модификатором толщины.
**Python**: PIL/numpy для генерации полутонов, ризо-сдвигов, бумажных «рваных» масок (Perlin-край); librosa/pydub — амплитуда голоса → JSON → выражение AE, по которому слова «прыгают» от голоса (замена Dumbar-музыке).

---

## Часть 3. 10 признаков «ИИ / шаблона» и человеческая альтернатива

| # | Признак ИИ-шаблона | Что делает человек |
|---|---|---|
| 1 | Каждый элемент входит через blur + scale 90→100% + fade | Появление за 1–3 кадра на Hold-ключах, «шлепком», вырезкой или рукой в кадре; разные входы для разных типов информации |
| 2 | Easy Ease 33/33 и одинаковая длительность 12–15 кадров у всего | Асимметричный тайминг (95/10), висы по 10–20 кадров, antic + бросок, разные скорости у соседних объектов |
| 3 | Всё по центру, симметричная композиция | Асимметрия, текст «прилипает» к краю и обрезается кадром, сетка из 2–3 колонок, графика рядом с лицом, а не поверх по центру |
| 4 | Скруглённые стеклянные карточки, blur-фон, мягкая тень | Бумажные вырезки, плашки с резким краем, жёсткая тень (Softness 0), стикерная обводка, скотч |
| 5 | Гладкие градиенты и идеально ровные векторы | Зерно в заливке, Roughen Edges, Wiggle Paths, сканы бумаги, недопечатка |
| 6 | 60 / 30 fps, идеально плавное движение | 24 fps, графика на 2s (12) или 8 fps для stop-motion, gate weave |
| 7 | Моно-капс подписи с трекингом как «UI-лейбл» везде | Крупный выразительный набор, рукопись, машинопись; 1–2 шрифта с характером; кегль меняется по смыслу |
| 8 | Чёрный фон + один неон / чистый белый #FFF | Глухие природные цвета, бумажный белый, ограниченная палитра 2–3 «краски» (риза, трафарет) |
| 9 | Плавные кросс-диссолвы и морфы между всеми сценами | Жёсткие склейки, smash cut, переходы в камере, match cut по форме (линия → график как у Ali Abdaal) |
| 10 | Звук «вжух» из библиотеки на каждом элементе или тишина | Фоли, записанное руками: бумага, маркер, клавиатура, телефон, дыхание; пауза как приём (Hayden Hillier-Smith) |

Бонус-признак: **нет следов процесса**. Живые работы показывают руку, стол, реальный телефон, ошибку (Winston Hacking оставляет ошибки специально). ИИ-монтаж всегда «стерилен».

---

## Часть 4. Четыре стилевых направления для вертикальных talking-head / продуктовых Reels

### Направление 1. «Редакционный коллаж / рабочий стол исследователя»
Вырезанное фото со стикерной обводкой, сканы документов, маркер, газетный полутон, бумажная подложка, камера едет по столу с распечатками. Говорящая голова — тоже вырезка поверх бумаги в части кадров. Звук: бумага, ножницы, маркер.
- Референсы: **Vox**, **Johnny Harris**, **Sam Ellis (Search Party)**, **Ariel Costa**, **Winston Hacking**.
- Подходит для: разборов, «почему так», исторических и религиозных контекстов (рукописи, карты, архив).

### Направление 2. «Ризо-плакат / кинетическая типографика»
2–3 печатные краски, огромный набор на весь кадр 9:16, слова режутся и разлетаются, сетка, надпечатка и сдвиг приводки. Шрифт двигается от амплитуды голоса. Лицо в кадре иногда как одноцветная плашка (Threshold + Multiply в одну краску).
- Референсы: **DIA Studio**, **Studio Dumbar/DEPT**, **Nicolas Ménard**, **Studio Moross**, **ManvsMachine** (кинетический тип в Affinity).
- Подходит для: тезисных роликов, хук-фраз, анонсов фич.

### Направление 3. «Рисованное поверх жизни» (draw-over, рука аниматора)
Живое видео остаётся главным. Поверх него покадровые линии на 2s, стрелки, обводки, маленькие персонажи-гэги, неровный штрих и «кипение». Интерфейс приложения показан на реальном телефоне в руке, рядом рисованные пометки, без стеклянных карточек.
- Референсы: **Golden Wolf**, **BUCK**, **Animade**, **Ordinary Folk** (тайминг), **Casey Neistat** (рукописные титры, переходы в камере).
- Подходит для: talking-head с объяснением, демо продукта, тёплый личный тон.

### Направление 4. «Тактильный предметный документ» (практика + тихий звук)
Один кадр, один объект, сплошной глухой фон, медленный темп, снятые руками переходы, плёночный кадр (зерно, gate weave, мягкая виньетка), минимум графики — только машинописные титры. Эмоцию держат пауза и фоли. Хорошо ложится на запрет музыки.
- Референсы: **Giant Ant** (трейлеры DOXA, Visa), **Allen Laseter** (книжная палитра, спокойный ритм), **Cleo Abram / Whitney Theis** (тёплая solarpunk-палитра, один ключевой визуал), **Hayden Hillier-Smith** (сдержанность), **Casey Neistat**.
- Подходит для: продуктового промо исламского приложения (предметы, руки, утро, свет), бренд-роликов.

---

## Источники
- [Creative Bloq: Texture, warmth and tactile rebellion — trends 2026](https://creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026)
- [Videobolt: Top Motion Graphics Trends 2026](https://blog.videobolt.net/post/top-motion-graphics-trends-2026)
- [Motionographer: Studio Stories — 12 years of Golden Wolf](https://motionographer.com/2025/05/12/studio-stories-12-years-of-golden-wolf/)
- [Motionographer: Blink my Brain (Ariel Costa)](https://motionographer.com/2016/08/29/blink-my-brain-continues-to-merge-old-guard-and-new-school/)
- [Motionographer: Step by Step — Allen Laseter](https://partners.motionographer.com/?p=67122)
- [Motionographer: Hybrid by birth — Animade](https://motionographer.com/2015/03/10/hybrid-by-birth-getting-to-know-animade/)
- [Motionographer: Catching up with Gunner](https://motionographer.com/2018/07/24/catching-up-with-gunner/)
- [Stash: ManvsMachine × Canva/Affinity](https://www.stashmedia.tv/?p=119582)
- [Stash: Ordinary Folk — Mainframe](https://www.stashmedia.tv/ordinary-folk-rescues-mainframe-motion-project-from-the-bin-of-destiny/)
- [Motion Array: Studio Spotlight — Giant Ant](https://blog.motionarray.com/learn/motion-design/studio-spotlight-giant-ant/)
- [Motion Array: Oddfellows spotlight](https://motionarray.com/blog/industry-spotlight-oddfellows)
- [It's Nice That: DIA](https://www.itsnicethat.com/features/dia-mitch-paone-meg-donohoe-graphic-design-animation-typography-180918)
- [Typeroom: Studio Dumbar kinetic type](https://www.typeroom.eu/from-north-sea-jazz-festival-to-amsterdam-sinfonietta-type-like-music-with-studio-dumbars-forward-thinking-kinetic-typographic-brilliance)
- [Skwigly: Nicolas Ménard](https://www.skwigly.co.uk/nicolas-menard/)
- [Winston Hacking — About](https://winstonhacking.substack.com/about)
- [Lesterbanks: Ben Marriott — paper cutout stop motion](https://lesterbanks.com/2020/02/an-easy-way-to-get-a-paper-cutout-stop-motion-look-in-ae/)
- [Lesterbanks: Ben Marriott — Roughen Edges grain](https://lesterbanks.com/2019/08/how-to-use-roughen-edges-for-animated-grain/)
- [Skillshare: Jake Bartlett — Texturing in AE](https://www.skillshare.com/en/classes/texturing-in-adobe-after-effects/1333636165)
- [Video Consortium: Cleo Abram](https://videoconsortium.org/mag/episode-8-cleo-abram)
- [RNDR: first edition (Cleo Abram)](https://rndr.beehiiv.com/p/rndr-firstever-edition) · [RNDR: 5 visuals](https://rndr.beehiiv.com/p/5-visuals-next-video)
- [aescripts: How Johnny Harris makes maps](https://aescripts.com/learn/how-johnny-harris-makes-maps/)
- [Musicbed: Hayden Hillier-Smith](https://www.musicbed.com/articles/?p=7556)
- [Artlist: Casey Neistat techniques](https://artlist.io/blog/editing-storytelling-techniques-casey-neistat/)
- [Cartoon Brew: Duolingo acquires Gunner](https://cartoonbrew.com/studios/duolingo-acquires-gunner-animation-studio-221889.html)
- [Stash: Ariel Costa joins Hornet](https://www.stashmedia.tv/ariel-costa-aka-blinkmybrain-joins-hornet-directing-roster)
- [MOO: Aries Moross](https://www.moo.com/blog/interviews/aries-moross-on-design-with-a-difference)
- [Sostav: лучший креатив весны по версии Behance](https://www.sostav.ru/publication/luchshij-kreativ-vesny-po-versii-behance-16826.html)
- [Wikipedia: Felix Colgrave](https://en.wikipedia.org/wiki/Felix_Colgrave)
