# Measure each word-pop cue in the reference: diff frame before vs after its appear time, keep white low-sat pixels.
import json,subprocess,cv2,numpy as np,os
W=json.load(open('cues.json'));REF='../../refs/ref.mp4'
def fr(t):
    p='/tmp/_m.png' if False else 'qa/_m.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.4f}','-i',REF,'-frames:v','1','-vf','scale=1440:1080',p],check=True);return cv2.imread(p)
out=[];prev_after=None
for i,c in enumerate(W):
    t=c['t'];a=fr(t+2.5/24);b=fr(t-1.5/24)
    hsv=cv2.cvtColor(a,cv2.COLOR_BGR2HSV).astype(int)
    white=(hsv[...,2]>215)&(hsv[...,1]<45)
    d=np.abs(a.astype(int)-b.astype(int)).max(2)>70
    m=(white&d).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,25),np.uint8))
    n,l,s,cc=cv2.connectedComponentsWithStats(m)
    # pick the component nearest to the spec position (if spec x given) with reasonable size
    sx=(c['x'] if c['x'] is not None else c['centre']-100)+60;sy=c['y']
    best=None
    for k in range(1,n):
        x,y,w,h,ar=s[k]
        if ar<150 or h<18 or h>260 or w>1200: continue
        dist=abs((x+w/2)-sx)/3+abs((y+h/2)-sy)
        if best is None or dist<best[0]: best=(dist,[int(x),int(y),int(x+w),int(y+h)])
    out.append(best[1] if best and best[0]<500 else None)
    print(i,c['txt'],out[-1])
json.dump(out,open('measured.json','w'))
