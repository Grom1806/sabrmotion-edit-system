---
name: github-backup
description: Vault/edit system is backed up to private GitHub repo Grom1806/sabrmotion-edit-system, also installable as a skill
metadata:
  type: project
  modified: 2026-10-20T23:50:25.977Z
---

2026-10-20 user asked to push the whole edit system to GitHub so it can't be lost and can be installed in other accounts ("like a skill").

Repo (private, user creates it himself; Claude can't create repos): Grom1806/sabrmotion-edit-system. Layout: SKILL.md (entry point), README.md, vault/ (merged PC + cloud mirror, newer file wins; first two commits keep each side's raw snapshot), project-memory/ (copy of this memory dir), tools/make_skill_zip.py -> dist/sabrmotion-edit-system.zip (text-only, ~600 KB) for claude.ai skill upload. Zip copy at /mnt/project-files/github-backup/.

On 2026-10-20 PC vault and cloud mirror had diverged (82 PC-only, 10 cloud-only, 26 edited on both sides).

**How to apply:** on "обнови бэкап": tar PC claude-edit\vault (exclude .smart-env) into claude-edit\_github-backup\, stage it, merge with /mnt/project-files/vault/ (newer mtime wins), refresh project-memory/, commit, push. Links: [[knowledge-vault]], [[edit-system-v3]].
