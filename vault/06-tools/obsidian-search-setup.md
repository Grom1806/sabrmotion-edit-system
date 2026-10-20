---
title: Поиск по vault (Obsidian + Smart Connections)
type: tool
tags: [tool, obsidian, search]
summary: Как искать по vault - встроенный поиск, Smart Connections (локальные эмбеддинги), опционально MCP для Claude Code
updated: 2026-10-13
---
# Поиск по vault

## Уровень 1 — уже работает (для Claude)
INDEX + теги + ripgrep. При ~45 заметках / ~270 KB этого хватает: Claude находит нужное за 1–2 вызова и читает только его.

## Уровень 2 — Smart Connections (для пользователя в Obsidian)
Плагин сам режет заметки на блоки и строит векторный индекс **локально** (встроенная модель, без API-ключа, без облака — это и есть «как Pinecone», только у вас на ПК).
1. Obsidian → Open folder as vault → `claude-edit\vault`.
2. Settings → Community plugins → Turn on → Browse → «Smart Connections» → Install → Enable.
3. Подождать индексацию (секунды при нашем объёме). Открыть панель Connections: справа видны похожие по смыслу заметки к открытой.
4. Для многоязычного русского текста в настройках модели выбрать multilingual-модель, если доступна.

## Уровень 3 — опционально: семантический поиск для Claude Code на ПК
Существуют сторонние MCP-серверы, читающие индекс Smart Connections (например smart-connections-mcp). Ставить только по решению пользователя: это сторонний код, а при текущем объёме выигрыш небольшой. Вернуться к этому, когда заметок станет 300+.
