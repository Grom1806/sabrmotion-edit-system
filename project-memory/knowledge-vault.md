---
name: knowledge-vault
description: Obsidian vault = single source of truth for editing knowledge; read START + INDEX + rules, then only the needed notes
metadata:
  type: project
---

2026-10-13 user asked for one working knowledge system (rules, brandbooks, techniques, research, lessons) in an Obsidian vault, saving tokens, with vector-style search.

Mirror: /mnt/project-files/vault/ (00-start/START.md protocol + INDEX.md, 01-rules, 02-brands, 03-techniques incl. motion/ = motion_library split per section, 04-lessons (+reels/ one note per reel), 05-research = brand styles K1-K9, 06-tools, _templates, _scripts/build_index.py). PC master copy installed 2026-10-13 at claude-edit\vault\ (44 notes; cloud mirror synced with PC on 2026-10-14 incl. 06-tools/tools-catalog.md). PC auto-mode classifier blocks tar extraction, running scripts from the archive and sending notes to the cloud: the user has to run such commands or confirm them; old lessons/, style/, _lessons\ are frozen archives.

**How to apply:** before an edit read vault START + INDEX + all 01-rules, then only the notes for the chosen tier/brand/move. After a reel add a note in 04-lessons/reels/ from the template and rerun build_index.py. Semantic search for the user = Smart Connections plugin (local embeddings); for Claude, INDEX + tags + rg. See [[edit-lessons-log]], [[motion-playbook]].
