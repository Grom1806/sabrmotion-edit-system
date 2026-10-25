# 2026-10-25 · iPhone Duo v3 (rebuild after AI-slop audit)

- Source: one take of a talking head, 25.5 s after cuts; built in code (HyperFrames), no AE.
- Fixed from the v2 audit:
  - Unbounded + 3-colour palette replaced by the "Белая студия" look (paper #F2F4F5, ink #111114, one blue accent used only in the bar).
  - Fonts: Noto Serif Display (headings) + Golos Text (subtitles).
  - Glow removed; subtitles are now phrases with a dark shadow.
  - Only 2 hero words: "нет." and "не советую".
  - Real official Apple footage (downloaded via Remote Control + yt-dlp on the PC, because the cloud copy is blocked by YouTube).
- Moves: square→scene price infographic that shrinks into a top card to reveal the face; line→card for the MacBook, which turns into 3 drawn iPads; the final loops back to the white first frame.
- Audio: 43 SFX (1.7/s), quiet room tone −48 dBFS, −14 LUFS.
- Lessons:
  - Subtitles must not sit over the hero product; remove them on the hook.
  - Check text clipping by the clip-path.
  - Spaces between inline-block words need margins.
  - Never `pkill -f` with a pattern that matches your own shell.
  - device_commit_files is limited to 25 MB per file; send the 1080 copy to the PC.
  - Price on screen = Apple's official figure, even if the speaker rounds it.

## v3.1 (после автопроверки readcheck)
- `readcheck` на v3 нашёл 13 мест, где текст держался меньше нормы, и 7 наездов надписей. Среди них: «3 iPad» 0.17 с из-за раннего ухода карточки, фраза-источник из 11 слов на 1.4 с, наезды соседних субтитров на 0.03–0.1 с, «лучше купить» поверх «не советую».
- Исправлено:
  - слова-герои держатся дольше;
  - «3 iPad» появляется раньше, карточка уходит позже;
  - источник сокращён до «Цены Apple, США»;
  - субтитр уходит до первого слова следующего;
  - финал продлён на 0.4 с, «или» перекрашивается в чернила на бумаге (было белым по белому).
- Осталось 3 мелких отклонения ≤0.18 с. Они сознательные: субтитры, синхронные с быстрой речью.
- `clean_cut.py` на этом исходнике сам нашёл оба брошенных дубля хука, результат совпал с ручной чисткой.
