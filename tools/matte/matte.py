# Маска человека для «текста за головой»: видео → person.webm (VP9 с альфой) + track.json (лицо, макушка по кадрам).
# python3 matte.py head.mp4 out_dir models_dir
# Модели: selfie_multiclass_256x256.tflite и blaze_face_short_range.tflite из storage.googleapis.com/mediapipe-models
# Нужно: pip install mediapipe opencv-python; в контейнере apt-get install libegl1 libgles2
import sys, os
import cv2, numpy as np, json, subprocess, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
src, out, models = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
seg=vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpt.BaseOptions(model_asset_path=os.path.join(models,"selfie_multiclass.tflite")),running_mode=vision.RunningMode.VIDEO,output_confidence_masks=True))
fd=vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=mpt.BaseOptions(model_asset_path=os.path.join(models,"face_detector.tflite")),running_mode=vision.RunningMode.VIDEO))
cap=cv2.VideoCapture(src); fps=cap.get(5); W,H=int(cap.get(3)),int(cap.get(4))
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(fps),"-i","-","-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","4M","-auto-alt-ref","0",os.path.join(out,"person.webm")],stdin=subprocess.PIPE)
prev=None; track=[]; i=0
while True:
    ok,fr=cap.read()
    if not ok: break
    rgb=cv2.cvtColor(fr,cv2.COLOR_BGR2RGB); img=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb); ts=int(i*1000/fps)
    r=seg.segment_for_video(img,ts)
    bg=r.confidence_masks[0].numpy_view()
    m=1.0-bg
    m=cv2.resize(m,(W,H),interpolation=cv2.INTER_LINEAR)
    m=np.clip((m-0.35)/0.3,0,1)
    if prev is not None: m=0.6*m+0.4*prev
    prev=m
    a=(cv2.GaussianBlur(m,(0,0),1.5)*255).astype(np.uint8)
    rgba=np.dstack([rgb,a]); ff.stdin.write(rgba.tobytes())
    # head top from matte (column band around face)
    d=fd.detect_for_video(img,ts); face=None
    if d.detections:
        b=d.detections[0].bounding_box; face=[b.origin_x,b.origin_y,b.width,b.height]
    top=None
    if face:
        cx=face[0]+face[2]//2; band=m[:, max(0,cx-60):cx+60].mean(1)
        ys=np.where(band>0.5)[0]; top=int(ys[0]) if len(ys) else None
    track.append({"t":round(i/fps,3),"face":face,"top":top}); i+=1
ff.stdin.close(); ff.wait()
json.dump(track,open(os.path.join(out,"track.json"),"w"))
print(i,"frames")
