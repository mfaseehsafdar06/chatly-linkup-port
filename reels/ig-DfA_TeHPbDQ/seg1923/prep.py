import cv2,numpy as np
# ---- hand key
im=cv2.imread('gen/hand.png').astype(np.float32)
b,g,r=im[...,0],im[...,1],im[...,2]
blueness=b-np.maximum(r,g)                     # bg ~ 255-70
a=np.clip(1-(blueness-40)/90,0,1)              # >130 transparent, <40 opaque
a=cv2.GaussianBlur(a,(0,0),1.0)
desp=im.copy(); desp[...,0]=np.minimum(b,np.maximum(r,g)+10)   # kill blue spill
out=np.dstack([desp,a*255]).clip(0,255).astype(np.uint8)
ys,xs=np.where(a>.5); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
out=out[y0:y1+1,x0:x1+1]; cv2.imwrite('gen/hand_rgba.png',out)
A=out[...,3]>128; o=out[...,:3].astype(int)
red=A&(o[...,2]>150)&(o[...,1]<90)&(o[...,0]<90)
ry,rx=np.where(red); i=rx.argmin(); tip=(int(rx[i]),int(np.median(ry[rx<rx.min()+6])))
# barrel back end: rightmost white pixel of the cap region (white, bright)
wh=A&(o.min(2)>215); wy,wx=np.where(wh); j=wx.argmax(); back=(int(wx[j]),int(np.median(wy[wx>wx.max()-8])))
ang=np.arctan2(back[1]-tip[1],back[0]-tip[0])
print('hand',out.shape,'tip',tip,'back',back,'axis deg',np.degrees(ang).round(2))
# ---- globe
gl=cv2.imread('gen/globe.png'); hsv=cv2.cvtColor(gl,cv2.COLOR_BGR2HSV)
m=((hsv[...,1]>70)&(hsv[...,2]>60)).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((25,25),np.uint8))
n,l,s,c=cv2.connectedComponentsWithStats(m); k=1+np.argmax(s[1:,4])
x,y,w,h=s[k,:4]; cx,cy,d=x+w/2,y+h/2,(w+h)/2
print('globe',x,y,w,h,'d',d)
sc=732/d
# paper whiten: levels so paper (~median of non-globe) -> 247
paper=np.median(gl[m==0].reshape(-1,3),0); print('paper',paper)
mdil=cv2.dilate(m,np.ones((61,61),np.uint8))
small=cv2.resize(gl,(600,448),interpolation=cv2.INTER_AREA);ms=cv2.resize(mdil,(600,448),interpolation=cv2.INTER_NEAREST)
bgs=cv2.inpaint(small,ms,15,cv2.INPAINT_TELEA);bgs=cv2.GaussianBlur(bgs,(0,0),25)
bg=cv2.resize(bgs,(gl.shape[1],gl.shape[0]),interpolation=cv2.INTER_CUBIC).astype(np.float32)
gw=np.clip(gl.astype(np.float32)/bg*np.array([249,248,246]),0,255).astype(np.uint8)
for v in range(4):
    R=np.random.default_rng(10+v)
    M=cv2.getRotationMatrix2D((cx,cy),R.uniform(-.6,.6),sc*R.uniform(.995,1.005))
    M[0,2]+=720-cx; M[1,2]+=558-cy
    M[0,2]+=R.uniform(-4,4); M[1,2]+=R.uniform(-3,3)
    pc=np.array([249,248,246],np.float32)
    fr=cv2.warpAffine(gw,M,(1440,1080),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=pc.tolist())
    mk=cv2.warpAffine(np.ones(gw.shape[:2],np.float32),M,(1440,1080),flags=cv2.INTER_LINEAR,borderValue=0)
    mk=cv2.erode(mk,np.ones((15,15),np.uint8));mk=cv2.GaussianBlur(mk,(0,0),12)[...,None]
    pn=cv2.GaussianBlur(R.normal(0,1,(1080,1440)).astype(np.float32),(0,0),1.2)[...,None]*2.0
    fr=(fr*mk+(pc+pn)*(1-mk)).clip(0,255).astype(np.uint8)
    # small organic displacement (re-photographed drawing wobble)
    dx=cv2.GaussianBlur(R.normal(0,1,(1080,1440)).astype(np.float32),(0,0),40); dx*=2.2/dx.std()
    dy=cv2.GaussianBlur(R.normal(0,1,(1080,1440)).astype(np.float32),(0,0),40); dy*=2.2/dy.std()
    gx,gy=np.meshgrid(np.arange(1440,dtype=np.float32),np.arange(1080,dtype=np.float32))
    fr=cv2.remap(fr,gx+dx,gy+dy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(f'gen/globe_v{v}.png',fr)
print('ok')
