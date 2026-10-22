---
name: no-ae-pipeline
description: 2026-10-22 user: without After Effects (absent/busy/AE_LOCK) edit via code with the same graphics properties — HyperFrames kit (default) or Python nae engine; vault/07-system/no-ae-pipeline.md
metadata:
  type: project
  modified: 2026-10-22T19:16:32.842Z
---
User (2026-10-22): «если нет After Effects… через HyperFrames… всё, чему научились, графика с теми же свойствами, как в After Effects, только монтаж через код». Asked to bring back the pre-AE code system (approved reels «Шкала должника» v3, plan-2-mosque, be-honest were HyperFrames + GSAP with node tools tts → words → gaps → inject → dump → mix → verify_solo).

Built and tested in cloud (QA PASS): HyperFrames kit at PC claude-edit\tools\hyperframes-kit\template (lib/sabr.js helpers enforce vault norms: sabr/sabrCam eases, tick per letter, small text no blur, no grain, rest scale 1, reading-time by seeking timeline; tools/build.cjs one-shot; qa.cjs) and Python engine claude-edit\tools\no-ae-engine (nae). Same in GitHub repo branch claude/project-thread-3knd8f. Doc with AE→code table, skills list, gotchas: vault/07-system/no-ae-pipeline.md; SYSTEM.md item 13.

**How to apply:** if AE is missing, locked or not responding, don't wait. Copy the template to the reel folder, build with `node tools/build.cjs <slug>` and tell the user one line: «собираю кодом». See [[edit-system-v3]], [[after-effects-usage]].
