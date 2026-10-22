---
name: pro-advanced-editing
description: 2026-10-21 "сложный дорогой монтаж" training: methodology note, demo reel, Python engine for text-behind/head-tracked text/transitions; plus big-file transfer trick to PC
metadata:
  type: project
  modified: 2026-10-21T01:31:57.771Z
---
User (2026-10-21) asked Claude to learn complex pro editing: angles/camera, text behind / beside / following the head, b-roll + text on video, complex transitions, infographics, SFX, styles of other AE authors.

Delivered: vault/03-techniques/pro-advanced-editing.md (7 text-in-person-space moves T1-T7, 4 angles from one 4K cam incl. z<1 "zoom-out" with dark top extension + bottom fade, 9 transitions П1-П9 with AE + Python recipes, through-line infographic, SFX table, author styles, QA). Lesson vault/04-lessons/reels/2026-10-21-pro-techniques-demo.md. Demo 25 s on user's DJI_0028 4K ("Какой ты должник"): PC VIDEOS\tests\2026-10-21_pro-techniques-demo\pro-techniques-demo_v2.mp4; engine (analyze.py MediaPipe face + RVM matte, render.py scenes/transitions/SFX-from-events, mix.py) in reels\2026-10-21_pro-techniques-demo\engine and repo tools/pro-techniques-engine (branch claude/project-thread-yzaxq4). APPROVED 2026-10-21 01:33 («наш монтаж улучшился… намного лучше, чем раньше»). Then the user clarified (01:37–01:38): the techniques are NOT mandatory — «все наши техники использовать по ситуации», otherwise «будут одинаковые видео каждый раз». So it is a situational arsenal (vault/01-rules/pro-baseline.md, SYSTEM.md item 10), and the general rule for ALL vault techniques is [[techniques-by-situation]] (vault/01-rules/techniques-by-situation.md, SYSTEM.md item 11).

Key lessons: offset side text from the person's MATTE edge (landmarks miss ears/hair); "text behind head" baseline = hair top (from matte) + ~40 px, tracked; word width ≤1000 px; white text on bright b-roll needs strong alpha shadow.

Transfer gotcha: device_commit_files rejects files >25 MB, and /mnt/project-files rewrites .mp4 files on write (bytes change). For big videos: gzip -1, split -b 22M, commit parts, then on device `cat parts | gunzip > file.mp4` and check md5. See [[talking-head-pro-guide]], [[sfx-expressive]].
