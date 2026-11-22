# python post.py <framesdir> <outdir>: per-shot Lab stats match to the reference shot, softness, grain
import sys,os,glob,cv2,numpy as np
fd,od=sys.argv[1],sys.argv[2];os.makedirs(od,exist_ok=True)
SHOTS=[('G',0,26,.6),('S1',27,44,1.5),('S2',45,58,1.5),('S3',59,69,1.5),('S4',70,83,1.5),('S5',84,94,1.5),('Z',95,97,1.2),('S6',98,101,1.6)]
lab=lambda im:cv2.cvtColor(cv2.resize(im,(480,360),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2LAB).reshape(-1,3).astype(np.float32)
rng=np.random.default_rng(7)
for name,k0,k1,sig in SHOTS:
    R=np.concatenate([lab(cv2.imread(f'ref24/r{k+4:03d}.png')) for k in range(k0,k1+1)])
    Mf=[cv2.imread(f'{fd}/k{k:03d}.png') for k in range(k0,k1+1)]
    Mm=np.concatenate([lab(x) for x in Mf])
    mr,sr=R.mean(0),R.std(0);mm,sm=Mm.mean(0),Mm.std(0)
    ratio=np.clip(sr/(sm+1e-6),.8,1.25);ratio[1:]=np.clip(ratio[1:],1.0,1.25)
    for i,k in enumerate(range(k0,k1+1)):
        L=cv2.cvtColor(Mf[i],cv2.COLOR_BGR2LAB).astype(np.float32)
        L=(L-mm)*ratio+mr
        out=cv2.cvtColor(np.clip(L,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR)
        if sig>0: out=cv2.GaussianBlur(out,(0,0),sig)
        out=np.clip(out.astype(np.float32)+rng.normal(0,2.5,out.shape[:2])[...,None],0,255).astype(np.uint8)
        cv2.imwrite(f'{od}/k{k:03d}.png',out)
    print(name,'ref mean',mr.round(1),'mine',mm.round(1),'ratio',ratio.round(2))
