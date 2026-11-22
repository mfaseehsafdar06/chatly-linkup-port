# Side-by-side ref vs ours at the same moments.
# python hf/lib/compare.py <assetDir> <shotStartSec> <tag> t1 t2 ...   (t = seconds from the asset start)
# needs: ours rendered as stills first (render.mjs --frames) or full frames in assetDir/tmp/frames (k = round(t*24)).
# writes assetDir/qa/<tag>_NN.jpg  (left = reference at shotStart+t, right = ours)
import sys,os,subprocess,cv2,numpy as np
d,t0,tag=sys.argv[1],float(sys.argv[2]),sys.argv[3];ts=[float(x) for x in sys.argv[4:]]
REF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','refs','ref.mp4')
os.makedirs(f'{d}/qa',exist_ok=True);rows=[]
for t in ts:
    k=round(t*24);mine=cv2.imread(f'{d}/tmp/frames/k{k:04d}.png',cv2.IMREAD_UNCHANGED)
    if mine is None: print('missing frame',k);continue
    if mine.shape[2]==4:  # alpha: show over checker
        a=mine[...,3:4]/255.;chk=np.indices(mine.shape[:2]).sum(0)//24%2*40+90;mine=(mine[...,:3]*a+chk[...,None]*(1-a)).astype(np.uint8)
    p=f'{d}/qa/_ref.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t0+t+0.5/24:.4f}','-i',REF,'-frames:v','1',p],check=True)
    r=cv2.resize(cv2.imread(p),(720,540));m=cv2.resize(mine,(720,540))
    row=np.hstack([r,np.full((540,8,3),255,np.uint8),m]);cv2.putText(row,f'+{t:.3f}s  abs {t0+t:.3f}',(10,32),0,.9,(0,255,255),2);rows.append(row)
for i in range(0,len(rows),3):
    cv2.imwrite(f'{d}/qa/{tag}_{i//3:02d}.jpg',np.vstack(rows[i:i+3]),[cv2.IMWRITE_JPEG_QUALITY,85])
print('ok',len(rows))
