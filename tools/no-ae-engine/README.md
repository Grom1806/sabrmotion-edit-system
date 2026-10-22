# nae — Python-движок монтажа без After Effects

Для документального моушена, проездов камеры с настоящим motion blur, фото-коллажей и всего, что удобнее считать пикселями. Описание и выбор движка: `vault/07-system/no-ae-pipeline.md`.

Нужно: Python 3.10+, `numpy`, `opencv-python-headless`, `Pillow`, ffmpeg в PATH.

```
python -m nae.run examples/demo_docu.py --out out/demo                  # рендер + микс + master/light + QA + лист
python -m nae.run project.py --out out --frames 1.2,6.0,12.5            # стиль-фреймы PNG
python -m nae.run project.py --out out --draft                          # черновик 540×960
python -m nae.run project.py --out out --voice voice.wav --sfx-root C:/Users/subhan/Desktop/subhan/claude-edit/assets/sfx
```
Проект — `.py` с `build() -> Comp` (пример `examples/demo_docu.py`). Слои: `Text` (буквы/слова, тик на букву, блюр только у заголовков ≥ 60 px), `Counter`, `Box` (из точки/линии/угла, рост контейнера), `Picture` (без апскейла), `Path` (trim path), `Clip` (видео с грейдом ffmpeg); `CamTrack` (станции с зумом ровно 1), `Defocus` (расфокус-переход). Звуки берутся из событий слоёв (`events.json`), карта `sfx_map.json`.
QA (`out/qa/report.md`): апскейл, резкость видео vs рендер ≥ 0.9, без зерна/мерцания, время чтения, буква = тик, нет звуков без события, нет звуковой каши, проявление не прерывается, поля ≥ 60 px, первый кадр, −14 LUFS / TP ≤ −1.
