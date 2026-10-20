---
title: AE подменяет Montserrat на Times (кроме ExtraBold)
type: lesson
tags: [lesson, after-effects, fonts, perset]
summary: В AE на этом ПК живой только Montserrat ExtraBold (Adobe Fonts); Black/Bold/SemiBold/Medium/Light/Regular молча становятся Times — проверять isSubstitute до сборки; G-Fill цвета из скрипта не задаются → Ramp + Set Matte
updated: 2026-10-20
source: PERSET reel 05 (perset/reel05_saas), стиль-фреймы 2026-10-20
---
# AE подменяет Montserrat на Times

**Ошибка:** в первых кадрах PERSET 05 подписи, цифры и «из-за границы» вышли шрифтом с засечками.
**Причина:** `app.fonts` видит Montserrat-Black/Light/… только как подстановку (`isSubstitute=true`, файл `times.ttf`); вариативные Montserrat-VF из Windows AE не подхватывает. Рабочий — только ExtraBold из Adobe Fonts.
**Решение:** перед сборкой запускать `ae/probe_montserrat.jsx` (печатает файл и `isSubstitute`); пока семейство не активировано в Adobe Fonts, тяжёлые роли = Montserrat ExtraBold, UI-подписи и тонкие строки = Segoe UI (Semibold/Regular/Light).

Ещё уроки той же сборки:
- Цвета `ADBE Vector Grad Colors` (G-Fill) из ExtendScript не задаются → градиент = эффект Gradient Ramp + Set Matte на собственную альфу слоя.
- У shape-слоя точки эффектов (Ramp Start/End) считаются от левого верхнего угла слоя: центр контента = [W/2, H/2]. Без этого сдвига градиент выходит плоским. После `addProperty` следующего эффекта ссылку на предыдущий эффект нужно брать заново (иначе «Недопустимый объект»).
- **inPoint сдвигает outPoint:** в AE присвоение `layer.inPoint` позже текущего сохраняет длительность слоя → outPoint уезжает вперёд, и слои «протекают» в следующие сцены. Поднимать inPoint только через `trimIn(l, t)` (запомнить out, поставить in, вернуть out).
- Имя функции не должно совпадать с `var` того же скоупа (`function card` перекрылась `var card = crect(…)` → «no layer»).
- Time Remap: удалить все ключи нельзя («свойство скрыто») — ставить свои ключи поверх и удалить только ключ по умолчанию в конце.
- Звук референса Pulse — музыкальная подложка с ударными (LRA 2.8, сплошной спектр); музыку не берём, копируем скелет: паузы-провалы и удар сразу после них, вжухи на проездах, тики на буквы.
- Синтаксическая ошибка в JSX оставляет модальное окно в AE → `run.ps1` висит до таймаута; закрыть через `ae_do instance.dismiss_dialog`.
- Text Animator: окно селектора `100·T/(step·n)` больше 100 % у коротких слов → ошибка «вне диапазона»; при `step·n < T` брать `step = T/n`.
- Свет «пятном» (эллипс + Gaussian Blur) даёт жёсткий край → радиальный Gradient Ramp на сплошной, режим Screen.

См. [[perset]], [[ae-pipeline]], [[ref-ui-card-build]].
