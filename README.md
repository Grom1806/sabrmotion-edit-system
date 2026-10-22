# SABRMOTION — система монтажа (бэкап)

Личная база знаний по монтажу рилсов, собранная вместе с Claude: правила, брендбуки, техники моушна, звук, цвет, AE-пайплайн, разборы референсов и уроки по каждому ролику. Это бэкап, чтобы ничего не потерять, и одновременно skill, который можно поставить в другом аккаунте Claude.

## Что внутри

| Папка | Что это |
|---|---|
| `SKILL.md` | Точка входа для Claude: как пользоваться базой перед монтажом |
| `vault/00-start` | START (протокол), SYSTEM (система монтажа v3), INDEX (оглавление всех заметок) |
| `vault/01-rules` | Правила, которые действуют всегда |
| `vault/02-brands` | SABRMOTION, PERSET, Ummah Link, Apple-стиль, клиентские бренды |
| `vault/03-techniques` | Каталоги моушна, цвета, типов монтажа, говорящая голова |
| `vault/04-lessons` | Уроки по каждому ролику, сводки тредов, открытые вопросы |
| `vault/05-research` | Ресерч стилей, брендов, референсов, трендов |
| `vault/06-tools` | Инструменты, грабли пайплайна, библиотека ассетов |
| `vault/07-system` | Пульт вопросов, ритм, звук/SFX, моушн v3, резкость, анти-ИИ QA |
| `vault/_tools`, `_scripts`, `_templates` | Пульт монтажа (HTML), скрипты проверки резкости, сборка индекса, шаблоны заметок |
| `project-memory/` | Снимок памяти проекта Claude (короткие факты и предпочтения) |
| `tools/hyperframes-kit/` | Монтаж без After Effects: шаблон HyperFrames + GSAP, помощники по нормам, сборка и QA одной командой |
| `tools/no-ae-engine/` | Монтаж без After Effects на Python (nae): документальный моушен, камера с motion blur, авто-SFX, QA |
| `tools/make_skill_zip.py` | Собирает лёгкий zip для загрузки skill в claude.ai |

## Как поставить в другом аккаунте

**Claude.ai (веб/приложение).** Собери архив `python tools/make_skill_zip.py` (или возьми готовый `sabrmotion-edit-system.zip`) и загрузи: Settings → Capabilities → Skills → Upload skill.

**Claude Code (терминал/ПК).**
```bash
git clone https://github.com/Grom1806/sabrmotion-edit-system ~/.claude/skills/sabrmotion-edit-system
```
На Windows: `git clone ... %USERPROFILE%\.claude\skills\sabrmotion-edit-system`.

**Obsidian.** Открой папку `vault/` как хранилище. Плагин Smart Connections (семантический поиск) ставится заново из Community plugins.

## Как обновлять

Главная копия vault живёт на ПК: `claude-edit\vault\`, зеркало в облачном проекте `vault/`. Попроси Claude в проекте «обнови бэкап на GitHub», и он сверит обе копии, возьмёт более свежие файлы и запушит новый коммит. История всех версий остаётся в git.

Ассеты (видео, фото, иконки, звуки, шрифты) сюда не входят: они остаются на ПК в `claude-edit\assets\` и `claude-edit\branding\`.
