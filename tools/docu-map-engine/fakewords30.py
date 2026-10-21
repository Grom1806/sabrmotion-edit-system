# черновые тайминги до озвучки: ~14.5 симв/с, паузы на точках
import json, re
txt = open('voice30.txt', encoding='utf-8').read().replace('́', '')
t = 0.3; out = []
for para in [p for p in txt.split('\n') if p.strip()]:
    for w in para.split():
        d = max(0.18, len(re.sub(r'[^\w-]', '', w)) / 14.5)
        out.append({'w': w, 't': round(t, 3), 'e': round(t + d, 3)}); t += d + 0.06
        if w[-1] in '.?!': t += 0.35
        elif w[-1] in ',:—': t += 0.15
    t += 0.25
json.dump(out, open('words.json', 'w'), ensure_ascii=False)
print(len(out), round(t, 2))
