---
title: Моушен: плейбук
type: technique
tags: [technique, motion]
summary: Что уже использовали и что ещё не пробовали; правило разнообразия и приёмов брендов
updated: 2026-10-19
source: lessons/motion-playbook.md
---
> **СИСТЕМА v2 (2026-10-19):** плотность «событие каждые 0.4–0.8 с», HUD и SFX 1.5–2/с отсюда больше не база. Ритм и звук — [[rhythm-v2]], [[sound-v2]], порядок работы — [[SYSTEM]]. Приёмы этой заметки — библиотека, их подбирают под идею ролика ([[concept-first]]).

# Моушен: плейбук

**Signature style = Apple-стиль SABRMOTION (2026-10-13):** user made Apple keynote/ad-style editing their own signature. For SABRMOTION and by default, follow section 9 of /mnt/project-files/branding/sabrmotion/brand.md: blur-in text (20→0 px, 500 ms, cubic-bezier(0.4,0,0.2,1)), word-as-screen, one gradient word per reel, big numbers, light sweep, floating cards, match cuts, dark pause before the key line, slow push-in instead of punch-ins, ~0.5 SFX/s, minimal HUD. Client brands still override.

**Brand moves rule (2026-10-13, user: "use their techniques in all future edits, keep it"):** every new reel takes 1 move from the brand-styles section K of [[motion-catalog]] (Apple macro-to-wide, Revolut card-stack flip / card spiral / 3D phone, Stripe live gradient inside objects, Linear border beam / rotating glow, Spotify number-as-hero + geometry, motion balls: metaballs, glossy Blender spheres, sphere recolor wipe, orbit). Max 1 per reel on top of the Apple-style signature, rotate so no move repeats in consecutive reels; choose by tier per table K8. Log which one was used in [[edit-lessons-log]].

**Intensity tiers (2026-10-08):** before every edit ask the level (Минимал / Стандарт / Мощный / Ультра; default Стандарт) and follow [[motion-tiers]]. Techniques below apply only within what the chosen tier allows. Principle: the edit supports the words, never drowns the meaning.

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
- **НОВОЕ 2026-10-19 (ресерч трендов, подробно в [[trends-2026-motion-web]]):** рваная бумага между сценами (N01); графика «на двойках» 12 fps (N02); «кипящая» рукописная линия (N03); ризограф 2 цвета + полутон (N04); кинетика с массой: слова сталкиваются и толкают друг друга (N06, Knife Motion); текст по кривой (N07); видео внутри букв как переход (N08); каллиграфия штрихом, для исламских тем арабская (N09); бенто-сетка с ячейкой спикера (N10); киноплёнка-лента (N11); стеклянная линза с дисперсией (N12); изометрическая схема (N13); выноска, нарисованная поверх экрана (N15); микро-петля конец→начало (N16); «сначала результат» (N17); перекрытие рукой/объектом (N18).

**Why:** user wants "lots of motion effects" and professional graphics, and wants Claude to improve each edit.
**How to apply:** pick techniques before writing compositions; after the reel move used items into "Used so far" with notes on what looked good.

- **Blender / After Effects as asset makers (2026-10-11):** Blender = real 3D object with lighting/reflections (tile+chrome ring spin-in, 4 s, ~30 s render) that CSS/GSAP cannot fake; use for hero object, product, logo mark; render PNG seq → mp4 on the reel's bg colour. AE = precise keyframed UI/shape motion (editing-timeline mock: clips sliding on 3 tracks + playhead, trim/ease via keyframe.apply) rendered to mp4, shown in a glass card with 3D tilt in HyperFrames. Use them when a scene needs a hero element; for text/UI/transitions GSAP is faster. Showcase reel used: 1,5 s ring countdown hook, scroll feed with final flick, retention chart (path draw), 6 hard-cut blocks + stamp, AE card, Blender object + giant outline «3D» + shockwave, colour/sound/subtitle rows, pipeline chips, DM typing CTA with ripple → final object.

**RULE — mandatory frame-by-frame timing & bug audit before delivery (2026-10-11, user: «всё должно попадать в тайминги, никаких глюков»).**
1. Contact sheets at 10 fps (`ffmpeg -ss S -t 4 -vf "fps=10,scale=216:-1,tile=10x4"`), a 4 s block per image; read EVERY block. For each word with a visual/sound event: the visual starts on the word (±1 frame), the sound hits on the visual.
2. Look specifically for: element visible before its entrance (FT must set `from` at t=0), empty panels/holes between scenes, text clipped/overflowing, duplicated text (subtitle vs headline), double exposure that lasts >0.3 s, grey/white overlay stuck on (flash), items sitting static >1 s without a pulse.
3. Audio: measure each SFX file's onset and peak and anchor by it (never by file start); no sound without a matching visual; print the placement table and `verify_sfx.js`; dense overlaps may need a gap rule.
4. Run `hyperframes check` AFTER the last edit (a contrast failure = something stuck on screen); re-render and re-read the sheets for every fixed range; only then deliver, with a short list of what was fixed.
