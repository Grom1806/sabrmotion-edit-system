---
title: Хаус-стиль по референсам (кратко)
type: technique
tags: [technique, style, tier/power]
summary: Кратко про референсы IMG_6708/6709: HUD, UI-метафоры, аватар+цитата, слот-машина; полная версия в reference-style-guide
updated: 2026-10-19
source: lessons/reference-style.md
---
> **СИСТЕМА v2 (2026-10-19):** плотность «событие каждые 0.4–0.8 с», HUD и SFX 1.5–2/с отсюда больше не база. Ритм и звук — [[rhythm-v2]], [[sound-v2]], порядок работы — [[SYSTEM]]. Приёмы этой заметки — библиотека, их подбирают под идею ролика ([[concept-first]]).

# Хаус-стиль по референсам (кратко)

User (2026-10-08) said our edits were "dry, no graphics" and gave two pro references (same "Шкала должника" script): /mnt/project-files/IMG_6708.MP4 (9:16), IMG_6709.MP4 (16:9). Full guide: /mnt/project-files/style/reference_style.md (copy on PC claude-edit\_lessons\reference_style.md).

Core rules:
- Reel = UI/game: persistent HUD (series label + "УРОВЕНЬ 01/12" + segmented progress bar), every beat gets a UI-mockup metaphor (calendar countdown, bank transfer card, push notification swiped, chat "печатает…", bank card 0,00 ₽ + stamp, incoming call, chat changing topic, letter grid, circular diagram) or a flat icon (16:9 version).
- Fixed grid per beat: HUD top, illustration upper half, speaker as round avatar (terracotta ring) + cream quote bubble typed word-by-word with blur, "СУММА ДОЛГА" slot-machine of blurred random numbers landing on value + underline draw + flying ₽ banknotes.
- Palette: bg #090708 with warm radial glow, accent terracotta #c85a43, cream #f4ece4. Fonts: ultra-bold wide digits (Unbounded Black), Inter/Manrope text, letter-spaced caps labels.
- Motion: motion blur on every move, counters always ticking, new visual event every 0.5-1 s, nothing static >1 s.
- Audio: (music bed NOT used — [[no-music]]) ~1 SFX/second in the reference; ours per [[sound-v2]] (55-65 per minute) + sub hits on level changes; finale = full terracotta fill, riser, money rain, then speaker big with CTA question on a plate.

**How to apply:** check every edit against the 7-point checklist at the end of the guide before showing a preview. See [[motion-playbook]], [[edit-lessons-log]].
