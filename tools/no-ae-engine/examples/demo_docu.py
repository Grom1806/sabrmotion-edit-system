# Пример проекта для движка без AE: 9 с, SABRMOTION. Запуск:
#   cd tools/no-ae-engine && python -m nae.run examples/demo_docu.py --out out/demo
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from nae import *

NAME = 'nae_demo'
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS['Unbounded'] = os.path.join(HERE, '..', 'fonts', 'Unbounded[wght].ttf')
FONTS['Manrope'] = os.path.join(HERE, '..', 'fonts', 'Manrope[wght].ttf')
RED, GRN, TX, PN = '#F2283B', '#20DD78', '#F4F4F1', '#16161A'

def build():
    # камера: станция 1 → проезд вниз → станция 2 (на станциях зум ровно 1.0)
    cam = CamTrack([(0, 540, 960, 1.0), (3.3, 540, 960, 1.0), (4.2, 540, 2880, 1.0), (9.0, 540, 2880, 1.0)])
    c = Comp(9.0, bg='#0B0B0C', cam=cam)
    c.add(Box('Карточка 1', 120, 640, 840, 520, -0.25, color=PN, enter='line', dur=0.6))   # хук уже в движении на кадре 0
    c.add(Text('Заголовок «Без AE»', 'Без After', 540, 760, 84, 0.45, font='Unbounded:800', anchor='c'))
    c.add(Text('Заголовок «Effects»', 'Effects', 540, 870, 84, 0.85, font='Unbounded:800', color=RED, anchor='c'))
    c.add(Text('Подпись движка', 'Python + numpy + ffmpeg', 540, 1010, 40, 1.25, font='Manrope:600', color='#8A8A92', anchor='c'))
    # станция 2: счётчик-герой и растущие полосы, контейнер растёт под контент
    c.add(Text('Подпись «Резкость»', 'Резкость в покое', 540, 2380, 40, 4.3, font='Manrope:600', color='#8A8A92', anchor='c'))
    c.add(Counter('Счётчик 100 %', 0, 100, 540, 2470, 200, 4.6, dur=1.1, suffix='%', font='Unbounded:800', color=GRN, anchor='c'))
    for i, (w, op) in enumerate([(700, 1.0), (560, 0.7), (420, 0.45)]):
        c.add(Box(f'Полоса {i + 1}', 190, 2780 + i * 64, w, 34, 4.8 + i * 0.12, color=GRN, radius=17, enter='point', shadow=False, op=op, sfx=True, sound='grow'))
    c.add(Path('Линия подчёркивания', [(240, 3020), (840, 3020)], 6.3, dur=0.5, color=RED, width=6))
    c.add(Text('Финал SABRMOTION', 'SABRMOTION', 540, 3080, 64, 6.9, font='Unbounded:800', anchor='c', kind='cta'))
    return c
