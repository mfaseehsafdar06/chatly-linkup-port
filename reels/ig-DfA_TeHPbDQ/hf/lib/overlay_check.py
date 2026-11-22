# Overlay an alpha track (tinted yellow) on the reference at the same reel times. python overlay_check.py <assetDir> <tag> <offset> t...
import sys,subprocess,cv2,numpy as np,os
d,tag,off=sys.argv[1],sys.argv[2],float(sys.argv[3]);ts=[float(x) for x in sys.argv[4:]]
REF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','refs','ref.mp4');rows=[]
for t in ts:
    k=round(t*24);m=cv2.imread(f'{d}/tmp/frames/k{k:04d}.png',cv2.IMREAD_UNCHANGED)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{off+t+0.5/24:.4f}','-i',REF,'-frames:v','1','-vf','scale=1440:1080',f'{d}/qa/_r.png'],check=True)
    r=cv2.imread(f'{d}/qa/_r.png').astype(np.float32);a=m[...,3:4]/255.*0.75
    o=r*(1-a)+np.array([0,230,255],np.float32)*a;o=cv2.resize(o.astype(np.uint8),(720,540));cv2.putText(o,f'{t:.2f}s',(10,30),0,.9,(0,0,255),2);rows.append(o)
while len(rows)%3:rows.append(np.zeros_like(rows[0]))
g=[np.hstack(rows[i:i+3]) for i in range(0,len(rows),3)]
cv2.imwrite(f'{d}/qa/{tag}.jpg',np.vstack(g),[cv2.IMWRITE_JPEG_QUALITY,82]);print('ok')
