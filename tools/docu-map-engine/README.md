# docu-map-engine

Python-движок «документального моушена на карте» (ролики без человека). Рецепт и правила: `vault/03-techniques/docu-map-motion.md`. Первый ролик: «Путь аль-Бухари» (Ummah Link, 2026-10-21).

- `mkmap.py` — собирает карту из NASA Black Marble + Blue Marble (кроп lon 25–75E, lat 52–8N, 240 px/град). Исходники NASA и шрифты (Montserrat, Amiri, Pacifico) скачиваются в `dl/` и `fonts/`, в репозиторий не входят.
- `docu.py` — библиотека: камера, рендер карты, glow, текст, стекло, Безье, trim, пунктир, контуры стран (Natural Earth).
- `render.py` — сцены ролика; все времена из `words.json` через `cue()`. `python3 render.py out.mp4 t0 t1` (рендерить кусками параллельно).
- `sfx30.py` — события SFX (буквы, города, плашки, пики скорости камеры) → `sfx_events30.json`.
- `mix30.py` — голос + SFX с сайдчейном → −14 LUFS, таблица `sfx_audit30.tsv`.
- `fakewords30.py` — черновые тайминги до озвучки.
