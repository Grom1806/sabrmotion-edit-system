---
title: Каталог инструментов
type: tool
tags: [tool, pc, catalog]
summary: Какой скилл/MCP брать под задачу монтажа (рилсы, субтитры, моушн, анализ, стоки, ffmpeg); 78 скиллов + 5 MCP с 2026-10-13
updated: 2026-10-13
source: _lessons/tools-catalog.md
---
# Каталог инструментов для монтажа (установлено 2026-10-13)

Всё стоит в user scope (`~/.claude`), поэтому доступно в любой сессии. После установки нужен **перезапуск Claude**.
Правило пользователя: **музыку не добавлять никогда**. Только голос и немелодичные SFX. Скиллы `music-to-video` и `soundtrack` для музыки не использовать.

## Что под какую задачу

| Задача | Чем пользоваться |
|---|---|
| **Talking-head рилс 9:16** (нарезка, зумы, B-roll, SFX) | `video-editing` (nopefallacy, вертикальный рилс на HyperFrames с верификацией), `talking-head-recut` (HyperFrames), `short-form-video` (hook → удержание → луп), `beat-sync-editing` (ритм склеек, J/L-cut), `video-talkcraft` (подача голос + моушн, Remotion) |
| **Субтитры** | `embedded-captions` (HyperFrames, 35 стилей, субтитры за спиной героя), `caption-animation` (karaoke, word-by-word), `remotion-captions`, ffmpeg-скиллы `ffmpeg-kinetic-captions` / `viral-video-animated-captions` |
| **Моушн-графика** | HyperFrames: `motion-graphics`, `hyperframes-animation`, `faceless-explainer`; iart-ai: `kinetic-typography`, `animated-infographic`, `chart-animation`, `diagram-animation`, `logo-animation`, `lower-thirds`, `motion-background`, `svg-animation`, `isometric-animation`, `particle-system`, `shader-glsl`, `threejs-animation`, `map-animation`, `whiteboard-animation`; `business-motion-film` (премиальный ролик для бизнеса); `video-shotcraft` (продуктовое видео: 2.5D-камера по скриншотам); `video-wrapper` (花字/карточки/плашки для интервью, Python + Chromium); Remotion: `remotion-*` (12), `remotion-video`; `manim` + MCP `manim-server` (математика и схемы); After Effects: MCP `aftereffects` + скилл `after-effects` (экспрешены, экспорт) |
| **Арт-дирекция и раскадровка** | `motion-art-direction`, `animation-principles`, `shot-composition`, `color-motion`, `brand-motion-guidelines`, `creative-brief`, `explainer-video` |
| **Анализ референса / видео** | MCP `claude-video-vision`: кадры + аудио. Бэкенд выбирается командой `/claude-video-vision:setup-video-vision`; Gemini требует ключ, локальный Whisper работает без ключа. Также `ffmpeg-core:ffmpeg-video-analysis`, Higgsfield `video_analysis_*` (облачный коннектор) |
| **B-roll / стоки** | MCP `pexels` (нужен `PEXELS_API_KEY`), Higgsfield: генерация видео и картинок (плагин `higgsfield:*` + облачный коннектор), OpenMontage (стоки Archive.org, NASA, Wikimedia, Pexels, Pixabay) |
| **Транскрипция** | MCP `sanzaru` (Whisper через OpenAI, нужен `OPENAI_API_KEY`), `claude-video-vision` с локальным Whisper (без ключа), локальный faster-whisper из нашего пайплайна (как в reel6) |
| **Операции ffmpeg** | MCP `ffmpeg` (ffmpeg-mcp-lite: обрезка, склейка, конвертация, кадры), плагины ffmpeg-master (5 пакетов), скилл `claude-video-edit` |
| **Готовые форматы** | iart-ai: `ad-creative-video`, `promo-video`, `launch-video`, `testimonial-video`, `text-message-animation`, `audiogram`, `photo-slideshow`, `presentation-video`, `youtube-intro-outro`, `countdown-video`, `wrapped-video`; HyperFrames: `product-launch-video`, `slideshow`, `pr-to-video`, `general-video` |
| **Экспорт / спеки площадок** | `video-delivery-specs`, `ffmpeg-social-video:viral-video-platform-specs` |
| **Полный автопайплайн** | `C:\Users\subhan\Desktop\subhan\OpenMontage` (открыть в Claude Code из этой папки; venv `.venv`, Remotion в `remotion-composer`, озвучка Piper офлайн). Музыкальные модули (Suno) не использовать |
| **YouTube-длинное видео** | `C:\Users\subhan\Desktop\subhan\claude-youtube-editor` (проект-пайплайн; открывать из его папки) |

## MCP-серверы (user scope)

| Имя | Статус | Нужно |
|---|---|---|
| `claude-video-vision` | ✔ | настройка бэкенда через `/claude-video-vision:setup-video-vision`; для Gemini нужен `GEMINI_API_KEY` |
| `ffmpeg` (ffmpeg-mcp-lite) | ✔ | запускается с `--with "mcp<2"` (пакет не совместим с mcp 2.x) |
| `sanzaru` | ✔ | `OPENAI_API_KEY` (без него транскрипция и картинки не работают); медиа в `Desktop\subhan\sanzaru-media` |
| `manim-server` | ✔ | в venv закреплён `mcp<2`; код в `Desktop\subhan\mcp-servers\manim-mcp-server` |
| `pexels` | ✔ | `PEXELS_API_KEY` (бесплатно на pexels.com/api) |
| `aftereffects` | ✔ (уже был) | открытый After Effects |
| `playwright` | ✔ (уже был) | — |
| Blender | был ранее | открытый Blender с аддоном |

Как добавить ключ (пример): `claude mcp remove -s user pexels`, затем `claude mcp add -s user pexels -e PEXELS_API_KEY=... -- node C:\Users\subhan\Desktop\subhan\mcp-servers\pexels-mcp-server\dist\main.js`.

## Плагины
- `hyperframes` (21 скилл), ffmpeg-master: `ffmpeg-core`, `ffmpeg-effects`, `ffmpeg-social-video`, `ffmpeg-platforms`, `ffmpeg-python`
- `higgsfield@higgsfield`: generate, soul-id, product-photoshoot, brandkit, marketplace-cards, websites, video-explainer, youtube-thumbnail. Авторизация Higgsfield CLI при первом запуске.

## Не поставлено и почему
- `video-creator/ffmpeg-mcp`: по README работает только на macOS.
- Premiere Pro MCP: Premiere не установлен.
- DaVinci Resolve MCP: стоит бесплатная Resolve 21.1, а внешний скриптинг работает только в Studio.
- Deprecated (по заданию): Remotion documentation MCP, vibe-motion/skills, старый elevenlabs-mcp, arcaputo3/mcp-server-whisper.

## Грабли установки (на будущее)
- `npx skills add ... --all` = все скиллы **и все агенты**. Отсюда ошибки «Eve/PromptScript does not support global». Для одного Claude: `--skill '*' -g -y -a claude-code`.
- npm-пакета `vertical-video-editing-skill` нет (404). Ставится через `npx skills add nopefallacy/vertical-video-editing-skills`.
- Python-MCP на FastMCP падают с mcp 2.x (`No module named 'mcp.server.fastmcp'`). Лечится закреплением `mcp<2`.
- В этой сессии классификатор auto mode блокирует установку внешнего кода. Решение: скрипт `_install\install-video-tools.ps1` пользователь запускает сам.
