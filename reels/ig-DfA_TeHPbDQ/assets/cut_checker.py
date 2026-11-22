# Key images whose "transparent" background is a baked-in checkerboard (GPT-06, GPT-12).
import cv2,numpy as np,json,sys
for gid in sys.argv[1:]:
    im=cv2.imread(f'gpt/{gid}.png')[...,:3];f=im.astype(np.float32)
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    mu=cv2.blur(g,(25,25));sd=np.sqrt(np.maximum(cv2.blur(g*g,(25,25))-mu*mu,0))
    neutral=(hsv[...,1]<18)&(g>195)
    bg=(neutral&(sd>2.2)).astype(np.uint8)
    bg=cv2.morphologyEx(bg,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    # bg must connect to the border
    n,l=cv2.connectedComponents(bg);border=set(np.unique(np.r_[l[0],l[-1],l[:,0],l[:,-1]]))-{0}
    bgm=np.isin(l,list(border))
    fg=(~bgm).astype(np.uint8);fg=cv2.morphologyEx(fg,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    fg=cv2.erode(fg,np.ones((3,3),np.uint8))
    a=cv2.GaussianBlur(fg.astype(np.float32),(0,0),1.2)
    n,l,s,c=cv2.connectedComponentsWithStats((a>.5).astype(np.uint8))
    items=sorted([i for i in range(1,n) if s[i,4]>0.004*a.size],key=lambda i:(s[i,1]//200,s[i,0]))
    if gid=='GPT-06': items=[None]
    idx=json.load(open('cut/index.json'));idx[gid]=[]
    for j,i in enumerate(items):
        if i is None: m=a;x,y,w,h=cv2.boundingRect((a>.5).astype(np.uint8))
        else: m=a*(cv2.dilate((l==i).astype(np.uint8),np.ones((9,9),np.uint8))>0);x,y,w,h=s[i,:4]
        p=10;x0,y0,x1,y1=max(0,x-p),max(0,y-p),min(im.shape[1],x+w+p),min(im.shape[0],y+h+p)
        out=np.dstack([f[y0:y1,x0:x1],m[y0:y1,x0:x1]*255]).clip(0,255).astype(np.uint8)
        fn=f'{gid}_{j:02d}.png';cv2.imwrite(f'cut/{fn}',out);idx[gid].append({'file':fn,'bbox':[int(x0),int(y0),int(x1-x0),int(y1-y0)]})
    json.dump(idx,open('cut/index.json','w'),indent=1);print(gid,len(idx[gid]))
