# Re-split merged sheets with watershed seeded from a strongly eroded mask. python cut_split.py GPT-04:41 GPT-05:41 ...
import cv2,numpy as np,json,sys
idx=json.load(open('cut/index.json'))
for arg in sys.argv[1:]:
    gid,ek=arg.split(':');ek=int(ek);group=gid=='GPT-12'
    im=cv2.imread(f'gpt/{gid}.png',cv2.IMREAD_UNCHANGED)
    if gid=='GPT-12':
        # reuse checker key alpha from the earlier full-res pieces: rebuild alpha the same way
        import subprocess
    bgr=im[...,:3].astype(np.float32)
    if gid=='GPT-12':
        g=cv2.cvtColor(im[...,:3],cv2.COLOR_BGR2GRAY).astype(np.float32);hsv=cv2.cvtColor(im[...,:3],cv2.COLOR_BGR2HSV)
        mu=cv2.blur(g,(25,25));sd=np.sqrt(np.maximum(cv2.blur(g*g,(25,25))-mu*mu,0))
        bg=((hsv[...,1]<18)&(g>195)&(sd>2.2)).astype(np.uint8);bg=cv2.morphologyEx(bg,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
        n,l=cv2.connectedComponents(bg);border=set(np.unique(np.r_[l[0],l[-1],l[:,0],l[:,-1]]))-{0}
        hard=(~np.isin(l,list(border))).astype(np.uint8);hard=cv2.morphologyEx(hard,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8));hard=cv2.erode(hard,np.ones((3,3),np.uint8))
        alpha=cv2.GaussianBlur(hard.astype(np.float32),(0,0),1.2)
        seeds=cv2.dilate(hard,np.ones((ek,ek),np.uint8))   # group hand+card
    else:
        b=np.concatenate([bgr[:8].reshape(-1,3),bgr[-8:].reshape(-1,3),bgr[:,:8].reshape(-1,3),bgr[:,-8:].reshape(-1,3)]);bgc=np.median(b,0)
        d=np.sqrt(((bgr-bgc)**2).sum(2));alpha=np.clip((d-14)/26,0,1)
        hard=(d>22).astype(np.uint8);hard=cv2.morphologyEx(hard,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
        ff=hard.copy();h,w=ff.shape;mk=np.zeros((h+2,w+2),np.uint8);cv2.floodFill(ff,mk,(0,0),1);hard=np.maximum(hard,(ff==0).astype(np.uint8))
        alpha=np.maximum(alpha,cv2.erode(hard,np.ones((5,5),np.uint8)).astype(np.float32))
        seeds=cv2.erode(hard,np.ones((ek,ek),np.uint8))
    n,mk=cv2.connectedComponents(seeds)
    sizes=[(mk==i).sum() for i in range(n)]
    markers=np.zeros(hard.shape,np.int32)
    keep=[i for i in range(1,n) if sizes[i]>0.003*hard.size]
    for j,i in enumerate(keep): markers[mk==i]=j+2
    if not group:
        markers[hard==0]=1
        ws=cv2.watershed(im[...,:3].copy(),markers)
    else:
        ws=np.where(hard>0,markers,1)
    items=[]
    for j in range(len(keep)):
        m=(ws==j+2).astype(np.uint8)
        if m.sum()==0: continue
        x,y,w,h=cv2.boundingRect(m);items.append((y//200,x,j,m,(x,y,w,h)))
    items.sort(key=lambda z:(z[0],z[1]));idx[gid]=[]
    for k,(_,_,j,m,(x,y,w,h)) in enumerate(items):
        p=12;x0,y0,x1,y1=max(0,x-p),max(0,y-p),min(im.shape[1],x+w+p),min(im.shape[0],y+h+p)
        a=alpha[y0:y1,x0:x1]*(cv2.dilate(m[y0:y1,x0:x1],np.ones((7,7),np.uint8))>0)
        out=np.dstack([bgr[y0:y1,x0:x1],a*255]).clip(0,255).astype(np.uint8)
        fn=f'{gid}_{k:02d}.png';cv2.imwrite(f'cut/{fn}',out);idx[gid].append({'file':fn,'bbox':[int(x0),int(y0),int(x1-x0),int(y1-y0)]})
    print(gid,len(idx[gid]))
json.dump(idx,open('cut/index.json','w'),indent=1)
