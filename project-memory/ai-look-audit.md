---
name: ai-look-audit
description: 2026-10-19 audit of why our reels look "AI-generic"; the tells to avoid and fixes proposed (report artifact link)
metadata:
  type: project
  modified: 2026-10-19T20:36:47.950Z
---

User (2026-10-19) felt our reels look like other AI edits; full audit report: https://claude.ai/artifact/Djp6YtePTgmK6bqPSh4D4x (source /mnt/project-files not used; scratchpad).

Tells found (reel6, reel7, showcase v2, adobe-free, openai-otmena, PERSET 02): web-UI components as graphics (3-dot windows, terminal, pills, mono caps labels = shadcn/Tailwind look); same grid every reel (card top-center, caps subtitle bottom with 1 red word); template HUD (REC 00:00, play icon, progress bar, green CTA pill) with no meaning; literal illustration + on-screen text duplicating voice; metronome rhythm (event every 0.5 s, 1.7-2.5 SFX/s); same blur-in entrances + generated SFX family; zero real footage/texture; AI voice clone with 0% face; same script formula. PERSET 02 closest to pro (one through-object/world).

Fixes became system v2 on 2026-10-19 (user asked to build it); see vault/00-start/SYSTEM.md. Original proposals: one visual idea per reel before picking techniques (replace "2 from list" in variety.md); drop default HUD/CTA; per-reel subtitle system; show what voice doesn't say; rhythm in waves with 1.5-2 s pauses, 0.5-1 SFX/s; real filmed shots + grain/on-twos texture; graphics tracked into room; own type pairs and easing curves; recorded foley; style frames first; anti-AI QA checklist. See [[motion-playbook]], [[knowledge-vault]].

**First v2 test rejected on density (2026-10-19):** "День 90" v2 (calm waves, plateaus 3-6 s, 15 quiet SFX) - user: "скучно, мало движения", "намного хуже стало" than v1; also heard background noise/interference (likely room tone + noise SFX) and blurry photos. **How to apply:** keep v2 quality fixes (idea, curves, no template HUD) but do NOT lower motion density below previous approved reels (default ~Мощный density, short 1-1.5 s plateaus); no room tone on clean voice; photos never upscaled.

**Blurry whole reel (Ummah Link riso, 2026-10-19):** user: "очень много мыла". Causes: animated grain/paper-fiber texture layered OVER text (edges turn to noise, compression smears it), camera constantly at 100-103% scale (every frame resampled), light exported at 720p. **How to apply:** texture only UNDER content (max static grain ≤3% on top); camera exactly 100%/0° between hits, wiggle rounded to whole px; site screenshots at DPR 2-3, never >100%; aerender Best/Full -> ProRes HQ -> H.264 master CRF 14 -tune animation; light = 1080x1920 CRF 18, never 720p; before delivery compare AE frame vs master vs light at 1:1. Full rule: PC vault 07-system/ae-pipeline.md "Против мыла".

**NO WHOLE-FRAME CAMERA MOVES (user 2026-10-19):** "должно меняться внутри видео, а не само видео": shifting/punching/shaking the whole frame is bad for the eyes. **How to apply:** frame stays still (no camera punch-ins, shakes or global zoom on beats); energy comes from elements moving inside the frame. Overrides "camera hits on words" from the Ummah Link riso reel.

**Ayat al-Kursi brief (user 2026-10-19):** wants a clearly different animation design each reel (asked for bone/rig animation: Puppet pins or null-parent rigs), more SFX, and a quiet halal ambience bed from assets\sfx\ambience\ under the voice (it is wanted, unlike room-tone noise).

**STUDY BEFORE DESIGNING (user 2026-10-19):** user stopped the Ayat al-Kursi reel and had its project deleted: "мы не должны делать видео, не зная этого". Collage/paper-sheets is NOT the only design. **How to apply:** before proposing any new reel design, review everything newly added to the project (vault 07-system/directions-v3.md menu D1-D6, SYSTEM.md v3, 05-research, 04-lessons/threads, user's new files) and offer designs from that, not the last reel's style.
