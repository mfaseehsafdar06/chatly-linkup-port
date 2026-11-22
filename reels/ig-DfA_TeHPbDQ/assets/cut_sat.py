import cv2,numpy as np,json,sys
idx=json.load(open('cut/index.json'))
def save(gid,items,im,alpha):
    idx[gid]=[]
    for k,(m,(x,y,w,h)) in enumerate(items):
        p=12;x0,y0,x1,y1=max(0,x-p),max(0,y-p),min(im.shape[1],x+w+p),min(im.shape[0],y+h+p)
        a=alpha[y0:y1,x0:x1]*(cv2.dilate(m[y0:y1,x0:x1],np.ones((7,7),np.uint8))>0)
        out=np.dstack([im[y0:y1,x0:x1,:3].astype(np.float32),a*255]).clip(0,255).astype(np.uint8)
        fn=f'{gid}_{k:02d}.png';cv2.imwrite(f'cut/{fn}',out);idx[gid].append({'file':fn,'bbox':[int(x0),int(y0),int(x1-x0),int(y1-y0)]})
    print(gid,len(items))
for gid in ['GPT-04','GPT-05','GPT-11']:
    im=cv2.imread(f'gpt/{gid}.png');hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV).astype(int);g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(int)
    # background luminance model from a heavy blur of the border-connected neutral area
    bgl=np.median(np.r_[g[:10].ravel(),g[-10:].ravel(),g[:,:10].ravel(),g[:,-10:].ravel()])
    fg=((hsv[...,1]>45)|(g>bgl+14)|(g<bgl-45)).astype(np.uint8)
    fg=cv2.morphologyEx(fg,cv2.MORPH_OPEN,np.ones((5,5),np.uint8));fg=cv2.morphologyEx(fg,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
    ff=fg.copy();h,w=ff.shape;mk=np.zeros((h+2,w+2),np.uint8);cv2.floodFill(ff,mk,(0,0),1);fg=np.maximum(fg,(ff==0).astype(np.uint8))
    alpha=cv2.GaussianBlur(fg.astype(np.float32),(0,0),1.0)
    n,l,s,c=cv2.connectedComponentsWithStats(fg)
    items=[((l==i).astype(np.uint8),tuple(s[i,:4])) for i in range(1,n) if s[i,4]>0.004*fg.size]
    items.sort(key=lambda z:(z[1][1]//250,z[1][0]));save(gid,items,im,alpha)
# GPT-12: split the merged palm / lower hand along a line
im=cv2.imread('gpt/GPT-12.png');a0=cv2.imread('cut/GPT-12_00.png',cv2.IMREAD_UNCHANGED)
b=idx['GPT-12'][0]['bbox'];x0,y0=b[0],b[1]
A=np.zeros(im.shape[:2],np.float32);A[y0:y0+a0.shape[0],x0:x0+a0.shape[1]]=a0[...,3]/255.
yy,xx=np.mgrid[0:im.shape[0],0:im.shape[1]]
H,W=im.shape[:2];line=(H*0.74)-(xx/W)*(H*0.12)       # y of the split line at each x
top=((A>.5)&(yy<line)).astype(np.uint8);bot=((A>.5)&(yy>=line)).astype(np.uint8)
a1=cv2.imread('cut/GPT-12_01.png',cv2.IMREAD_UNCHANGED);b1=idx['GPT-12'][1]['bbox']
A1=np.zeros_like(A);A1[b1[1]:b1[1]+a1.shape[0],b1[0]:b1[0]+a1.shape[1]]=a1[...,3]/255.
pin=(A1>.5).astype(np.uint8);alpha=np.maximum(A,A1)
items=[(top,cv2.boundingRect(top)),(pin,cv2.boundingRect(pin)),(bot,cv2.boundingRect(bot))]
for f in ['GPT-12_00.png','GPT-12_01.png']:
    import os;os.remove('cut/'+f)
save('GPT-12',items,im,alpha)
json.dump(idx,open('cut/index.json','w'),indent=1)
