# SABR-kit — модульные стили (субтитры, движение, инфографика)

Документация и правила смешения: `vault/03-techniques/style-kit.md`. Разбор рефов: `vault/05-research/ref-captions-pro-2026-10-25.md`.

| Файл | Что это |
|---|---|
| `sabr-kit.js` | модули: `SK.pop/bounce/spring/slide/depth/slice/scan/rgb/letters/type`, `SK.whip/fade/shrink`, `SK.punch/push/flash/leak`, `SK.win/open/cursor/glide/click/count/karaoke` |
| `sabr-kit.css` | шрифтовые роли `sk-cond/sk-script/sk-sans/sk-ui`, цвета, `sk-lift`, `sk-bloom`, окна `glass`/`retro` |
| `example-iphone-duo-v4.html` | полный пример ролика (10 сцен, маска человека, инфографика вокруг головы) |
| `example-mix-sfx.py` | микс голоса и звуков, у каждого звука подпись видимого события |

## Шрифты (положить в `assets/fonts/`, кириллица есть)
```
curl -L -o Oswald.ttf          "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
curl -L -o PlayfairItalic.ttf  "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf"
curl -L -o Montserrat.ttf      "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
curl -L -o Inter.ttf           "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf"
```

## Порядок сборки
1. `tools/matte/matte.py head.mp4 assets models` → `person.webm` + `track.json` (где лицо и макушка).
2. Слои: `#bg` → `#win0 > #cam > [голова, #behind, person.webm]` → `#front` → сцены → `#leak` → `#flash`.
3. Тексты по таймингам слов (faster-whisper). Позиция только инлайн-стилем.
4. `node tools/readcheck/readcheck.mjs .` → 0 FAIL / 0 OVERLAP.
5. Звук: таблица «модуль → звук» в style-kit.md, мастер −14 LUFS.
