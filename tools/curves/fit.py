import json,numpy as np
from scipy.optimize import least_squares
def bez(t,x1,y1,x2,y2):
    # solve x(s)=t then y(s)
    s=np.linspace(0,1,2001)
    X=3*(1-s)**2*s*x1+3*(1-s)*s**2*x2+s**3
    Y=3*(1-s)**2*s*y1+3*(1-s)*s**2*y2+s**3
    return np.interp(t,X,Y)
def fit(ts,vs):
    ts=np.array(ts);vs=np.array(vs,float)
    tn=(ts-ts[0])/(ts[-1]-ts[0]); vn=(vs-vs[0])/(vs[-1]-vs[0])
    r=least_squares(lambda p:bez(tn,*p)-vn,[.4,0,.2,1],bounds=([0,-1,0,0],[1,2,1,2]))
    err=np.abs(r.fun).max()
    # where is peak velocity
    v=np.gradient(vn,tn); pk=tn[np.argmax(v)]
    return [round(x,2) for x in r.x],round(err,3),round(pk,2),round(v.max(),2)
d=json.load(open('ui.json'));R=d['rows']
def seg(a,b,fn):
    xs=[r for r in R if a<=r['t']<=b and r['bb']]
    return [r['t'] for r in xs],[fn(r['bb']) for r in xs]
H=lambda b:b[3]-b[1]; W=lambda b:b[2]-b[0]
for name,a,b,fn in [("линия→карточка: рост высоты",0.067,1.1,H),("карточка растёт до квадрата (ширина)",1.0,2.0,W),("после смены: досадка высоты",2.2,3.0,H),("дрейф камеры к следующей станции",3.0,3.95,W)]:
    t,v=seg(a,b,fn); print(name, f"{t[-1]-t[0]:.2f}s", fit(t,v))
# AE ease influence 90% both sides
print("наш AE ease 90/90 ~ bezier(0.9,0,0.1,1); peak vel at 0.5, max vel", round(max(np.gradient(bez(np.linspace(0,1,300),.9,0,.1,1),np.linspace(0,1,300))),2))
