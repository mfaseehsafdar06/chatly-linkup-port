# Clean the GPT-12 hand cutouts: drop the blank white card the hand holds and stray fragments.
# Writes hands/H0.png (slap palm), H1.png (pinch), H2.png (grip) + hands.json (crop offsets, normalised to the cleaned image).
import cv2,numpy as np,json,os
C='../../assets/cut/'; out={}
for i in range(3):
    im=cv2.imread(f'{C}GPT-12_0{i}.png',cv2.IMREAD_UNCHANGED).astype(np.float32)
    rgb=im[...,:3]; a=im[...,3]/255.
    mn=rgb.min(2); mx=rgb.max(2)
    white=(mn>195)&((mx-mn)<28)
    keep=(a>0.5)&~white
    keep=cv2.morphologyEx(keep.astype(np.uint8),cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    n,l,s,_=cv2.connectedComponentsWithStats(keep); k=1+np.argmax(s[1:,4]); m=(l==k).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    mf=cv2.GaussianBlur(m.astype(np.float32),(0,0),1.2)
    na=np.minimum(a,mf)
    # kill white fringe: despill toward skin where alpha partial
    o=np.dstack([rgb,na*255]).clip(0,255).astype(np.uint8)
    ys,xs=np.where(na>0.05); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    o=o[y0:y1,x0:x1]; cv2.imwrite(f'hands/H{i}.png',o)
    H,W=im.shape[:2]
    out[f'H{i}']={'orig':[W,H],'crop':[int(x0),int(y0),int(x1),int(y1)]}
    print(i,o.shape,(x0,y0,x1,y1))
json.dump(out,open('hands/hands.json','w'),indent=1)
# H2 cleanup: remove the beige card sliver at the top-left of the arm (left 260 px, top 150 px of H2)
im=cv2.imread('hands/H2.png',cv2.IMREAD_UNCHANGED); im[:150,:260,3]=0
r=im[...,:3].astype(int); sl=(im[...,3]>0)&(r.min(2)>170)&(np.arange(im.shape[1])[None,:]<300); im[sl,3]=0
cv2.imwrite('hands/H2.png',im); print('H2 cleaned')
# H0L: slap palm with a long forearm (bottom rows stretched downward) so the arm can run off-frame at small hand sizes.
im=cv2.imread('hands/H0.png',cv2.IMREAD_UNCHANGED); h,w=im.shape[:2]
a=im[...,3]; rows=[y for y in range(h) if (a[y]>128).sum()>20]; yb=rows[-1]
band=im[yb-60:yb-20]                                   # forearm band just above the cut
ext=cv2.resize(band,(w,1400),interpolation=cv2.INTER_LINEAR)
xs=np.where(band[...,3].max(0)>128)[0]; cx=(xs.min()+xs.max())/2
for y in range(ext.shape[0]):                          # forearm widens toward the elbow (x1.0 -> x1.45)
    k=1+.45*min(1,y/900); M=np.float32([[k,0,cx*(1-k)]]); row=ext[y:y+1]
    ext[y:y+1]=cv2.warpAffine(row,np.vstack([M,[[0,1,0]]]).astype(np.float32),(w,1),flags=cv2.INTER_LINEAR)
ext=cv2.GaussianBlur(ext,(0,0),sigmaX=1.5,sigmaY=12)
out=np.vstack([im[:yb-20],ext]); out=np.hstack([np.zeros((out.shape[0],250,4),np.uint8),out,np.zeros((out.shape[0],250,4),np.uint8)]); cv2.imwrite('hands/H0L.png',out); print('H0L',out.shape)
