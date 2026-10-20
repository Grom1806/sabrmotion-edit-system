---
title: Цветокор: плейбук
type: technique
tags: [technique, color, ffmpeg]
summary: Цепочки ffmpeg для грейда: определить источник (bt709/D-Log/HLG), замерить signalstats, базовый look, кожа
updated: 2026-10-13
source: lessons/color-playbook.md
---
# Цветокор: плейбук

**Tools (2026-10-07):** ffmpeg-master plugin is installed on the PC: use `/ffmpeg-color` and its color-grading-chromakey skill to build the chain below.

Living playbook, grown after each reel (see [[edit-lessons-log]]). Status: reels 1-2 (2026-10-07) shipped WITHOUT any grade; reel 3 must be the first graded one.

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

**Used on reel 2 v2 (DJI Osmo Nano, bt709, low-key room):** eq=contrast=1.06:saturation=0.92, curves master 0/0 0.08/0.012 0.22/0.17 0.45/0.47 0.70/0.76 1/0.96, colorbalance rs=.02 bs=-.03 rm=.03 gm=.005 bm=-.03 bh=-.02, selectivecolor reds 0 .03 .03 0 / whites 0 0 .03 -.03, vignette PI/5, noise alls=3. YAVG 47 -> 32 (face stays readable, background to black) - close to ref 6708 low key. A first try with brightness -0.025 + steeper curve gave YAVG 27: too dark.

**Why:** user asked (2026-10-07) for professional color work and for Claude to learn from every edit.
**How to apply:** read this + [[motion-playbook]] before an edit; append what actually worked (exact numbers) after it.
