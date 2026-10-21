import cv2,numpy as np,sys
for p in sys.argv[1:]:
    cap=cv2.VideoCapture(p);prev=None;S=[];C=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(180,320))
        if prev is not None:
            d=np.abs(g.astype(int)-prev.astype(int)).mean()
            if d>25: S.append(np.nan); 
            else:
                fl=cv2.calcOpticalFlowFarneback(prev,g,None,.5,3,15,3,5,1.2,0)
                S.append(np.percentile(np.linalg.norm(fl,axis=2),90))
        prev=g
    S=np.array(S); ratios=[];durs=[]
    i=0;n=len(S)
    while i<n:
        if np.isnan(S[i]) or S[i]<0.3: i+=1; continue
        j=i
        while j<n and not np.isnan(S[j]) and S[j]>=0.3: j+=1
        seg=S[i:j]
        if j-i>=6 and seg.max()>1.0: ratios.append(seg.max()/seg.mean()); durs.append((j-i)/30)
        i=j
    r=np.array(ratios)
    print(f"{p.split('/')[-1][:30]:30s} движений {len(r):3d}  пик/среднее медиана {np.median(r):.2f}  (25-75%: {np.percentile(r,25):.2f}-{np.percentile(r,75):.2f})  длит. медиана {np.median(durs):.2f}s")
