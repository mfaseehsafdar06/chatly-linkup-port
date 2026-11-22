# Derived art from cutouts (re-run if assets/cut changes):
#  derived/P9_ink.png : GPT-01_06 "9PM" keyed to ink-only alpha and fattened to the reference's brush weight.
import cv2,numpy as np
C='../../assets/cut/'
im=cv2.imread(C+'GPT-01_06.png',cv2.IMREAD_UNCHANGED); a0=im[...,3].astype(np.float32)/255
g=cv2.cvtColor(im[...,:3],cv2.COLOR_BGR2GRAY).astype(np.float32)
paper=np.percentile(g[a0>.9],80)
ink=np.clip((paper-g)/(paper-60),0,1)*a0
ink[ink<.12]=0
inner=cv2.erode((a0>.5).astype(np.uint8),np.ones((25,25),np.uint8)).astype(np.float32); ink*=inner
r=int(round(im.shape[1]*0.010))  # dilation ~1.9% of width
k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r+1,2*r+1))
fat=cv2.dilate(ink,k); fat=cv2.GaussianBlur(fat,(0,0),1.2)
# brush texture: dry-brush streaks
rng=np.random.default_rng(3); st=cv2.GaussianBlur(rng.normal(0,1,im.shape[:2]).astype(np.float32),(0,0),sigmaX=1.0,sigmaY=6); st=st/st.std()
alpha=np.clip(fat*(1-.0*np.clip(st,0,3)),0,1)
o=np.dstack([np.full(g.shape,52),np.full(g.shape,50),np.full(g.shape,52),alpha*255]).astype(np.uint8)
cv2.imwrite('derived/P9_ink.png',o); print('P9',o.shape,'r',r,'paper',paper)
