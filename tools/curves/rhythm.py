import cv2,numpy as np,sys
for p in sys.argv[1:]:
    cap=cv2.VideoCapture(p);fps=cap.get(5);prev=None;D=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(270,480)).astype(int)
        if prev is not None:D.append(np.abs(g-prev).mean())
        prev=g
    D=np.array(D);n=len(D);dur=n/fps
    static=(D<0.15).mean();cuts=(D>25).sum()
    # longest static run
    run=m=0
    for x in D<0.15:
        run=run+1 if x else 0; m=max(m,run)
    # motion "waves": smooth 0.5s and count peaks
    k=int(fps/2);s=np.convolve(D,np.ones(k)/k,'same')
    cv=s.std()/s.mean()
    print(f"{p.split('/')[-1][:34]:34s} {dur:5.1f}s статично {static*100:4.0f}% макс.пауза {m/fps:4.2f}s резов/мин {cuts/dur*60:5.1f} вариативность {cv:.2f}")
