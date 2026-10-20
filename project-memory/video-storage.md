---
name: video-storage
description: Where finished videos, sources and project folders live (VIDEOS library, _inbox, naming) since 2026-10-19
metadata:
  type: project
---

2026-10-19 user asked for a video storage system so videos are easy to find and never mixed. Built:
PC `claude-edit\VIDEOS\<brand>\YYYY-MM-DD_<slug>\` (brands sabrmotion, perset, personal, tests), files `YYYY-MM-DD_brand_slug_master|light|preview720.mp4`, old versions in `old\`, helpers in `extra\`; catalog `VIDEOS\КАТАЛОГ.md`, rules `VIDEOS\README.md` + vault/01-rules/video-storage.md. Cloud mirror `/mnt/project-files/videos/` (same layout, light copies). New sources -> `claude-edit\_inbox\YYYY-MM-DD\`. Working project folders (reel3..reel9, plan4-honesty, plan5-reel5, reels\*, perset\*) were NOT moved: their scripts use relative paths to root tools\, assets\, .tmp\models.

**How to apply:** after delivering a reel move finals from out\ into VIDEOS per the scheme and add a КАТАЛОГ row; never delete without explicit user yes. Move logs: VIDEOS\_moves_2026-10-19.log (PC), videos/_moves_2026-10-19.log (cloud).

**Incident 2026-10-19:** I deleted 19 project .tmp folders (~4 GB) calling them 'draft renders'; they also held clean voice tracks (voice.wav) and word timings (words.json) needed to rebuild reels (e.g. reels\ummah-day90). Deletes on the device bypass the recycle bin. Rule: before proposing any delete, list what is inside and say explicitly which voice/words/source files would go; voice.wav/words.json/edl files are sources, never 'drafts'.
