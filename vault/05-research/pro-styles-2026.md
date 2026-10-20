---
title: pro-styles-2026
type: research
tags: [research, system-v2]
summary: Полный ресерч 2026-10-19 для системы монтажа v2 (источник для 07-system)
updated: 2026-10-19
source: веб-ресерч + браузер ПК, тред «аудит монтажа»
---
# Профессиональные стили монтажа и моушена для вертикальных Reels (9:16), 2024–2026

Для кого: русскоязычный автор, объясняющий AI/tech в формате «говорящая голова», финтех-бренд PERSET, промо исламского приложения.
Ограничение: **без музыки**, только голос и SFX/фоли.

Пометки: **[src]** означает, что пункт подтверждён источником (URL указан рядом). **[практика]** означает общепринятую индустриальную практику и мои рабочие цифры. Их стоит проверить на своём материале.

---

## 0. Короткий диагноз текущего монтажа

Почти каждый элемент текущего монтажа совпадает с «дефолтами», от которых профессионалы ушли:

- Капс-субтитры с одним красным словом. Это вариация Hormozi-captions. Сам Hormozi от них уже отказался, а на Fiverr 2500+ продавцов предлагают этот стиль. Креативный директор Starter Story Марко Бенни говорит, что пролистывает такие ролики сразу. [src: https://videobuilders.beehiiv.com/p/hormozi-captions]
- Событие каждые 0,5 с. Ретеншн-аналитики прямо называют бесконечные зумы, вуши и склейки утомляющими. Если переход не двигает историю, это шум. [src: https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8]
- Сгенерированные woosh/pop на каждый титр. Там же: «When every subtitle pops, the video feels over-processed».
- UI-карточки по центру на тёмном фоне, «Tron»-палитра. Клео Абрам (ex-Vox, Huge If True) сознательно уходит от серо-чёрно-неонового «Tron»-лука техношоу к тёмно-коричневым, зелёным и синим тонам. [src: https://videoconsortium.org/mag/episode-8-cleo-abram]
- REC-HUD и прочий декор без смысла. Принцип Apple: «одна мысль = один кадр», убирать лишние фоны, глоу и наслоения. [src: https://youmind.com/landing/x-viral-articles/apple-product-video-design-secrets]

---

## 1. Стили (13 штук)

### 1. «Documentary Explainer» (семейство Johnny Harris / Vox / Cleo Abram)
**Примеры:** Johnny Harris (YouTube, карты в GEOlayers), Vox (Joss Fong), Cleo Abram «Huge If True».
- Карты: https://aescripts.com/learn/how-johnny-harris-makes-maps/ , https://aescripts.com/learn/making-maps-for-johnny-harris---volcanoes/
- Процесс Vox: https://www.theopennotebook.com/2020/01/07/videogram-how-a-vox-video-explains-the-science-behind-the-first-photo-of-a-black-hole/

**Почему выглядит дорого и по-человечески:**
- Каждый визуал является **доказательством**: скрин статьи, график, архивный кадр, карта. Это не декорация. Клео начинает с вопроса «какой ключевой визуал делает это видео, а не текст?» и пишет сценарий в три колонки: уши / глаза / источники. [src: videoconsortium]
- Фактура: зерно, бумага, film burn, light leaks, виньетка через размытую копию с инвертированной маской. Источник прямо пишет, что фактура играет «огромную роль». [src: https://blog.motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/]
- Отложенное раскрытие. Vox показывает сначала, как трудно было получить фото чёрной дыры, и только потом само фото. После главных мыслей оставлены паузы, чтобы зритель успел осознать. [src: theopennotebook]
- **Шрифты (кириллица):** для заголовков и «газетных» вставок PT Serif, Literata, EB Garamond, Spectral. Для подписей и лейблов карт Inter / Inter Tight, IBM Plex Sans, а для чисел и дат IBM Plex Mono.
- **Грейд:** тёплый, слегка ненасыщенный, приподнятые чёрные, зерно 3–6 % [практика].

**Ритм:**
- Монтажная фраза с «match cut on text»: 12+ скринов, где ключевая фраза выровнена по центру по линейкам. Клипы начинаются с ~8 кадров и укорачиваются к концу. На каждую склейку щелчок затвора. [src: motionarray]
- Остальное время смена плана каждые 2–5 с. В горячих точках короткие очереди [практика].

**Переходы и движение:**
- Фото «въезжает» со смягчённым торможением (кривая в Graph Editor) и одновременно размытие уходит с ~50 до 0. [src: motionarray]
- Выделение маркером в скрине статьи, маска-ревил по строке.
- Плавный 3D-пролёт виртуальной камеры над картой. Vox советует, чтобы движения камеры в Google Earth Studio были «не слишком безумными». [src: theopennotebook]

**Звук без музыки:**
- Щелчок затвора или проектора на ревил фото [src: motionarray]. Шорох бумаги, маркер по бумаге, клавиатура.
- Room tone под всей сценой. Тишина перед ревилом вместо «бума».

**Сборка в AE:**
- GEOlayers 3 для карт.
- Скриншоты статей открываются в браузере, затем 3D-слой + камера с Depth of Field. Выделение через Shape-маркер с Trim Paths.
- Фактуры: overlay-слой бумаги в режиме Multiply / Overlay. Зерно: Add Grain или FilmConvert.
- Нужна реальная фактура: настоящие скрины, документы, фото автора с телефона и **свой B-roll**.

**Наши форматы:** AI/tech explainer (идеально), финтех (регуляторика, курсы, «как устроена комиссия»).

**Чем убить стиль:** фейковые «газетные» вырезки, сгенерированные ИИ. Одинаковая бумажная текстура на каждом кадре. Карта ради карты.

---

### 2. «Clean Talking Head + Margin Captions» (семейство Ali Abdaal)
**Пример:** Ali Abdaal, разбор: https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/

**Почему выглядит премиально:**
- Субтитры **не по центру внизу**. Это фраза за фразой, колонкой сбоку от спикера, в sentence case, белым, с одним акцентным цветом (жёлтым) на ключевых словах. Без обводки и тени. [src: choppity]
- Спикер смещён от центра, чтобы оставить место для текста. Средний план с руками. Ровный мягкий свет, чистый серый фон. [src: choppity]
- Грейд почти монохромный, единственный акцент повторяет цвет предмета в кадре (наушники). [src: choppity]
- **Шрифты:** вместо рукописного кириллического лучше чистый гротеск с характером: Onest, Golos Text, Manrope. Рукописный вариант: Caveat, Shantell Sans (оба поддерживают кириллицу). [src: https://astastudio.substack.com/p/8-cyrillic-fonts-are-pro-open-source-flawless]

**Ритм:** план держится 2–5 с, склейки ложатся на смену мысли, джамп-катов меньше, чем у Hormozi. Хук строится как вопрос или рефрейм, а не шок. [src: choppity]

**Движение:** текстовые блоки появляются с короткой ease-out, без overshoot. Зум 100→108 % на смене мысли. Резкие зумы не используются.

**Звук без музыки:** чистый голос и тихий room tone. Мягкий «тик» бумаги максимум на 1 из 4 появлений текста. Остальное идёт в тишине.

**AE/Premiere:**
- Essential Graphics: шаблон колонки текста с якорем, отслеженным за плечом спикера. Mocha или трекер для лёгкой привязки.
- Hue/Saturation с маской на акцентный предмет.
- Съёмка: 2 источника света, фон в 1,5–2 м от спикера.

**Наши форматы:** talking head explainer, исламское приложение (спокойный, доверительный тон).

**Чем убить стиль:** анимировать каждое слово. Использовать больше одного акцентного цвета. Ставить текст поверх лица.

---

### 3. «Apple Restraint / Product Minimal»
**Примеры:** продуктовые ролики и кейноуты Apple. Разборы: https://youmind.com/landing/x-viral-articles/apple-product-video-design-secrets , https://9to5mac.com/2023/06/21/apple-keynote-videos-transitions-and-editing/

**Почему выглядит дорого:**
- «One shot = one idea». Убраны лишние фоны, глоу и наложенные эффекты, пустота используется как элемент дизайна. Фон чисто чёрный или белый, единственный громкий цвет принадлежит продукту или UI. Максимум 2 гарнитуры из брендсистемы, одни правила для титров, UI и дисклеймеров. Склейки почти невидимы, кричащих переходов нет. [src: youmind]
- Бесшовные переходы, которые трудно заметить без покадрового просмотра. Пример: через крупный план камеры iPhone в общий план Apple Park. [src: 9to5mac]
- **Шрифты (кириллица, аналоги SF Pro):** Inter / Inter Display, Golos UI, Onest. Из платных: TT Interphases Pro, Helvetica Now Display (есть кириллица). [src: https://typetype.org/de/blog/20-best-cyrillic-fonts-of-2025/]

**Ритм:** длинные холды 1,5–3 с на одном объекте. Типографика появляется словом или строкой и **держится** [практика].

**Движение [практика]:**
- Easing в духе Apple: быстрый старт и очень долгий хвост, примерно cubic-bezier(0.2, 0, 0, 1) / expo-out, длительность 18–30 кадров при 30 fps. Overshoot отсутствует.
- Масштаб текста 96→100 % вместе с opacity и лёгким размытием 8→0 px.
- Motion blur включён (180° shutter).

**Звук без музыки:** «механический» фоли самого объекта: клик кнопки, тап по стеклу, мягкий щелчок магнита. Тишина между событиями. SFX тихие и редкие. [src: youmind]

**AE:** 3D-слои + камера с DOF. Мокапы экранов через Corner Pin или CC Power Pin на реальное видео телефона в руке. Плагин Flow / Motion для кривых. Нужна макросъёмка реального телефона с приложением PERSET или исламским приложением.

**Наши форматы:** продуктовые демо PERSET и исламского приложения, финтех.

**Чем убить стиль:** градиентный фон «как у Apple», сделанный из шаблона. Неоновое свечение. Текст по центру на каждом кадре.

---

### 4. «Screen-Studio Product Demo» (кинематографичная запись экрана)
**Пример:** Screen Studio, тренд SaaS-демо 2024–2026. Разбор: https://daveswift.com/screen-studio/

**Почему выглядит дорого:**
- Зум на точку клика и плавный выезд обратно. Камера «скользит», пока приближена. Курсор сглажен физикой (tension / friction / mass) и поворачивается при движении. Motion blur включён по умолчанию для курсора, зумов и панорам. [src: daveswift]
- Окно «плавает» на фоне: паддинг, скругление, тень. Вебкамера уменьшается до 70 % во время зума. [src: daveswift]

**Ритм:** 1 действие = 1 зум. Между действиями 0,4–0,8 с покоя [практика].

**AE [практика]:**
- Запись экрана в высоком разрешении. Нужна реальная запись телефона в 1290×2796 и выше.
- Зум на null-объекте с expo-ease. CC Force Motion Blur или Pixel Motion Blur.
- Курсор/тап: свой слой «пальца» (круг 60 px, opacity 30 %) с ripple на тапе, 8–10 кадров.
- Альтернатива: снимать в Screen Studio или Rotato и докомпоновывать в AE.

**Звук:** реальные тапы и тактильные щелчки iOS, свайп ткани/бумаги на скролле. Сгенерированные «поп» не используются.

**Наши форматы:** демо приложений, онбординг PERSET.

**Чем убить стиль:** зум на каждый тап подряд, отчего возникает морская болезнь. Фон «по умолчанию» Screen Studio, который узнают все.

---

### 5. «Editorial Grid / Swiss Kinetic Type»
**Примеры:** тренд «systematic grids and typographic tension» 2025 (https://abduzeedo.com/design-trends-2025-systematic-grids-and-typographic-tension), Swiss в моушене (https://wearefevr.com/the-influence-of-swiss-design). Айдентики Collins, DixonBaxi, Koto работают в той же логике сеток.

**Почему выглядит дорого:**
- Видимая модульная сетка, резкий контраст масштаба (огромный заголовок против мелкого текста), сильная базовая линия, асимметричный баланс. Элементы движутся по осям сетки. [src: abduzeedo, fevr]
- Сплошные чёрные блоки против белого. Пары вроде тёмно-синий + оранжевый. Бумажная фактура как тактильный контраст. [src: abduzeedo]
- **Шрифты (кириллица):** Inter Tight, Sofia Sans (включая Condensed), Golos, TT Hoves Pro, TT Norms Pro, Suisse Int'l (есть кириллица), Helvetica Now. Для узких и плотных акцентов Oswald (кириллица с 2023), Sofia Sans Extra Condensed. Акцидентный экспрессивный: Unbounded.

**Ритм:** типографические «удары» на смысловые слова, 1–2 в 3–4 с. Остальное время сетка держит кадр [практика].

**Движение [практика]:**
- Маски-ревилы строк снизу вверх по базовой линии, ease-out 10–14 кадров, задержка между строками 2–3 кадра.
- Сетка «перестраивается»: блоки сдвигаются, не исчезая.
- Без overshoot, без motion blur на тексте, либо очень лёгкий.

**Звук:** сухие механические щелчки (тумблер, степлер, печатная машинка на ревиле строки). Тишина между ними.

**AE:**
- Guides / Grid Overlay (Ctrl+'), rulers.
- Text Animator: Range Selector по строкам (Animate → Position Y + Opacity), а не Transform. [src: https://www.premiumbeat.com/blog/10-after-effects-mistakes-avoid]
- Матовые маски через Track Matte.
- Talking head снят с запасом пространства (camera wide, 4K), чтобы кадрировать спикера в ячейку сетки.

**Наши форматы:** финтех PERSET (цифры, ставки, сравнение), AI-новости.

**Чем убить стиль:** «свисс» без реальной сетки, то есть элементы на глаз. Слишком много шрифтов. Типографика поверх каждого предложения.

---

### 6. «Brand Type-as-Form» (Spotify Wrapped)
**Пример:** Spotify Wrapped 2024. Разбор: https://alexjimenezdesign.substack.com/p/three-design-elements-that-made-spotify . Инженерия: https://engineering.atspotify.com/2024/1/exploring-the-animation-landscape-of-2023-wrapped

**Почему выглядит дорого:**
- Цифры и буквы трактуются как формы: увеличены, залиты градиентом, размножены в паттерны. Текст всегда стоит на плоском цвете, градиенты остаются только числам. Палитра ограничена и контрастна. Варьируется сжатое начертание. 2024 год сдержаннее по анимации, чем 2022–2023. [src: substack]
- Данные управляют цветом и движением (Audio Aura, Sound Town). [src: Spotify Engineering]

**Ритм:** панель-интро, затем простой текстовый слайд, затем финальный «шер»-лейаут [src: substack]. Для Reels: 1 число = 1 экран, холд 1,2–2 с.

**Движение [практика]:** масштаб числа с лёгким overshoot (5–8 %) только на «герое» и паттерн-повторы с offset по времени. Шрифты: Unbounded, Sofia Sans Condensed. Druk (Commercial Type) поддерживает кириллицу; если её нет в вашей лицензии, используйте Oswald.

**Звук:** «механика» счётчика (табло), один тяжёлый удар на итоговую цифру.

**AE:** Text → Source Text expression для счётчика (`Math.round(linear(time, t0, t1, 0, 1250000))` + форматирование разрядов). Repeater в shape-слоях для паттернов. Gradient Ramp только на цифры.

**Наши форматы:** финтех (итоги, проценты, кэшбэк), годовые отчёты приложения.

**Чем убить стиль:** кислотные градиенты под текстом (нечитаемо). Overshoot на всём подряд.

---

### 7. «Tactile Collage / Paper Cut-out on Twos»
**Примеры:** Vox-коллаж, тренд «torn paper / analog textures / reduced frame rates» в прогнозах 2026 (https://blog.videobolt.net/post/top-motion-graphics-trends-2026). Методика stop-motion в AE: https://motionarray.com/learn/after-effects/stop-motion-style-animation-in-after-effects/ , https://lesterbanks.com/2020/02/an-easy-way-to-get-a-paper-cutout-stop-motion-look-in-ae/

**Почему выглядит по-человечески:**
- Рваные края, бумажные волокна, пыль. Сниженный фреймрейт даёт «рубленое» тактильное ощущение, сборка идёт кусочками. [src: videobolt]
- Видна рука и несовершенство. Это прямой ответ на «AI-лоск», и прогноз 2026 так и называется: «Crafted Content Stands Out in the Age of AI Rush». [src: videobolt]
- **Шрифты:** вырезанные буквы из реальных фото газет. Для набранного текста PT Serif / EB Garamond + Courier Prime (кириллица есть). Проверять!

**Ритм и движение:**
- Анимация **on twos / threes**: Posterize Time 12 или 8 fps внутри 30 fps композиции. Лёгкий «бойл» позиции и поворота (wiggle с низкой частотой, тоже на постеризованном времени). [src: motionarray]
- Motion blur выключен: на «двойках» он выдаёт цифровое происхождение.

**Звук:** реальные записанные звуки: рвётся бумага, ножницы, скотч, щелчок степлера. Каждый звук разный: записывайте 10–20 дублей и рандомизируйте.

**AE:**
- Сканы или фото настоящей бумаги (бумага, крафт, газета). Рваные края делаются вручную или из фото.
- Drop Shadow с маленьким distance, Turbulent Displace на краях. Posterize Time на adjustment-слое.
- Выражение для бойла на позиции: `posterizeTime(8); wiggle(8,2)`.
- Нужны реальные фото и вырезки. Отлично работает с фото автора.

**Наши форматы:** AI-объяснения («история технологии»), исламское приложение (тёплые, ремесленные текстуры, без изображений живых существ, если важно для аудитории).

**Чем убить стиль:** шаблонные «torn paper» паки с одинаковыми краями. Постеризация на голове спикера.

---

### 8. «Flat Vector Explainer» (семейство Kurzgesagt)
**Пример:** Kurzgesagt. Процесс: https://kurzgesagt.org/youtube/ ; курс: https://www.skillshare.com/en/classes/Motion-Graphics-with-Kurzgesagt-%E2%80%93-Part-1/631970755

**Почему выглядит дорого:**
- Векторная иллюстрация с поддержкой из пиксельных иллюстраций и инфографики, плоское 2D с 3D-элементами. Аниматоры работают вручную, **тайминг задаёт озвучка**. Факты собраны в историю, сценарий проходит около дюжины драфтов. SFX создаются вместе с саундтреком (Epic Mountain). [src: kurzgesagt.org]
- [практика] Строгая палитра (5–7 цветов на сцену), мягкие градиентные тени, «персонажи-символы».

**Ритм:** вторичная анимация: всё в кадре слегка дышит, фон медленно параллаксит. Главное действие на слове VO.

**Движение [практика]:** overshoot 10–15 % на появлении иконок (bounce-expression или Ease and Wizz «Back»). Squash & stretch на 2–3 кадра. 24/30 fps on ones.

**Звук без музыки:** «мультяшный», но **сделанный под каждое действие** фоли: пузырьки, мягкие клики, атмосферные пэды-эмбиенты (это не музыка, а атмосфера: шум космоса, гул машины).

**AE:** Illustrator → AE (Overlord или нативный импорт), shape-слои, Duik / Joysticks 'n Sliders для персонажей. Ручной кейфрейминг, никаких пресетов. Реальный футаж не нужен, нужен иллюстратор.

**Наши форматы:** voice-over-графика (объяснение, как работает нейросеть, ипотека, закят).

**Чем убить стиль:** стоковые векторные персонажи. Одинаковый bounce у всех элементов. Слишком медленная для Reels экспозиция.

---

### 9. «Cinematic Mixed-Media 3D» (ManvsMachine / Buck / Ordinary Folk)
**Примеры:** ManvsMachine: Nike Air Max Day (3D-«кинетические машины», «индустриальный минимализм + кинетический балет», отдельная палитра на каждый эпизод), гибрид механических риг и лайв-экшна. https://motionarray.com/learn/motion-design/studio-spotlight-manvsmachine/ ; портфолио: https://www.watchthetitles.com/studio/manvsmachine . Buck: https://motionographer.com/2009/05/20/buck-dews-it-again/ . Ordinary Folk: https://schoolofmotion.com/podcast/ordinary-folk-interview

**Почему выглядит дорого:**
- Физика материалов, крупные планы, свет. Монтаж привязан к звуку так, что визуал и аудио ощущаются единым целым. [src: motionarray ManvsMachine]
- Гибрид 2D и 3D, стекло и дисперсия входят в топ трендов 2026. [src: videobolt]

**Ритм:** 0,8–1,5 с на «механическое» действие, кадр строится как loop [практика].

**Движение [практика]:** Ease-in-out с длинными плато и симуляции. Нет motion blur только тогда, когда это сознательный приём.

**Звук без музыки:** это сильнейший стиль для запрета музыки. Ритм создают **механические фоли** (шестерни, щелчки, пневматика, металл по стеклу). Звук становится «саундтреком».

**Пайплайн:** Cinema 4D + Redshift/Octane/Arnold, Houdini для сложного, композ в AE/Nuke. [src: motionarray] Для нас практичнее Blender + AE: 3D-монета или карта PERSET как механизм.

**Наши форматы:** имиджевые финтех-ролики, заставки серии, продукт PERSET.

**Чем убить стиль:** стоковые 3D-ассеты, «глянцевый пластик» по умолчанию, отсутствие звука механики.

---

### 10. «Analog Hand-Drawn Annotation» (рукописная разметка поверх видео)
**Примеры:** тренд «hand-drawn visuals: loose strokes, uneven outlines, frame-by-frame» (https://blog.videobolt.net/post/top-motion-graphics-trends-2026). Рукописные пометки в духе Ali Abdaal и Veritasium.

**Почему выглядит по-человечески:** неровный штрих, обводка от руки вокруг важного места на скрине или в кадре, стрелка, подчёркивание. Это сигнал «тут работал человек».

**Движение:**
- Обводка Trim Paths за 6–10 кадров с ease-out на shape-слое (не Stroke effect). [src: premiumbeat]
- Затем постеризованный бойл линии (Turbulent Displace с `posterizeTime(8)` на evolution).

**Звук:** маркер по бумаге или по доске, записанный вживую.

**Сборка:** рисовать на iPad (Procreate) поверх кадров или в AE пером + Roughen Edges. Нужно реальное видео или скрины, на которых есть что выделять.

**Наши форматы:** talking head + скрины AI-интерфейсов, финтех-договоры («мелкий шрифт»).

**Чем убить стиль:** векторная «идеальная» стрелка из пака. Обводка на каждом предложении.

---

### 11. «Depth-Layered Talking Head» (текст за спикером, рото)
**Пример:** повсеместный тренд Reels 2024–2026: заголовок стоит за головой спикера. Техника: https://www.adobe.com/learn/after-effects/web/rotoscope-subject , https://www.premiumbeat.com/blog/rotobrush-after-effects-tutorial

**Почему выглядит дорого (если сделано честно):** глубина кадра, текст живёт в пространстве комнаты, а не стикером сверху. Крупный, жирный, 1–3 слова.

**Шрифты:** Unbounded, Geologica, Inter Tight Black, TT Norms Pro ExtraBold. Для финтеха лучше узкий: Sofia Sans Condensed.

**Ритм:** 1 раз на ролик, в хуке или на «главном тезисе». Не чаще.

**AE:** Roto Brush 3 (AI) + Refine Edge на волосах. Текст между фоновой плитой и маской спикера. 3D Camera Tracker, чтобы текст «прилип» к стене при движении камеры. Нужен спикер на фоне с отступом 1,5+ м и **ручная камера с лёгким движением**: на статике эффект выглядит как наклейка.

**Звук:** глухой низкий «вес» (sub-удар −30…−20 dB) на появлении. Без вуша.

**Наши форматы:** talking head explainer.

**Чем убить стиль:** «текст за головой» в каждом ролике, мерцающий роу-край волос, статичная камера.

---

### 12. «Lo-fi Authentic / Creator-native»
**Примеры:** нативные Reels, снятые на телефон. Клео Абрам для TikTok перезаписывает прямые обращения на телефон, переиспользует свои анимации и архив. Каждый шорт сам по себе, ~60 с на одну мысль, а тизеры «смотри на YouTube» работали хуже. [src: videoconsortium]. Фраза MrBeast: «This is not Hollywood and I do not want to be Hollywood… I'm not fake». [src: https://www.tubefilter.com/2024/09/17/mrbeast-internal-production-guide-leaked-key-points/]

**Почему работает:** реальная локация, естественный свет, оговорки оставлены (выбрасываются только паузы-«эээ»). Субтитры нативные или минималистичные. Видеорядом служат собственные кадры телефона, а не сток.

**Ритм:** на говорящей голове 3–6 с без склейки, если мысль сильная. Дыхание оставлено.

**Звук:** живая акустика комнаты, реальные звуки локации (улица, кафе) как фактура.

**AE/Premiere:** минимум: цветокор (скоупы!), шумодав голоса, лёгкая стабилизация. Графика только «служебная» (имя, цифра, источник).

**Наши форматы:** AI/tech мнение, исламское приложение (доверие, «от себя»).

**Чем убить стиль:** прятать «lo-fi» под фильтр VHS. Фейковая «небрежность».

---

### 13. «Data-Journalism Chart Motion» (финтех-графики)
**Примеры:** графики Vox и Johnny Harris, Bloomberg Originals, The Economist (стандарты дата-визуализации).

**Почему выглядит дорого:**
- Один график = одна мысль.
- Ось и подпись появляются раньше данных. Линия «рисуется» по времени, ключевая точка подсвечивается акцентом, всё остальное серое.
- Источник указан мелким шрифтом в углу. Сам Vox ставит лейбл объекта ровно в момент его появления. [src: theopennotebook]

**Шрифты:** IBM Plex Sans + IBM Plex Mono (табличные цифры), Inter с `tnum`, Golos. Цифры только моноширинные или табличные, чтобы не «прыгали» на счётчике.

**Ритм:** холд 2–3 с после того, как линия дошла (зритель должен прочитать).

**Движение:** Trim Paths на линии, ease-in-out 20–40 кадров. Камера медленно наезжает на ключевую точку.

**Звук:** тихий «тик» на каждой подписи оси (−30 dB), один акцентный щелчок на ключевой точке. Без ударов.

**AE:** данные из CSV (Data-driven animation: импорт .csv/.json в AE, expressions `footage("data.csv").dataValue([col,row])`). Плагин Datamatic или ручная сборка shape-слоев.

**Наши форматы:** PERSET (ставки, инфляция, сравнение тарифов), AI-рынки.

**Чем убить стиль:** 3D-диаграммы, неоновые бары, график без источника.

---

## 2. Звуковой дизайн без музыки: общая система

1. **Room tone под всем роликом**, без провалов в цифровую тишину: провалы делают паузы заметными и «постановочными». Один тон на локацию, кроссфейды на стыках. Проверка: выключите тон, и если стало «пусто», уровень верный. [src: https://www.tunepocket.com/how-to-make-your-video-sound-professional-without-adding-music/]
2. **Тишина — это инструмент, а не дефолт.** Тихий бит перед ударом делает удар сильнее. Чтобы тишина не была «пустой», нужны суб-слой 30–80 Hz ниже −35 dB, отфильтрованный room tone около −30 dB, микро-транзиенты −40…−30 dB на склейках и кроссфейды 5–20 ms против щелчков. [src: https://krotos.studio/blog/no-sound-in-sound-design]
3. **Молчание перед ревилом эффективнее SFX.** [src: air.io]
4. **Фоли под видимое действие, немного на сцену**: ткань, стул, клавиатура. [src: tunepocket]
5. **Только реальные записи, с вариациями.** Записать 10–20 дублей каждого звука (бумага, клик, тап) и никогда не ставить один и тот же файл дважды подряд [практика].
6. **Иерархия громкости [практика]:** голос −14…−16 LUFS интеграл (Reels нормализует ~−14), SFX на 12–20 dB тише голоса, акцентный удар не громче голоса.
7. **Пэды атмосферы — это не музыка.** Гул города, шум зала, ветер, механизмы могут держать эмоцию без нот.

---

## 3. Ключевые технические принципы моушена (сквозные)

- **Никаких линейных ключей.** Только Easy Ease или кастомные кривые, motion blur на движущихся объектах (кроме стилей on twos). Перемещать через Align, анимировать текст через Animate-меню, обводки через Trim Paths. [src: https://www.premiumbeat.com/blog/10-after-effects-mistakes-avoid]
- **Одна система кривых на бренд [практика]:**
  - PERSET (финтех, доверие): expo-out, без overshoot, 12–18 кадров.
  - Исламское приложение: мягкий sine in-out, 18–24 кадра, без «пружин».
  - AI-explainer: допустим лёгкий overshoot 5 % на одном типе элемента.
- **Фреймрейт:** 30 fps (или 25 под русский эфирный стандарт, если снимаете в 25). Коллаж и рукописное делаются on twos (Posterize 12/15) и не смешиваются с on ones в одном кадре.
- **Шрифты с кириллицей (проверены):**
  - Бесплатные: Inter / Inter Tight, Onest, Golos Text/UI, Manrope, Unbounded, Geologica, Montserrat, Oswald, Fira Sans, Sofia Sans, IBM Plex Sans/Mono, PT Serif, EB Garamond, Literata, Caveat, Shantell Sans.
  - Платные: TT Norms Pro, TT Commons Pro, TT Hoves Pro, TT Interphases Pro, Helvetica Now, Suisse Int'l.
  - Для исламского приложения добавить арабский: Noto Naskh Arabic, Amiri, IBM Plex Sans Arabic.
  - [src: astastudio, typetype]

---

## 4. Чем профессиональный монтаж отличается от «AI-generic» (15 проверяемых признаков)

| # | AI-generic | Pro | Проверка / источник |
|---|---|---|---|
| 1 | Событие каждые 0,5 с, всегда | Ритм меняется: плотные очереди 5–10 склеек, затем спокойные участки, и так периодически | В таймлайне есть участки ≥3 с без графики? [air.io] |
| 2 | SFX на каждый титр | SFX только на ключевые моменты, тихие | Посчитать SFX на 10 с: обычно не больше 2 [youmind; air.io] |
| 3 | Сгенерированные вуши/попы, один файл повторяется | Реальные записи, вариации, room tone под всем | Нет одинаковых волн подряд; нет цифровой тишины [tunepocket] |
| 4 | Капс, слово-за-словом, красное слово | Фраза-за-фразой, sentence case, один акцентный цвет, место сбоку | [videobuilders; choppity] |
| 5 | Графика — декор (HUD, рамки) | Графика — доказательство (скрин, источник, данные) | Каждый графический элемент отвечает на вопрос «что это доказывает?» [videoconsortium; theopennotebook] |
| 6 | Всё по центру | Композиция по сетке и асимметрии, спикер смещён | Наложить сетку 4×8, элементы на линиях [abduzeedo; choppity] |
| 7 | Линейные или пресетные одинаковые движения | Кастомные кривые, motion blur, своя easing-система бренда | Graph Editor: нет прямых линий [premiumbeat] |
| 8 | Тёмный фон + неон «Tron» | Продуманная палитра: тёплые тёмные, один акцент | [videoconsortium] |
| 9 | Нет пауз после важных мыслей | Паузы-«выдохи» после ключевых тезисов | Есть 0,5–1 с тишины после пунчлайна [theopennotebook] |
| 10 | Сразу показать главное | Отложенное раскрытие: сначала контекст или сложность, потом ответ | [theopennotebook] |
| 11 | Переходы ради переходов | Переход маркирует смену сцены, главное откровение или эмоциональный пик | [air.io] |
| 12 | Склейки на середине слова или жеста | Склейки на смене мысли, на дыхании | [air.io; choppity] |
| 13 | Сток и ИИ-картинки | Свой B-roll, реальные документы, руки, телефон | [videoconsortium; tubefilter] |
| 14 | Много шрифтов и стилей | 1–2 гарнитуры, одни правила для всех титров | [youmind] |
| 15 | Нет фактуры, «вакуумная» чистота | Зерно, бумага, оптические несовершенства, реальный свет | [motionarray; videobolt] |
| 16 | Одинаковая подача на все платформы и тизеры | Нативный формат: одна мысль за ~60 с, самостоятельный шорт | [videoconsortium] |
| 17 | Цвет на глаз | Цвет по скоупам, проверка на телефоне | [premiumbeat] |

---

## 5. Рекомендуемая система для трёх продуктов

- **AI/tech talking head:** база из стиля 2 (Clean Talking Head + Margin Captions), доказательства из стиля 1 (Documentary), разметка из стиля 10 (Annotation), 1 акцент стиля 11 (Depth-Layered) на ролик.
- **PERSET (финтех):** стиль 5 (Editorial Grid) + стиль 13 (Chart Motion) + стиль 3 (Apple Restraint) для продукта, иногда стиль 9 (Cinematic 3D) для имиджа. Палитра: тёмно-синий + один тёплый акцент. Шрифты Inter Tight / TT Norms Pro + IBM Plex Mono для цифр.
- **Исламское приложение:** стиль 12 (Lo-fi Authentic) + стиль 3 (Apple Restraint) для экранов приложения + стиль 7 (Tactile Collage) с орнаментальной фактурой. Мягкие sine-кривые, тишина и живые звуки (страницы, чётки, шаги в мечети при наличии разрешения). Арабский шрифт Amiri или Noto Naskh.

---

## Источники
- https://blog.motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/
- https://aescripts.com/learn/how-johnny-harris-makes-maps/
- https://aescripts.com/learn/making-maps-for-johnny-harris---volcanoes/
- https://www.theopennotebook.com/2020/01/07/videogram-how-a-vox-video-explains-the-science-behind-the-first-photo-of-a-black-hole/
- https://videoconsortium.org/mag/episode-8-cleo-abram
- https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/
- https://videobuilders.beehiiv.com/p/hormozi-captions
- https://youmind.com/landing/x-viral-articles/apple-product-video-design-secrets
- https://9to5mac.com/2023/06/21/apple-keynote-videos-transitions-and-editing/
- https://daveswift.com/screen-studio/
- https://abduzeedo.com/design-trends-2025-systematic-grids-and-typographic-tension
- https://wearefevr.com/the-influence-of-swiss-design
- https://alexjimenezdesign.substack.com/p/three-design-elements-that-made-spotify
- https://engineering.atspotify.com/2024/1/exploring-the-animation-landscape-of-2023-wrapped
- https://blog.videobolt.net/post/top-motion-graphics-trends-2026
- https://motionarray.com/learn/after-effects/stop-motion-style-animation-in-after-effects/
- https://lesterbanks.com/2020/02/an-easy-way-to-get-a-paper-cutout-stop-motion-look-in-ae/
- https://kurzgesagt.org/youtube/
- https://motionarray.com/learn/motion-design/studio-spotlight-manvsmachine/
- https://www.watchthetitles.com/studio/manvsmachine
- https://schoolofmotion.com/podcast/ordinary-folk-interview
- https://partners.motionographer.com/?p=82945
- https://www.adobe.com/learn/after-effects/web/rotoscope-subject
- https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8
- https://www.tunepocket.com/how-to-make-your-video-sound-professional-without-adding-music/
- https://krotos.studio/blog/no-sound-in-sound-design
- https://www.premiumbeat.com/blog/10-after-effects-mistakes-avoid
- https://www.tubefilter.com/2024/09/17/mrbeast-internal-production-guide-leaked-key-points/
- https://astastudio.substack.com/p/8-cyrillic-fonts-are-pro-open-source-flawless
- https://typetype.org/de/blog/20-best-cyrillic-fonts-of-2025/

**Ограничения исследования:** Pinterest и Behance не открывались напрямую, использованы статьи-описания. Страницы Ordinary Folk и Buck не дали технических деталей (интервью в видео/подкасте). Цифры easing и громкости с пометкой [практика] — рабочие ориентиры, а не цитаты.
