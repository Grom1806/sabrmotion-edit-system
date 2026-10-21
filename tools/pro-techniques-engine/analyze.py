# Pass 1: person map. face_track.json (per frame, coords in 1920x1080) + matte.mkv (gray alpha 1920x1080)
import subprocess, json, numpy as np, onnxruntime as ort, mediapipe as mp, sys, time
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
W,H=1920,1080; FPS=30000/1001
src=sys.argv[1]; out=sys.argv[2]
dec=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-vf',f'scale={W}:{H}:flags=lanczos','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','gray','-s',f'{W}x{H}','-r','30000/1001','-i','-','-c:v','ffv1',out+'/matte.mkv'],stdin=subprocess.PIPE)
so=ort.SessionOptions(); so.intra_op_num_threads=4
sess=ort.InferenceSession(out+'/models/rvm_mobilenetv3_fp32.onnx',so,providers=['CPUExecutionProvider'])
rec=[np.zeros([1,1,1,1],np.float32)]*4; ds=np.array([0.375],np.float32)
lm=vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=out+'/models/face_landmarker.task'),running_mode=vision.RunningMode.VIDEO,num_faces=1,output_facial_transformation_matrixes=True))
track=[]; i=0; t0=time.time()
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3)
    small=np.ascontiguousarray(f[::2,::2])
    r=lm.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB,data=small),int(i*1000/FPS))
    d=None
    if r.face_landmarks:
        p=np.array([[q.x*W,q.y*H] for q in r.face_landmarks[0]])
        x0,y0=p.min(0); x1,y1=p.max(0)
        le,re=p[33],p[263]; roll=float(np.degrees(np.arctan2(re[1]-le[1],re[0]-le[0])))
        # yaw proxy: nose tip offset vs eye midpoint, normalized by eye distance
        mid=(le+re)/2; ed=np.linalg.norm(re-le); yaw=float((p[1][0]-mid[0])/ed)
        def ear(a,b,c,d_,e,f_): return (np.linalg.norm(p[b]-p[f_])+np.linalg.norm(p[c]-p[e]))/(2*np.linalg.norm(p[a]-p[d_]))
        blink=float((ear(33,160,158,133,153,144)+ear(362,385,387,263,373,380))/2)
        d=dict(cx=float((x0+x1)/2),cy=float((y0+y1)/2),w=float(x1-x0),h=float(y1-y0),roll=roll,yaw=yaw,ear=blink,
               eyes=[float(mid[0]),float(mid[1])],chin=[float(p[152][0]),float(p[152][1])],top=[float(p[10][0]),float(p[10][1])])
    track.append(d)
    x=(f.astype(np.float32)/255).transpose(2,0,1)[None]
    fgr,pha,*rec=sess.run(None,{'src':x,'r1i':rec[0],'r2i':rec[1],'r3i':rec[2],'r4i':rec[3],'downsample_ratio':ds})
    enc.stdin.write((pha[0,0]*255+0.5).clip(0,255).astype(np.uint8).tobytes())
    i+=1
    if i%50==0: print(i, round(time.time()-t0,1), flush=True)
enc.stdin.close(); enc.wait()
json.dump(dict(W=W,H=H,fps=FPS,frames=track),open(out+'/face_track.json','w'))
print('done',i)
