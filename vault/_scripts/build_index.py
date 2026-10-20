#!/usr/bin/env python3
"""Regenerates 00-start/INDEX.md from note frontmatter (title, tags, summary).
Run from the vault root:  python _scripts/build_index.py
INDEX is the only file Claude reads in full; it then opens just the notes it needs."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
GROUPS = [("00-start", "Старт и система v2 (читать первым)"), ("07-system", "Система монтажа v2 (читать перед каждым роликом)"), ("01-rules", "Правила (всегда действуют)"), ("02-brands", "Бренды"),
          ("03-techniques", "Техники"), ("05-research", "Исследования"),
          ("04-lessons", "Уроки"), ("06-tools", "Инструменты")]


def fm(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    d = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                d[k.strip()] = v.strip()
    return d


lines = ["---", "title: INDEX", "type: moc", "tags: [moc]",
         "summary: Карта всех заметок с одной строкой о каждой (генерируется скриптом)", "---", "",
         "# INDEX — карта vault", "",
         "Генерируется `python _scripts/build_index.py`. Не править руками.", ""]
total = 0
for folder, label in GROUPS:
    notes = [n for n in sorted((ROOT / folder).rglob("*.md")) if n.stem != "INDEX"]
    if not notes:
        continue
    lines += [f"## {label}", ""]
    for p in notes:
        d = fm(p.read_text(encoding="utf-8"))
        kb = p.stat().st_size / 1024
        lines.append(f"- [[{p.stem}]] ({kb:.1f} KB) {d.get('tags', '')} — {d.get('summary', '')}")
        total += 1
    lines.append("")
(ROOT / "00-start/INDEX.md").write_text("\n".join(lines), encoding="utf-8")
print(f"INDEX.md: {total} notes")
