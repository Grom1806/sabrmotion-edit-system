# HyperFrames-кит — монтаж без After Effects

Шаблон ролика на HTML + GSAP с помощниками по нормам vault. Полная инструкция и таблица «свойство AE → код»: `vault/07-system/no-ae-pipeline.md`.

```
template/
  index.html        композиция 1080×1920: сцены, ключи времени, вызовы помощников (пример 12.4 с)
  lib/sabr.js       letters / words / counter / grow / lineToBlock / pop / cam / defocus / captions / finish
  sfx_map.json      вид события → файлы claude-edit\assets\sfx (якорь начало/пик, обрезка)
  gaps.json         паузы-вдохи после слов
  tools/            tts → words → gaps → inject → dump → mix → verify_solo → qa, build.cjs (всё по порядку)
  assets/fonts/     Unbounded, Manrope (OFL)
```

Запуск (из папки ролика, куда скопирован template):
```
node tools/build.cjs <слаг>                        # без голоса
node tools/tts.js fv3LKrS09h3gGy4GZW1e .tmp/vo/take1 script.txt   # голос пользователя (.tmp/vo создать заранее)
node tools/build.cjs <слаг> --take take1 --tempo 1.05
node tools/build.cjs <слаг> --draft                # быстрый черновик
npx --yes hyperframes@0.8.140 preview              # студия со скраббером («таймлайн»)
```
Выход: `out/<слаг>_master.mp4` (CRF 14), `out/<слаг>_1080.mp4` (CRF 18), `_sheet.jpg`, `_QA.md`, `_reading_time.md`, `_sharpcheck.txt`; SFX-аудит `.tmp/sfx_audit.tsv`, сдвиги `.tmp/sfx_placement.txt`.
Без библиотеки звуков (облако): `SABR_SYNTH=1` — шумовые заглушки, только для теста. Папка библиотеки: env `SABR_SFX` (по умолчанию `../../assets/sfx/` от папки ролика в `claude-edit\reels\`).
