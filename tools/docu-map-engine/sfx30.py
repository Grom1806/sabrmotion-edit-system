# SFX-события «Путь аль-Бухари» 30 с: каждый звук привязан к видимому событию в том же кадре
import sys, json
sys.argv = ['render.py']; __file__ = sys.path[0] + '/render.py'
exec(open('render.py').read().split("if __name__ == '__main__':")[0])
EV = []
def ev(t, key, f, db, pitch=0.0, pan=0.0, align='start', dur=None):
    EV.append(dict(t=round(t, 3), key=key, f=f, db=db, pitch=pitch, pan=pan, align=align, dur=dur))
KEYS6 = [f'desk/key_0{i}.wav' for i in range(1, 7)]
def typewriter(txt, sub, t_in, tag):
    ev(t_in, f'{tag}_bar', 'desk/card_slide.mp3', -25, pan=-0.3)
    s = txt + sub
    for i, ch in enumerate(s):
        if ch.strip() and ch not in '—':
            ev(t_in + 0.15 + (i + 1) * TYPE_DT - 0.001, f'{tag}_ch{i}', KEYS6[i % 6], -31, pitch=(i % 3 - 1) * 0.4, pan=-0.35 + 0.7 * i / len(s))
# хук
ev(0.15, 'hook_lead', 'ui/kenney_select_001.wav', -28)
ev(C['buh'] - 0.1, 'uz_outline', 'desk/marker_stroke.mp3', -25, pan=0.2)
ev(C['buh'], 'pt_bukhara', 'ui/kenney_drop_002.wav', -24, pan=0.1)
ev(C['kniga'] - 0.05, 'kniga_hit', 'stamp/kenney_impactSoft_heavy_000.wav', -15)
ev(C['kniga'] - 0.05, 'kniga_sub', 'sub/el_sub_hit_3.wav', -22, align='peak')
ev(C['kniga'] + 0.45, 'tail1', 'ui/kenney_select_001.wav', -29, pitch=1)
ev(C['kniga'] + 0.75, 'tail2', 'ui/kenney_select_001.wav', -29, pitch=2)
typewriter('Бухара — 810 год (194 г. х.)', 'Родился аль-Бухари', C['kniga'] + 0.9, 'chr1')
ev(C['s16'] - 0.3, 'hook_out', 'whoosh/mixkit_small_sweep.wav', -27)
typewriter('В 16 лет — хадж в Мекку', 'и годы в поиске хадисов', C['hajj'], 'chr2')
# города маршрута
for i, key in enumerate(ROUTE[1:]):
    ev(ARRIVE[i], f'pt_{key}', 'ui/kenney_drop_002.wav', -25, pitch=[0, 1, -1, 2, 0, -2, 1][i], pan=[-.3, -.2, .2, .1, .2, -.4, -.3][i])
# перелёты камеры: пики скорости
sp = [(n / FPS, cam_speed(n / FPS)) for n in range(int(C['end'] * FPS))]
peaks = [(t, s) for (t0, a), (t, s), (t1, b) in zip(sp, sp[1:], sp[2:]) if s > 14 and s >= a and s > b]
for t, s in peaks:
    f = 'whoosh/mixkit_windy_swoosh.wav' if s > 60 else ('whoosh/el_whoosh_long.wav' if s > 30 else 'whoosh/mixkit_short_sweep.wav')
    ev(t, f'cam_{t:.2f}_{s:.0f}px', f, -21 if s > 30 else -25, align='peak')
# цепочка
n = len(CHAIN); t0, t1 = C['cep'], C['prophet'] + 0.4
ev(C['cep'], 'chain_caption', 'ui/kenney_select_001.wav', -28)
ev(t0, 'snake_line', 'desk/marker_stroke.mp3', -27)
for j in range(n):
    ev(t0 - 0.35 + (t1 - t0) * j / (n - 1), f'plate_{j}', 'desk/card_drop.mp3' if j % 2 == 0 else 'desk/card_slide.mp3', -24, pitch=j * 0.3, pan=(-.25 if (n - 1 - j) % 2 == 0 else .25))
for k in range(n):
    ev(C['prov'] + (C['zveno'] + 0.4 - C['prov']) * k / (n - 1), f'loupe_{k}', 'tick/kenney_tick_001.wav', -27, pan=(-.25 if k % 2 == 0 else .25))
# числа
ev(C['k600'] - 0.3, 'num_label', 'ui/kenney_select_001.wav', -29)
ev(C['k600'] - 0.1, 'counter', 'tick/el_slot_ticks.wav', -23, dur=1.25)
ev(C['k7'] - 0.6, 'dots_out', 'paper/mixkit_paper_quick.wav', -25)
ev(C['k7'] - 0.05, 'n7000', 'stamp/kenney_impactSoft_heavy_002.wav', -16)
ev(C['k7'] + 0.25, 'n7000_label', 'ui/kenney_select_001.wav', -29, pitch=1)
# книга и мир
ev(C['sahih'] - 0.2, 'book_in', 'paper/mixkit_page_turn.wav', -21)
ev(C['world'] - 0.2, 'arcs', 'whoosh/mixkit_arrow.wav', -24)
ev(C['world'] - 0.1, 'read_label', 'ui/kenney_select_001.wav', -29)
ev(C['t1100'] - 0.05, 'y1100', 'stamp/kenney_impactSoft_heavy_000.wav', -16, pitch=-1)
ev(C['t1100'] - 0.05, 'y1100_sub', 'sub/el_sub_hit_3.wav', -24, align='peak')
ev(C['outro'] - 0.3, 'texts_out', 'whoosh/mixkit_short_sweep.wav', -27)
ev(C['outro'], 'outro_label', 'ui/kenney_select_001.wav', -28)
ev(C['outro'] + 0.5, 'wordmark', 'stamp/kenney_impactGeneric_light_001.wav', -20)
ev(C['outro'] + 0.5, 'wordmark_pop', 'notification/mixkit_dry_pop.wav', -26)
EV.sort(key=lambda e: e['t'])
json.dump(EV, open('sfx_events30.json', 'w'), ensure_ascii=False, indent=0)
print(len(EV), 'events; camera peaks:', [(round(t, 2), round(s)) for t, s in peaks])
