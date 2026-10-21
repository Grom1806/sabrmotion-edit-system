from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS=None
box=(6000,9120,18000,19680)  # lon 25..75E, lat 52..8N, 240 px/deg
L=np.asarray(Image.open('dl/bmC1.jpg').crop(box)).astype(np.float32)/255
T=np.asarray(Image.open('dl/topoC1.jpg').crop(box)).astype(np.float32)/255
lum=T@np.array([.3,.59,.11],np.float32)
water=(T[...,2]>T[...,0]+0.03)&(T[...,2]>T[...,1]-0.02)
terr=np.clip(lum*1.25,0,1)**1.25
base=np.stack([terr*0.34,terr*0.25,terr*0.15],-1)
base[water]=base[water]*0.18+np.array([0.012,0.02,0.022],np.float32)
ll=L@np.array([.3,.59,.11],np.float32)
lights=np.clip((ll-0.10)/0.55,0,1)**1.35
gold=np.array([1.0,0.74,0.32],np.float32)
out=1-(1-base)*(1-lights[...,None]*gold)
Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8)).save('map_full.png')
Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8)).resize((1500,1050)).save('map_prev.jpg')
