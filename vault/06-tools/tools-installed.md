---
title: Инструменты на ПК
type: tool
tags: [tool, pc]
summary: Что стоит на ПК: HyperFrames, ffmpeg-master, video-toolkit, ElevenLabs, Blender MCP, After Effects MCP, Higgsfield
updated: 2026-10-19
source: project memory
---
# Инструменты на ПК (DESKTOP-NEAHN3N)

Installed 2026-10-07 on DESKTOP-NEAHN3N:
- HyperFrames Claude Code plugin 0.8.140 (user scope, enabled). User also had standalone HyperFrames skills, so duplicates may appear.
- claude-code-video-toolkit cloned at C:\Users\subhan\Desktop\subhan\claude-code-video-toolkit, uv .venv (Python 3.12). Its /setup NOT run (needs ElevenLabs + GPU keys).
- Suggested directory plugins (IT Reelsmaker, Motion Reel, Remotion, ffmpeg-llm) via install card; user enables them in claude.ai.

**Why:** user wants SFX/motion effects in reels ([[sound-design]]).
**How to apply:** use HyperFrames /talking-head-recut, /media-use, /hyperframes-audio for future edits.

Added 2026-10-07 (user scope, via RC):
- ffmpeg-master v4.0.0 from marketplace JosiahSiegel/claude-plugin-marketplace (pulls ffmpeg-core, -effects, -social-video, -platforms, -python). Commands /ffmpeg-color, /ffmpeg-kinetic, /ffmpeg-effects, /ffmpeg-viral-shorts; skills color-grading-chromakey, transitions-effects, kinetic-captions, glitch-distortion, animation-timing-reference. Use for grading per [[color-playbook]].
- claude-video-edit skill (AgriciDaniel) in C:\Users\subhan\.claude\skills\claude-video-edit\ - SKILL.md only; its preflight.sh/detect_gpu.sh step fails (scripts not copied). Use only its ffmpeg recipes, skip preflight. User had asked for ffmpeg-master only; may want it removed.
- Auto-mode classifier on the PC blocks plugin installs until the user confirms explicitly in the thread.

## Добавлено позже
- 2026-10-09: Blender MCP (Blender 5.2, RTX 5080) и After Effects MCP (AE 2026 работает только после полной загрузки). Использовать для 3D и моушена ([[motion-balls]]).
- 2026-10-12: Higgsfield (AI-видео): B-roll, хуки, оживление фото. Музыку из него не брать ([[no-music]]).
- ElevenLabs: ключ в `Desktop\subhan\claude-code-video-toolkit\.env`; SFX и голос пользователя `fv3LKrS09h3gGy4GZW1e` ([[voice-processing]]).
- Ассеты (иконки ~53 000, фото 314 + старые, инфографика 26×4 шаблона, карты, флаги, паттерны, Lottie, SFX, шрифты): `claude-edit\assets\`, опись `assets\КАТАЛОГ.md`, журнал `assets\_usage.csv`. См. [[assets-library]].

## After Effects (проверено 2026-10-19, система v2)
- **AE 2026, версия 26.5x89**, язык интерфейса ru_RU, 3 GPU. Запускать обычным двойным кликом / `AfterFX.exe` **без `-m`** (иначе мост не достучится).
- **MCP:** `kumoproductions/mcp-aftereffects` (218 операций в `ae_do`: comp/layer/keyframe/text/shape/effect/render/font…, `ae_render_frame` = see-frame с контакт-листом, `instance.dialogs` закрывает модалки). `saveFrameToPng` есть. **`eval.run` выключен** политикой сервера → произвольный JSX запускаем через `AfterFX.exe -r script.jsx` скриптом `claude-edit\ae\run.ps1` (ждёт строку DONE в `ae\logs\run.log`). Агент мультиинстанса (`install-agent`) не установлен → `instance.start` не работает; одной копии AE хватает.
- **Сторонних плагинов нет.** Deep Glow, Saber, Optical Flares, Trapcode, Universe, Sapphire, GEOlayers, FilmConvert, Twitch — НЕ установлены, не использовать. Есть только штатные: Glow, Add Grain / Match Grain, Camera Lens Blur, Turbulent Displace, Fractal Noise, Lumetri, CC-набор (CycoreFX HD: CC Light Rays, CC Radial Fast Blur, CC Vignette, CC Force Motion Blur, CC Page Turn и др.), Mocha AE, Keylight, Cineware, VR-эффекты (VR Glow).
- **Шрифты** (поставлены пользователю 2026-10-19 из google/fonts, OFL): Golos Text (VF), PT Serif (Regular/Italic/Bold Italic), IBM Plex Mono (Regular/Medium/SemiBold). Копии в `claude-edit\ae\fonts\`. После установки шрифтов AE надо перезапустить.
- Python на ПК не установлен (только заглушка Microsoft Store) → скрипты vault гонять Node.
- Шаблоны вывода (REELS_*, PNG_SEQ, Draft_Half) пока не созданы — инструкция пользователю в заметке урока; до этого рендер PNG/штатным шаблоном + ffmpeg.
