import cv2,numpy as np,sys,json
p=sys.argv[1]; thr=int(sys.argv[2]) if len(sys.argv)>2 else 80
cap=cv2.VideoCapture(p); fps=cap.get(5); rows=[]; prev=None; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    m=(g<thr).astype(np.uint8)
    ys,xs=np.nonzero(m)
    bb=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs)>200 else None
    d=float(np.abs(g.astype(int)-prev.astype(int)).mean()) if prev is not None else 0
    rows.append(dict(t=round(i/fps,4),bb=bb,diff=round(d,3))); prev=g; i+=1
json.dump(dict(fps=fps,rows=rows),open(sys.argv[3],'w'))
print(len(rows),fps)
