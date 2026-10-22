---
name: docu-motion-map
description: Person-less documentary motion on a night satellite map (user's 3 refs 2026-10-21) — research note, Python engine, first reel «Путь аль-Бухари», ElevenLabs credit limit
metadata:
  type: project
---
2026-10-21 the user asked to learn "сложный монтаж, прям motion" from 3 reference reels (_inbox IMG_0625–0627) for videos WITHOUT a person, and make one for Ummah Link.
- Research: vault/05-research/ref-docu-motion-2026-10-21.md — 24 techniques Д1–Д24 (one map-world, camera flies between city stations, neon country outlines, gold routes, glass name plates, isnad chain, typewriter chronicle strip, giant gold words, book-as-proof). Do NOT copy: music beds, human figures (even faceless), debates, grain.
- Engine (Python/OpenCV, no AE): NASA Black Marble + Blue Marble crop lon 25–75E lat 52–8N at 240 px/deg, Natural Earth outlines; files in /mnt/project-files/reels/2026-10-21_ummah-bukhari-path/engine (docu.py, render.py, sfx30.py, mix30.py). Render ~3 s/frame per core in the cloud — split into parallel chunks.
- First reel: «Путь аль-Бухари», user chose the 30 s cut (voice 26.5 s) because ElevenLabs had only 164 credits left.
- ElevenLabs cost ≈0.4 credits per character with eleven_v4 (777 chars → 310). After this reel ~8 credits remain: next voice-over needs a top-up or the user's own recording. tts.js writes to the reel root, words.js reads work/vo/ — copy files there.
- 2026-10-21 19:16 user: «возьми всё, чему ты научился отсюда» → folded into the system: recipe vault/03-techniques/docu-map-motion.md, SYSTEM.md item 12, edit type Т16, main panel build option «Документалка на карте» + preset, sfx-expressive (whoosh by camera-speed peaks, typewriter 0.042 s/char), engine in repo tools/docu-map-engine. Delivered v1: PC VIDEOS\ummah\2026-10-21_bukhari-path\bukhari30_v1.mp4, awaiting feedback.
Related: [[ummah-ideas-panel]], [[techniques-by-situation]], [[pro-advanced-editing]].

- 2026-10-22: user stored a BACKUP ElevenLabs API key on PC in claude-edit\.env as ELEVENLABS_API_KEY_BACKUP (value never in memory/repo/chat). Use it when the main key runs out.
