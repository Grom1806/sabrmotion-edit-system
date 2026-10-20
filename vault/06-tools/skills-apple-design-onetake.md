---
title: Скиллы apple-design и onetake
type: tool
tags: [tools, skill, apple, motion]
summary: Два внешних скилла в claude-edit\.claude\skills. apple-design = ревью UI по Apple HIG (для UI-мокапов в рилсах). onetake = моушен-ролики про продукт из HTML (только некоммерческая лицензия).
updated: 2026-10-18
source: github.com/dickwu/apple-design-skill, github.com/feitangyuan/onetake
---
# Скиллы apple-design и onetake

Установлены 2026-10-18 в `C:\Users\subhan\Desktop\subhan\claude-edit\.claude\skills\` (их видят RC-сессии, запущенные в claude-edit). Вызов: `/apple-design`, `/onetake`.

## apple-design (dickwu)
- Что это: ревьюер дизайна интерфейсов приложений по Apple Human Interface Guidelines (123 страницы HIG + гид по Liquid Glass). Для монтажа видео он НЕ предназначен.
- Не дублирует [[apple-style-signature]]: наш документ про язык монтажа keynote (blur-in, слово-экран, push-in, тишина), а скилл про кнопки, таб-бары, типографику и цвет в UI.
- Когда брать: когда в рилсе рисуем UI-мокап (парящая карточка, экран приложения, Liquid Glass). Открыть `references/hig/liquid-glass.md`, `materials.md`, `typography.md`, `color.md`, чтобы мокап выглядел как настоящий iOS/macOS.
- Полезная мысль для монтажа (из branding.md / craft lens): смелость тратится в одном месте, всё вокруг тихое; не делать «шаблонный» вид (чёрный фон + один кислотный акцент + огромная цифра без причины).

## onetake (feitangyuan)
- Что это: пайплайн коротких моушен-роликов про продукт (10–60 с): один HTML, всё функция времени, библиотека 39 движений (`lib/motion.js`), рендер с настоящим motion blur, синтез SFX, оракул `verify_promo.py`, который ловит «слайд-шоу».
- Сам скилл пишет: talking-head и монтаж готовых исходников НЕ его задача. Подходит для отдельных графических вставок, промо приложений/скиллов, B-roll из UI.
- ЛИЦЕНЗИЯ: PolyForm Noncommercial. Для роликов заказчиков (PERSET и др.) использовать его код нельзя без разрешения автора; для своих некоммерческих экспериментов можно. Идеи (принципы ниже) брать можно.
- КОНФЛИКТ: по умолчанию onetake кладёт музыку. У нас [[no-music]], только SFX.
- Что взять в наши правила:
  - Ритм: длины кадров различаются ≥4× (0.25 с рядом с 2.5 с), есть участок почти полной тишины в картинке и звуке. Равные длины = «как PPT».
  - Carry: на каждой границе бита что-то переживает склейку и двигается в следующий бит (карточка растёт в сцену, zoomThrough, iris). Иначе смена слайда.
  - Причина видна: реакция без видимой причины (рука, точка, курсор) читается как скринсейвер.
  - Звук: один набор материалов в одной комнате (air, wood, glass, sub), событий меньше, чем битов. Совпадает с [[sound-design]] и [[variety]].
  - Без конфетти/частиц, кривые выбирать по t80 (expoOut для щелчка, пружины для посадки), всё быстрее 80 px/кадр с motion blur.
- Референсы: `references/rhythm.md`, `motion-library.md`, `sound.md`, `reference-deconstruction.md`; скрипт `scripts/analyze_ref.py` меряет энергию/склейки/неподвижность референса.

См. также: [[tools-catalog]], [[motion-playbook]], [[brand-apple]].
