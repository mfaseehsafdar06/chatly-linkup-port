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
