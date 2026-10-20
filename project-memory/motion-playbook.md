---
name: motion-playbook
description: Motion/graphics techniques used and still-to-try for talking-head reels; variety rule; read before every edit
metadata:
  type: project
  modified: 2026-10-07T23:37:36.177Z
---

**Intensity tiers (2026-10-08):** before every edit ask the level (Минимал / Стандарт / Мощный / Ультра; default Стандарт) and follow [[motion-tiers]]. Techniques below apply only within what the chosen tier allows. Principle: the edit supports the words, never drowns the meaning.

**Signature style = Apple-стиль SABRMOTION (2026-10-13):** user made Apple keynote/ad-style editing their own signature. For SABRMOTION and by default, follow section 9 of /mnt/project-files/branding/sabrmotion/brand.md: blur-in text (20→0 px, 500 ms, cubic-bezier(0.4,0,0.2,1)), word-as-screen, one gradient word per reel, big numbers, light sweep, floating cards, match cuts, dark pause before the key line, slow push-in instead of punch-ins, ~0.5 SFX/s, minimal HUD. Client brands still override.

**Brand moves rule (2026-10-13, user: "use their techniques in all future edits, keep it"):** every new reel takes 1 move from the brand-styles section K of /mnt/project-files/style/motion_library.md (Apple macro-to-wide, Revolut card-stack flip / card spiral / 3D phone, Stripe live gradient inside objects, Linear border beam / rotating glow, Spotify number-as-hero + geometry, motion balls: metaballs, glossy Blender spheres, sphere recolor wipe, orbit). Max 1 per reel on top of the Apple-style signature, rotate so no move repeats in consecutive reels; choose by tier per table K8. Log which one was used in [[edit-lessons-log]].

**Variety rule:** every new reel uses at least 2 techniques from "Not tried yet" and does not repeat the previous reel's signature move as-is. Log what was used in [[edit-lessons-log]].

**Used so far (HyperFrames + GSAP, cues from whisper word timings):**
- Speaker shrinks/slides down (scale ~0.58) and an info panel takes the top; items appear on keywords (reel 1).
- Viewfinder frame + REC overlay (reel 1).
- Word-by-word captions with one accent word (reels 1, 2).
- Full-screen terracotta (#c8623c) wipe with a drawn icon/"?" for the climax (reels 1, 2) - already repeated twice, change it next time.
- Scoreboard/counter (01-11) with a progress bar of segments (reel 2).
- Face-tracked crop from 16:9 4K, punch-ins 100/108% on every cut, bottom fading into background (reel 2).
- SFX mapped to cues: whoosh on panel entry, swish on item change, tick on numbers, pop on badges, riser+impact on full screen, chime on outro (reel 2).

**Not tried yet (pick 2+ next reel):**
- Speed ramp / smash zoom on the hook line (scale 1->1.25 in 150ms + motion blur).
- Whip-pan or zoom-blur transition between sections.
- Kinetic typography: big words filling the frame, masked reveals, per-letter stagger.
- Camera shake on impact words; light leaks / film burn overlay.
- B-roll or screenshot cards with 3D tilt (perspective) and parallax.
- Split screen / picture-in-picture comparisons.
- Highlighter/underline that draws under subtitle words; emoji/icon pops.
- Progress bar for the whole reel at the top; animated lower third with name.
- Color shift per section (graded B/W flash on a "problem" line).
- NEW 2026-10-19 (trend research, vault/05-research/trends-2026-motion-web.md, N01-N20): torn-paper scene reveal; graphics animated on twos (12 fps steps); boiling hand-drawn lines; riso 2-color halftone; weighted kinetic type where words collide/push (Knife Motion); text on a curve path; video inside giant letters as transition; calligraphy stroke write-on (Arabic for Islamic topics, respectfully); bento grid with speaker cell; vertical film-strip scroll; glass lens with RGB dispersion; isometric process diagram; callouts drawn over screen recordings; micro-loop end->start; reveal-first structure; hand/object cover wipe; blink cut.

**Why:** user wants "lots of motion effects" and professional graphics, and wants Claude to improve each edit.
**How to apply:** pick techniques before writing compositions; after the reel move used items into "Used so far" with notes on what looked good.
