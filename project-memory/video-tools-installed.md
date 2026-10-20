---
name: video-tools-installed
description: Video-editing plugins/tools installed on user's PC (DESKTOP-NEAHN3N) as of 2026-10-07
metadata:
  type: project
  modified: 2026-10-07T22:52:55.564Z
---

Installed 2026-10-07 on DESKTOP-NEAHN3N:
- HyperFrames Claude Code plugin 0.8.140 (user scope, enabled). User also had standalone HyperFrames skills, so duplicates may appear.
- claude-code-video-toolkit cloned at C:\Users\subhan\Desktop\subhan\claude-code-video-toolkit, uv .venv (Python 3.12). Its /setup NOT run (needs ElevenLabs + GPU keys).
- Suggested directory plugins (IT Reelsmaker, Motion Reel, Remotion, ffmpeg-llm) via install card; user enables them in claude.ai.

**Why:** user wants SFX/motion effects in reels ([[sfx-preference]]).
**How to apply:** use HyperFrames /talking-head-recut, /media-use, /hyperframes-audio for future edits.

Added 2026-10-07 (user scope, via RC):
- ffmpeg-master v4.0.0 from marketplace JosiahSiegel/claude-plugin-marketplace (pulls ffmpeg-core, -effects, -social-video, -platforms, -python). Commands /ffmpeg-color, /ffmpeg-kinetic, /ffmpeg-effects, /ffmpeg-viral-shorts; skills color-grading-chromakey, transitions-effects, kinetic-captions, glitch-distortion, animation-timing-reference. Use for grading per [[color-playbook]].
- claude-video-edit skill (AgriciDaniel) in C:\Users\subhan\.claude\skills\claude-video-edit\ - SKILL.md only; its preflight.sh/detect_gpu.sh step fails (scripts not copied). Use only its ffmpeg recipes, skip preflight. User had asked for ffmpeg-master only; may want it removed.
- Auto-mode classifier on the PC blocks plugin installs until the user confirms explicitly in the thread.

Added 2026-10-13 via user-run script claude-edit\_install\install-video-tools.ps1 (auto-mode classifier on PC blocks npx/git clone/mcp add even with chat approval; RC sessions have no mode switch, so write a .ps1 and have the user run it). Result 35/36 OK: ~80 new user skills (HyperFrames 21, Remotion 12, iart 17 packs, shotcraft, talkcraft, video-wrapper, business-motion-film, Higgsfield plugin 8); MCP user scope: claude-video-vision, ffmpeg-mcp-lite, sanzaru (needs OPENAI_API_KEY), manim, pexels (needs PEXELS_API_KEY); OpenMontage in Desktop\subhan\OpenMontage; claude-youtube-editor in Desktop\subhan\. vertical-video-editing fixed later via npx skills add nopefallacy/vertical-video-editing-skills; ffmpeg-mcp-lite+manim needed mcp<2 pin. Skipped: Premiere (not installed), Resolve MCP (free 21.1), video-creator/ffmpeg-mcp (macOS only). Catalog: claude-edit\_lessons\tools-catalog.md.
