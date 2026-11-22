# Split GPT sheets into transparent cutouts: assets/cut/GPT-XX_NN.png + assets/cut/index.json + contact sheet
import cv2,numpy as np,json,os,sys,glob
os.makedirs('cut',exist_ok=True)
WHOLE={'GPT-07','GPT-10'}          # keep as full plates (zoomed/tracked), no cut
idx={}
ids=sys.argv[1:] or sorted(os.path.basename(p)[:6] for p in glob.glob('gpt/GPT-??.png'))
for gid in ids:
    im=cv2.imread(f'gpt/{gid}.png',cv2.IMREAD_UNCHANGED)
    if im is None: continue
    if gid in WHOLE: cv2.imwrite(f'cut/{gid}_00.png',im);idx[gid]=[{'file':f'{gid}_00.png','bbox':[0,0,im.shape[1],im.shape[0]]}];continue
    bgr=im[...,:3].astype(np.float32)
    if im.shape[2]==4 and im[...,3].min()<250: alpha=im[...,3].astype(np.float32)/255
    else:
        b=np.concatenate([bgr[:8].reshape(-1,3),bgr[-8:].reshape(-1,3),bgr[:,:8].reshape(-1,3),bgr[:,-8:].reshape(-1,3)])
        bg=np.median(b,0);d=np.sqrt(((bgr-bg)**2).sum(2))
        # soft matte: 0 at d<14, 1 at d>40
        alpha=np.clip((d-14)/26,0,1)
        hard=(d>22).astype(np.uint8);hard=cv2.morphologyEx(hard,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
        # fill holes inside each item (white paper inside stickers)
        ff=hard.copy();h,w=ff.shape;mask=np.zeros((h+2,w+2),np.uint8);cv2.floodFill(ff,mask,(0,0),1);holes=(ff==0)
        alpha=np.maximum(alpha,holes.astype(np.float32));alpha=np.maximum(alpha,cv2.erode(hard,np.ones((5,5),np.uint8)).astype(np.float32))
    n,l,s,c=cv2.connectedComponentsWithStats((alpha>.5).astype(np.uint8))
    items=sorted([i for i in range(1,n) if s[i,4]>0.002*alpha.size],key=lambda i:(round(s[i,1]/150),s[i,0]))
    idx[gid]=[]
    for j,i in enumerate(items):
        x,y,w,h=s[i,:4];p=12;x0,y0,x1,y1=max(0,x-p),max(0,y-p),min(im.shape[1],x+w+p),min(im.shape[0],y+h+p)
        a=alpha[y0:y1,x0:x1]*((cv2.dilate((l[y0:y1,x0:x1]==i).astype(np.uint8),np.ones((15,15),np.uint8)))>0)
        a=cv2.GaussianBlur(a,(0,0),.7)
        out=np.dstack([bgr[y0:y1,x0:x1],a*255]).clip(0,255).astype(np.uint8)
        f=f'{gid}_{j:02d}.png';cv2.imwrite(f'cut/{f}',out);idx[gid].append({'file':f,'bbox':[int(x0),int(y0),int(x1-x0),int(y1-y0)]})
    print(gid,len(idx[gid]),'pieces')
old=json.load(open('cut/index.json')) if os.path.exists('cut/index.json') else {}
old.update(idx);json.dump(old,open('cut/index.json','w'),indent=1)
