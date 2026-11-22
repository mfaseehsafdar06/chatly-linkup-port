# QA for alpha overlays: composite our RGBA frame over the exact reference frame (QA only; finals never contain ref pixels).
# python qa_over.py <assetDir> <refStartFrame> <tag> j1 j2 ...   -> <asset>/qa/<tag>_NN.jpg  rows: ref | ours-over-ref
import sys,os,subprocess,cv2,numpy as np
d,K0,tag=sys.argv[1],int(sys.argv[2]),sys.argv[3]; js=[int(x) for x in sys.argv[4:]]
REF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','refs','ref.mp4'); os.makedirs(f'{d}/qa',exist_ok=True); rows=[]
for j in js:
    p=f'{d}/qa/_r.png'; subprocess.run(['ffmpeg','-v','error','-y','-i',REF,'-vf',f'select=eq(n\\,{K0+j}),scale=1440:1080','-frames:v','1',p],check=True)
    r=cv2.imread(p).astype(np.float32); m=cv2.imread(f'{d}/tmp/frames/k{j:04d}.png',cv2.IMREAD_UNCHANGED)
    if m is None: print('missing',j); continue
    if m.shape[2]==4: a=m[...,3:4]/255.; c=m[...,:3]*a+r*(1-a)
    else: c=m
    row=np.hstack([cv2.resize(r,(720,540)),np.full((540,8,3),255),cv2.resize(c.astype(np.float32),(720,540))]).astype(np.uint8)
    cv2.putText(row,f'j{j} ref{K0+j}',(10,32),0,.9,(0,255,255),2); rows.append(row)
for i in range(0,len(rows),3): cv2.imwrite(f'{d}/qa/{tag}_{i//3:02d}.jpg',np.vstack(rows[i:i+3]),[cv2.IMWRITE_JPEG_QUALITY,85])
print('ok',len(rows))
