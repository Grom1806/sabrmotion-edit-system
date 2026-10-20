"""Собирает dist/sabrmotion-edit-system.zip для загрузки как skill в claude.ai
(Settings -> Capabilities -> Skills -> Upload). В архив идут SKILL.md и текстовые
заметки vault без картинок, чтобы архив был лёгким."""
import pathlib, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = "sabrmotion-edit-system"
KEEP = {".md", ".py", ".jsx", ".html", ".json", ".csv", ".txt"}
SKIP_DIRS = {".obsidian", ".smart-env"}

out = ROOT / "dist" / f"{NAME}.zip"
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT / "SKILL.md", f"{NAME}/SKILL.md")
    for folder in ("vault", "project-memory"):
        for p in sorted((ROOT / folder).rglob("*")):
            if p.is_file() and p.suffix.lower() in KEEP and not SKIP_DIRS & set(p.parts):
                z.write(p, f"{NAME}/{p.relative_to(ROOT).as_posix()}")
print(out, round(out.stat().st_size / 1024), "KB")
