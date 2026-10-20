// ae_sharp_preflight.jsx — защита от «мыла» (SABRMOTION, 2026-10-19)
// Запуск: AfterFX.exe -r "...\vault\_tools\ae_sharp_preflight.jsx" (через ae\run.ps1) ПЕРЕД стиль-фреймами и ПЕРЕД рендером.
// Что делает: (1) чинит безопасное автоматически (разрешение Full, качество слоёв Best, бикубика);
// (2) находит причины мыла и пишет отчёт ae\logs\sharp_preflight.txt. Если есть FAIL — фреймы/рендер не показывать.
(function () {
    var STEP = 3;                 // проверять каждый 3-й кадр
    var BLUR_MATCH = {"ADBE Gaussian Blur 2":1,"ADBE Fast Blur":1,"ADBE Box Blur2":1,"ADBE Camera Lens Blur":1,
                      "ADBE Motion Blur":1,"ADBE Radial Blur":1,"CC Radial Fast Blur":1,"ADBE Glo2":1};
    var NOISE_MATCH = {"ADBE Noise":1,"ADBE Add Grain":1,"ADBE Fractal Noise":1,"ADBE Turbulent Noise":1};
    var out = [], fails = 0, warns = 0, fixes = 0;
    function log(kind, msg) { out.push(kind + "  " + msg); if (kind == "FAIL") fails++; if (kind == "WARN") warns++; if (kind == "FIX ") fixes++; }
    function tc(comp, t) { return timeToCurrentFormat(t, comp.frameRate); }
    function isRaster(layer) {
        if (!(layer instanceof AVLayer)) return false;
        var s = layer.source;
        if (!s) return false;
        if (s instanceof CompItem) return !layer.collapseTransformation; // прекомп без «непрерывной растеризации» = растр
        if (s instanceof FootageItem) {
            if (s.mainSource instanceof SolidSource) return false;
            var n = (s.file ? s.file.name.toLowerCase() : "");
            if (/\.(ai|eps|pdf|svg)$/.test(n)) return !layer.collapseTransformation;
            return true;
        }
        return false;
    }
    function tr(layer, name) { try { return layer.property("ADBE Transform Group").property(name); } catch (e) { return null; } }
    function val(p, t) { try { return p ? p.valueAtTime(t, false) : null; } catch (e) { return null; } }
    function same(a, b) {
        if (a === null || b === null) return true;
        if (typeof a == "number") return Math.abs(a - b) < 0.001;
        for (var i = 0; i < a.length; i++) if (Math.abs(a[i] - b[i]) > 0.001) return false;
        return true;
    }
    function scaleOf(layer, t) { var v = val(tr(layer, "ADBE Scale"), t); return v ? v : [100, 100]; }

    for (var ci = 1; ci <= app.project.numItems; ci++) {
        var comp = app.project.item(ci);
        if (!(comp instanceof CompItem)) continue;
        var fd = comp.frameDuration;
        if (comp.resolutionFactor[0] != 1 || comp.resolutionFactor[1] != 1) { comp.resolutionFactor = [1, 1]; log("FIX ", comp.name + ": разрешение превью → Full"); }
        if (comp.motionBlur && comp.shutterAngle > 180) log("WARN", comp.name + ": shutter angle " + comp.shutterAngle + "° > 180° — смаз длиннее нормы");

        for (var li = 1; li <= comp.numLayers; li++) {
            var L = comp.layer(li);
            if (!(L instanceof AVLayer || L instanceof TextLayer || L instanceof ShapeLayer)) continue;
            if (!L.enabled) continue;
            try { if (L.quality != LayerQuality.BEST) { L.quality = LayerQuality.BEST; log("FIX ", comp.name + " › " + L.name + ": качество слоя → Best"); } } catch (e) {}
            try { if (L.samplingQuality != LayerSamplingQuality.BICUBIC) { L.samplingQuality = LayerSamplingQuality.BICUBIC; } } catch (e) {}

            var raster = isRaster(L);
            var t0 = Math.max(L.inPoint, 0), t1 = Math.min(L.outPoint, comp.duration);
            var props = ["ADBE Position", "ADBE Scale", "ADBE Rotate Z", "ADBE Opacity"];
            var prev = null, upscaleReported = false, restBlurReported = false, restScaleReported = false, restPosReported = false;

            // эффекты размытия / шума на слое
            var fx = L.property("ADBE Effect Parade"), blurs = [], noisy = false;
            if (fx) for (var ei = 1; ei <= fx.numProperties; ei++) {
                var e = fx.property(ei); if (!e.enabled) continue;
                if (BLUR_MATCH[e.matchName]) blurs.push(e);
                if (NOISE_MATCH[e.matchName]) noisy = true;
            }
            if (noisy || /зерно|grain|noise|шум|фактур|texture/i.test(L.name)) {
                // 2026-10-19 22:37: пользователь видит зерно/шум как «мыло», даже на фоне — по умолчанию запрещено везде
                var op = val(tr(L, "ADBE Opacity"), t0);
                if (op === null || op > 0) log("FAIL", comp.name + " › " + L.name + ": зерно/шум в кадре (opacity " + op + "%) — фон должен быть чистым; оставить только если фактура прямо есть в брифе");
            }
            if (L instanceof TextLayer) for (var b = 0; b < blurs.length; b++) if (blurs[b].matchName == "ADBE Glo2")
                log("WARN", comp.name + " › " + L.name + ": Glow на тексте — допустим только на входе, в покое выключить");

            for (var t = t0; t < t1; t += fd * STEP) {
                var cur = [];
                for (var pi = 0; pi < props.length; pi++) cur.push(val(tr(L, props[pi]), t));
                var rest = false;
                if (prev) { rest = true; for (var q = 0; q < cur.length; q++) if (!same(cur[q], prev[q])) { rest = false; break; } }
                prev = cur;
                var sc = cur[1] || [100, 100];
                if (raster && !upscaleReported && (Math.abs(sc[0]) > 100.5 || Math.abs(sc[1]) > 100.5) && !(L.source instanceof CompItem)) {
                    log("FAIL", comp.name + " › " + L.name + ": растр увеличен до " + sc[0].toFixed(1) + "% в " + tc(comp, t) + " — заменить исходник большего размера"); upscaleReported = true;
                }
                if (!rest) continue;
                // в покое: размытие должно быть ровно 0
                for (var bb = 0; bb < blurs.length && !restBlurReported; bb++) {
                    var p1 = blurs[bb].property(1); var bv = val(p1, t);
                    var amount = (typeof bv == "number") ? bv : 0;
                    if (blurs[bb].matchName == "ADBE Glo2") continue;
                    if (amount > 0.01) { log("FAIL", comp.name + " › " + L.name + ": «" + blurs[bb].name + "» = " + amount.toFixed(2) + " на неподвижном слое в " + tc(comp, t) + " — вход должен заканчиваться ровно на 0"); restBlurReported = true; }
                }
                // в покое: растр/прекомп только на ровном масштабе и целых пикселях
                if (raster && !restScaleReported && (Math.abs(sc[0] - Math.round(sc[0])) > 0.01 || (Math.abs(sc[0] - 100) > 0.01 && L.source instanceof CompItem))) {
                    log("FAIL", comp.name + " › " + L.name + ": в покое масштаб " + sc[0].toFixed(3) + "% (не ровно) в " + tc(comp, t) + " — bounce/expression не дотягивает до значения → пересэмплинг"); restScaleReported = true;
                }
                var pos = cur[0];
                if (raster && !restPosReported && pos && (Math.abs(pos[0] - Math.round(pos[0])) > 0.01 || Math.abs(pos[1] - Math.round(pos[1])) > 0.01) && Math.abs(sc[0] - 100) < 0.01) {
                    log("WARN", comp.name + " › " + L.name + ": в покое позиция не на целом пикселе (" + pos[0].toFixed(2) + ", " + pos[1].toFixed(2) + ") — округлить"); restPosReported = true;
                }
            }
        }
    }
    var head = "ПРЕДПОЛЁТНАЯ ПРОВЕРКА РЕЗКОСТИ  " + new Date().toString() + "\nFAIL: " + fails + "   WARN: " + warns + "   исправлено автоматически: " + fixes + "\n" +
               (fails ? "ИТОГ: НЕЛЬЗЯ показывать/рендерить — сначала исправить FAIL.\n" : "ИТОГ: можно рендерить. Затем запустить sharpcheck.py.\n");
    var proj = app.project.file ? app.project.file.parent : Folder.desktop;
    var lf = new Folder(proj.fsName + "/logs"); if (!lf.exists) lf.create();
    var f = new File(lf.fsName + "/sharp_preflight.txt"); f.encoding = "UTF-8"; f.open("w"); f.write(head + "\n" + out.join("\n")); f.close();
    try { $.writeln(head); } catch (e) {}
})();
