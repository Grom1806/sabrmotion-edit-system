---
title: Клипы с телефона
type: rule
tags: [rule, source]
summary: Проверять SAR/rotation, чтобы горизонтальное не растянулось; не глушить живую речь в клипах
updated: 2026-10-13
source: project memory
---
# Клипы с телефона

2026-10-08 (влог): проверять `ffprobe` поля SAR и rotation (rotation=-90 = на самом деле вертикаль). Перед заглушением исходного звука прогнать silero-vad: если в клипе слышна речь, оставлять её. См. [[color-playbook]] (HLG-источники iPhone).
