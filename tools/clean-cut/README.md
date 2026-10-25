# clean-cut — чистка дублей, запинок и пауз

```
python3 clean_cut.py words.json voice16k.wav [--keep 17.3:0.32] [--thr -44] [--start 2.0] --out segs.json --report cut_report.md
python3 render_cut.py source.mp4 segs.json cut.mov
```
`words.json` — слова faster-whisper (`word_timestamps=True`): `[{"w","s","e","p"}]`.
Методика: vault/03-techniques/clean-cut-pro.md. Отчёт обязательно прослушать.
