import cv2,numpy as np,json,os,subprocess
FPS=30;LEAD=0.5;TAIL=0.7
VD=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','voice.mp3']))
DUR=LEAD+VD+TAIL;N=int(round(DUR*FPS))
cues=json.load(open('mouth.json'))['mouthCues']
M={k:cv2.imread(f'../v4/mouths/{k}.jpg').astype(np.float32) for k in 'XABCDEFGH'}
E={k:cv2.imread(f'../v4/eyes/{k}.png',cv2.IMREAD_UNCHANGED).astype(np.float32) for k in ['half','closed']}
H,W=720,1280;yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
# whisker regions: rotation-like vertical offset growing with distance from muzzle root
def region(x0,x1,y0,y1,f=14):
  m=np.zeros((H,W),np.float32);m[y0:y1,x0:x1]=1;return cv2.GaussianBlur(m,(0,0),f)
mL=region(500,600,335,425);mR=region(715,930,335,430)
dL=np.clip((605-xx)/100,0,1.4);dR=np.clip((xx-712)/215,0,1.2)
blinks=[LEAD-0.15,LEAD+2.9]
os.makedirs('/tmp/v5f',exist_ok=True)
OPEN=set('BCDEGH')
import sys,time
NN=int(sys.argv[1]) if len(sys.argv)>1 else N
T0=time.time()
for i in range(NN):
  t=i/FPS;vt=t-LEAD;v='X'
  for q in cues:
    if q['start']<=vt<q['end']:v=q['value']
  im=M[v].copy()
  for b in blinks:
    d=t-b
    if 0<=d<0.12:
      e=E['closed' if 0.04<=d<0.08 else 'half'];a=e[...,3:]/255;r=im[180:380,440:880];im[180:380,440:880]=r*(1-a)+e[...,:3]*a
  # whiskers: slow sway + small twitch at open-mouth onsets
  tw=0
  for q in cues:
    if q['value'] in OPEN:
      d=vt-q['start']
      if 0<=d<0.18:tw=max(tw,np.sin(d/0.18*np.pi))
  A=1.6*np.sin(t*2.1)+0.9*tw   # px at full distance
  B=1.6*np.sin(t*2.1+0.7)+0.9*tw
  dy=(mL*dL*np.float32(A)+mR*dR*np.float32(B)).astype(np.float32)
  im=cv2.remap(im,xx,(yy-dy).astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
  # sway + breathing like v4
  a=np.sin(t*1.3)*0.35;sc=1.004+np.sin(t*0.9)*0.004
  Mx=cv2.getRotationMatrix2D((640,540),a,sc);im=cv2.warpAffine(im,Mx,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
  cv2.imwrite(f'/tmp/v5f/f{i:04d}.png',im.clip(0,255).astype(np.uint8))
print(N,DUR,time.time()-T0)
