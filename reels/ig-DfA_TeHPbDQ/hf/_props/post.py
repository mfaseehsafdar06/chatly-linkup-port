# "Photographed paper" pass + encode, for frames written by hf/lib/render.mjs into <asset>/tmp/frames/k%04d.png
# python post.py <assetDir> [--seg k0:k1:r0:r1 ...] [--alpha] [--grain 1.8] [--soft 0.8] [--edge 2.4] [--vig .05] [--name out] [--qa]
#  --seg: our frames k0..k1 get a Lab mean/std match to reference frames r0..r1 (24 fps indices in refs/ref.mp4). Stats only, no ref pixels.
#  --alpha: keep alpha, write ProRes 4444 .mov (grade/grain applied to colour only)
import sys,os,glob,subprocess,cv2,numpy as np
a=sys.argv[1:]; d=os.path.abspath(a[0]); name=os.path.basename(d)
def opt(k,dv):
    return type(dv)(a[a.index(k)+1]) if k in a else dv
segs=[a[i+1] for i,x in enumerate(a) if x=='--seg']; alpha='--alpha' in a
grain,soft,edge,vig=opt('--grain',1.8),opt('--soft',.8),opt('--edge',2.4),opt('--vig',.05); texa=opt('--tex',.012); lift=opt('--lift',1.0); outname=opt('--name',name)
ratio_lo,ratio_hi=opt('--rlo',.85),opt('--rhi',1.15)
F=f'{d}/tmp/frames'; P=f'{d}/tmp/frames' if '--stills' in a else f'{d}/tmp/post'; os.makedirs(P,exist_ok=True); fs0=sorted(glob.glob(F+'/k*.png'))
if '--stills' not in a: [os.remove(x) for x in glob.glob(P+'/*.png')]
fs=sorted(glob.glob(F+'/k*.png')); H,W=1080,1440
REF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','refs','ref.mp4')
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); rr=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
ramp=np.clip((rr-.55)/.6,0,1)[...,None]; vg=(1-vig*rr**2)[...,None]
rng=np.random.default_rng(5)
tex=cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype(np.float32),(0,0),40); tex=(tex/tex.std())[...,None]
fib=cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype(np.float32),(0,0),1.3); fib=(fib/fib.std())[...,None]
def refframes(r0,r1):
    tmp=f'{d}/tmp/_ref'; os.makedirs(tmp,exist_ok=True); [os.remove(x) for x in glob.glob(tmp+'/*')]
    subprocess.run(['ffmpeg','-v','error','-i',REF,'-vf',f"select=between(n\\,{r0}\\,{r1}),scale=480:360",'-fps_mode','passthrough',f'{tmp}/r%03d.png'],check=True)
    return sorted(glob.glob(tmp+'/*.png'))
def look(im):
    f=im.astype(np.float32)
    s1=cv2.GaussianBlur(f,(0,0),soft) if soft>0 else f; s2=cv2.GaussianBlur(f,(0,0),edge)
    o=s1*(1-ramp)+s2*ramp
    o=o*(1+texa*tex+texa*.5*fib)*vg*lift
    return o
GR={}
for s_ in segs:
    k0,k1,r0,r1=map(int,s_.split(':')); RF=refframes(r0,r1)
    ks=[int(os.path.basename(x)[1:5]) for x in fs]; ks=[k for k in ks if k0<=k<=k1]; ks=ks[::max(1,len(ks)//12)]
    R=[];M=[]
    for k in ks:
        im=cv2.imread(f'{F}/k{k:04d}.png',cv2.IMREAD_UNCHANGED)
        ri=min(len(RF)-1,round((k-k0)*(r1-r0)/max(1,k1-k0))); ref=cv2.imread(RF[ri])
        rgb=np.clip(look(im[...,:3]),0,255).astype(np.uint8); sm=cv2.resize(rgb,(480,360),interpolation=cv2.INTER_AREA)
        msk=(cv2.resize(im[...,3],(480,360))>220) if im.shape[2]==4 else np.ones((360,480),bool)
        M.append(cv2.cvtColor(sm,cv2.COLOR_BGR2LAB)[msk].astype(np.float64)); R.append(cv2.cvtColor(ref,cv2.COLOR_BGR2LAB)[msk].astype(np.float64))
    R=np.concatenate(R);M=np.concatenate(M); mr,sr=R.mean(0),R.std(0); mm,sm_=M.mean(0),M.std(0)
    ratio=np.clip(sr/(sm_+1e-6),ratio_lo,ratio_hi)
    for k in range(k0,k1+1): GR[k]=(mm,mr,ratio)
    print('seg',s_,'ref',mr.round(1),'ours',mm.round(1),'ratio',ratio.round(2))
for p in fs:
    k=int(os.path.basename(p)[1:5]); im=cv2.imread(p,cv2.IMREAD_UNCHANGED)
    rgb=look(im[...,:3])
    if k in GR:
        mm,mr,ratio=GR[k]; L=cv2.cvtColor(np.clip(rgb,0,255).astype(np.uint8),cv2.COLOR_BGR2LAB).astype(np.float32)
        L=(L-mm)*ratio+mr; rgb=cv2.cvtColor(np.clip(L,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR).astype(np.float32)
    rgb=rgb+np.random.default_rng(k).normal(0,grain,(H,W))[...,None]
    o=np.clip(rgb,0,255).astype(np.uint8)
    if alpha and im.shape[2]==4:
        al=cv2.GaussianBlur(im[...,3],(0,0),.6); o=np.dstack([o,al])
    cv2.imwrite(f'{P}/k{k:04d}.png',o)
if '--stills' in a: print('stills post done',len(fs)); sys.exit(0)
os.makedirs(f'{d}/out',exist_ok=True)
if alpha: subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',f'{P}/k%04d.png','-c:v','prores_ks','-profile:v','4444','-pix_fmt','yuva444p10le',f'{d}/out/{outname}.mov'],check=True); print('wrote',f'{d}/out/{outname}.mov',len(fs))
else: subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',f'{P}/k%04d.png','-c:v','libx264','-crf','14','-pix_fmt','yuv420p',f'{d}/out/{outname}.mp4'],check=True); print('wrote',f'{d}/out/{outname}.mp4',len(fs))
