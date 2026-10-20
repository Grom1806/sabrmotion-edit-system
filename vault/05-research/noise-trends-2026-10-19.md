# Noise-фоны: тренды Instagram и паки (2026-10-19)

Источник: браузер пользователя, Instagram-поиск «noise background», «grainy gradient background», «noise texture pack», «noise overlay» (~100 постов). Скрины: `noise-2026-10-19/`.

> ⚠️ Конфликт с правилом NO GRAIN ([[sharpness-guard]]): шум/зерно запрещены **по умолчанию**. Всё ниже — только опция, которую пользователь выбирает в брифе (вопрос «фон: чистый / noise?»). Звуковой «шум» (white/brown noise, природа) — не наше: фон только нашид.

## 5 трендовых семейств

| # | Семейство | Как выглядит | Риск «мыла» | Как применять у нас |
|---|---|---|---|---|
| N1 | **Grainy gradient / aurora** | мягкий 2–3-цветный градиент (фиолет→синий, красный→белый, оранж→графит) с крупным зерном | высокий: мелкое зерно рушит сжатие IG | зерно **крупное** (2–3 px), статичное или 12 fps; текст/графика на слое над шумом, не под ним; в палитре бренда |
| N2 | **Glass blur / chrome Y2K** | размытые стеклянные формы, хромовая звезда/блоб, светящаяся «таблетка» | средний | фон-объект за спикером в голосовых рилсах; можно в AE (CC Glass + Fast Box Blur) без шума вообще |
| N3 | **Film grain / dust & scratches** | плёнка 16/35 мм, пыль, царапины, light leak | высокий | только короткие вставки (флешбэк, «история»), не весь ролик |
| N4 | **VHS / TV static / scanlines** | белый шум ТВ, полосы, rgb-сдвиг | низкий, если ≤0.5 с | как **переход** (статик-флеш 6–10 кадров) между сценами, с SFX «щелчок ТВ» |
| N5 | **Glitch / datamosh / audioreactive** (TouchDesigner) | цифровые разрывы, пиксель-сортинг, реагирует на голос | низкий как акцент | акцент на 1–2 ключевых словах, не фон |
| + | **Grunge/print textures** (photocopy, Berlin grunge, riso «light noise») | бумага, фотокопия, мятый лист | средний | для коллаж-направлений, под контентом, статично |

Наблюдение: паки в IG почти всегда раздают через «комментируй слово → пришлю ссылку» (напр. @bratachakraborty «Noise Overlay for Cinematic Edits», 1.5k комментариев) — сами файлы на Gumroad/Telegram.

## Паки (проверить лицензию перед клиентской работой)

- **Grain Haven** — 4K film grain, Super8/16/35 мм, верт+гор, pay-what-you-want: https://editorpacks.gumroad.com/l/grainhaven
- **Ghostpaper Grainy Gradients 4K** — 10 анимированных 4K-лупов + 100 стиллов, $12.95: https://ghostpaper.gumroad.com/l/grainygradients4k
- **Craftwork Mesh Gradients** — 97 бесплатных mesh-градиентов с зерном (PNG/Figma): https://craftwork.design/product/mesh-gradients
- **ZOSIA free gradients** — 6 grainy-градиентов, коммерция ок: https://thisiszosia.gumroad.com/l/gradient-backgrounds-free
- **Zarrar 30 grainy gradients 4K** (стиллы, $1+): https://zarrar.gumroad.com/l/grainygradients
- **VHS/CRT**: Snowman Digital (верт. 4K VHS) https://snowmandigital.gumroad.com ; Envato Elements VHS noise с альфой https://elements.envato.com/vhs-noise-FZYV9GN
- **Filmyie bundle** $29 (VHS-текстуры/переходы + 4K grain): https://filmyiedotin.gumroad.com/l/mdpack

## Свой генератор вместо паков (рекомендация)
Лицензия чистая и разрешение точное: AE Fractal Noise (Contrast 300, Brightness −40, Complexity 1, Size 3–6 px, Evolution `time*720` с Posterize Time 12) поверх Gradient Ramp/4-Color Gradient в цветах бренда → это и есть N1. Статик N4: Noise 100% + Venetian Blinds + Wave Warp, 8 кадров. Экспорт master CRF 14, проверка sharpcheck.py.

## Правило безопасности
1. Noise никогда не поверх текста и мелкой графики.
2. Зерно ≥2 px, иначе после IG-сжатия = «мыло».
3. Если в брифе нет noise — фон чистый (NO GRAIN действует).
