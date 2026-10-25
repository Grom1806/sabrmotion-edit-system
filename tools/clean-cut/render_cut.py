#!/usr/bin/env python3
"""Склейка по segs.json: видео trim/concat, звук с кроссфейдом 15 мс на каждом резе.
  python3 render_cut.py исходник.mp4 segs.json cut.mov [--xf 0.015]
"""
import json, subprocess, sys, tempfile

src, segs_path, out = sys.argv[1:4]
xf = float(sys.argv[sys.argv.index("--xf") + 1]) if "--xf" in sys.argv else 0.015
s = json.load(open(segs_path)); h = xf / 2
fc = []
for i, (a, b) in enumerate(s):
    fc.append(f"[0:a]atrim={max(0, a - h):.4f}:{b + h:.4f},asetpts=PTS-STARTPTS[a{i}]")
    fc.append(f"[0:v]trim={a:.4f}:{b:.4f},setpts=PTS-STARTPTS[v{i}]")
prev = "a0"
for i in range(1, len(s)):
    fc.append(f"[{prev}][a{i}]acrossfade=d={xf}:c1=tri:c2=tri[x{i}]"); prev = f"x{i}"
fc.append("".join(f"[v{i}]" for i in range(len(s))) + f"concat=n={len(s)}:v=1:a=0[v]")
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
    f.write(";".join(fc)); script = f.name
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex_script", script, "-map", "[v]", "-map", f"[{prev}]",
                "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "pcm_s16le", "-ar", "48000", out], check=True)
print("ok", out, f"{sum(b - a for a, b in s):.2f} s")
