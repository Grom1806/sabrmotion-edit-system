# matte — маска человека (текст и окна «за головой» без After Effects)

```
python3 matte.py head.mp4 out_dir models_dir
```
- **Выход:**
  - `person.webm` — человек с альфой, VP9 yuva420p;
  - `track.json` — по кадрам `{t, face:[x,y,w,h], top}`.
- **Модели MediaPipe:** selfie_multiclass_256x256 (сегментация) и blaze_face_short_range (лицо). Сохранить как `selfie_multiclass.tflite` и `face_detector.tflite`.
- **Слой в HyperFrames:** `<video src="person.webm">` поверх текста, который должен уйти «за голову». Двигать в той же обёртке камеры, что и видео головы.
- **Качество:** края смягчены на 1.5 px, сглаживание по времени 0.6/0.4. На тёмном фоне за волосами проверять кадры 1:1.
