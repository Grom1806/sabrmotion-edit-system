---
title: ae-pipeline-research
type: research
tags: [research, system-v2]
summary: Полный ресерч 2026-10-19 для системы монтажа v2 (источник для 07-system)
updated: 2026-10-19
source: веб-ресерч + браузер ПК, тред «аудит монтажа»
---
# After Effects как основной motion-инструмент агента: практический пайплайн для вертикальных Reels

Контекст: Windows, RTX 5080, After Effects 2026 (v26.x) через MCP-мост (ExtendScript), Blender 5.2 MCP, ffmpeg, HyperFrames/GSAP, ElevenLabs, Higgsfield. Цель: уйти от «генерического HTML-вида» к AE-графике уровня моушн-дизайнера.

Пометка: всё, что ниже помечено **[проверить]**, я вывел сам (по API или по опыту) и не нашёл подтверждения в источниках. Такие места нужно один раз проверить на своей машине.

---

## 0. Главные выводы (TL;DR)

1. **Не стройте графику с нуля скриптом.** Самый большой прирост качества даёт **мастер-проект .aep с заранее задизайненными прекомпами** (титры, плашки, подложки, переходы, «hero»-элементы), у которых наружу выведены параметры (Essential Properties, Slider/Color/Checkbox Controls). Агент дублирует прекомпы, подставляет текст, цвета и тайминги из JSON и рендерит. Генерация «с нуля» через `addText`/`addShape` упирается в тот же generic-вид, что и HTML.
2. **Одна сборка = один большой JSX.** MCP-мосты для AE работают через опрос файлов: панель внутри AE раз в N секунд читает `ae_command.json`. Десятки мелких tool-вызовов медленные и хрупкие. Правильно так: агент пишет `timeline.json` и `build.jsx`, затем делает один вызов `run-script`/`execute-script`, который собирает всё внутри одной undo-группы.
3. **Рендер: `aerender` в фоне, а не `renderQueue.render()`.** Рендер из скрипта блокирует UI и мост, и MCP-вызов отваливается по таймауту. Формат выходного модуля из скрипта выставить нельзя, поэтому один раз создайте Output Module-шаблоны в UI и затем применяйте их по имени.
4. **То, что не скриптуется** (Roto Brush, Mocha, анализ 3D Camera Tracker, Warp Stabilizer по сути, UI-расширения вроде Flow/Motion Bro/Overlord), выносится наружу. Маски человека делаются нейросетевым маттингом в Python на 5080 (MatAnyone / RVM / SAM 2), трекинг делается в Blender (bpy-скриптуемый) или через MediaPipe, ключи пишутся в AE через `setValuesAtTimes`.
5. **Говорящую голову лучше класть внутрь AE-компа** (полный рендер в AE), если нужен текст за человеком, трекинг или общий грейд и зерно. ProRes 4444 с альфой плюс ffmpeg-оверлей годится для простых оверлеев.

---

## 1. Какие есть MCP-серверы для AE и что они умеют

| Проект | Архитектура | Что даёт | Замечания |
|---|---|---|---|
| **a-y-ibrahim/after-effects-mcp** — https://github.com/a-y-ibrahim/after-effects-mcp | Node/TS-сервер, ScriptUI-панель `mcp-bridge-auto.jsx` в AE, обмен через папку `%LOCALAPPDATA%\ae-mcp-bridge` | 57 инструментов: инспекция (`see-frame`, `contact-sheet`, `match-reference`, `inspect-comp/layer`), композиции и слои, `populate-template`, `precompose-layers`, `animate-from-data`, `animate-to-audio`, эффекты (`add-any-effect`, `set-effect-property/keyframe`, `apply-effect-template`), пресеты (`search/apply-preset`), маркеры, аудиоанализ, рендер (`add-to-render-queue`, `render-aerender`, `render-status`), `execute-script` (произвольный ExtendScript) | Самый полный набор для агента. ID на каждую команду (без «протухших» результатов), одна undo-группа на команду, `check-bridge` проверяет версию. AE 2022+, Node 18+. OneDrive может мешать общей папке, путь переопределяется через `AE_MCP_BRIDGE_DIR` |
| **Dakkshin/after-effects-mcp** — https://github.com/Dakkshin/after-effects-mcp (`npx -y after-effects-mcp`) | Тот же паттерн: панель опрашивает команды каждые несколько секунд при включённом «Auto-run commands» | `create-composition`, `run-script`, `get-results`, `setLayerKeyframe`, `setLayerExpression`, `setLayerProperties`, `batchSetLayerProperties`, `createCamera`, `createNullObject`, `setLayerMask`, `duplicate/deleteLayer` | Оригинал, от которого пошли форки (~760★ по https://prismix.dev/mcp/dakkshin-after-effects-mcp) |
| **TheLlamainator/after-effects-mcp** — https://mcpservers.org/de/servers/thellamainator/after-effects-mcp | Файловый мост (`ae_command.json` → `ae_mcp_result.json`) | Эффекты и пресеты, маркеры, аудиоанализ (WAV), диагностика | Результаты асинхронные: команда может вернуть «queued», потом нужен `get-results` |
| **kumoproductions/mcp-aftereffects** — https://github.com/kumoproductions/mcp-aftereffects | Файловый IPC через mailbox в temp. Опционально резидентный стартап-скрипт в `Scripts/Startup`, панель не нужна | `ae_context`, `ae_do` (операции), `instance.start/stop`, **`instance.dialogs` / `instance.dismiss_dialog`** (закрывает блокирующие модальные окна), `project.open/merge`, рендер кадров. Несколько инстансов AE (`AfterFX.exe -m`) как воркеры | AE 2024–2026, Node 24+. Произвольный ExtendScript по умолчанию выключен. Хорошо продумана работа с модальными диалогами |
| **p10q/ae-mcp** — https://github.com/p10q/ae-mcp | Документации почти нет (https://mcpservers.org/servers/p10q/ae-mcp) | — | Не рекомендую как основной |

