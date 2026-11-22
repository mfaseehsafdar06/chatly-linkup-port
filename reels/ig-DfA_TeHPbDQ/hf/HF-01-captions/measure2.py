import json,subprocess,cv2,numpy as np
from PIL import ImageFont
W=json.load(open('cues.json'));M=json.load(open('measured.json'));REF='../../refs/ref.mp4'
F=lambda s,it=False:ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',int(s),index=(3 if it else 1))
def ink(txt,size,it=False):
    b=F(size,it).getbbox(txt);return b[2]-b[0],b[3]-b[1]
# global scale from good measurements
ks=[]
for i,c in enumerate(W):
    b=M[i]
    if not b:continue
    w,h=ink(c['txt'],100,c.get('italic'));s=100*(b[2]-b[0])/w;hp=h*s/100
    if .75<(b[3]-b[1])/hp<1.33: ks.append(s/c['size'])
k=float(np.median(ks));print('scale',round(k,3))
def fr(t):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.4f}','-i',REF,'-frames:v','1','-vf','scale=1440:1080','qa/_m.png'],check=True);return cv2.imread('qa/_m.png')
over={}
groups={}
for i,c in enumerate(W): groups.setdefault(round(c['t'],2),[]).append(i)
for t,ids in groups.items():
    ok=all(M[i] and .75<(M[i][3]-M[i][1])/(ink(W[i]['txt'],100,W[i].get('italic'))[1]*(100*(M[i][2]-M[i][0])/ink(W[i]['txt'],100,W[i].get('italic'))[0])/100)<1.33 for i in ids) and len(ids)==1
    if ok and not (ids[0]>0 and M[ids[0]-1]==M[ids[0]]): continue
    a=fr(t+3/24);b=fr(t-1.5/24)
    hsv=cv2.cvtColor(a,cv2.COLOR_BGR2HSV).astype(int);white=(hsv[...,2]>210)&(hsv[...,1]<50)
    d=np.abs(a.astype(int)-b.astype(int)).max(2)>60
    m=cv2.morphologyEx((white&d).astype(np.uint8),cv2.MORPH_CLOSE,np.ones((7,int(30*k/1.5)),np.uint8))
    n,l,s,cc=cv2.connectedComponentsWithStats(m)
    txt=' '.join(W[i]['txt'] for i in ids);size=W[ids[0]]['size']*k
    ew,eh=ink(txt,size,W[ids[0]].get('italic'))
    c0=W[ids[0]];sx=(c0['x'] if c0['x'] is not None else c0['centre']-ew/2)+ew/2;sy=c0['y']
    best=None
    for q in range(1,n):
        x,y,w,h,ar=s[q]
        if ar<100: continue
        rw=w/ew;rh=h/eh
        if not(.6<rw<1.6 and .55<rh<1.7): continue
        dist=abs(x+w/2-sx)/2+abs(y+h/2-sy)
        if best is None or dist<best[0]: best=(dist,(x,y,w,h))
    if not best or best[0]>450: print('miss',t,txt);continue
    x,y,w,h=best[1]
    if len(ids)==1: over[ids[0]]=[int(x),int(y),int(x+w),int(y+h)]
    else:  # split horizontally by text widths (same line) — if stacked vertically we'd mis-split; check aspect
        sc=w/ew;cur=x
        for i in ids:
            wi,hi=ink(W[i]['txt'],size,W[i].get('italic'));over[i]=[int(cur),int(y),int(cur+wi*sc),int(y+h)];cur+=(wi+ink(' ',size)[0]+size*.25)*sc
    print('fix',t,txt,best[1])
json.dump(over,open('overrides.json','w'))
