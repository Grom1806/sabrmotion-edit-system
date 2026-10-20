---
title: Библиотека ассетов claude-edit\assets — что есть и где
type: tool
tags: [tool, assets, icons, photos, infographics, maps]
summary: Опись паков: ~53 000 иконок (линейные, 3D, флэт, логотипы, тематические подборки islamic/tech/business), 314 фото CC0 по 24 темам, 26 шаблонов инфографики × 4 палитры, карта мира по странам, 270 флагов, исламский паттерн khatam; полный каталог в assets\КАТАЛОГ.md
updated: 2026-10-19
source: докачка ассетов 2026-10-19 (npm iconify, lobehub fluent-emoji-3d, flag-icons, world-atlas, WordPress Photo Directory CC0, свои генераторы)
---
# Библиотека ассетов

Полная опись с путями и советами: `claude-edit\assets\КАТАЛОГ.md`. Лицензии: `assets\LICENSES.md` (только CC0/PD/MIT/Apache/ISC/OFL и свои). Журнал использования: `assets\_usage.csv`. Как обязательно использовать: [[use-everything]].

| Раздел | Что | Когда брать |
|---|---|---|
| `icons\_themes\<тема>` | готовые подборки: islamic 114, tech-ai 931, business-finance 737, growth-data 255, communication 631, time-calendar 244, security 292, people-creator 828 | первым делом по теме ролика |
| `icons\` семьи | lucide, tabler, phosphor, hugeicons, iconoir, heroicons, mingcute, material-symbols, remixicon (белые SVG) | одна семья на ролик |
| `icons\fluent-emoji-3d`, `fluent-emoji-flat` | 3D-PNG 256 px и плоские SVG | 3D только акцент 1–2 раза |
| `icons\brand-logos-*` | логотипы сервисов | только упоминание, без критики ([[no-negativity-about-others]]) |
| `photos\<группа>\<тема>` | islamic (мечети, луна, пустыня, финики), tech, business, creator, nature, texture; 2000–3200 px | реальный материал против «ИИ-вида»; не апскейлить |
| `infographics\templates` | 26 SVG с id на каждом элементе, палитры sabrmotion-dark / perset-light / islamic-emerald / overlay-white | число, процесс, сравнение, рост, список |
| `infographics\maps`, `flags` | страны как `<path id>`, точечная карта, 270 флагов | звучит страна/город/«по миру» |
| `infographics\patterns` | khatam, 5 цветов, 2160 px | исламские темы: фон, переходы, рамки |
| старое | `images\`, `lottie\` (67), `sfx\`, `fonts\` | `music\` НЕ использовать ([[no-music]]) |

Пробелы: фото Корана/молитвы/Мекки в хорошем качестве (своя съёмка или Higgsfield), видео-B-roll, бумага 4K.