**UXP для AE.** Adobe ведёт бету UXP для After Effects (https://developer.adobe.com/after-effects/uxp/). В справочнике API (например, OutputModule, https://developer.adobe.com/after-effects/uxp/after-effects-api/outputmodule) указан минимум «27.0». Значит, в продакшене на AE 2026 (26.x) основным остаётся **ExtendScript (ES3)**, а UXP ждёт следующего мажора **[проверить]**.

### Общие ограничения мостов (важно для агента)

- **AE должен быть полностью загружен, а панель моста открыта** (Window → mcp-bridge-auto.jsx). Холодный старт AE со шрифтами и плагинами занимает 30–90 с. Перед сборкой нужен `check-bridge` или ping-скрипт.
- **Модальные диалоги блокируют весь скриптинг**: missing footage/fonts, crash recovery и Safe Mode после падения, апдейты, лицензии плагинов. Помогает обёртка `app.beginSuppressDialogs()` … `app.endSuppressDialogs(false)`, а для того, что вылезает при старте, нужен kumo-подобный `dismiss_dialog` (https://github.com/kumoproductions/mcp-aftereffects).
- В настройках должен быть включён Preferences → Scripting & Expressions → **Allow Scripts to Write Files and Access Network**.
- **Скорость ExtendScript.** Каждое обращение к DOM AE дорогое. Ключи ставьте пачкой через `prop.setValuesAtTimes(times, values)`, а не циклом `setValueAtTime`. Не держите открытым тяжёлый комп во вьювере во время сборки (Caps Lock в AE отключает обновление вьювера). Всё делайте в одной `app.beginUndoGroup`.
- **В ExtendScript нет `JSON`** (это ES3). Подключайте `json2.js` через `#include` / `$.evalFile` или используйте `eval('(' + str + ')')` для доверенных файлов **[проверить на вашем мосте: некоторые мосты сами подкладывают полифилл]**.
- **`renderQueue.render()` синхронный**: UI и мост висят до конца рендера. Используйте `aerender` отдельным процессом (у a-y-ibrahim есть `render-aerender`).

---

## 2. Безголовый рендер и настройки вывода

### 2.1 aerender (основной путь)

Путь: `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\aerender.exe`. Опции (https://helpx.adobe.com/en/after-effects/using/automated-rendering-network-rendering.html):

- `-project`, `-comp` (без него рендерится вся очередь), `-rqindex`, `-s/-e` (кадры, конец включительно), `-i`
- `-RStemplate` / `-OMtemplate`: **по имени шаблона**. Если шаблона нет, команда падает
- `-output`, `-log`, `-v ERRORS_AND_PROGRESS`
- `-mfr ON 90`: Multi-Frame Rendering с лимитом CPU. Флага `-mp` больше нет
- `-mem_usage image_cache_% max_mem_%`
- `-reuse`: рендер в уже запущенном AE (UI будет занят). Без флага запускается отдельный инстанс, это как раз то, что нужно агенту
- `-continueOnMissingFootage`: вместо остановки подставляет цветные полосы. **Для QA лучше не включать**, пусть падает
- `-close DO_NOT_SAVE_CHANGES|SAVE_CHANGES|DO_NOT_CLOSE`

aerender читает **сохранённый** .aep, поэтому перед рендером нужен `app.project.save(File(path))`.

```bat
"C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\aerender.exe" ^
  -project "D:\reels\ep042\build\ep042.aep" -comp "MAIN_1080x1920" ^
  -RStemplate "Best Settings" -OMtemplate "REELS_ProRes4444_Straight" ^
  -output "D:\reels\ep042\render\gfx.mov" ^
  -mfr ON 90 -v ERRORS_AND_PROGRESS -log "D:\reels\ep042\render\aerender.log"
```

Для быстрого превью сделайте свой RS-шаблон «Draft_Half» (Resolution Half, Motion Blur Off) и рендерьте им же.

### 2.2 Очередь рендера из скрипта (подготовка для aerender)

Формат выходного модуля **из скрипта не выставляется** (getSettings может его прочитать, setSettings не может), поэтому нужны шаблоны (https://ae-scripting.docsforadobe.dev/renderqueue/outputmodule/). Один раз в UI создайте через Edit → Templates → Output Module:

- `REELS_H264`: H.264, 1080×1920, 40 Mbps preset, AAC 48 kHz. Нативный H.264 в очереди есть с AE 23 и умеет аппаратное кодирование; пресеты 5/15/40 Мбит/с (https://helpx.adobe.com/after-effects/desktop/render-and-export/export-h-264-from-the-after-effects/exporting-h264-from-the-after-effects-render-queue.html)
- `REELS_ProRes4444_Straight`: QuickTime, Apple ProRes 4444, Channels **RGB + Alpha**, Depth Trillions/Millions+, Color **Straight (Unmatted)**
- `REELS_ProRes422HQ`: мастер без альфы для финальной упаковки в ffmpeg
- `REELS_PNG_Seq`: PNG RGBA. Самый надёжный вариант для альфы и докомпозитинга, переживает падения (можно дорендерить с кадра)

```javascript
// queue_render.jsx — подготовить элемент очереди (рендер запускать aerender'ом)
(function () {
  var comp = findComp("MAIN_1080x1920");
  var rq = app.project.renderQueue;
  while (rq.numItems > 0) rq.item(1).remove();          // чистая очередь
  var item = rq.items.add(comp);
  item.applyTemplate("Best Settings");
  var om = item.outputModule(1);
  om.applyTemplate("REELS_ProRes4444_Straight");
  om = item.outputModule(1);                              // после смены настроек OM может «протухнуть», берём заново
  om.file = new File("D:/reels/ep042/render/gfx.mov");
  app.project.save();
  function findComp(n){for(var i=1;i<=app.project.numItems;i++){var it=app.project.item(i);if(it instanceof CompItem&&it.name===n)return it;}throw new Error("no comp "+n);}
})();
```

Через Media Encoder: `app.project.renderQueue.queueInAME(true)`. Но пресеты AME из AE-скрипта не контролируются, поэтому для агента aerender предсказуемее.

### 2.3 Финальное кодирование (ffmpeg)

Рекомендую рендерить из AE ProRes 422 HQ или 4444, а для платформы кодировать в ffmpeg (контроль CRF, тегов цвета, faststart):

```bash
# финал Reels: H.264 High, BT.709, 30 fps CFR
ffmpeg -i master.mov -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -r 30 -c:a aac -b:a 320k -ar 48000 -movflags +faststart final.mp4
# быстрее на RTX 5080:
ffmpeg -i master.mov -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 18 -b:v 0 -pix_fmt yuv420p ... final.mp4
# ProRes 4444 с альфой из PNG-секвенции:
ffmpeg -framerate 30 -i gfx_%05d.png -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le -alpha_bits 16 gfx.mov
# оверлей альфы на голову (overlay по умолчанию ждёт straight alpha; для premultiplied — alpha=premultiplied)
ffmpeg -i talking.mp4 -i gfx.mov -filter_complex "[0][1]overlay=0:0:format=auto" ...
```

---

## 3. Лучшие практики скриптовой сборки в AE

### 3.1 Архитектура: мастер-проект + JSON-таймлайн

```
D:\reels\_brand\MASTER_v07.aep        ← дизайн-библиотека (не трогать агентом напрямую)
   ├─ 00_GUIDES (safe zones, сетка)
   ├─ LIB_Title_Kinetic_A (precomp, Essential Properties: Text, Accent Color, Scale)
   ├─ LIB_Caption_WordPop (precomp + Expression controls)
   ├─ LIB_Callout_Arrow, LIB_Number_Counter, LIB_Transition_Swipe, LIB_BG_Gradient_Noise
   └─ LIB_Grade_Grain (adjustment: Lumetri/Curves + Add Grain + Vignette)
D:\reels\ep042\
   ├─ timeline.json   ← агент генерирует
   ├─ build.jsx       ← общий сборщик (версионируется в git)
   └─ build\ep042.aep ← результат (копия мастера + сборка)
```

Как это работает: сборщик копирует MASTER в `ep042.aep` (или импортирует через `app.project.importFile` и `ImportOptions`), создаёт `MAIN_1080x1920`, кладёт футаж и для каждого события JSON дублирует нужный `LIB_*` прекомп (`item.duplicate()` или просто `comp.layers.add(libComp)`, если параметры вынесены в Essential Properties), ставит `startTime/inPoint/outPoint`, пишет текст и параметры.

**Master Properties / Essential Properties** — ключ к шаблонам. Свойства внутри прекомпа добавляются в Essential Graphics (`prop.addToMotionGraphicsTemplate(comp)`; проверка: `prop.canAddToMotionGraphicsTemplate(comp)`), и на каждом экземпляре-слое прекомпа их можно переопределять отдельно, не дублируя прекомп. Экспорт .mogrt: `comp.exportAsMotionGraphicsTemplate(true, path)` (https://helpx.adobe.com/ca/after-effects/desktop/automate-in-after-effects/automate-animation/scripts.html; известен баг возвращаемого значения в 24.2: https://community.adobe.com/bug-reports-528/after-effects-24-2-1-exportasmotiongraphicstemplate-not-returning-correct-value-1217054). Доступ к переопределениям на слое идёт через группу `"ADBE Layer Overrides"` (Essential Properties) **[проверить имена на своём шаблоне: пройдитесь по `layer.property("Essential Properties")` и выведите `matchName`]**. Для агента это проще и надёжнее, чем дублировать прекомп на каждый титр.

**Альтернатива (data-driven рендер без GUI): nexrender** (https://github.com/inlife/nexrender, форк с документацией: https://github.com/inmagik/nexrender). Job-JSON описывает шаблон .aep, композицию и ассеты (`image/audio/video` для замены футажа, `data` для свойства или выражения, `script` для JSX до рендера с параметрами через `NX`). Дальше aerender и postrender-экшены (`action-encode`, `action-copy`). Полезно, когда шаблоны стабилизировались и нужен конвейер «JSON → mp4» вообще без участия GUI-моста.

### 3.2 JSON-таймлайн из word timings

Источники таймингов:
- ElevenLabs TTS «with timestamps» отдаёт посимвольное выравнивание, слова собираются из символов. Для готовой записи голоса есть Forced Alignment от ElevenLabs.
- Для отснятой говорящей головы используйте WhisperX (word-level) локально на 5080.

Пример формата:

```json
{
  "fps": 30, "w": 1080, "h": 1920, "duration": 38.4,
  "footage": [{"path": "D:/reels/ep042/src/talk_cfr30.mov", "start": 0}],
  "matte": "D:/reels/ep042/src/talk_matte_[00000-01151].png",
  "words": [{"w":"Нейросети","s":0.42,"e":0.98},{"w":"делают","s":0.98,"e":1.31}],
  "events": [
    {"type":"title","lib":"LIB_Title_Kinetic_A","s":0.4,"e":2.6,"text":"НЕЙРОСЕТИ\nДЕЛАЮТ МОНТАЖ","accent":[1,0.36,0.1],"behind":true},
    {"type":"callout","lib":"LIB_Number_Counter","s":6.2,"e":8.0,"value":87,"suffix":"%"},
    {"type":"sfx","name":"whoosh_03","s":0.35}
  ]
}
```

Субтитры по словам. Вариант A: один текстовый слой на фразу (2–4 слова), подсветка текущего слова через Expression Selector, который читает маркеры слоя (маркеры ставятся пачкой). Вариант B: `sourceText.setValuesAtTimes(times, textDocs)` с HOLD-интерполяцией. A красивее (анимация на уровне символов), B проще.

```javascript
// маркеры для слов одной фразы — потом их читает выражение
var mv = []; var tm = [];
for (var i = 0; i < words.length; i++) {
  var m = new MarkerValue(words[i].w); m.duration = words[i].e - words[i].s;
  tm.push(words[i].s - layer.startTime); mv.push(m);
}
for (var j = 0; j < tm.length; j++) layer.property("Marker").setValueAtTime(tm[j], mv[j]);
```

### 3.3 Easing из скрипта: «про»-кривые

`KeyframeEase(speed, influence)`: influence от 0.1 до 100. Для пространственных свойств (Position с separated=false) передаётся один объект на сторону, для многомерных непространственных (Scale и др.) по одному на каждое измерение (https://ae-scripting.docsforadobe.dev/other/keyframeease/).

**Конвертер cubic-bezier → AE.** Позволяет взять кривые из Flow, GSAP или easings.net и перенести их в AE. Для 1D-отрезка между ключами k1(t1,v1) и k2(t2,v2):
- средняя скорость `avg = (v2 − v1)/(t2 − t1)` (для Position это длина пути, делённая на длительность)
- выход из k1: `influence = x1·100`, `speed = (y1/x1)·avg`
- вход в k2: `influence = (1 − x2)·100`, `speed = ((1 − y2)/(1 − x2))·avg`

```javascript
// ease.jsx — применить cubic-bezier к отрезку [k, k+1] любого свойства
function applyBezier(prop, k, x1, y1, x2, y2) {
  var t1 = prop.keyTime(k), t2 = prop.keyTime(k + 1);
  var v1 = prop.keyValue(k), v2 = prop.keyValue(k + 1);
  var dims = (v1 instanceof Array) ? v1.length : 1;
  var spatial = (prop.propertyValueType === PropertyValueType.TwoD_SPATIAL ||
                 prop.propertyValueType === PropertyValueType.ThreeD_SPATIAL);
  function seg(a, b) { return (b - a) / (t2 - t1); }
  var outE = [], inE = [];
  var n = spatial ? 1 : dims;
  for (var d = 0; d < n; d++) {
    var avg;
    if (spatial) { var s = 0; for (var i = 0; i < dims; i++) s += Math.pow(v2[i]-v1[i],2); avg = Math.sqrt(s)/(t2-t1); }
    else avg = dims > 1 ? seg(v1[d], v2[d]) : seg(v1, v2);
    outE.push(new KeyframeEase((y1 / x1) * avg, Math.max(0.1, x1 * 100)));
    inE.push(new KeyframeEase(((1 - y2) / (1 - x2)) * avg, Math.max(0.1, (1 - x2) * 100)));
  }
  prop.setInterpolationTypeAtKey(k, prop.keyInInterpolationType(k), KeyframeInterpolationType.BEZIER);
  prop.setInterpolationTypeAtKey(k + 1, KeyframeInterpolationType.BEZIER, prop.keyOutInterpolationType(k + 1));
  prop.setTemporalEaseAtKey(k, prop.keyInTemporalEase(k), outE);
  prop.setTemporalEaseAtKey(k + 1, inE, prop.keyOutTemporalEase(k + 1));
}
// Пресеты «как у моушн-дизайнеров»:
var EASE = {
  expoOut:  [0.16, 1, 0.3, 1],     // резкий старт, длинное мягкое приземление — дефолт для появлений
  quintOut: [0.22, 1, 0.36, 1],
  inOutQuart:[0.76, 0, 0.24, 1],   // переходы, свайпы
  backOut:  [0.34, 1.56, 0.64, 1], // y>1 даёт overshoot (скорость > avg)
  easyEase: [0.333, 0, 0.667, 1]   // = F9 в AE (speed 0, influence 33.3)
};
```

Дальше практические замечания.

- **«Дорого выглядящая» анимация** — это асимметрия. Выход из ключа короткий (influence 10–30%), вход длинный (70–95%, speed 0). Ещё сюда относятся стаггер 2–4 кадра между элементами, overshoot только на масштабе или повороте, и никогда на opacity.
- Перед нестандартным overshoot для spatial Position сделайте `prop.dimensionsSeparated = true` (или используйте Scale), иначе bezier по пути даёт неожиданные «петли».
- Движение без ключей (inertia/bounce, wiggle по маркерам) лучше держать **выражениями в шаблоне** и управлять ими через Slider Controls (`"ADBE Slider Control"`).

### 3.4 Motion blur, 3D, камера

```javascript
comp.motionBlur = true;            // переключатель композиции
comp.shutterAngle = 180;           // 180–270 для кинетики текста
comp.shutterPhase = -90;
comp.motionBlurSamplesPerFrame = 16;
comp.motionBlurAdaptiveSampleLimit = 128;
layer.motionBlur = true;           // на каждом движущемся слое
layer.threeDLayer = true;
var cam = comp.layers.addCamera("CAM", [comp.width/2, comp.height/2]);
cam.property("ADBE Camera Options Group").property("ADBE Camera Depth of Field").setValue(1);
// рендерер: не хардкодить строку — выбрать из comp.renderers (массив доступных имён)
// var r = comp.renderers; $.writeln(r.join(", ")); comp.renderer = r[<индекс Advanced 3D>];
```

Внутренние имена рендереров (Classic 3D, Cinema 4D, Advanced 3D) разные в разных версиях, поэтому берите их из `comp.renderers` **[проверить на 26.x]**. В AE 26.0 Advanced 3D получил тени от Spot/Parallel, параметрические меши (куб, сфера, тор), нативные Substance-материалы (.sbsar), импорт SVG в шейпы и анимацию до 8 осей вариативных шрифтов (https://www.cgchannel.com/2026/01/adobe-releases-after-effects-26-0-with-native-substance-support/). Для простых «hero»-объектов (иконка, логотип, монета) теперь часто хватает самого AE без Blender.

### 3.5 Эффекты по matchName

`layer.property("ADBE Effect Parade").addProperty(matchName)`. Полезные встроенные:

| Эффект | matchName |
|---|---|
| Gaussian Blur | `ADBE Gaussian Blur 2` |
| Glow | `ADBE Glo2` |
| Fill | `ADBE Fill` |
| Drop Shadow | `ADBE Drop Shadow` |
| Fractal Noise | `ADBE Fractal Noise` |
| Turbulent Displace | `ADBE Turbulent Displace` |
| Lumetri Color | `ADBE Lumetri` |
| Add Grain / Match Grain | `VISINF Grain Implant` / `VISINF Grain Duplication` **[проверить]** |
| CC Light Sweep | `CC Light Sweep` |
| Slider / Color / Checkbox Control | `ADBE Slider Control` / `ADBE Color Control` / `ADBE Checkbox Control` |

**Правило для агента:** не угадывать matchName сторонних плагинов, а один раз снять реестр: `for (i in app.effects) → app.effects[i].displayName, .matchName, .category` и сохранить в `effects_registry.json` (у a-y-ibrahim для этого есть `list-available-effects`). Параметры плагина перечисляются обходом `effect.numProperties`. Многие плагины прячут часть параметров в «Arbitrary Data» или в собственном UI, такие параметры скриптом не выставить.

### 3.6 Текстовые аниматоры из скрипта

matchNames: https://ae-scripting.docsforadobe.dev/matchnames/layer/textlayer/

```javascript
function addFadeUpAnimator(textLayer, stagger) {
  var anims = textLayer.property("ADBE Text Properties").property("ADBE Text Animators");
  var an = anims.addProperty("ADBE Text Animator"); an.name = "FadeUp";
  var props = an.property("ADBE Text Animator Properties");
  props.addProperty("ADBE Text Opacity").setValue(0);
  props.addProperty("ADBE Text Position 3D").setValue([0, 60, 0]);
  props.addProperty("ADBE Text Blur").setValue([12, 12]);
  var sel = an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  var adv = sel.property("ADBE Text Range Advanced");
  adv.property("ADBE Text Range Units").setValue(2);      // 1=percent, 2=index
  adv.property("ADBE Text Levels Max Ease").setValue(100); // Ease High → плавный «хвост»
  var off = sel.property("ADBE Text Percent Offset");
  var t0 = textLayer.inPoint;
  off.setValuesAtTimes([t0, t0 + stagger], [0, 100]);
  applyBezier(off, 1, 0.16, 1, 0.3, 1);
}
```

Шрифты: `textDoc.font` принимает PostScript-имя. Если шрифта нет, AE молча подставит замену. В AE 24+ есть `app.fonts` для проверки наличия **[проверить API на 26.x]**. Делайте проверку перед сборкой.

### 3.7 Пресеты .ffx

`layer.applyPreset(File(".../X.ffx"))` — метод **слоя**. Комп должен быть активным (`comp.openInViewer()`), а целевой слой желательно единственным выделенным (https://community.adobe.com/questions-529/script-for-applying-animation-preset-to-layer-65840). .ffx — лучший способ упаковать сложный «look» (стек эффектов плюс выражения плюс настройки плагинов, включая те, что недоступны скриптом, например Element 3D-сцену или дизайн Optical Flares) и затем применить его одной строкой.

### 3.8 Что НЕ скриптуется (или скриптуется плохо)

| Функция | Статус | Обход |
|---|---|---|
| Roto Brush (в т.ч. Next-Gen/3.x) | Штрихи и propagate через API не создать | Внешний маттинг (MatAnyone, https://arxiv.org/abs/2501.14677; RVM; SAM 2) → PNG-секвенция маски → track matte |
| 3D Camera Tracker | Эффект добавить можно, анализ и «Create Camera» нормально не вызываются. Есть хрупкий `app.executeCommand(id)` по номеру меню, который меняется между версиями (https://community.adobe.com/questions-529/api-for-3d-camera-tracker-30443, список ID: https://www.provideocoalition.com/after-effects-menu-command-ids/) | Трек камеры в Blender через bpy (см. §5) → экспорт камеры в AE как .jsx |
| Mocha AE | Не скриптуется | Планарный трек можно заменить точечным (OpenCV) или Blender plane track |
| Point Tracker / Warp Stabilizer | Запуск анализа не через API | Трекинг лиц и тела через MediaPipe/OpenCV в Python → `setValuesAtTimes` |
| Content-Aware Fill, Scene Edit Detection | Только UI/menu | ffmpeg `scdet` для склеек |
| UI-расширения (Flow, Motion Bro, FX Console, Overlord, Ease and Wizz) | Это панели для человека | Перенести их результат в шаблоны и .ffx или в свой код (bezier-конвертер выше) |
| Формат Output Module | Не выставляется | Шаблоны (§2.2) |

---

## 4. Плагины и встроенные средства для «премиального» вида

Принцип: любой **эффект**-плагин скриптуется как эффект (addProperty по matchName плюс параметры). **Расширения-панели** не скриптуются, но их можно применить заранее при дизайне шаблонов.

| Инструмент | Тип / цена | Зачем | Скриптуемость агентом |
|---|---|---|---|
| **Deep Glow 2** (aescripts, https://aescripts.com/deep-glow) | эффект, $99.95 | Физически правдоподобное свечение, тональное отображение, линзовая грязь — сразу «кинематографичный» неон и UI-glow | Да, параметры эффекта |
| Glow (встроенный) + Gaussian Blur в стеке | бесплатно | Бюджетный вариант glow (2–3 копии с разным радиусом) | Да |
| **Saber** (Video Copilot) | эффект, бесплатно | Энергетические обводки, электричество, обводка текста или маски | Да (Core, Glow Intensity и т.д.). Пресеты внутри эффекта — меню **[проверить]** |
| **Optical Flares** (Video Copilot) | эффект, платно | Блики | Позиция, яркость — да. Сам дизайн бликов — через .ffx/пресет |
| **Element 3D** (Video Copilot) | эффект, платно | 3D-текст и модели внутри AE | Сцену собирают в UI → сохраняют .ffx. В 2026 частично заменяется Advanced 3D и Blender |
| **Red Giant Trapcode / Universe / Magic Bullet** (Maxon, только подписка; 2026.0 без новых фич, https://digitalproduction.com/2025/09/17/maxon-drops-red-giant-2026-0/) | эффекты | Particular (частицы), Shine, Universe (глитчи, переходы, текст), Magic Bullet Looks (грейд) | Эффекты — да. Магазины пресетов и Designer — UI |
| **Sapphire** (Boris FX) | эффекты, подписка | Glow, Flares, переходы на хорошем уровне | Да |
| **FX Console** (Video Copilot, бесплатно) | панель | Быстрый поиск эффектов (для человека) | Не нужен агенту |
| **Motion Bro** (бесплатное расширение + паки) | панель | Готовые переходы и титры | Импортировать паки в MASTER и превращать в LIB-прекомпы |
| **Flow** (ease-кривые) | панель | Редактор кривых | Не скриптуется. Брать кривые как cubic-bezier в свой конвертер |
| **Ease and Wizz** (Ian Haigh) | скрипт с выражениями | Expo/Back/Elastic через выражения | Можно звать его .jsx с параметрами или класть выражения в шаблон **[проверить]** |
| **Overlord** (Battle Axe, $75 perpetual, https://www.battleaxe.co/overlord/) | десктоп-приложение | Illustrator/Photoshop/**Figma** → AE: шейпы, градиенты, текст, Essential Graphics-прекомпы | Не headless. Использовать для переноса дизайна стиль-фреймов в MASTER. Альтернатива: импорт SVG в шейпы в AE 26 |
| Встроенные в AE 26 | — | Advanced 3D + тени, Substance-материалы, параметрические меши, вариативные шрифты (до 8 осей), Unmult, SVG → shape | Создание через скрипт частично, проверять по объектной модели |

**Минимальный «премиум»-стек** для старта: Deep Glow 2 + Saber + встроенные (Fractal Noise, Turbulent Displace, Lumetri, Add Grain) + хорошие шрифты + motion blur + собственные ease-пресеты. Это даёт 80% разницы. Universe и Trapcode стоит брать, если нужны частицы и глитчи.

---

## 5. Компоновка с говорящей головой

### 5.1 Альфа ProRes 4444 или футаж внутри AE

| | ProRes 4444/PNG с альфой → ffmpeg overlay | Полный комп в AE (футаж внутри) |
|---|---|---|
| Простота | Графика независима от монтажа головы, рендерится параллельно | Один проект, один рендер |
| Текст за человеком, трекинг, тени на «комнату» | Нужен второй проход (маска человека поверх) | Естественно |
| Общий грейд, зерно, motion blur, «вплавление» | Нет: графика выглядит наклеенной | Да: adjustment-слой поверх всего |
| Риски | Премультипликация (тёмные или светлые ореолы), рассинхрон fps | Тяжёлый рендер, VFR-футаж в AE |

**Рекомендация.** Для премиального вида собирайте **финал в AE** с футажом внутри. ProRes 4444 straight оставьте для переиспользуемых оверлеев и для B-roll из HyperFrames и Higgsfield. При ffmpeg-оверлее рендерите **Straight** (overlay по умолчанию ждёт straight alpha) либо указывайте `alpha=premultiplied`.

### 5.2 Подготовка футажа (частые провалы)

- **VFR с телефона** → AE рассинхронизирует звук. Перед импортом конвертируйте: `ffmpeg -i in.mov -vf fps=30 -c:v prores_ks -profile:v 3 -c:a pcm_s16le talk_cfr30.mov`.
- **iPhone HDR (HLG/Dolby Vision)** выглядит выбеленным или «пережатым». Конвертируйте в SDR Rec.709 до AE (zscale/tonemap в ffmpeg) или снимайте SDR.
- Fps композиции = fps футажа (30 или 29.97). Не смешивайте 25 и 30.

### 5.3 Цвет

- В AE есть нативный OCIO/ACES (https://helpx.adobe.com/after-effects/desktop/adjust-colors/opencolorio-and-aces-color-management/opencolorio-aces-color-management.html). Для Reels с Rec.709-футажом проще оставить **Adobe-управление, Rec.709 рабочее пространство, 16 bpc** (меньше бандинга в градиентах и glow). На 32 bpc linear переходите, только если комбинируете EXR из Blender и много glow.
- Цвета бренда в JSON задавайте в sRGB 0–1. Проверка по скопам: Lumetri Scopes. На выходе ставьте теги BT.709 в ffmpeg.

### 5.4 Зерно и «вплавление»

Верхний adjustment-слой `LIB_Grade_Grain`: лёгкий общий грейд, **Add Grain или Match Grain** по футажу (Match Grain снимает характер шума с головы и применяет к графике), Vignette, иногда Chromatic aberration 0.5–1 px и лёгкий glow/halation. Только графику (до грейда) немного размывайте (0.3–0.6 px) или добавляйте motion blur, иначе вектор выглядит «слишком чистым» на фоне сжатого видео.

### 5.5 Текст за человеком

Стек слоёв (сверху вниз):
1. `talk.mov` (копия), track matte → `matte_seq` (Alpha или Luma)
2. `matte_seq` (скрыт, используется как матте)
3. Текст/графика (`behind:true`)
4. `talk.mov` (оригинал)

```javascript
// AE 23+: новый API выбираемых трек-матте
var top = comp.layers.add(talkItem); var matte = comp.layers.add(matteItem);
matte.moveBefore(top);           // матте может быть где угодно, но держим рядом
top.setTrackMatte(matte, TrackMatteType.LUMA);   // или ALPHA
```
(Новый API выбираемых трек-матте: https://community.adobe.com/questions-534/new-scripting-api-for-selectable-track-matte-layers-314161.)

Маска человека: прогоните MatAnyone (CVPR 2025, стабилен на волосах и во времени), RobustVideoMatting или SAM 2 на 5080 → PNG-секвенция (белый = человек). Roto Brush в AE даёт отличное качество, но только руками человека.

### 5.6 Трекинг графики к комнате

- **2D (плашка у головы, стрелка на предмет):** MediaPipe Face/Pose или OpenCV-трекер в Python → JSON позиций по кадрам → `position.setValuesAtTimes` (сглаживание делайте в Python).
- **3D (текст «стоит» на столе, на стене):** трек камеры в **Blender** (Movie Clip Editor полностью доступен из bpy: `clip.detect_features`, `clip.track_markers`, `clip.solve_camera`, `clip.setup_tracking_scene`; операторам нужен контекст CLIP_EDITOR через `context.temp_override`) → экспорт камеры аддоном «Export to After Effects» (.jsx, https://extensions.blender.org/add-ons/io-export-after-effects/reviews) → в AE ставится 3D-камера и нуль-плоскости. Говорящая голова со штатива обычно не требует 3D-трека: хватает лёгкого «handheld» wiggle на графике, совпадающего по характеру с камерой.
- Mocha AE и 3D Camera Tracker — только если человек готов сделать это руками.

---

## 6. Как вписывается Blender

Когда Blender, а когда AE 26:
- **Blender**: сложные hero-объекты (продукт, логотип с фаской и стеклом, телефон с UI-экраном, жидкости и частицы с физикой), Cycles-качество, трек камеры.
- **AE Advanced 3D**: простые меши, экструзия текста, GLB-импорт, быстрые итерации.

Пайплайн Blender → AE:
1. Камера и масштаб совпадают с AE: 1080×1920, тот же fps. Если 3D-объект должен двигаться синхронно с AE-слоями, экспортируйте камеру и нули в .jsx (аддон выше) или, наоборот, передавайте ключевые тайминги из `timeline.json` в Blender-скрипт.
2. Рендер: **EEVEE** для стилизованных и быстрых вещей (секунды на кадр на 5080), **Cycles + OptiX** для стекла, металла и каустики. Film → Transparent.
3. Вывод:
   - простой вариант: PNG RGBA 16-bit (или ProRes 4444 через ffmpeg)
   - композитный: **OpenEXR Multilayer** с пассами (Combined, Diffuse/Glossy, Emission для glow, Mist/Z для DOF и тумана, AO, Shadow-catcher, Cryptomatte для масок объектов). AE с версии 17.0 нативно читает многоканальные EXR и Cryptomatte (https://www.cgchannel.com/2019/11/adobe-releases-after-effects-cc-17-0/); есть ProEXR/EXtractoR от fnord (https://fnordware.com/ProEXR/). Видеоразбор цветового пространства EXR в AE 2025: https://www.blendernation.com/2025/07/01/blender-to-after-effects-2025-new-ocio-module-colorspace-workflow/
4. Цвет: Blender по умолчанию AgX (view transform). Для PNG рендерите с AgX или Standard и берите как sRGB. Для EXR (linear) в AE включайте 32 bpc linear или OCIO и интерпретируйте футаж как Linear Rec.709/sRGB **[проверить в своём проекте; частая ошибка — «выбеленный» или слишком контрастный EXR]**.
5. Shadow catcher: тени от объекта на «комнату» отдельным пассом, в AE режим Multiply поверх головы.

---

## 7. Рекомендуемый пошаговый пайплайн для агента

### Шаг 0. Один раз (setup)
- MASTER_v01.aep: 8–15 LIB-прекомпов в одном визуальном языке (2 шрифта, 1–2 акцентных цвета, сетка, safe zones). Делается вместе с человеком или по референсам. Ускоряет Overlord (Figma/Illustrator → AE) и паки Motion Bro как сырьё.
- Шаблоны: Output Module (`REELS_*`), Render Settings (`Best Settings`, `Draft_Half`).
- `effects_registry.json` (реестр matchName), `fonts_registry.json`.
- Библиотека `lib.jsx`: json2, `findComp`, `applyBezier`, `addLib(eventJson)`, `setText`, `setColor`, логирование в файл, `beginSuppressDialogs`.
- Скрипт `ping.jsx` возвращает версию AE, открыт ли проект и наличие модалок.
- Safe zones Reels как guide-слой: держать важное примерно в 950×980 по центру; консервативная рекламная разметка: верх ~270 px, низ ~670 px, бока ~65 px, справа внизу ~770 px (https://www.hopperhq.com/blog/instagram-reel-size/).

### Шаг 1. Концепт (5–10 мин агентного времени)
- Сценарий → разметка на «биты» (хук 0–2 с, 3–6 смысловых битов, CTA).
- Для каждого бита: какой LIB-элемент, текст (≤ 5 слов на экран), где графика (над, за человеком, полноэкранная вставка), SFX.
- Голос: ElevenLabs (с таймстемпами) или запись → WhisperX → `words[]`.

### Шаг 2. Стиль-фреймы (стоп-кадры)
- Собрать **только ключевые кадры** (3–5) через `build.jsx --stills`: комп той же сборки, рендер `comp.saveFrameToPng(t, file)` (недокументированный, но рабочий метод, асинхронный: дождитесь появления файла) или через `see-frame` / `contact-sheet` у a-y-ibrahim.
- Показать человеку и утвердить. Это дешевле, чем переделывать анимацию.
- Higgsfield и Blender-стиллы на этом шаге — для hero-объектов и фонов.

### Шаг 3. Аниматик
- Полная сборка по `timeline.json`, рендер `Draft_Half` без motion blur и тяжёлых эффектов (флаг `draft:true` выключает Deep Glow и Particular через `effect.enabled=false`).
- ffmpeg-контактный лист и проверка таймингов:
  `ffmpeg -i draft.mp4 -vf "fps=2,scale=270:-1,tile=6x5" sheet.png`
- Тайминг текста: появление за 2–4 кадра **до** слова, уход через 6–10 кадров после.

### Шаг 4. AE build (финал)
- Тот же `build.jsx` с `draft:false`: motion blur, glow, грейд и зерно, текст за человеком.
- `app.project.save()` → `queue_render.jsx` или прямой вызов aerender.

### Шаг 5. Рендер
- aerender в фоне (`-mfr ON 90`), лог в файл, опрос `render-status` или наличия файла.
- Мастер ProRes 422 HQ (с полным звуком из AE или без звука) → ffmpeg финал.

### Шаг 6. Звук
- Экспорт маркеров и ключевых событий из AE в JSON (скрипт обходит `comp.markerProperty` и события сборки) → ElevenLabs SFX (whoosh, pop, riser, hit) с генерацией по описанию → ffmpeg `adelay` + `amix`, громкость: голос около −14 LUFS integrated для Reels, SFX на 8–14 дБ тише голоса, ducking музыки (`sidechaincompress`).
- Привязка: whoosh начинается за 2–4 кадра до движения, hit — точно в кадр приземления (в момент, когда ease доходит до 0).

### Шаг 7. QA (автоматически и глазами)
- `ffprobe`: 1080×1920, CFR, yuv420p, BT.709-теги, длительность совпадает с аудио.
- Контактный лист плюс 3–5 кадров в моменты событий: текст не в UI-зонах, нет пропущенных шрифтов (красный текст или замена), нет цветных полос (missing footage).
- Чёрные кадры и фризы: `blackdetect`, `freezedetect`. Громкость: `ebur128`.
- Сравнение со стиль-фреймами (у a-y-ibrahim есть `match-reference`).

### Экономия времени
- **Шаблоны важнее кода**: каждый новый «вид» сначала превращать в LIB-прекомп или .ffx, только потом использовать.
- Один JSX на сборку. Идемпотентность: сборщик удаляет и пересоздаёт `MAIN`, не «допиливает».
- Тяжёлое (маттинг, трек, Blender) запускать параллельно с AE-сборкой.
- PNG-секвенции для промежуточных проходов: дорендер с кадра после падения.
- Пре-рендер тяжёлых LIB-элементов (частицы, 3D) в ProRes 4444 и подстановка как футажа (proxy).
- Версионировать `build.jsx`, `lib.jsx`, `timeline.json` в git. `.aep` воспроизводимо собирается из них.

### Типичные провалы (failure modes)
| Симптом | Причина | Решение |
|---|---|---|
| MCP-вызов висит или «queued» навсегда | Закрыта панель моста, модальный диалог, AE ещё грузится, рендер в UI | `ping.jsx`, kumo-подобный dismiss, aerender вместо `render()` |
| `JSON is undefined` | ES3 | `json2.js` |
| aerender: «template not found» | Шаблон OM/RS не создан в этой версии AE (шаблоны хранятся в prefs, пер-версионно) | Создать шаблоны в AE 2026 или сохранить через `om.saveAsTemplate` |
| aerender рендерит старое | Проект не сохранён | `app.project.save()` перед рендером |
| Ореолы вокруг графики | Premult vs straight | Straight для ffmpeg или `alpha=premultiplied` |
| Рассинхрон звука | VFR-футаж | CFR-конверсия ffmpeg |
| Выбеленная картинка | HDR-футаж с iPhone или EXR в неверном пространстве | Tonemap в SDR, корректная интерпретация |
| Шрифт заменён | Нет шрифта или неверное PostScript-имя | Реестр шрифтов, проверка до сборки |
| `applyPreset` ничего не делает | Комп не активен или выбраны другие слои | `openInViewer()`, снять выделение |
| Ease «ломается» на Position | Пространственная кривая и overshoot | `dimensionsSeparated=true` или анимация Scale/Offset |
| Графика «наклеена» | Нет общего грейда, зерна, motion blur, теней | `LIB_Grade_Grain`, motion blur 180°, shadow pass |
| Медленная сборка | Тысячи `setValueAtTime`, открытый вьювер | `setValuesAtTimes`, Caps Lock / закрыть вьювер |

---

## Источники
- a-y-ibrahim/after-effects-mcp: https://github.com/a-y-ibrahim/after-effects-mcp
- Dakkshin/after-effects-mcp: https://github.com/Dakkshin/after-effects-mcp ; https://prismix.dev/mcp/dakkshin-after-effects-mcp
- TheLlamainator/after-effects-mcp: https://mcpservers.org/de/servers/thellamainator/after-effects-mcp
- kumoproductions/mcp-aftereffects: https://github.com/kumoproductions/mcp-aftereffects
- p10q/ae-mcp: https://mcpservers.org/servers/p10q/ae-mcp
- UXP for After Effects (beta): https://developer.adobe.com/after-effects/uxp/ ; https://developer.adobe.com/after-effects/uxp/after-effects-api/outputmodule
- aerender: https://helpx.adobe.com/en/after-effects/using/automated-rendering-network-rendering.html
- Нативный H.264 в очереди рендера: https://helpx.adobe.com/after-effects/desktop/render-and-export/export-h-264-from-the-after-effects/exporting-h264-from-the-after-effects-render-queue.html
- OutputModule (ExtendScript): https://ae-scripting.docsforadobe.dev/renderqueue/outputmodule/
- KeyframeEase: https://ae-scripting.docsforadobe.dev/other/keyframeease/
- Text layer matchNames: https://ae-scripting.docsforadobe.dev/matchnames/layer/textlayer/
- applyPreset: https://community.adobe.com/questions-529/script-for-applying-animation-preset-to-layer-65840
- MOGRT/Essential Graphics scripting: https://helpx.adobe.com/ca/after-effects/desktop/automate-in-after-effects/automate-animation/scripts.html ; https://community.adobe.com/bug-reports-528/after-effects-24-2-1-exportasmotiongraphicstemplate-not-returning-correct-value-1217054
- Track matte API: https://community.adobe.com/questions-534/new-scripting-api-for-selectable-track-matte-layers-314161
- 3D Camera Tracker и скриптинг: https://community.adobe.com/questions-529/api-for-3d-camera-tracker-30443 ; menu command IDs: https://www.provideocoalition.com/after-effects-menu-command-ids/
- AE 26.0: https://www.cgchannel.com/2026/01/adobe-releases-after-effects-26-0-with-native-substance-support/ ; https://digitalproduction.com/2026/01/23/adobe-after-effects-2026-lands-with-3d-text-and-performance-boosts/
- OCIO/ACES в AE: https://helpx.adobe.com/after-effects/desktop/adjust-colors/opencolorio-and-aces-color-management/opencolorio-aces-color-management.html
- EXR и Cryptomatte в AE 17: https://www.cgchannel.com/2019/11/adobe-releases-after-effects-cc-17-0/ ; ProEXR: https://fnordware.com/ProEXR/
- Blender → AE: https://extensions.blender.org/add-ons/io-export-after-effects/reviews ; https://www.blendernation.com/2025/07/01/blender-to-after-effects-2025-new-ocio-module-colorspace-workflow/
- nexrender: https://github.com/inmagik/nexrender (форк inlife/nexrender)
- Deep Glow 2: https://aescripts.com/deep-glow
- Overlord: https://www.battleaxe.co/overlord/
- Red Giant 2026.0: https://digitalproduction.com/2025/09/17/maxon-drops-red-giant-2026-0/
- MatAnyone: https://arxiv.org/abs/2501.14677
- Safe zones Reels: https://www.hopperhq.com/blog/instagram-reel-size/
