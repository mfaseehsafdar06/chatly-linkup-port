# python post2.py <framesdir> <outdir>: Lab match per shot + photographed-print look on map shots
import sys,os,cv2,numpy as np
fd,od=sys.argv[1],sys.argv[2];os.makedirs(od,exist_ok=True)
SHOTS=[('G',0,26),('S1',27,44),('S2',45,58),('S3',59,69),('S4',70,83),('S5',84,94),('Z',95,97),('S6',98,101)]
# per shot: focus ramp direction (angle deg of the blurry side), glare band angle/pos
LOOK={'S1':(90,30,.35),'S2':(80,25,.55),'S3':(100,35,.3),'S4':(85,28,.6),'S5':(95,32,.4),'Z':(90,30,.5),'S6':(90,22,.45)}
H,W=1080,1440;yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
lab=lambda im:cv2.cvtColor(cv2.resize(im,(480,360),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2LAB).reshape(-1,3).astype(np.float32)
rng=np.random.default_rng(7)
tex=cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype(np.float32),(0,0),2.5);tex=tex/tex.std()
tex2=cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype(np.float32),(0,0),60);tex2=tex2/tex2.std()
vig=1-.06*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
def printlook(im,name,k):
    fa,ga,gp=LOOK[name]
    th=np.radians(fa);d=((xx-W/2)*np.cos(th)+(yy-H/2)*np.sin(th))/(H/2)   # -1..1 toward blurry side
    ramp=np.clip((-d+.15)/1.0,0,1)[...,None]                                # far side = up
    soft=cv2.GaussianBlur(im,(0,0),1.0);far=cv2.GaussianBlur(im,(0,0),3.6)
    f=im.astype(np.float32);out=soft*(1-ramp)+far*ramp
    # paper/laminate texture
    out=out*(1+.007*tex[...,None]+.018*tex2[...,None])
    # glare band (laminate)
    ga_=np.radians(ga);u=((xx/W)*np.cos(ga_)+(yy/H)*np.sin(ga_))
    drift=.015*np.sin(k*.21)
    band=np.exp(-((u-gp-drift)/.09)**2)*.16+np.exp(-((u-gp-.12-drift)/.03)**2)*.07
    out=out+(255-out)*band[...,None]
    out=out*vig[...,None]
    # chromatic aberration: scale R out, B in
    o=np.clip(out,0,255).astype(np.uint8);b,g,r=cv2.split(o)
    def sc(ch,s):M=cv2.getRotationMatrix2D((W/2,H/2),0,s);return cv2.warpAffine(ch,M,(W,H),borderMode=cv2.BORDER_REFLECT)
    return cv2.merge([sc(b,.9985),g,sc(r,1.0018)])
for name,k0,k1 in SHOTS:
    R=np.concatenate([lab(cv2.imread(f'ref24/r{k+4:03d}.png')) for k in range(k0,k1+1)])
    Mf=[cv2.imread(f'{fd}/k{k:03d}.png') for k in range(k0,k1+1)]
    if name!='G':Mf=[printlook(x,name,k0+i) for i,x in enumerate(Mf)]
    Mm=np.concatenate([lab(x) for x in Mf])
    mr,sr=R.mean(0),R.std(0);mm,sm=Mm.mean(0),Mm.std(0)
    ratio=np.clip(sr/(sm+1e-6),.8,1.15)
    for i,k in enumerate(range(k0,k1+1)):
        L=cv2.cvtColor(Mf[i],cv2.COLOR_BGR2LAB).astype(np.float32);L=(L-mm)*ratio+mr
        out=cv2.cvtColor(np.clip(L,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR)
        if name=='G':out=cv2.GaussianBlur(out,(0,0),.7)
        out=np.clip(out.astype(np.float32)+rng.normal(0,1.6,out.shape[:2])[...,None],0,255).astype(np.uint8)
        cv2.imwrite(f'{od}/k{k:03d}.png',out)
    print(name,'ratio',ratio.round(2))
