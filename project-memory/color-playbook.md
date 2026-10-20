---
name: color-playbook
description: Accumulated color-grading techniques for talking-head reels (ffmpeg chains, DJI/phone sources, checks); read before every edit
metadata:
  type: project
  modified: 2026-10-07T23:37:26.672Z
---

Living playbook, grown after each reel (see [[edit-lessons-log]]). Status: reels 1-2 (2026-10-07) shipped WITHOUT any grade; reel 3 must be the first graded one.

**Tools (2026-10-07):** ffmpeg-master plugin is installed on the PC: use `/ffmpeg-color` and its color-grading-chromakey skill to build the chain below.

**Order:** grade the cut footage (`.tmp/cut.mp4`) BEFORE copying it into `project/assets/`, so HyperFrames graphics stay ungraded and their brand colors (`#c8623c`) stay exact.

**1. Identify the source first** (`ffprobe -show_streams`): color_transfer / color_primaries.
- bt709 phone footage: normal grade.
- DJI D-Log M / D-Log: apply DJI's official Rec.709 LUT first: `lut3d=file=dlogm_709.cube:interp=tetrahedral`, then grade. LUT file lives with the toolkit, not in the repo.
- HLG/HDR10 (arib-std-b67 / smpte2084): tone-map `zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p`.
- Always tag output: `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`.

**2. Measure, don't guess:** `signalstats` on ~1 fps: YAVG (target ~110-130 of 255 for a face), YMIN/YMAX (want ~16/235), UAVG/VAVG (~128 = neutral; V>132 too warm/magenta, U>132 too blue). Correct white balance with `colorbalance` or `colortemperature` until U/V near 128 on neutral areas.

**3. Base look chain (start, then tune):**
`eq=contrast=1.06:saturation=1.08:gamma=0.98, curves=master='0/0.02 0.25/0.22 0.5/0.5 0.75/0.79 1/0.98', colorbalance=rs=-0.02:bs=0.03:rh=0.03:bh=-0.02, vignette=PI/5, unsharp=5:5:0.4, noise=alls=2:allf=t`
(gentle S-curve, teal shadows / warm highlights, lifted blacks for a filmic feel, light grain hides banding.)

**4. Skin tones are the priority:** never push global saturation past ~1.15; if skin goes orange use `selectivecolor=reds='0 0.02 0.04 0':yellows='0 0 0.05 0'` or lower saturation and add `vibrance=0.15` instead.

**5. Verify:** export before/after frames side by side (`hstack`) into a contact sheet and look at it; recheck signalstats; check graphics contrast still passes `hyperframes check`.

**Why:** user asked (2026-10-07) for professional color work and for Claude to learn from every edit.
**How to apply:** read this + [[motion-playbook]] before an edit; append what actually worked (exact numbers) after it.

**CORRECTION (2026-10-20, test 2 akimbosd):** user: "плохая цветокоррекция, видео тёмное". The base chain above is outdated: drop `vignette` and `noise` (NO GRAIN rule), no gamma <1 or curves that darken. Grade must never make the face darker than the raw source: compare YAVG of face vs raw (face ~60-70 IRE), keep shadows uncrushed, save before/after hstack frames and check before delivery.
