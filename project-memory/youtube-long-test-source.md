---
name: youtube-long-test-source
description: Test source for first long-form 16:9 YouTube edit (Ward Cunningham interview, CC BY-SA) and how it was fetched to the PC
metadata:
  type: project
  modified: 2026-10-21T00:16:37.896Z
---

2026-10-21 user asked to try a beautiful LONG YouTube video (not reels) on a test source from the internet.
Found: Wikimedia Commons "File:Ward Cunningham, Inventor of the Wiki.webm" — 17:13, 1920x1080 23.976, CC BY-SA 3.0 (author Vgrigas/Wikimedia), documentary interview, brick wall, 2 angles, already has Wikipedia b-roll inserts. Audio clean pauses; first ~80 s have no pauses below -45 dB (possible music under intro -> must be cut/muted, NO MUSIC rule).
Saved: PC claude-edit\_inbox\2026-10-21\ward-cunningham_interview_1080p.webm (md5 38c2b5d8...), cloud /mnt/project-files/sources/2026-10-21_youtube-test_ward-cunningham/.

**How to apply:** Wikimedia original-file URLs return 429 from the cloud egress; the `/transcoded/...1080p.vp9.webm` derivative downloads fine. The PC VM proxy blocks upload.wikimedia.org, so download in cloud, split into 24 MB parts, device_commit_files, cat on PC. Leftover parts moved (not deleted) to claude-edit\_to_delete\2026-10-21_ward-parts\.

Status 2026-10-21 00:50: user chose 8–10 min, «Стандарт с пиками» (long-format density: event every 3–6 s, peaks on key ideas), Russian translated subtitles, direction D1 «Стол исследователя». Brief/EDL (8 chapters, 9:15)/RU subs/rough cut in /mnt/project-files/reels/2026-10-21_youtube-long_ward-cunningham/ and PC claude-edit\reels\ same name. AE build delegated to Remote Control session on PC.

Delivered 2026-10-21 ~evening: 8:39 16:9 in PC VIDEOS\tests\2026-10-21_youtube-ward-cunningham\ (master/light/preview540/contact/_ru.srt, extra\ with .aep, sfx_table, youtube_chapters.txt). Lesson vault/04-lessons/reels/2026-10-21-youtube-ward-cunningham.md. Gotcha: aerender/fresh AE substitutes Times for our fonts — run ae\fonts_register.ps1 first, render via AE queue. Awaiting user feedback.

2026-10-21 20:24 user: v1 «до профессионального монтажёра не доходишь» for long-form. Wrote vault/03-techniques/long-form-pro.md (story-first workflow, 3 picture registers A/B/C instead of graphics over face, tension/release rhythm, sound without music, real archive over invented UI, retention, review passes) with a v1 critique table. Read it before any long-form edit.

2026-10-21 20:35: PC also has vault\05-research\longform-pro-editing-2026-10-21.md + vault\07-system\longform-v1.md (written in the PC session, same conclusions; its numeric minimums like ≥35 % archive / ≥6 forms are guidelines per [[techniques-by-situation]]). Cloud has vault/03-techniques/long-form-pro.md — merge both on next vault backup. v2 paper edit + radio cut (8:29, mp3/720p mp4/srt) in the cloud reels folder; awaiting user's yes to build v2.

v2 DELIVERED 2026-10-21 ~23:30: 8:57 (8:36 voice + 20 s credits) in PC VIDEOS\tests\2026-10-21_youtube-ward-cunningham-v2\ (master/light/preview540/contact/srt/chapters/timeline.png/SFX table/licenses). Registers A51/B27/C22, 40 SFX, real archive (Commons + Wayback c2.com 1996 shot on PC). Lesson vault\04-lessons\reels\2026-10-22-youtube-ward-v2.md. AE on PC is shared via lock claude-edit\ae\AE_LOCK.json + ae\ae_lock.ps1 (user rule 22:47). Awaiting user feedback.
