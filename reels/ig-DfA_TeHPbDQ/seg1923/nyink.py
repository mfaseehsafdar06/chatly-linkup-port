import cv2,numpy as np
def red(n):
    im=cv2.imread(f'ref24/r{n:03d}.png');im=cv2.resize(im,(1440,1080),interpolation=cv2.INTER_CUBIC)
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV).astype(int);h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    a=(((h<10)|(h>165))&(s>95)&(v>70)).astype(np.float32)
    return cv2.GaussianBlur(a,(0,0),1.2)
roi=np.zeros((1080,1440),np.float32);cv2.fillPoly(roi,[np.array([[620,250],[1220,250],[1220,720],[900,720],[860,520],[620,560]])],1)
# exclude NYC circle region (ellipse) and Canada circle
cv2.ellipse(roi,(687,657),(175,140),0,0,360,0,-1)
full=red(87)*roi; early=red(76)*roi
ys,xs=np.where(full>.3);print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
n,l,s,c=cv2.connectedComponentsWithStats((full>.3).astype(np.uint8))
for i in range(1,n):
    if s[i,4]>80: print(i,s[i][:5],'early frac',round(float((early[l==i]>.3).mean()),2))
cv2.imwrite('gen/ny_full.png',(full*255).astype(np.uint8));cv2.imwrite('gen/ny_early.png',(early*255).astype(np.uint8))
np.save('gen/ny_labels.npy',l)
# ---- build ink layers
l=cv2.connectedComponents((full>.3).astype(np.uint8))[1]
def comp_ids(pred):
    n2,l2,s2,c2=cv2.connectedComponentsWithStats((full>.3).astype(np.uint8));return l2,[i for i in range(1,n2) if pred(s2[i])]
l2,_=comp_ids(lambda s:True)
n2,l2,s2,c2=cv2.connectedComponentsWithStats((full>.3).astype(np.uint8))
groups={'base':[],'bang':[],'dot':[]}
for i in range(1,n2):
    x,y,w,h,a=s2[i]
    if a<200: continue
    if x>=1000 and y>=460 and a<9000: groups['bang'].append(i)
    elif a<2000 and y>640: groups['dot'].append(i)
    else: groups['base'].append(i)
print(groups)
rng=np.random.default_rng(3)
tex=cv2.GaussianBlur(rng.normal(0,1,(1080,1440)).astype(np.float32),(0,0),3)
for k,ids in groups.items():
    m=np.isin(l2,ids).astype(np.float32); m=cv2.dilate(m,np.ones((3,3),np.uint8))
    a=cv2.GaussianBlur(m,(0,0),1.3)
    er=cv2.GaussianBlur(cv2.erode(m,np.ones((9,9),np.uint8)),(0,0),2)
    core=np.array([46,34,222],np.float32);edge=np.array([30,14,176],np.float32)
    col=edge*(1-er[...,None])+core*er[...,None]
    col=col*(1+.06*tex[...,None])
    rgba=np.dstack([np.clip(col,0,255),np.clip(a*245,0,255)]).astype(np.uint8)
    cv2.imwrite(f'gen/ny_{k}.png',rgba)
