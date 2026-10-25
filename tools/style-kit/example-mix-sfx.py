import numpy as np,subprocess,wave
SR=48000;L="/tmp/w/lib/sfx/"
def load(p):
    r=subprocess.run(["ffmpeg","-v","error","-i",p,"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True)
    return np.frombuffer(r.stdout,dtype=np.float32).reshape(-1,2).copy()
voice=load("/tmp/w/voice.wav")
N=int(25.62*SR); mix=np.zeros((N,2),np.float32); mix[:len(voice)]+=voice[:N]
POP="notification/mixkit_dry_pop.wav"; SW="swipe/el_swipe_ui.wav"; WH="whoosh/mixkit_fast_swoosh.wav"; GL="glitch/el_glitch_short.wav"
ST="stamp/el_stamp_thump.wav"; OPEN="ui/kenney_maximize_002.wav"; TK="tick/kenney_tick_002.wav"; SOFT="tick/el_tick_soft.wav"
BUB="notification/mixkit_bubble_pop.wav"; ZM="impact/mixkit_quick_zoom.wav"; SCAN="typing/mixkit_soft_digital.wav"
EV=[ # время, файл, дБ, якорь (s=начало, p=пик), макс.длина — каждое = видимое событие в кадре
(0.05,"whoosh/mixkit_air_woosh.wav",-6,'s',.8,"окно раскрывается в кадр"),
(0.02,POP,-8,'s',.3,"pop «Самый»"),
(0.72,"stamp/kenney_impactSoft_heavy_000.wav",-3,'s',.6,"ДОРОГОЙ падает и отскакивает"),(0.95,TK,-12,'s',.15,"отскок ДОРОГОЙ"),
(1.50,SW,-6,'s',.5,"slide iPhone"),
(1.76,WH,-6,'p',.5,"whip вверх/вправо"),
(1.80,OPEN,-4,'s',.5,"окно Apple открывается"),(1.82,POP,-11,'s',.3,"pop «только что»"),
(2.05,"whoosh/mixkit_small_sweep.wav",-12,'s',.5,"курсор едет"),
(2.14,GL,-7,'s',.4,"slice ПОСТУПИЛ"),
(2.62,"ui/kenney_click_002.wav",-2,'s',.2,"клик курсора"),(2.64,POP,-10,'s',.3,"pop «в продажу»"),
(3.04,"whoosh/mixkit_fast_transition.wav",-6,'p',.5,"всё уходит вниз"),
(3.10,ZM,-4,'s',.6,"панч-ин"),(3.12,POP,-10,'s',.3,"pop СТОИТ ЛИ"),
(3.60,POP,-10,'s',.3,"pop «она своих»"),(3.96,ST,-4,'s',.5,"ДЕНЕГ? штамп"),
(4.10,"whoosh/el_whoosh_short.wav",-9,'p',.4,"СТОИТ ЛИ улетает вверх"),(4.28,WH,-7,'p',.5,"whip влево"),
(4.32,SW,-7,'s',.5,"slide «я»"),(4.70,SW,-7,'s',.5,"slide «думаю»"),
(4.96,"sub/el_sub_hit_1.wav",-3,'s',1.0,"НЕТ удар"),(4.96,"glitch/kenney_glitch_002.wav",-8,'s',.3,"RGB-раздвоение НЕТ"),
(5.00,"ui/el_error_buzz.wav",-8,'s',.4,"красная кнопка-стоп"),
(5.22,"whoosh/mixkit_cinematic_fast.wav",-5,'p',.7,"жёлтая сцена въезжает + засвет"),
(5.30,SCAN,-10,'s',.35,"scan «когда она»"),
(5.36,"whoosh/mixkit_tech_slide.wav",-7,'s',.6,"телефон-окно открывается"),
(5.50,BUB,-8,'s',.3,"окошко с лицом"),
(6.10,GL,-7,'s',.4,"slice СЛОЖЕНА"),(6.62,POP,-10,'s',.3,"pop «простой»"),
(7.12,"stamp/kenney_impactPunch_medium_001.wav",-5,'s',.5,"iPhone падает"),
(7.26,WH,-8,'p',.5,"тексты разлетаются"),(7.30,"whoosh/el_whoosh_short.wav",-5,'s',.5,"телефон крутится"),
(7.50,SCAN,-10,'s',.35,"scan «когда»"),(7.68,GL,-7,'s',.4,"slice РАСКРЫТА"),(8.22,POP,-10,'s',.3,"pop «просто»"),
]+[(8.60+i*0.045,TK,-11,'s',.12,"буква iPad mini") for i in range(9)]+[
(9.10,WH,-5,'p',.5,"жёлтая сцена уезжает вверх"),
(9.32,POP,-10,'s',.3,"строка караоке"),(9.52,SOFT,-12,'s',.2,"слово «она»"),(9.80,SOFT,-12,'s',.2,"слово «стоит»"),(10.10,SOFT,-12,'s',.2,"слово «как»"),
(10.30,OPEN,-4,'s',.5,"окно MacBook"),(10.34,"digital/kenney_highUp.wav",-10,'s',.4,"MacBook загорается"),
(10.58,WH,-8,'p',.5,"строка вниз"),(10.80,POP,-8,'s',.3,"«или» + «=»"),
(11.16,BUB,-5,'s',.3,"айпад 1"),(11.30,BUB,-5,'s',.3,"айпад 2"),(11.44,BUB,-5,'s',.3,"айпад 3"),(11.16,SW,-9,'s',.5,"slide ТРИ АЙПАДА"),
(11.82,"whoosh/mixkit_fast_transition.wav",-5,'p',.5,"белая сцена въезжает"),
(11.86,"whoosh/mixkit_light_pop_whoosh.wav",-8,'s',.5,"«зачем» из глубины"),(12.32,"whoosh/mixkit_light_pop_whoosh.wav",-8,'s',.5,"«это» из глубины"),
(12.56,POP,-6,'s',.3,"pop «вам?»"),(12.56,"desk/marker_stroke.mp3",-4,'s',.3,"красная линия рисуется"),
(12.78,"impact/mixkit_whoosh_deep_impact.wav",-4,'s',.9,"вспышка, шарнир крупно"),
(12.84,"glitch/kenney_glitch_003.wav",-7,'s',.3,"RGB iPhone Duo"),
(13.74,"whoosh/mixkit_cinematic_fast.wav",-6,'p',.6,"засвет + отъезд камеры"),
(13.84,OPEN,-4,'s',.5,"карточка цены"),(14.08,"tick/el_counter_roll.wav",-4,'s',.55,"счётчик $2 000"),(14.58,"money/el_coin_single.wav",-5,'s',.4,"счётчик встал"),
(14.90,POP,-10,'s',.3,"строка «и получаете»"),(15.08,SOFT,-12,'s',.2,"слово"),(15.56,SOFT,-10,'s',.2,"«только»"),
(15.78,BUB,-4,'s',.3,"чип 256 ГБ"),(16.00,"digital/kenney_highUp.wav",-9,'s',.4,"полоса 12%"),
(16.90,WH,-8,'p',.5,"строка вниз"),(17.20,POP,-9,'s',.3,"«а за»"),
(18.04,ZM,-4,'s',.6,"панч-ин"),(18.04,"tick/el_counter_roll.wav",-4,'s',.55,"счётчик $3 000"),(18.54,"money/el_coin_single.wav",-5,'s',.4,"счётчик встал"),
(18.88,POP,-10,'s',.3,"строка «и получаете»"),(19.08,SOFT,-12,'s',.2,"слово"),
(19.78,GL,-6,'s',.4,"slice 2 ТБ"),(20.00,"digital/kenney_phaserUp3.wav",-7,'s',.5,"полоса до 100%"),
(20.30,WH,-8,'p',.5,"строка вниз"),(20.56,"whoosh/el_whoosh_short.wav",-9,'s',.4,"камера назад"),(20.58,POP,-10,'s',.3,"«которая»"),
(20.62,"digital/kenney_lowDown.wav",-6,'s',.8,"полоса краснеет и ползёт"),
(20.90,ST,-5,'s',.5,"ОЧЕНЬ падает"),(21.18,SW,-6,'s',.6,"МЕДЛЕННАЯ въезжает"),
(21.84,WH,-5,'p',.5,"всё разлетается"),
(21.96,"sub/el_sub_hit_3.wav",-2,'s',1.1,"красная вспышка"),(21.98,"stamp/kenney_impactPunch_heavy_000.wav",-5,'s',.5,"панч-ин"),
(21.98,"swipe/mixkit_fast_swipe_zoom.wav",-7,'s',.5,"красная лента въезжает"),(22.02,POP,-9,'s',.3,"НЕ"),
(22.44,GL,-6,'s',.4,"slice СОВЕТУЮ"),(22.46,ST,-6,'s',.5,"СОВЕТУЮ встаёт"),
(23.16,WH,-5,'p',.5,"лента улетает вправо"),(23.24,"whoosh/el_whoosh_short.wav",-9,'s',.4,"камера назад"),
(23.28,POP,-9,'s',.3,"«лучше»"),(23.72,"stamp/kenney_impactSoft_heavy_002.wav",-3,'s',.6,"КУПИТЬ падает"),
(24.24,OPEN,-4,'s',.5,"окно iPad"),(24.70,POP,-8,'s',.3,"«или»"),(24.96,OPEN,-4,'s',.5,"окно iPhone"),
(25.10,"ui/kenney_minimize_002.wav",-4,'s',.5,"кадр сжимается в окно"),(25.24,WH,-8,'p',.4,"КУПИТЬ вниз"),
(25.42,"whoosh/mixkit_fast_transition.wav",-5,'p',.3,"окно улетает вниз"),
]
rows=[]
for t,f,g,anc,ml,ev in EV:
    x=load(L+f)[:int(ml*SR)]
    fo=min(len(x),int(.03*SR)); x[-fo:]*=np.linspace(1,0,fo)[:,None]
    x=x/ (np.abs(x).max()+1e-9) * 0.5   # одинаковая база: пик -6 dBFS до усиления
    pk=int(np.argmax(np.abs(x).max(1))) if anc=='p' else 0
    st=int(t*SR)-pk
    if st<0: x=x[-st:]; st=0
    e=min(N,st+len(x)); mix[st:e]+=x[:e-st]*10**(g/20)
    rows.append(f"{t:.2f}\t{f}\t{g}\t{ev}")
out=np.clip(mix,-1,1)
with wave.open("/tmp/w/v4/audio/mix4_pre.wav","wb") as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes())
open("/tmp/w/v4/audio/sfx_audit_v4.tsv","w").write("t\tfile\tdB\tвидимое событие\n"+"\n".join(rows))
print(len(EV),"events",round(len(EV)/25.62,2),"/s")
